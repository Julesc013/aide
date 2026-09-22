"""Normalize bounded raw GitHub facts without inventing target qualification."""
from urllib.parse import quote

from .common import Refused, OID, identity
from .github_api import object_value, positive, text_value
from .github_checks import check_observations
from .pr_observation import validate_plan, decision


def commit(api, sha, *, missing=False):
    identity(sha, OID)
    raw = api.get(api.prefix + "/git/commits/" + sha, missing=missing)
    if raw is None and missing:
        return None
    raw = object_value(raw)
    if raw.get("sha") != sha:
        raise Refused("GitHub commit response is another object")
    tree = identity(object_value(raw.get("tree")).get("sha"), OID)
    parents = raw.get("parents")
    if not isinstance(parents, list) or len(parents) > 2:
        raise Refused("GitHub commit parent bounds refused")
    return {"commit": sha, "tree": tree, "parents": [identity(object_value(p).get("sha"), OID) for p in parents]}


def reference(api, name, *, missing=False):
    path = api.prefix + "/git/ref/" + quote(name.removeprefix("refs/"), safe="/")
    raw = api.get(path, missing=missing)
    if raw is None and missing:
        return None
    raw = object_value(raw)
    obj = object_value(raw.get("object"))
    if raw.get("ref") != name or obj.get("type") != "commit":
        raise Refused("GitHub ref response is another name or type")
    return {"ref": raw["ref"], "commit": identity(obj.get("sha"), OID)}


def repository_access(api, expected_actor):
    actor = object_value(api.get("/user"))
    if actor.get("login") != expected_actor or actor.get("type") != "User":
        raise Refused("GitHub authenticated user differs; installation principals need separate qualification")
    positive(actor.get("id"))
    repository = object_value(api.get(api.prefix))
    permissions = object_value(repository.get("permissions"))
    if (repository.get("full_name") != api.repository or repository.get("archived") is not False or
            repository.get("disabled") is not False or permissions.get("pull") is not True or permissions.get("push") is not True):
        raise Refused("GitHub repository access is not the admitted readable/writable target")
    return {"actor": actor["login"], "actor_id": actor["id"], "repository": repository["full_name"],
            "repository_id": positive(repository.get("id")), "permissions": permissions}


def pull_observation(api, plan, target):
    branch = plan["branch_ref"].removeprefix("refs/heads/")
    query = {"state": "all", "head": plan["repository"].split("/")[0] + ":" + branch}
    # Do not filter by base: a retargeted request must be detected, not presented
    # as absent and followed by an attempted second PR.
    listed = api.pages(api.prefix + "/pulls", None, query=query)
    if len(listed) > 1:
        raise Refused("GitHub request branch has ambiguous pull requests")
    if not listed:
        return None
    number = positive(listed[0].get("number"))
    raw = object_value(api.get(api.prefix + "/pulls/" + str(number)))
    if raw.get("number") != number or raw.get("id") != listed[0]["id"]:
        raise Refused("GitHub pull list/detail identity changed")
    base, head = object_value(raw.get("base")), object_value(raw.get("head"))
    for endpoint, expected_ref in ((base, plan["target_ref"]), (head, plan["branch_ref"])):
        if ("refs/heads/" + text_value(endpoint.get("ref")) != expected_ref or
                object_value(endpoint.get("repo")).get("full_name") != plan["repository"]):
            raise Refused("GitHub PR target or source repository/ref changed")
    if (type(raw.get("merged")) is not bool or type(raw.get("draft")) is not bool or
            raw.get("state") not in ("open", "closed") or
            (raw["merged"] and raw["state"] != "closed")):
        raise Refused("GitHub pull state facts refused")
    value = {"number": number, "state": "merged" if raw["merged"] else raw["state"], "draft": raw["draft"],
             "base": identity(base.get("sha"), OID), "base_ref": "refs/heads/" + base["ref"],
             "base_repository": base["repo"]["full_name"], "head": identity(head.get("sha"), OID),
             "head_ref": "refs/heads/" + head["ref"], "head_repository": head["repo"]["full_name"],
             "author": text_value(object_value(raw.get("user")).get("login"), 100),
             "merge_commit": None, "merge_tree": None, "merge_parents": None, "integrated_ancestor": None}
    if raw["merged"]:
        merged = commit(api, identity(raw.get("merge_commit_sha"), OID))
        if len(merged["parents"]) != 2:
            raise Refused("GitHub merged object must have two ordered parents")
        ancestor = target == merged["commit"]
        if not ancestor:
            compared = object_value(api.get(api.prefix + "/compare/" + merged["commit"] + "..." + target))
            ancestor = (compared.get("status") == "ahead" and type(compared.get("behind_by")) is int and
                        compared["behind_by"] == 0 and positive(compared.get("ahead_by")) > 0 and
                        object_value(compared.get("base_commit")).get("sha") == merged["commit"] and
                        object_value(compared.get("merge_base_commit")).get("sha") == merged["commit"])
        # PR base.sha is a mutable projection after merge. The actual merge
        # object's first parent provides the integration base identity.
        value.update(base=merged["parents"][0], merge_commit=merged["commit"], merge_tree=merged["tree"],
                     merge_parents=merged["parents"], integrated_ancestor=ancestor)
    return value


def collect(api, plan):
    """Return facts suitable for decision(); target policy pins remain absent.

    This source collector does not install a credential reader/HTTP client or
    prove server rules. The future qualified target observer must independently
    attest policy and merge-contract digests; the desired plan is never copied.
    """
    validate_plan(plan)
    if api.repository != plan["repository"]:
        raise Refused("GitHub reader does not bind the plan repository")
    access = repository_access(api, plan["actor"])
    target = reference(api, plan["target_ref"])["commit"]
    # Establish actual contents access before a candidate-object 404 can mean
    # absence. Other HTTP errors always refuse rather than infer missing state.
    commit(api, target)
    candidate = commit(api, plan["candidate_commit"], missing=True)
    branch = reference(api, plan["branch_ref"], missing=True)
    pull = pull_observation(api, plan, target)
    checks, checks_complete = check_observations(api, plan) if candidate is not None else ([], True)
    if (pull_observation(api, plan, target) != pull or
            reference(api, plan["target_ref"])["commit"] != target or
            reference(api, plan["branch_ref"], missing=True) != branch or
            repository_access(api, plan["actor"]) != access):
        raise Refused("GitHub target, branch or access changed during observation")
    result = {"schema": "aide.broker.pr-observation.v1", "request_digest": plan["request_digest"],
              "repository": access["repository"], "actor": access["actor"], "target_commit": target,
              "candidate": candidate, "branch": branch, "pull": pull, "checks_complete": checks_complete,
              "checks": checks, "policy_digest": None, "merge_contract_sha256": None}
    decision(plan, result)
    return result
