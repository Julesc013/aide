"""Offline PR identity, policy, intent and lost-observation refusal tests."""
import copy
from pathlib import Path
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.runtime.integration_broker.common import Refused
from core.runtime.integration_broker.pr_observation import decision, ObservationStore


def plan(key="a"):
    return {"schema": "aide.broker.pr-plan.v1", "request_digest": key * 64,
            "repository": "fixture/repo", "actor": "fixture-broker", "target_ref": "refs/heads/dev",
            "base": "b" * 40, "candidate_commit": "c" * 40, "candidate_tree": "d" * 40,
            "branch_ref": "refs/heads/task/aide-cw-" + key * 64,
            "checks": [{"name": "required", "app_id": 1, "workflow_sha": "e" * 40}],
            "policy_digest": "f" * 64, "merge_contract_sha256": "9" * 64,
            "expires_at": 2000, "max_observations": 16}


def observed(p, stage="merge"):
    value = {"schema": "aide.broker.pr-observation.v1", "request_digest": p["request_digest"],
             "repository": p["repository"], "actor": p["actor"], "target_commit": p["base"],
             "candidate": {"commit": p["candidate_commit"], "tree": p["candidate_tree"], "parents": [p["base"]]},
             "branch": {"ref": p["branch_ref"], "commit": p["candidate_commit"]},
             "pull": {"number": 8, "state": "open", "draft": False, "base": p["base"],
                      "base_ref": p["target_ref"], "base_repository": p["repository"],
                      "head": p["candidate_commit"], "head_ref": p["branch_ref"],
                      "head_repository": p["repository"], "author": p["actor"],
                      "merge_commit": None, "merge_tree": None, "merge_parents": None, "integrated_ancestor": None},
             "checks_complete": True,
             "checks": [dict(p["checks"][0], head_commit=p["candidate_commit"], status="completed", conclusion="success")],
             "policy_digest": p["policy_digest"], "merge_contract_sha256": p["merge_contract_sha256"]}
    if stage == "publish_objects":
        value["candidate"] = value["branch"] = value["pull"] = None
    elif stage == "create_branch":
        value["branch"] = value["pull"] = None
    elif stage == "create_pr":
        value["pull"] = None
    elif stage == "integrated":
        value["pull"].update(state="merged", merge_commit="8" * 40, merge_tree=p["candidate_tree"],
                            merge_parents=[p["base"], p["candidate_commit"]], integrated_ancestor=True)
        value["target_commit"] = "8" * 40
    return value


class PrObservationTests(unittest.TestCase):
    def store(self):
        temporary = tempfile.TemporaryDirectory(prefix="aide-pr-observation-")
        self.addCleanup(temporary.cleanup)
        store = ObservationStore(Path(temporary.name))
        self.addCleanup(store.close)
        return store, Path(temporary.name)

    def test_explicit_stages_and_incomplete_check_or_policy_never_merge(self):
        p = plan()
        for stage in ("publish_objects", "create_branch", "create_pr", "merge", "integrated"):
            self.assertEqual(decision(p, observed(p, stage)), stage)
        for mutation, expected in (
                (lambda value: value.update(checks_complete=False), "wait_checks"),
                (lambda value: value["checks"][0].update(conclusion="skipped"), "wait_checks"),
                (lambda value: value.update(policy_digest=None), "qualify_target"),
                (lambda value: value.update(merge_contract_sha256=None), "qualify_target"),
                (lambda value: value["pull"].update(draft=True), "blocked_pr"),
                (lambda value: value["pull"].update(state="closed"), "blocked_pr")):
            value = observed(p)
            mutation(value)
            self.assertEqual(decision(p, value), expected)
        p["merge_contract_sha256"] = None
        self.assertEqual(decision(p, observed(p)), "qualify_target")

    def test_moving_base_and_foreign_check_sources_refuse(self):
        p = plan()
        mutations = (
            lambda value: value.update(target_commit="1" * 40),
            lambda value: value.update(actor="other-user"),
            lambda value: value.update(repository="other/repo"),
            lambda value: value["candidate"].update(tree="1" * 40),
            lambda value: value["candidate"].update(parents=[]),
            lambda value: value["branch"].update(commit="1" * 40),
            lambda value: value["pull"].update(base="1" * 40),
            lambda value: value["pull"].update(head="1" * 40),
            lambda value: value["checks"][0].update(app_id=True),
            lambda value: value["checks"][0].update(app_id=2),
            lambda value: value["checks"][0].update(workflow_sha="1" * 40),
            lambda value: value["checks"][0].update(head_commit="1" * 40),
            lambda value: value["checks"].append(dict(value["checks"][0])),
        )
        for index, mutation in enumerate(mutations):
            value = observed(p)
            mutation(value)
            with self.subTest(index=index), self.assertRaises(Refused):
                decision(p, value)

    def test_same_oid_wrong_target_ref_and_forks_refuse_open_and_merged_prs(self):
        p = plan()
        for stage in ("merge", "integrated"):
            for field, value in (("base_ref", "refs/heads/main"), ("base_repository", "fork/repo"),
                                 ("head_repository", "fork/repo")):
                with self.subTest(stage=stage, field=field):
                    observation = observed(p, stage)
                    observation["pull"][field] = value
                    with self.assertRaisesRegex(Refused, "PR does not bind"):
                        decision(p, observation)

    def test_first_observed_pr_number_cannot_be_replaced_or_disappear(self):
        store, root = self.store()
        p = plan()
        store.reserve(p)
        value = observed(p)
        store.observe(p, value)
        value["pull"]["number"] += 1
        with self.assertRaisesRegex(Refused, "PR identity"):
            store.observe(p, value)
        value["pull"] = None
        with self.assertRaisesRegex(Refused, "PR identity"):
            store.observe(p, value)

    def test_absence_after_intent_never_grants_replay_after_restart(self):
        store, root = self.store()
        p, value = plan(), observed(plan(), "create_branch")
        self.assertTrue(store.reserve(p))
        store.observe(p, value)
        self.assertTrue(store.intent(p, value, "create_branch", now=1000))
        second = ObservationStore(root)
        self.addCleanup(second.close)
        second.observe(p, value)
        self.assertFalse(second.intent(p, value, "create_branch", now=1000))
        self.assertEqual(second.db.execute("SELECT COUNT(*) FROM intents").fetchone()[0], 1)

    def test_merge_requires_latest_checks_intent_and_immutable_result(self):
        store, root = self.store()
        p = plan()
        store.reserve(p)
        with self.assertRaisesRegex(Refused, "no durable merge intent"):
            store.observe(p, observed(p, "integrated"))
        value = observed(p)
        store.observe(p, value)
        stale = copy.deepcopy(value)
        value["checks_complete"] = False
        store.observe(p, value)
        with self.assertRaises(Refused):
            store.intent(p, stale, "merge", now=1000)
        store.observe(p, stale)
        self.assertTrue(store.intent(p, stale, "merge", now=1000))
        merged = observed(p, "integrated")
        self.assertEqual(store.observe(p, merged), "integrated")
        merged["pull"]["merge_commit"] = "7" * 40
        with self.assertRaisesRegex(Refused, "cannot regress or change"):
            store.observe(p, merged)

    def test_target_writer_observation_budget_expiry_and_plan_drift_refuse(self):
        store, root = self.store()
        p = plan()
        p["max_observations"] = 2
        store.reserve(p)
        with self.assertRaisesRegex(Refused, "target writer"):
            store.reserve(plan("2"))
        drift = copy.deepcopy(p)
        drift["actor"] = "changed-actor"
        with self.assertRaises(Refused):
            store.reserve(drift)
        value = observed(p)
        store.observe(p, value)
        with self.assertRaisesRegex(Refused, "expired"):
            store.intent(p, value, "merge", now=2000)
        store.observe(p, value)
        with self.assertRaisesRegex(Refused, "observation budget"):
            store.observe(p, value)

    def test_concurrent_reservation_and_intent_have_one_winner(self):
        store, root = self.store()
        p, value = plan(), observed(plan(), "create_branch")
        outcomes, failures = [], []
        barrier = threading.Barrier(2)
        def run():
            local = ObservationStore(root)
            try:
                barrier.wait(timeout=5)
                reserved = local.reserve(p)
                local.observe(p, value)
                outcomes.append((reserved, local.intent(p, value, "create_branch", now=1000)))
            except BaseException as error:
                failures.append(error)
            finally:
                local.close()
        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(10)
        self.assertFalse(any(thread.is_alive() for thread in threads))
        self.assertEqual(failures, [])
        self.assertEqual(sum(row[0] for row in outcomes), 1)
        self.assertEqual(sum(row[1] for row in outcomes), 1)


if __name__ == "__main__":
    unittest.main()
