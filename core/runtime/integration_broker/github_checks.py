"""Bind required check runs to actual GitHub Actions push runs and attempt jobs."""
import re

from .common import Refused, OID, identity
from .github_api import ORIGIN, object_value, positive, text_value


def check_observations(api, plan):
    prefix, head = api.prefix, plan["candidate_commit"]
    checks = api.pages(prefix + "/commits/" + head + "/check-runs", "check_runs", query={"filter": "latest"})
    required = {item["name"] for item in plan["checks"]}
    names, selected, pending = set(), [], False
    expected = {item["name"]: item for item in plan["checks"]}
    for check in checks:
        name = text_value(check.get("name"), 200)
        if name in names:
            raise Refused("GitHub duplicate check name")
        names.add(name)
        if name in required:
            if (positive(object_value(check.get("app")).get("id")) != expected[name]["app_id"] or
                    check.get("head_sha") != head or
                    check.get("url") != ORIGIN + prefix + "/check-runs/" + str(positive(check.get("id")))):
                raise Refused("GitHub required check application or head mismatch")
            positive(object_value(check.get("check_suite")).get("id"))
            if check.get("status") in ("queued", "in_progress"):
                if check.get("conclusion") is not None:
                    raise Refused("GitHub pending check carries a completed conclusion")
                # GitHub may publish a queued check before its run/job appears.
                # Do not invent workflow provenance or turn this normal window
                # into a terminal transport refusal. Complete success below is
                # still required before any check can count toward integration.
                pending = True
            elif check.get("status") == "completed":
                selected.append(check)
            else:
                raise Refused("GitHub unknown required check state")
    if not selected:
        return [], not pending
    runs = api.pages(prefix + "/actions/runs", "workflow_runs", query={"head_sha": head, "event": "push"})
    by_suite = {}
    for run in runs:
        suite = positive(run.get("check_suite_id"))
        if suite in by_suite:
            raise Refused("GitHub ambiguous workflow check suite")
        by_suite[suite] = run
    jobs, result = {}, []
    for check in selected:
        suite = positive(object_value(check.get("check_suite")).get("id"))
        run = by_suite.get(suite)
        if run is None:
            raise Refused("GitHub required check lacks its actual Actions push run")
        run_id, attempt = positive(run.get("id")), positive(run.get("run_attempt"))
        workflow_path = text_value(run.get("path"))
        # The entry workflow is taken from the actual push event's commit. Any
        # workflow/action dependencies still require target-workflow qualification.
        if (not re.fullmatch(r"\.github/workflows/[A-Za-z0-9_.-]+\.ya?ml(?:@[A-Za-z0-9_./-]+)?", workflow_path) or
                run.get("event") != "push" or run.get("head_sha") != head or
                run.get("head_branch") != plan["branch_ref"].removeprefix("refs/heads/") or
                object_value(run.get("repository")).get("full_name") != plan["repository"] or
                object_value(run.get("head_repository")).get("full_name") != plan["repository"] or
                object_value(run.get("head_commit")).get("id") != head or
                run.get("url") != ORIGIN + prefix + "/actions/runs/" + str(run_id)):
            raise Refused("GitHub workflow source or repository does not bind the push head")
        key = run_id, attempt
        if key not in jobs:
            listed = api.pages(prefix + "/actions/runs/" + str(run_id) + "/attempts/" + str(attempt) + "/jobs", "jobs")
            jobs[key] = {positive(job.get("id")): job for job in listed}
        candidates = [job for job in jobs[key].values() if job.get("check_run_url") == check.get("url")]
        if len(candidates) != 1:
            raise Refused("GitHub check has no unique attempt job")
        job = candidates[0]
        if (check.get("url") != ORIGIN + prefix + "/check-runs/" + str(positive(check.get("id"))) or
                check.get("head_sha") != head or job.get("head_sha") != head or
                positive(job.get("run_id")) != run_id or positive(job.get("run_attempt")) != attempt or
                job.get("name") != check.get("name") or job.get("status") != check.get("status") or
                job.get("conclusion") != check.get("conclusion")):
            raise Refused("GitHub check/job/run attempt facts disagree")
        identity(run["head_sha"], OID)
        result.append({"name": check["name"], "app_id": positive(object_value(check.get("app")).get("id")),
                       "workflow_sha": run["head_sha"], "head_commit": check["head_sha"],
                       "status": check.get("status"), "conclusion": check.get("conclusion")})
    # Re-read every used run: a rerun after jobs were read must not promote stale
    # attempt facts. This is a bounded consistency observation, not a server CAS.
    for run_id, attempt in jobs:
        latest = object_value(api.get(prefix + "/actions/runs/" + str(run_id)))
        original = next(run for run in runs if run["id"] == run_id)
        for key in ("id", "run_attempt", "check_suite_id", "head_sha", "head_branch", "event", "path", "status", "conclusion", "repository", "head_repository"):
            if latest.get(key) != original.get(key):
                raise Refused("GitHub workflow run changed during observation")
    return result, not pending
