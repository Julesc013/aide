"""Offline PR identity, policy, intent and lost-observation refusal tests."""
import copy
import os
import shutil
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

    def test_read_attempt_budget_is_atomic_and_retains_legacy_observation_cost(self):
        store, root = self.store()
        fixed = plan()
        fixed["max_observations"] = 2
        store.reserve(fixed)
        # An earlier v1 writer could persist an observation before this additive
        # read-attempt API existed. It still costs one of the finite calls.
        store.observe(fixed, observed(fixed, "create_branch"))
        results, failures = [], []
        barrier = threading.Barrier(2)
        def reserve():
            local = ObservationStore(root)
            try:
                barrier.wait(timeout=5)
                local.observation_attempt(fixed)
                results.append("reserved")
            except Refused:
                results.append("refused")
            except BaseException as error:
                failures.append(error)
            finally:
                local.close()
        threads = [threading.Thread(target=reserve) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(10)
        self.assertFalse(any(thread.is_alive() for thread in threads))
        self.assertEqual(failures, [])
        self.assertCountEqual(results, ["reserved", "refused"])
        self.assertEqual(store.db.execute("SELECT COUNT(*) FROM observation_attempts").fetchone()[0], 2)

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


class ScriptedStageAdapter:
    """Local fact/dispatch fixture, not authenticated production transport."""
    def __init__(self, fixture, fixed):
        self.fixture, self.fixed = fixture, fixed
        self.stage = "publish_objects"
        self.calls, self.qualifications = [], []
        self.lost_after = False
        self.fail_before = False
        self.qualified = True
        self.raw_override = None
        self.observe_hook = None
        self.merge_oid = None
        self.observation_calls = 0

    def assert_current(self, broker, request, fixed, purpose):
        if not self.qualified:
            raise Refused("fixture host qualification refused")
        if fixed != self.fixed:
            raise Refused("fixture plan drift")
        self.qualifications.append(purpose)

    def observe(self, fixed, *, attempt):
        from core.runtime.integration_broker.common import canonical
        self.observation_calls += 1
        if self.observe_hook:
            self.observe_hook()
        if self.raw_override is not None:
            return self.raw_override
        value = observed(fixed, self.stage)
        if self.merge_oid:
            value["pull"]["merge_commit"] = self.merge_oid
            value["target_commit"] = self.merge_oid
        return canonical(value).encode()

    def dispatch(self, operation, fixed, prepared):
        self.calls.append(operation)
        if self.fail_before:
            raise OSError("fixture failed before acceptance")
        folder = prepared["directory"]
        # These are actual object-bound Windows handles and a real local Git
        # commit/object store, even though the remote service is scripted.
        with self.fixture.assertRaises(OSError):
            folder.rename(folder.with_name("forbidden-substitution"))
        actual = self.fixture.git.run(folder, "cat-file", "commit", fixed["candidate_commit"])
        self.fixture.assertEqual(actual, prepared["commit_bytes"])
        if operation == "merge":
            raw = (f"tree {fixed['candidate_tree']}\nparent {fixed['base']}\n"
                   f"parent {fixed['candidate_commit']}\nauthor fixture <fixture@example.invalid> 0 +0000\n"
                   "committer fixture <fixture@example.invalid> 0 +0000\n\nfixture merge\n").encode()
            self.merge_oid = self.fixture.git.run(folder, "hash-object", "-t", "commit", "-w", "--stdin", data=raw).decode().strip()
        sequence = ["publish_objects", "create_branch", "create_pr", "merge", "integrated"]
        self.fixture.assertEqual(operation, self.stage)
        self.stage = sequence[sequence.index(operation) + 1]
        if self.lost_after:
            raise OSError("fixture lost reply after acceptance")


@unittest.skipUnless(os.name == "nt" and shutil.which("git"), "requires bounded Windows Git host")
class StagedBrokerTests(unittest.TestCase):
    def fixture(self, *, max_observations=16, expires_at=2000):
        import test_continuous_worker_integration_broker as native
        from core.runtime.integration_broker.common import digest
        from core.runtime.integration_broker.staged_transport import StagedTransport, commit_object
        helper = native.BrokerTests(methodName="runTest")
        helper.setUp()
        self.addCleanup(helper.doCleanups)
        fixed = plan()
        fixed.update(max_observations=max_observations, expires_at=expires_at)
        fixed.update(request_digest=digest(helper.request), base=helper.base,
                     candidate_tree=helper.manifest["candidate_tree"],
                     branch_ref="refs/heads/task/aide-cw-" + digest(helper.request))
        fixed["checks"][0]["name"] = "unit"
        oid, raw = commit_object(fixed["candidate_tree"], fixed["base"], fixed["actor"],
                                 "Implement fixture candidate\n\nWork-Item: BROKER-FIXTURE-01\n")
        fixed["candidate_commit"] = oid
        adapter = ScriptedStageAdapter(helper, fixed)
        transport = StagedTransport(fixed, raw, adapter=adapter)
        broker = helper.broker(transport)
        return helper, fixed, raw, adapter, transport, broker

    def test_literal_commit_plan_rejects_extra_headers_and_changed_bytes(self):
        from core.runtime.integration_broker.staged_transport import StagedTransport, commit_object
        fixed = plan()
        oid, raw = commit_object(fixed["candidate_tree"], fixed["base"], fixed["actor"], "Fixture\n")
        fixed["candidate_commit"] = oid
        self.assertEqual(commit_object(fixed["candidate_tree"], fixed["base"], fixed["actor"], "Fixture\n"), (oid, raw))
        StagedTransport(fixed, raw)
        for altered in (raw + b"changed\n", raw.replace(b"\n\n", b"\ngpgsig forged\n\n"), b"null", raw.decode()):
            with self.subTest(altered=type(altered).__name__), self.assertRaises(Refused):
                StagedTransport(fixed, altered)
        for bad in ("", "no final newline", "nul\x00\n", "CRLF\r\n"):
            with self.assertRaises(Refused):
                commit_object(fixed["candidate_tree"], fixed["base"], fixed["actor"], bad)

    def test_four_stages_use_real_candidate_objects_and_query_never_dispatches(self):
        from core.runtime.integration_broker.common import digest
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        self.assertEqual(broker.query(helper.request)["status"], "absent")
        for stage in ("publish_objects", "create_branch", "create_pr", "merge"):
            with self.subTest(stage=stage):
                before = list(adapter.calls)
                broker.reconcile(helper.request)
                self.assertEqual(adapter.calls, before + [stage])
                broker.query(helper.request)
                self.assertEqual(adapter.calls, before + [stage])
        result = broker.reconcile(helper.request)
        self.assertEqual(result["status"], "integrated")
        self.assertEqual(result["receipt"]["integrated_commit"], adapter.merge_oid)
        self.assertEqual(result["receipt"]["integrated_tree"], helper.manifest["candidate_tree"])
        folder = helper.state / broker.ledger.preparation(digest(helper.request))["generation"]
        tree = helper.git.run(folder, "ls-tree", "-r", adapter.merge_oid).decode()
        self.assertIn("src/new.bin", tree)
        self.assertNotIn("src/remove.bin", tree)
        self.assertEqual(len(adapter.calls), 4)

    def test_each_lost_reply_restarts_into_a_later_stage_without_replay(self):
        from core.runtime.integration_broker.staged_transport import StagedTransport
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        adapter.lost_after = True
        for stage in ("publish_objects", "create_branch", "create_pr", "merge"):
            with self.subTest(stage=stage), self.assertRaisesRegex(OSError, "lost reply"):
                broker.reconcile(helper.request)
            broker.close()
            broker = helper.broker(StagedTransport(fixed, raw, adapter=adapter))
        self.assertEqual(broker.reconcile(helper.request)["status"], "integrated")
        self.assertEqual(adapter.calls, ["publish_objects", "create_branch", "create_pr", "merge"])

    def test_absence_after_intent_never_repeats_uncertain_dispatch(self):
        from core.runtime.integration_broker.staged_transport import StagedTransport
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        adapter.fail_before = True
        with self.assertRaisesRegex(OSError, "before acceptance"):
            broker.reconcile(helper.request)
        broker.close()
        adapter.fail_before = False
        broker = helper.broker(StagedTransport(fixed, raw, adapter=adapter))
        self.assertEqual(broker.reconcile(helper.request)["status"], "pending")
        self.assertEqual(adapter.calls, ["publish_objects"])

    def test_missing_or_revoked_adapter_refuses_before_broker_reservation(self):
        from core.runtime.integration_broker.common import digest
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        transport.adapter = None
        with self.assertRaisesRegex(Refused, "not installed"):
            broker.reconcile(helper.request)
        transport.adapter = adapter
        adapter.qualified = False
        with self.assertRaisesRegex(Refused, "qualification refused"):
            broker.reconcile(helper.request)
        self.assertIsNone(broker.ledger.get(digest(helper.request)))
        self.assertFalse((helper.state / "pr-observations.sqlite3").exists())
        self.assertEqual(adapter.calls, [])

    def test_malformed_observations_cannot_reserve_a_remote_intent(self):
        import sqlite3
        from contextlib import closing
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        for malformed in (b"null", b"true", b"[]", b'{"schema":0,"schema":1}', {}, b" " * (1024 * 1024 + 1)):
            adapter.raw_override = malformed
            with self.subTest(kind=type(malformed).__name__), self.assertRaises(Refused):
                broker.reconcile(helper.request)
        self.assertEqual(adapter.calls, [])
        with closing(sqlite3.connect(helper.state / "pr-observations.sqlite3")) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM intents").fetchone()[0], 0)

    def test_prepared_content_and_local_base_drift_refuse_later_stage(self):
        from core.runtime.integration_broker.common import digest
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        broker.reconcile(helper.request)
        folder = helper.state / broker.ledger.preparation(digest(helper.request))["generation"]
        index = (folder / "index").read_bytes()
        helper.git.run(folder, "update-index", "-z", "--index-info",
                       data=("0 " + "0" * 40 + "\tsrc/new.bin").encode() + b"\0")
        with self.assertRaisesRegex(Refused, "index differs"):
            broker.reconcile(helper.request)
        (folder / "index").write_bytes(index)
        # Move the real local dev ref to a different existing commit. Its new
        # object has the candidate tree and is copied as raw bytes, without Git transport.
        helper.git.run(helper.repo, "hash-object", "-t", "commit", "-w", "--stdin", data=raw)
        helper.git.run(helper.repo, "update-ref", "refs/heads/dev", fixed["candidate_commit"])
        with self.assertRaisesRegex(Refused, "target base moved"):
            broker.reconcile(helper.request)
        self.assertEqual(adapter.calls, ["publish_objects"])

    def test_remote_base_moves_during_final_observation_without_dispatch(self):
        from core.runtime.integration_broker.common import canonical
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        count = 0
        def drift():
            nonlocal count
            count += 1
            if count == 2:
                value = observed(fixed, "publish_objects")
                value["target_commit"] = "1" * 40
                adapter.raw_override = canonical(value).encode()
        adapter.observe_hook = drift
        with self.assertRaisesRegex(Refused, "remote target base moved"):
            broker.reconcile(helper.request)
        self.assertEqual(adapter.calls, [])

    def test_failed_reads_consume_durable_attempt_budget_across_restart(self):
        from core.runtime.integration_broker.staged_transport import StagedTransport
        helper, fixed, raw, adapter, transport, broker = self.fixture(max_observations=2)
        adapter.raw_override = b"null"
        with self.assertRaises(Refused):
            broker.reconcile(helper.request)
        broker.close()
        broker = helper.broker(StagedTransport(fixed, raw, adapter=adapter))
        def timeout():
            raise TimeoutError("fixture observation timed out")
        adapter.observe_hook = timeout
        with self.assertRaises(TimeoutError):
            broker.reconcile(helper.request)
        adapter.observe_hook = None
        adapter.raw_override = None
        with self.assertRaisesRegex(Refused, "attempt budget"):
            broker.reconcile(helper.request)
        self.assertEqual(adapter.observation_calls, 2)
        self.assertEqual(adapter.calls, [])

    def test_refused_attempt_write_prevents_provider_read(self):
        from unittest.mock import patch
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        with patch.object(ObservationStore, "observation_attempt", side_effect=OSError("durable attempt refused")):
            with self.assertRaisesRegex(OSError, "durable attempt refused"):
                broker.reconcile(helper.request)
        self.assertEqual(adapter.observation_calls, 0)
        self.assertEqual(adapter.calls, [])

    def test_expiry_after_durable_intent_preserves_intent_without_dispatch(self):
        from contextlib import closing
        import sqlite3
        from core.runtime.integration_broker.common import digest
        for expiry in (2000, 1500):
            with self.subTest(plan_expiry=expiry):
                helper, fixed, raw, adapter, transport, broker = self.fixture(expires_at=expiry)
                def expire(phase):
                    if phase == "intent:publish_objects":
                        broker.now = lambda: expiry + 1
                transport.checkpoint = expire
                with self.assertRaisesRegex(Refused, "expired"):
                    broker.reconcile(helper.request)
                self.assertEqual(adapter.calls, [])
                self.assertEqual(broker.ledger.get(digest(helper.request))["stage"], "apply_intent")
                with closing(sqlite3.connect(helper.state / "pr-observations.sqlite3")) as db:
                    self.assertEqual(db.execute("SELECT COUNT(*) FROM intents").fetchone()[0], 1)
                # Even a subsequently restored earlier clock cannot grant a
                # repeat of the already reserved uncertain operation.
                broker.now = lambda: 1000
                transport.checkpoint = lambda phase: None
                self.assertEqual(broker.reconcile(helper.request)["status"], "pending")
                self.assertEqual(adapter.calls, [])

    def test_actual_child_death_after_stage_intent_is_not_replayed(self):
        import json
        import subprocess
        from core.runtime.integration_broker.common import canonical
        helper, fixed, raw, adapter, transport, broker = self.fixture()
        broker.reconcile(helper.request)
        config = helper.root / "stage-fixture.json"
        config.write_text(json.dumps({"plan": fixed, "commit": raw.decode(), "authority": helper.authority,
                         "request": helper.request, "state": str(helper.state), "repo": str(helper.repo),
                         "exchange": str(helper.exchange), "git": str(helper.git.executable),
                         "git_sha": helper.git.sha256, "observation": observed(fixed, "create_branch")}), encoding="utf-8")
        script = r"""
import json, os, sys
from pathlib import Path
from core.runtime.integration_broker.common import Git, canonical
from core.runtime.integration_broker.service import Broker
from core.runtime.integration_broker.staged_transport import StagedTransport
c=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
class Fixture:
    def assert_current(self, *args): pass
    def observe(self, plan, *, attempt): return canonical(c['observation']).encode()
    def dispatch(self, *args): raise AssertionError('dispatch must not occur')
def checkpoint(phase):
    if phase=='intent:create_branch': os._exit(71)
t=StagedTransport(c['plan'],c['commit'].encode(),adapter=Fixture(),checkpoint=checkpoint)
b=Broker(c['state'],c['exchange'],c['repo'],Git(c['git'],c['git_sha']),c['authority'],transport=t,now=lambda:1000)
b.reconcile(c['request'])
"""
        result = subprocess.run([sys.executable, "-B", "-c", script, str(config)], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=45)
        self.assertEqual(result.returncode, 71, result.stdout.decode(errors="replace"))
        self.assertEqual(broker.reconcile(helper.request)["status"], "pending")
        self.assertEqual(adapter.calls, ["publish_objects"])


if __name__ == "__main__":
    unittest.main()
