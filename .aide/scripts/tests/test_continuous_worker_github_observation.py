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
from core.runtime.integration_broker.github_merge import classify_response, merge_request
from core.runtime.integration_broker.github_observation import collect
from core.runtime.integration_broker.pr_observation import decision, ObservationStore
from core.runtime.integration_broker.github_target_policy import (
    REQUIRED_PERMISSIONS,
    REPOSITORY_SETTINGS,
    canonical_policy_bytes,
    desired_target_policy,
    target_policy_review_plan,
    validate_target_policy,
)

REPO = "fixture/repo"
PREFIX = "/repos/" + REPO
BRANCH = "task/aide-cw-" + "a" * 64
BASE, HEAD, TREE, MERGE = "b" * 40, "c" * 40, "d" * 40, "e" * 40


def plan():
    return {"schema": "aide.broker.pr-plan.v1", "request_digest": "a" * 64,
            "repository": REPO, "actor": "fixture-broker", "target_ref": "refs/heads/dev",
            "base": BASE, "candidate_commit": HEAD, "candidate_tree": TREE,
            "branch_ref": "refs/heads/" + BRANCH,
            "checks": [{"name": "required", "app_id": 99, "workflow_sha": HEAD,
                        "workflow_path": ".github/workflows/aide-cw-checks.yml",
                        "workflow_ref": "refs/heads/" + BRANCH,
                        "workflow_event": "push"}],
            "policy_digest": "f" * 64, "merge_contract_sha256": "9" * 64,
            "expires_at": 2000, "max_observations": 16}


def git_commit(sha, parents, tree=TREE):
    return {"sha": sha, "tree": {"sha": tree}, "parents": [{"sha": p} for p in parents]}


def page(key, values):
    return {"total_count": len(values), key: values}


def qualified_observation():
    p = plan()
    value = collect(Fixture().api(), p)
    value["policy_digest"] = p["policy_digest"]
    value["merge_contract_sha256"] = p["merge_contract_sha256"]
    return p, value


def owner():
    return {"login": "fixture-owner", "user_id": 76}


def broker():
    return {"login": "fixture-broker", "user_id": 77, "type": "User",
            "permissions": dict(REQUIRED_PERMISSIONS)}


def workflow():
    return {"app_id": 99, "check_name": "AIDE Continuous Worker / required",
            "event": "push", "path": ".github/workflows/aide-cw-checks.yml",
            "repository_id": 880, "source_commit": HEAD, "source_ref": "refs/heads/dev"}


def target_policy(*, resolved=True):
    return desired_target_policy(REPO, repository_id=880, owner=owner(),
        broker=broker() if resolved else None, workflow=workflow() if resolved else None)


def target_observation(policy, *, current=False):
    records = []
    if current and policy["rulesets"] is not None:
        records = [{"id": 400 + index, "role": item["role"], "source_type": "Repository",
                    "source": REPO, "body": copy.deepcopy(item["body"])}
                   for index, item in enumerate(policy["rulesets"])]
    return {
        "schema": "aide.github-target-observation.v1",
        "repository": REPO,
        "repository_id": 880,
        "observed_by": {"login": owner()["login"], "user_id": owner()["user_id"],
                        "type": "User", "repository_permission": "admin"},
        "visibility": {"bypass_actors_complete": True, "effective_rules_complete": True,
                       "rulesets_complete": True, "workflows_complete": True},
        "repository_settings": (dict(REPOSITORY_SETTINGS) if current else {
            **REPOSITORY_SETTINGS, "allow_rebase_merge": True, "allow_squash_merge": True}),
        "principal": copy.deepcopy(policy["broker"]),
        "workflow": copy.deepcopy(policy["workflow"]),
        "rulesets": records,
        "effective_rules": {"status": "observed", "target_ref": "refs/heads/dev",
                            "rules": copy.deepcopy([item["body"] for item in records])},
        "classic_branch_protection": {"status": "absent", "target_ref": "refs/heads/dev",
                                      "body": None},
    }


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
                    "head_branch": BRANCH, "event": "push",
                    "path": REPO + "/.github/workflows/aide-cw-checks.yml@" + BRANCH,
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
    def test_merge_request_has_fixed_expected_head_and_ordinary_merge(self):
        p, observation = qualified_observation()
        request = merge_request(p, observation)
        self.assertEqual(request["method"], "PUT")
        self.assertEqual(request["url"], ORIGIN + PREFIX + "/pulls/8/merge")
        self.assertEqual(request["headers"], {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2026-03-10",
        })
        self.assertEqual(json.loads(request["body"]), {"merge_method": "merge", "sha": HEAD})
        self.assertNotIn("base", json.loads(request["body"]))

    def test_merge_request_rechecks_base_head_actor_and_policy(self):
        mutations = (
            lambda p, value: value.update(target_commit="1" * 40),
            lambda p, value: value["pull"].update(base="1" * 40),
            lambda p, value: value["pull"].update(head="1" * 40),
            lambda p, value: value["pull"].update(author="another-actor"),
            lambda p, value: value.update(policy_digest="1" * 64),
            lambda p, value: value.update(merge_contract_sha256="1" * 64),
        )
        for mutation in mutations:
            p, observation = qualified_observation()
            mutation(p, observation)
            with self.subTest(mutation=mutation), self.assertRaises(Refused):
                merge_request(p, observation)

    def test_merge_response_is_submission_not_integration(self):
        p, observation = qualified_observation()
        request = merge_request(p, observation)
        response = Response(request["url"], 200,
            (("Content-Type", "application/json; charset=utf-8"),),
            json.dumps({"sha": MERGE, "merged": True, "message": "Pull Request successfully merged"}).encode())
        result = classify_response(p, observation, response)
        self.assertEqual(result, {"status": "submitted", "response_sha": MERGE})
        self.assertNotEqual(result["status"], "integrated")
        self.assertEqual(decision(p, observation), "merge")

    def test_head_conflict_and_nonmerge_responses_refuse_without_rewrite(self):
        p, observation = qualified_observation()
        request = merge_request(p, observation)
        frozen = copy.deepcopy(observation)
        for status in (405, 409, 422):
            response = Response(request["url"], status,
                (("Content-Type", "application/json"),),
                json.dumps({"message": "server refused candidate"}).encode())
            with self.subTest(status=status):
                self.assertEqual(classify_response(p, observation, response),
                                 {"status": "refused", "http_status": status})
        self.assertEqual(observation, frozen)
        self.assertEqual(json.loads(merge_request(p, observation)["body"])["sha"], HEAD)

    def test_merge_response_requires_exact_endpoint_shape_and_bounds(self):
        p, observation = qualified_observation()
        request = merge_request(p, observation)
        bodies = (
            (200, {"sha": MERGE, "merged": False, "message": "not merged"}),
            (200, {"sha": MERGE, "merged": True, "message": "ok", "extra": True}),
            (201, {"message": "unexpected"}),
        )
        first = Response(request["url"], bodies[0][0], (("Content-Type", "application/json"),),
                         json.dumps(bodies[0][1]).encode())
        self.assertEqual(classify_response(p, observation, first),
                         {"status": "refused", "http_status": 200})
        for status, body in bodies[1:]:
            response = Response(request["url"], status, (("Content-Type", "application/json"),),
                                json.dumps(body).encode())
            with self.subTest(status=status), self.assertRaises(Refused):
                classify_response(p, observation, response)
        for response in (
            Response("https://api.github.com/repos/foreign/repo/pulls/8/merge", 409,
                     (("Content-Type", "application/json"),), b'{"message":"conflict"}'),
            Response(request["url"], 409, (("Content-Type", "text/plain"),), b"conflict"),
            Response(request["url"], 409, (("Content-Type", "application/json"),) * 2,
                     b'{"message":"conflict"}'),
            Response(request["url"], 409, (("Content-Type", "application/json"),),
                     b'{"message":"' + b"x" * 65536 + b'"}'),
        ):
            with self.assertRaises(Refused):
                classify_response(p, observation, response)

    def test_complete_raw_observation_never_invents_policy_qualification(self):
        fixture, p = Fixture(), plan()
        result = collect(fixture.api(), p)
        self.assertEqual(decision(p, result), "qualify_target")
        self.assertIsNone(result["policy_digest"])
        self.assertIsNone(result["merge_contract_sha256"])
        self.assertEqual(result["checks"][0]["workflow_sha"], HEAD)
        self.assertEqual(result["checks"][0]["workflow_path"],
                         ".github/workflows/aide-cw-checks.yml")
        self.assertEqual(result["checks"][0]["workflow_ref"], "refs/heads/" + BRANCH)
        self.assertEqual(result["checks"][0]["workflow_event"], "push")
        self.assertEqual(result["checks"][0]["workflow_run_id"], 51)
        self.assertEqual(result["checks"][0]["workflow_run_attempt"], 2)
        self.assertEqual(result["checks"][0]["check_run_id"], 31)
        self.assertEqual(result["checks"][0]["check_suite_id"], 41)
        for key, value in (("workflow_sha", "1" * 40),
                           ("workflow_path", ".github/workflows/other.yml"),
                           ("workflow_ref", "refs/heads/dev"),
                           ("workflow_event", "pull_request")):
            changed = plan()
            changed["checks"][0][key] = value
            with self.subTest(key=key), self.assertRaises(Refused):
                collect(fixture.api(), changed)

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

    def test_workflow_run_path_ref_accepts_documented_relative_and_repo_forms(self):
        for source in (
                ".github/workflows/aide-cw-checks.yml@" + BRANCH,
                REPO + "/.github/workflows/aide-cw-checks.yml@" + BRANCH):
            with self.subTest(source=source):
                fixture = Fixture()
                fixture.run["path"] = source
                result = collect(fixture.api(), plan())
                check = result["checks"][0]
                self.assertEqual(check["workflow_path"], ".github/workflows/aide-cw-checks.yml")
                self.assertEqual(check["workflow_ref"], "refs/heads/" + BRANCH)

    def test_workflow_run_path_ref_refuses_wrong_missing_and_malformed_selectors(self):
        cases = (
            ".github/workflows/other.yml@" + BRANCH,
            ".github/workflows/aide-cw-checks.yml@dev",
            "other/repo/.github/workflows/aide-cw-checks.yml@" + BRANCH,
            ".github/workflows/aide-cw-checks.yml",
            ".github/workflows/aide-cw-checks.yml@",
            ".github/workflows/aide-cw-checks.yml@refs/heads/" + BRANCH,
            ".github/workflows/aide-cw-checks.yml@task//broken",
        )
        for source in cases:
            with self.subTest(source=source):
                fixture = Fixture()
                fixture.run["path"] = source
                with self.assertRaises(Refused):
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


class GitHubTargetPolicyTests(unittest.TestCase):
    def test_unresolved_identities_produce_an_empty_blocked_plan(self):
        policy = target_policy(resolved=False)
        self.assertEqual(policy["identity_requirements"]["broker"], {
            "type": "User", "permissions": REQUIRED_PERMISSIONS})
        self.assertEqual(policy["identity_requirements"]["workflow"]["path"],
                         ".github/workflows/aide-cw-checks.yml")
        observation = target_observation(policy)
        observation["principal"] = None
        observation["workflow"] = None
        result = target_policy_review_plan(policy, observation)
        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["operations"], [])
        self.assertEqual(result["blockers"], [
            "broker_principal_unresolved", "workflow_check_identity_unresolved"])
        self.assertFalse(result["apply_authorized"])
        self.assertEqual(result["network_calls"], "none")
        self.assertFalse(result["settings_mutated"])
        self.assertFalse(result["workflow_installed"])
        self.assertFalse(result["hosted_effects_run"])

    def test_resolved_empty_target_materializes_exact_review_operations(self):
        policy = target_policy()
        result = target_policy_review_plan(policy, target_observation(policy))
        self.assertEqual(result["status"], "ready_for_review")
        self.assertFalse(result["apply_authorized"])
        self.assertEqual([(item["method"], item["path"]) for item in result["operations"]], [
            ("PATCH", "/repos/fixture/repo"),
            ("POST", "/repos/fixture/repo/rulesets"),
            ("POST", "/repos/fixture/repo/rulesets"),
        ])
        self.assertEqual(result["operations"][0]["body"], REPOSITORY_SETTINGS)
        self.assertEqual([item.get("role") for item in result["operations"][1:]], [
            "broker_non_dev_confinement", "dev_integration"])

    def test_policy_requires_pr_merge_strict_app_check_and_non_dev_confinement(self):
        policy = target_policy()
        by_role = {item["role"]: item["body"] for item in policy["rulesets"]}
        dev = by_role["dev_integration"]
        self.assertEqual(dev["bypass_actors"], [])
        self.assertEqual(dev["conditions"], {"ref_name": {"include": ["refs/heads/dev"], "exclude": []}})
        pull = next(rule for rule in dev["rules"] if rule["type"] == "pull_request")
        self.assertEqual(pull["parameters"]["allowed_merge_methods"], ["merge"])
        required = next(rule for rule in dev["rules"] if rule["type"] == "required_status_checks")
        self.assertTrue(required["parameters"]["strict_required_status_checks_policy"])
        self.assertEqual(required["parameters"]["required_status_checks"], [
            {"context": workflow()["check_name"], "integration_id": workflow()["app_id"]}])
        self.assertNotIn("workflows", [rule["type"] for rule in dev["rules"]])
        self.assertNotIn("exact_required_workflow",
                         policy["guarantees"]["destination_enforced_when_qualified"])
        self.assertIn("exact_workflow_run_path_event_and_head",
                      policy["guarantees"]["local_preconditions"])
        self.assertEqual(policy["guarantees"]["monitored"], [
            "workflow_run_and_attempt_identity",
            "check_run_and_suite_identity",
        ])
        self.assertIn("server_enforced_exact_workflow_source",
                      policy["guarantees"]["unsupported"])
        self.assertIn("same_app_same_check_name_collision_exclusion",
                      policy["guarantees"]["unsupported"])
        confined = by_role["broker_non_dev_confinement"]
        self.assertEqual(confined["conditions"], {
            "ref_name": {"include": ["~ALL"], "exclude": ["refs/heads/dev"]}})
        self.assertEqual([rule["type"] for rule in confined["rules"]], [
            "update", "deletion", "non_fast_forward"])
        self.assertEqual(confined["rules"][0]["parameters"], {
            "update_allows_fetch_and_merge": False})
        self.assertEqual(confined["bypass_actors"], [
            {"actor_id": owner()["user_id"], "actor_type": "User", "bypass_mode": "always"}])

    def test_exact_current_target_needs_no_operation_but_not_self_authorization(self):
        policy = target_policy()
        result = target_policy_review_plan(policy, target_observation(policy, current=True))
        self.assertEqual(result["status"], "already_current")
        self.assertEqual(result["operations"], [])
        self.assertFalse(result["apply_authorized"])
        self.assertEqual(len(result["required_reviews"]), 4)

    def test_incomplete_visibility_and_wrong_observer_fail_closed(self):
        policy = target_policy()
        for mutation, blocker in (
            (lambda value: value["visibility"].update(bypass_actors_complete=False),
             "incomplete_visibility:bypass_actors_complete"),
            (lambda value: value["observed_by"].update(login="another-owner"),
             "owner_admin_observer_unresolved"),
            (lambda value: value["observed_by"].update(repository_permission="write"),
             "owner_admin_observer_unresolved"),
        ):
            observation = target_observation(policy)
            mutation(observation)
            result = target_policy_review_plan(policy, observation)
            with self.subTest(blocker=blocker):
                self.assertEqual(result["status"], "blocked")
                self.assertIn(blocker, result["blockers"])
                self.assertEqual(result["operations"], [])

    def test_principal_and_workflow_drift_fail_before_plan_materialization(self):
        policy = target_policy()
        for mutation, blocker in (
            (lambda value: value["principal"].update(login="other-broker"),
             "broker_principal_mismatch"),
            (lambda value: value["workflow"].update(source_commit=BASE),
             "workflow_check_identity_mismatch"),
            (lambda value: value["workflow"].update(app_id=100),
             "workflow_check_identity_mismatch"),
        ):
            observation = target_observation(policy)
            mutation(observation)
            result = target_policy_review_plan(policy, observation)
            with self.subTest(blocker=blocker):
                self.assertEqual(result["status"], "blocked")
                self.assertIn(blocker, result["blockers"])
                self.assertEqual(result["operations"], [])

    def test_unknown_or_drifted_rulesets_refuse_automatic_repair(self):
        policy = target_policy()
        observation = target_observation(policy, current=True)
        observation["rulesets"][0]["role"] = "foreign_policy"
        result = target_policy_review_plan(policy, observation)
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(any(item.startswith("unexpected_rulesets:") for item in result["blockers"]))
        self.assertEqual(result["operations"], [])

        observation = target_observation(policy, current=True)
        observation["rulesets"][0]["body"]["enforcement"] = "disabled"
        result = target_policy_review_plan(policy, observation)
        self.assertEqual(result["status"], "blocked")
        self.assertTrue(any(item.startswith("ruleset_drift:") for item in result["blockers"]))
        self.assertEqual(result["operations"], [])

    def test_ruleset_observation_identity_and_structure_are_bounded(self):
        policy = target_policy()
        mutations = (
            lambda record: record.update(role={"not": "text"}),
            lambda record: record.update(role="Not-Stable"),
            lambda record: record.update(body={"deep": [[[[[[[[[[[[[[[[["x"]]]]]]]]]]]]]]]]]}),
            lambda record: record.update(body={"large": "x" * 65537}),
        )
        for mutation in mutations:
            observation = target_observation(policy, current=True)
            mutation(observation["rulesets"][0])
            with self.subTest(mutation=mutation), self.assertRaises(Refused):
                target_policy_review_plan(policy, observation)

    def test_overprivileged_principal_and_unbound_workflow_are_refused(self):
        bad_broker = broker()
        bad_broker["permissions"]["administration"] = "write"
        with self.assertRaisesRegex(Refused, "principal or permissions"):
            desired_target_policy(REPO, repository_id=880, owner=owner(),
                                  broker=bad_broker, workflow=workflow())
        for key, value in (("path", ".github/workflows/other.yml"),
                           ("event", "pull_request"), ("source_ref", "refs/heads/main")):
            bad_workflow = workflow()
            bad_workflow[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(Refused, "workflow event"):
                desired_target_policy(REPO, repository_id=880, owner=owner(),
                                      broker=broker(), workflow=bad_workflow)

    def test_owner_and_broker_bypass_identities_must_be_distinct(self):
        for mutation in (
                lambda value: value.update(user_id=owner()["user_id"]),
                lambda value: value.update(login=owner()["login"].swapcase())):
            bad_broker = broker()
            mutation(bad_broker)
            with self.assertRaisesRegex(Refused, "distinct from owner"):
                desired_target_policy(REPO, repository_id=880, owner=owner(),
                                      broker=bad_broker, workflow=workflow())

    def test_repository_effective_rules_and_classic_protection_are_digest_bound(self):
        policy = target_policy()
        for mutation, blocker in (
                (lambda value: value.update(repository_id=881), "repository_id_mismatch"),
                (lambda value: value["effective_rules"]["rules"].append({"type": "deletion"}),
                 "effective_rules_drift"),
                (lambda value: value["classic_branch_protection"].update(
                    status="present", body={"enforce_admins": {"enabled": True}}),
                 "classic_branch_protection_requires_review")):
            observation = target_observation(policy)
            original = target_policy_review_plan(policy, observation)
            mutation(observation)
            changed = target_policy_review_plan(policy, observation)
            with self.subTest(blocker=blocker):
                self.assertNotEqual(original["observation_digest"], changed["observation_digest"])
                self.assertNotEqual(original["plan_digest"], changed["plan_digest"])
                if blocker is not None:
                    self.assertIn(blocker, changed["blockers"])

        for mutation in (
                lambda value: value.pop("effective_rules"),
                lambda value: value.pop("classic_branch_protection"),
                lambda value: value["classic_branch_protection"].update(body={}),
                lambda value: value["effective_rules"].update(status="asserted")):
            observation = target_observation(policy)
            mutation(observation)
            with self.assertRaises(Refused):
                target_policy_review_plan(policy, observation)

    def test_invalid_github_login_boundaries_are_refused(self):
        for login in ("-owner", "owner-", "owner_name", "x" * 40):
            bad_owner = owner()
            bad_owner["login"] = login
            with self.subTest(login=login), self.assertRaisesRegex(Refused, "login identity"):
                desired_target_policy(REPO, repository_id=880, owner=bad_owner)

    def test_policy_rulesets_are_derived_and_cannot_be_caller_replaced(self):
        policy = target_policy()
        validate_target_policy(policy)
        policy["rulesets"][0]["body"]["bypass_actors"] = [
            {"actor_id": broker()["user_id"], "actor_type": "User", "bypass_mode": "always"}]
        with self.assertRaisesRegex(Refused, "do not derive"):
            validate_target_policy(policy)

    def test_digests_and_canonical_bytes_bind_every_review_input(self):
        policy = target_policy()
        observation = target_observation(policy)
        first = target_policy_review_plan(policy, observation)
        second = target_policy_review_plan(policy, copy.deepcopy(observation))
        self.assertEqual(first, second)
        self.assertEqual(canonical_policy_bytes(first), canonical_policy_bytes(second))
        observation["repository_settings"]["delete_branch_on_merge"] = True
        changed = target_policy_review_plan(policy, observation)
        self.assertNotEqual(first["observation_digest"], changed["observation_digest"])
        self.assertNotEqual(first["plan_digest"], changed["plan_digest"])
        self.assertFalse(any(term in canonical_policy_bytes(first).decode().lower()
            for term in ("authorization:", "bearer ", "token=")))

    def test_committed_unresolved_review_packet_matches_the_pure_generator(self):
        evidence = ROOT / ".aide/queue/AIDE-CW-GITHUB-TARGET-QUALIFICATION-01/evidence"
        desired = json.loads((evidence / "desired-target-policy-2026-09-22.json").read_text(encoding="utf-8"))
        current = json.loads((evidence / "current-target-policy-2026-09-22.json").read_text(encoding="utf-8"))
        recorded_plan = json.loads((evidence / "target-policy-review-plan-2026-09-22.json").read_text(encoding="utf-8"))
        self.assertEqual(desired, desired_target_policy(
            "Julesc013/aide", repository_id=1192621212,
            owner={"login": "Julesc013", "user_id": 30209022}))
        self.assertEqual(recorded_plan, target_policy_review_plan(desired, current))
        self.assertEqual(recorded_plan["operations"], [])
        self.assertEqual(recorded_plan["status"], "blocked")


if __name__ == "__main__":
    unittest.main()
