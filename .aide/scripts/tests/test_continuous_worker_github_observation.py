"""Offline raw REST refusals; no HTTP client, credentials or hosted qualification."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit, urlencode

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.runtime.integration_broker.common import Refused
from core.runtime.integration_broker.github_api import Reads, Response, ORIGIN, MAX_BODY
from core.runtime.integration_broker.github_observation import collect
from core.runtime.integration_broker.pr_observation import decision, ObservationStore

REPO = "fixture/repo"
PREFIX = "/repos/" + REPO
BRANCH = "task/aide-cw-" + "a" * 64
BASE, HEAD, TREE, MERGE = "b" * 40, "c" * 40, "d" * 40, "e" * 40


def plan():
    return {"schema": "aide.broker.pr-plan.v1", "request_digest": "a" * 64,
            "repository": REPO, "actor": "fixture-broker", "target_ref": "refs/heads/dev",
            "base": BASE, "candidate_commit": HEAD, "candidate_tree": TREE,
            "branch_ref": "refs/heads/" + BRANCH,
            "checks": [{"name": "required", "app_id": 99, "workflow_sha": HEAD}],
            "policy_digest": "f" * 64, "merge_contract_sha256": "9" * 64,
            "expires_at": 2000, "max_observations": 16}


def git_commit(sha, parents, tree=TREE):
    return {"sha": sha, "tree": {"sha": tree}, "parents": [{"sha": p} for p in parents]}


def page(key, values):
    return {"total_count": len(values), key: values}


class Fixture:
    """REST-shaped records independent of desired-plan mutation."""
    def __init__(self):
        self.clock, self.calls, self.hook = 1000, [], None
        self.pull = {"id": 801, "number": 8, "state": "open", "merged": False, "draft": False,
                     "base": {"ref": "dev", "sha": BASE, "repo": {"full_name": REPO}},
                     "head": {"ref": BRANCH, "sha": HEAD, "repo": {"full_name": REPO}},
                     "user": {"login": "fixture-broker"}, "merge_commit_sha": None}
        self.check = {"id": 31, "name": "required", "app": {"id": 99}, "head_sha": HEAD,
                      "check_suite": {"id": 41}, "status": "completed", "conclusion": "success",
                      "url": ORIGIN + PREFIX + "/check-runs/31"}
        self.run = {"id": 51, "run_attempt": 2, "check_suite_id": 41, "head_sha": HEAD,
                    "head_branch": BRANCH, "event": "push", "path": ".github/workflows/checks.yml",
                    "status": "completed", "conclusion": "success", "repository": {"full_name": REPO},
                    "head_repository": {"full_name": REPO}, "head_commit": {"id": HEAD},
                    "url": ORIGIN + PREFIX + "/actions/runs/51"}
        self.job = {"id": 61, "run_id": 51, "run_attempt": 2, "head_sha": HEAD, "name": "required",
                    "status": "completed", "conclusion": "success", "check_run_url": self.check["url"]}
        self.routes = {
            "/user": {"login": "fixture-broker", "id": 77, "type": "User"},
            PREFIX: {"id": 888, "full_name": REPO, "archived": False, "disabled": False,
                     "permissions": {"pull": True, "push": True, "admin": False}},
            PREFIX + "/git/ref/heads/dev": {"ref": "refs/heads/dev", "object": {"type": "commit", "sha": BASE}},
            PREFIX + "/git/ref/heads/" + BRANCH: {"ref": "refs/heads/" + BRANCH, "object": {"type": "commit", "sha": HEAD}},
            PREFIX + "/git/commits/" + BASE: git_commit(BASE, ["8" * 40]),
            PREFIX + "/git/commits/" + HEAD: git_commit(HEAD, [BASE]),
            PREFIX + "/pulls": [self.pull], PREFIX + "/pulls/8": self.pull,
            PREFIX + "/commits/" + HEAD + "/check-runs": page("check_runs", [self.check]),
            PREFIX + "/actions/runs": page("workflow_runs", [self.run]),
            PREFIX + "/actions/runs/51": self.run,
            PREFIX + "/actions/runs/51/attempts/2/jobs": page("jobs", [self.job]),
        }

    def read(self, url, *, headers, timeout, max_bytes):
        assert headers == {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2026-03-10"}
        assert 0 < timeout <= 10 and 0 < max_bytes <= MAX_BODY
        self.calls.append(url)
        path = urlsplit(url).path
        body = copy.deepcopy(self.routes.get(path, 404))
        value = Response(url, body if type(body) is int else 200,
                         (("Content-Type", "application/json; charset=utf-8"),),
                         json.dumps({"message": "error"} if type(body) is int else body).encode())
        return self.hook(url, value) if self.hook else value

    def api(self, **kwargs):
        return Reads(REPO, self.read, deadline=1100, now=lambda: self.clock, **kwargs)

    def merged(self, *, descendant=False):
        self.pull.update(state="closed", merged=True, merge_commit_sha=MERGE)
        self.pull["base"]["sha"] = "7" * 40  # Later mutable PR base projection.
        self.routes[PREFIX + "/git/commits/" + MERGE] = git_commit(MERGE, [BASE, HEAD])
        target = "6" * 40 if descendant else MERGE
        self.routes[PREFIX + "/git/ref/heads/dev"]["object"]["sha"] = target
        self.routes[PREFIX + "/git/commits/" + target] = git_commit(target, [MERGE]) if descendant else self.routes[PREFIX + "/git/commits/" + MERGE]
        if descendant:
            self.routes[PREFIX + "/compare/" + MERGE + "..." + target] = {
                "status": "ahead", "ahead_by": 1, "behind_by": 0,
                "base_commit": {"sha": MERGE}, "merge_base_commit": {"sha": MERGE}}


class GitHubObservationTests(unittest.TestCase):
    def test_complete_raw_observation_never_invents_policy_qualification(self):
        fixture, p = Fixture(), plan()
        result = collect(fixture.api(), p)
        self.assertEqual(decision(p, result), "qualify_target")
        self.assertIsNone(result["policy_digest"])
        self.assertIsNone(result["merge_contract_sha256"])
        self.assertEqual(result["checks"][0]["workflow_sha"], HEAD)
        p["checks"][0]["workflow_sha"] = "1" * 40
        with self.assertRaises(Refused):
            collect(fixture.api(), p)

    def test_exact_object_branch_and_pr_absence_select_each_preparation_stage(self):
        for stage in ("publish_objects", "create_branch", "create_pr"):
            fixture = Fixture()
            fixture.routes[PREFIX + "/pulls"] = []
            if stage != "create_pr":
                fixture.routes[PREFIX + "/git/ref/heads/" + BRANCH] = 404
            if stage == "publish_objects":
                fixture.routes[PREFIX + "/git/commits/" + HEAD] = 404
            with self.subTest(stage=stage):
                self.assertEqual(decision(plan(), collect(fixture.api(), plan())), stage)

    def test_null_or_scalar_success_never_masquerades_as_missing_candidate(self):
        for value in (None, False, 4.5, "unknown", []):
            fixture = Fixture()
            fixture.routes[PREFIX + "/git/commits/" + HEAD] = value
            with self.subTest(value=value), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_http_errors_refuse_and_consume_attempt_without_retry(self):
        for status in (401, 403, 404, 429, 500):
            fixture = Fixture()
            fixture.routes["/user"] = status
            api = fixture.api()
            with self.subTest(status=status), self.assertRaises(Refused):
                collect(api, plan())
            self.assertEqual(api.calls, 1)
            self.assertEqual(len(fixture.calls), 1)
        fixture = Fixture()
        def failed(*args, **kwargs):
            raise TimeoutError("fixture timeout")
        api = Reads(REPO, failed, deadline=1100, now=lambda: 1000, max_calls=1)
        with self.assertRaises(TimeoutError):
            api.get("/user")
        with self.assertRaisesRegex(Refused, "budget"):
            api.get("/user")

    def test_redirect_bad_headers_json_and_body_limits_refuse(self):
        transforms = (
            lambda v: Response("https://foreign.invalid/user", v.status, v.headers, v.body),
            lambda v: Response(v.url, 302, v.headers, v.body),
            lambda v: Response(v.url, v.status, v.headers + (("content-type", "application/json"),), v.body),
            lambda v: Response(v.url, v.status, (("Content-Type", "text/html"),), v.body),
            lambda v: Response(v.url, v.status, v.headers, b'{"id":1,"id":2}'),
            lambda v: Response(v.url, v.status, v.headers, b'{"id":NaN}'),
            lambda v: Response(v.url, v.status, v.headers, b'{"a":' * 50 + b'0' + b'}' * 50),
            lambda v: Response(v.url, v.status, v.headers, b'x' * (MAX_BODY + 1)),
        )
        for i, transform in enumerate(transforms):
            fixture = Fixture()
            fixture.hook = lambda url, value: transform(value)
            with self.subTest(case=i), self.assertRaises(Refused):
                collect(fixture.api(), plan())
            self.assertEqual(len(fixture.calls), 1)

    def test_finite_deadline_calls_and_total_bytes_are_checked_before_reads(self):
        fixture = Fixture()
        fixture.clock = 2000
        with self.assertRaises(Refused):
            collect(fixture.api(), plan())
        self.assertEqual(fixture.calls, [])
        for kwargs in ({"max_calls": 2}, {"max_bytes": 1}):
            fixture = Fixture()
            with self.subTest(kwargs=kwargs), self.assertRaises(Refused):
                collect(fixture.api(**kwargs), plan())
            self.assertLessEqual(len(fixture.calls), 2)
        fixture = Fixture()
        def expire(url, value):
            fixture.clock = 2000
            return value
        fixture.hook = expire
        with self.assertRaisesRegex(Refused, "deadline"):
            collect(fixture.api(), plan())
        self.assertEqual(len(fixture.calls), 1)

    def test_plan_reader_repository_must_match_and_read_deadline_is_independent(self):
        fixture, p = Fixture(), plan()
        p["repository"] = "other/repo"
        with self.assertRaises(Refused):
            collect(fixture.api(), p)
        self.assertEqual(fixture.calls, [])
        p = plan()
        p["expires_at"] = 900  # Mutation authority expired before this read.
        fixture.merged()
        self.assertEqual(decision(p, collect(fixture.api(), p)), "integrated")
        with self.assertRaisesRegex(Refused, "120 seconds"):
            Reads(REPO, fixture.read, deadline=1121, now=lambda: 1000)

    def test_backwards_wall_clock_cannot_extend_observation_budget(self):
        fixture = Fixture()
        clock = [0]
        api = Reads(REPO, fixture.read, deadline=1100, now=lambda: fixture.clock, monotonic=lambda: clock[0])
        clock[0], fixture.clock = 121, 500
        with self.assertRaisesRegex(Refused, "deadline"):
            api.get("/user")
        self.assertEqual(fixture.calls, [])

    def test_invalid_repository_paths_never_dispatch(self):
        for name in ("../repo", "owner/..", "owner/./repo", "owner/repo?x=1", "owner/repo#x", "owner/rep\\o"):
            with self.subTest(name=name), self.assertRaises(Refused):
                Reads(name, Fixture().read, deadline=1100)

    def test_wrong_actor_repository_refs_candidate_and_pull_facts_refuse(self):
        cases = (
            ("/user", "login", "other"), ("/user", "type", "Bot"),
            (PREFIX, "full_name", "foreign/repo"), (PREFIX, "archived", True),
            (PREFIX + "/git/ref/heads/dev", "ref", "refs/heads/main"),
            (PREFIX + "/git/commits/" + HEAD, "sha", BASE),
            (PREFIX + "/git/commits/" + HEAD, "parents", [{"sha": "1" * 40}]),
            (PREFIX + "/git/commits/" + HEAD, "tree", {"sha": "1" * 40}),
            (PREFIX + "/pulls/8", "user", {"login": "other"}),
            (PREFIX + "/pulls/8", "number", 9),
        )
        for route, field, value in cases:
            fixture = Fixture()
            fixture.routes[route][field] = value
            with self.subTest(route=route, field=field), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_same_oid_wrong_ref_fork_and_retargeted_pr_are_not_absence(self):
        for merged in (False, True):
            for endpoint, field, value in (("base", "ref", "main"), ("head", "ref", "task/other"),
                                            ("base", "repo", {"full_name": "fork/repo"}),
                                            ("head", "repo", {"full_name": "fork/repo"})):
                fixture = Fixture()
                if merged:
                    fixture.merged()
                fixture.pull[endpoint][field] = value
                with self.subTest(merged=merged, endpoint=endpoint, field=field), self.assertRaises(Refused):
                    collect(fixture.api(), plan())
        fixture = Fixture()
        fixture.pull["base"]["ref"] = "main"
        with self.assertRaises(Refused):
            collect(fixture.api(), plan())
        pulls_url = next(url for url in fixture.calls if urlsplit(url).path == PREFIX + "/pulls")
        self.assertNotIn("base", parse_qs(urlsplit(pulls_url).query))

    def test_check_application_and_duplicate_names_refuse_skipped_waits(self):
        fixture = Fixture()
        fixture.check["app"]["id"] = 100
        with self.assertRaises(Refused):
            collect(fixture.api(), plan())
        fixture = Fixture()
        duplicate = dict(fixture.check, id=32)
        fixture.routes[PREFIX + "/commits/" + HEAD + "/check-runs"] = page("check_runs", [fixture.check, duplicate])
        with self.assertRaisesRegex(Refused, "duplicate check name"):
            collect(fixture.api(), plan())
        fixture = Fixture()
        fixture.check["conclusion"] = fixture.job["conclusion"] = "skipped"
        self.assertEqual(decision(plan(), collect(fixture.api(), plan())), "wait_checks")

    def test_check_provenance_needs_actual_push_run_and_entry_workflow(self):
        cases = (("head_sha", BASE), ("head_branch", "dev"), ("event", "pull_request"),
                 ("path", "foreign/workflow.yml"), ("repository", {"full_name": "fork/repo"}),
                 ("head_repository", {"full_name": "fork/repo"}), ("head_commit", {"id": BASE}),
                 ("check_suite_id", 42), ("url", ORIGIN + PREFIX + "/actions/runs/52"),
                 ("run_attempt", True))
        for field, value in cases:
            fixture = Fixture()
            fixture.run[field] = value
            with self.subTest(field=field), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_actual_attempt_job_cannot_be_replaced_or_mixed(self):
        cases = (("run_id", 52), ("run_attempt", 1), ("run_attempt", True), ("head_sha", BASE),
                 ("name", "foreign"), ("status", "queued"), ("conclusion", "failure"),
                 ("check_run_url", ORIGIN + PREFIX + "/check-runs/32"))
        for field, value in cases:
            fixture = Fixture()
            fixture.job[field] = value
            with self.subTest(field=field), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_late_workflow_rerun_is_refused(self):
        fixture = Fixture()
        def rerun(url, value):
            if urlsplit(url).path == PREFIX + "/actions/runs/51":
                body = json.loads(value.body)
                body["run_attempt"] += 1
                return Response(value.url, value.status, value.headers, json.dumps(body).encode())
            return value
        fixture.hook = rerun
        with self.assertRaisesRegex(Refused, "run changed"):
            collect(fixture.api(), plan())

    def test_late_pull_retarget_or_state_change_is_refused(self):
        for change in ("base", "state"):
            fixture, seen = Fixture(), 0
            def mutate(url, value):
                nonlocal seen
                if urlsplit(url).path == PREFIX + "/pulls/8":
                    seen += 1
                    if seen == 2:
                        body = json.loads(value.body)
                        if change == "base":
                            body["base"]["ref"] = "main"
                        else:
                            body["state"] = "closed"
                        return Response(value.url, value.status, value.headers, json.dumps(body).encode())
                return value
            fixture.hook = mutate
            with self.subTest(change=change), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_late_target_branch_and_access_changes_refuse(self):
        for changed in (PREFIX + "/git/ref/heads/dev", PREFIX + "/git/ref/heads/" + BRANCH, PREFIX, "/user"):
            fixture, seen = Fixture(), {}
            def mutate(url, value):
                path = urlsplit(url).path
                seen[path] = seen.get(path, 0) + 1
                if path == changed and seen[path] == 2:
                    body = json.loads(value.body)
                    if "object" in body:
                        body["object"]["sha"] = "1" * 40
                    else:
                        body["id"] += 1
                    return Response(value.url, value.status, value.headers, json.dumps(body).encode())
                return value
            fixture.hook = mutate
            with self.subTest(changed=changed), self.assertRaisesRegex(Refused, "changed"):
                collect(fixture.api(), plan())

    def test_merged_base_is_immutable_parent_with_actual_target_ancestry(self):
        for descendant in (False, True):
            fixture = Fixture()
            fixture.merged(descendant=descendant)
            value = collect(fixture.api(), plan())
            self.assertEqual(value["pull"]["base"], BASE)
            self.assertEqual(value["pull"]["merge_parents"], [BASE, HEAD])
            self.assertEqual(decision(plan(), value), "integrated")
        for parents in ([HEAD, BASE], [BASE], [BASE, "1" * 40]):
            fixture = Fixture()
            fixture.merged()
            fixture.routes[PREFIX + "/git/commits/" + MERGE]["parents"] = [{"sha": p} for p in parents]
            with self.subTest(parents=parents), self.assertRaises(Refused):
                collect(fixture.api(), plan())
        fixture = Fixture()
        fixture.merged(descendant=True)
        fixture.routes[PREFIX + "/compare/" + MERGE + "..." + "6" * 40]["status"] = "diverged"
        with self.assertRaises(Refused):
            collect(fixture.api(), plan())

    def test_ambiguous_pull_and_workflow_lists_refuse(self):
        for kind in ("pulls", "runs", "jobs"):
            fixture = Fixture()
            if kind == "pulls":
                fixture.routes[PREFIX + "/pulls"].append(dict(fixture.pull, id=802, number=9))
            elif kind == "runs":
                fixture.routes[PREFIX + "/actions/runs"] = page("workflow_runs", [fixture.run, dict(fixture.run, id=52)])
            else:
                fixture.routes[PREFIX + "/actions/runs/51/attempts/2/jobs"] = page("jobs", [fixture.job, dict(fixture.job, id=62)])
            with self.subTest(kind=kind), self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_pending_check_before_run_job_publication_waits_then_advances(self):
        with tempfile.TemporaryDirectory(prefix="aide-github-pending-") as temporary:
            store = ObservationStore(Path(temporary))
            try:
                store.reserve(plan())
                for status in ("queued", "in_progress"):
                    fixture = Fixture()
                    fixture.check.update(status=status, conclusion=None)
                    fixture.routes[PREFIX + "/actions/runs"] = page("workflow_runs", [])
                    fixture.routes[PREFIX + "/actions/runs/51/attempts/2/jobs"] = 404
                    store.observation_attempt(plan())
                    observation = collect(fixture.api(), plan())
                    self.assertFalse(observation["checks_complete"])
                    self.assertEqual(observation["checks"], [])
                    self.assertEqual(store.observe(plan(), observation), "wait_checks")
                    self.assertFalse(any("actions/runs" in url for url in fixture.calls))
                store.observation_attempt(plan())
                self.assertEqual(store.observe(plan(), collect(Fixture().api(), plan())), "qualify_target")
                self.assertEqual(store.db.execute("SELECT COUNT(*) FROM intents").fetchone()[0], 0)
            finally:
                store.close()

    def test_pending_status_never_relaxes_success_or_foreign_provenance(self):
        fixture = Fixture()
        fixture.routes[PREFIX + "/actions/runs"] = page("workflow_runs", [])
        with self.assertRaisesRegex(Refused, "actual Actions push run"):
            collect(fixture.api(), plan())
        for mutation in (lambda check: check["app"].update(id=100),
                         lambda check: check.update(head_sha=BASE),
                         lambda check: check.update(conclusion="success")):
            fixture = Fixture()
            fixture.check.update(status="queued", conclusion=None)
            mutation(fixture.check)
            with self.assertRaises(Refused):
                collect(fixture.api(), plan())

    def test_missing_required_checks_wait_without_inventing_run_provenance(self):
        fixture = Fixture()
        fixture.routes[PREFIX + "/commits/" + HEAD + "/check-runs"] = page("check_runs", [])
        value = collect(fixture.api(), plan())
        self.assertEqual(decision(plan(), value), "wait_checks")
        self.assertFalse(any("actions/runs" in url for url in fixture.calls))

    def test_two_page_collection_is_complete_and_finite(self):
        fixture = Fixture()
        path = PREFIX + "/actions/runs"
        def pages(url, value):
            number = int(parse_qs(urlsplit(url).query)["page"][0])
            items = [{"id": i} for i in (range(1, 101) if number == 1 else range(101, 108))]
            headers = value.headers
            if number == 1:
                headers += (("Link", '<' + ORIGIN + path + '?page=2&per_page=100>; rel="next"'),)
            return Response(url, 200, headers, json.dumps({"total_count": 107, "workflow_runs": items}).encode())
        fixture.hook = pages
        result = fixture.api().pages(path, "workflow_runs")
        self.assertEqual([x["id"] for x in result], list(range(1, 108)))
        self.assertEqual(len(fixture.calls), 2)

    def test_incomplete_foreign_cyclic_duplicate_and_changed_pages_refuse(self):
        path = PREFIX + "/actions/runs"
        for case in ("truncated", "foreign_next", "loop", "duplicate", "count_drift", "too_large", "next_without_full_page"):
            fixture = Fixture()
            def pages(url, value):
                number = int(parse_qs(urlsplit(url).query)["page"][0])
                count = 101
                items = [{"id": i} for i in (range(1, 101) if number == 1 else [101])]
                headers = value.headers
                if number == 1 and case != "truncated":
                    target = ORIGIN + path + "?per_page=100&page=2"
                    if case == "foreign_next":
                        target = "https://foreign.invalid/leak"
                    elif case == "loop":
                        target = url
                    headers += (("Link", '<' + target + '>; rel="next"'),)
                if case == "duplicate" and number == 2:
                    items[0]["id"] = 1
                if case == "count_drift" and number == 2:
                    count = 100
                if case == "too_large":
                    count = 129
                if case == "next_without_full_page":
                    items = items[:1]
                return Response(url, 200, headers, json.dumps({"total_count": count, "workflow_runs": items}).encode())
            fixture.hook = pages
            with self.subTest(case=case), self.assertRaises(Refused):
                fixture.api().pages(path, "workflow_runs")
            self.assertLessEqual(len(fixture.calls), 2)
            self.assertTrue(all(url.startswith(ORIGIN) for url in fixture.calls))

    def test_foreign_non_next_links_and_encoded_path_traversal_refuse(self):
        fixture = Fixture()
        fixture.hook = lambda url, v: Response(url, 200, v.headers +
            (("Link", '<https://foreign.invalid/?page=1>; rel="last"'),), v.body)
        with self.assertRaises(Refused):
            fixture.api().pages(PREFIX + "/actions/runs", "workflow_runs")
        for path in (PREFIX + "/%2e%2e/user", PREFIX + "/%5cuser", PREFIX + "//user"):
            fixture = Fixture()
            with self.subTest(path=path), self.assertRaises(Refused):
                fixture.api().get(path)
            self.assertEqual(fixture.calls, [])

    def test_boolean_count_or_id_and_unknown_complete_list_shapes_refuse(self):
        for body in ({"total_count": True, "workflow_runs": []}, {"total_count": 1, "workflow_runs": [{"id": True}]},
                     {"total_count": 0, "workflow_runs": None}, {"total_count": 0}, None):
            fixture = Fixture()
            fixture.routes[PREFIX + "/actions/runs"] = body
            with self.subTest(body=body), self.assertRaises(Refused):
                fixture.api().pages(PREFIX + "/actions/runs", "workflow_runs")


if __name__ == "__main__":
    unittest.main()
