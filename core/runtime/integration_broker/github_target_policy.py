"""Pure GitHub target-policy comparison; no settings sender is installed."""
from __future__ import annotations

import re

from .common import Refused, OID, canonical, digest, fields, identity
from .github_api import VERSION, positive, repository_name, text_value

TARGET_REF = "refs/heads/dev"
WORKFLOW_PATH = ".github/workflows/aide-cw-checks.yml"
REQUIRED_PERMISSIONS = {
    "actions": "read",
    "administration": "none",
    "checks": "read",
    "contents": "write",
    "metadata": "read",
    "pull_requests": "write",
    "workflows": "none",
}
REPOSITORY_SETTINGS = {
    "allow_auto_merge": False,
    "allow_merge_commit": True,
    "allow_rebase_merge": False,
    "allow_squash_merge": False,
    "delete_branch_on_merge": False,
}


def _identity_requirements():
    return {
        "broker": {"type": "User", "permissions": dict(REQUIRED_PERMISSIONS)},
        "workflow": {
            "app_id": "positive_integer_required",
            "check_name": "nonempty_bounded_text_required",
            "event": "push",
            "path": WORKFLOW_PATH,
            "repository_id": "positive_integer_required",
            "source_commit": "full_sha1_required",
            "source_ref": TARGET_REF,
        },
    }


def _login(value):
    value = text_value(value, 100)
    if (not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", value) or
            value.endswith("-")):
        raise Refused("GitHub login identity refused")
    return value


def _bounded_json(value):
    remaining = 2048

    def visit(item, depth):
        nonlocal remaining
        remaining -= 1
        if remaining < 0 or depth > 16:
            raise Refused("target ruleset body structural bounds refused")
        if isinstance(item, dict):
            if any(not isinstance(key, str) for key in item):
                raise Refused("target ruleset body keys refused")
            for child in item.values():
                visit(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                visit(child, depth + 1)
        elif item is not None and type(item) not in (bool, int, str):
            raise Refused("target ruleset body value refused")

    visit(value, 0)
    if len(canonical(value).encode("utf-8")) > 65536:
        raise Refused("target ruleset body byte bound refused")


def _owner(value):
    fields(value, "login user_id")
    return {"login": _login(value["login"]), "user_id": positive(value["user_id"])}


def _broker(value):
    if value is None:
        return None
    fields(value, "login user_id type permissions")
    permissions = value["permissions"]
    if value["type"] != "User" or permissions != REQUIRED_PERMISSIONS:
        raise Refused("restricted broker principal or permissions refused")
    return {
        "login": _login(value["login"]),
        "user_id": positive(value["user_id"]),
        "type": "User",
        "permissions": dict(REQUIRED_PERMISSIONS),
    }


def _workflow(value):
    if value is None:
        return None
    fields(value, "app_id check_name event path repository_id source_commit source_ref")
    if value["path"] != WORKFLOW_PATH or value["event"] != "push" or value["source_ref"] != TARGET_REF:
        raise Refused("workflow event, path or source ref refused")
    identity(value["source_commit"], OID)
    return {
        "app_id": positive(value["app_id"]),
        "check_name": text_value(value["check_name"], 200),
        "event": "push",
        "path": WORKFLOW_PATH,
        "repository_id": positive(value["repository_id"]),
        "source_commit": value["source_commit"],
        "source_ref": TARGET_REF,
    }


def _rulesets(owner, workflow):
    return [
        {
            "role": "dev_integration",
            "body": {
                "name": "AIDE broker dev integration v1",
                "target": "branch",
                "enforcement": "active",
                "bypass_actors": [],
                "conditions": {"ref_name": {"include": [TARGET_REF], "exclude": []}},
                "rules": [
                    {"type": "deletion"},
                    {"type": "non_fast_forward"},
                    {
                        "type": "pull_request",
                        "parameters": {
                            "allowed_merge_methods": ["merge"],
                            "dismiss_stale_reviews_on_push": True,
                            "require_code_owner_review": False,
                            "require_last_push_approval": False,
                            "required_approving_review_count": 0,
                            "required_review_thread_resolution": True,
                        },
                    },
                    {
                        "type": "required_status_checks",
                        "parameters": {
                            "do_not_enforce_on_create": False,
                            "required_status_checks": [
                                {"context": workflow["check_name"], "integration_id": workflow["app_id"]}
                            ],
                            "strict_required_status_checks_policy": True,
                        },
                    },
                    {
                        "type": "workflows",
                        "parameters": {
                            "do_not_enforce_on_create": False,
                            "workflows": [{
                                "path": workflow["path"],
                                "ref": workflow["source_ref"],
                                "repository_id": workflow["repository_id"],
                                "sha": workflow["source_commit"],
                            }],
                        },
                    },
                ],
            },
        },
        {
            "role": "broker_non_dev_confinement",
            "body": {
                "name": "AIDE broker non-dev confinement v1",
                "target": "branch",
                "enforcement": "active",
                "bypass_actors": [
                    {"actor_id": owner["user_id"], "actor_type": "User", "bypass_mode": "always"}
                ],
                "conditions": {"ref_name": {"include": ["~ALL"], "exclude": [TARGET_REF]}},
                "rules": [
                    {"type": "update", "parameters": {"update_allows_fetch_and_merge": False}},
                    {"type": "deletion"},
                    {"type": "non_fast_forward"},
                ],
            },
        },
    ]


def desired_target_policy(repository, *, repository_id, owner, broker=None, workflow=None):
    """Build exact desired state or a deliberately unresolved review subject."""
    repository = repository_name(repository)
    repository_id = positive(repository_id)
    owner = _owner(owner)
    broker = _broker(broker)
    workflow = _workflow(workflow)
    if broker is not None and (broker["user_id"] == owner["user_id"] or
            broker["login"].casefold() == owner["login"].casefold()):
        raise Refused("broker principal must be distinct from owner bypass identity")
    if workflow is not None and workflow["repository_id"] != repository_id:
        raise Refused("workflow repository identity differs from target")
    materialized = _rulesets(owner, workflow) if broker is not None and workflow is not None else None
    return {
        "schema": "aide.github-target-policy.v1",
        "repository": repository,
        "repository_id": repository_id,
        "api_version": VERSION,
        "target_ref": TARGET_REF,
        "merge_method": "merge",
        "repository_settings": dict(REPOSITORY_SETTINGS),
        "identity_requirements": _identity_requirements(),
        "owner": owner,
        "broker": broker,
        "workflow": workflow,
        "rulesets": materialized,
        "guarantees": {
            "destination_enforced_when_qualified": [
                "expected_head",
                "strict_app_bound_required_check",
                "exact_required_workflow",
                "pull_request_only_dev_update",
                "non_dev_update_restriction",
                "deletion_restriction",
                "non_fast_forward_restriction",
            ],
            "local_preconditions": [
                "expected_base",
                "expected_actor",
                "expected_policy_digest",
                "expected_workflow_source",
            ],
            "unsupported": [
                "atomic_expected_base_argument",
                "atomic_policy_compare_and_swap",
                "hidden_bypass_inference",
                "uncertain_mutation_replay",
            ],
        },
    }


def validate_target_policy(policy):
    fields(policy, "schema repository repository_id api_version target_ref merge_method repository_settings identity_requirements owner broker workflow rulesets guarantees")
    if (policy["schema"] != "aide.github-target-policy.v1" or
            policy["api_version"] != VERSION or policy["target_ref"] != TARGET_REF or
            policy["merge_method"] != "merge" or policy["repository_settings"] != REPOSITORY_SETTINGS or
            policy["identity_requirements"] != _identity_requirements()):
        raise Refused("target policy version, endpoint or repository settings refused")
    repository_name(policy["repository"])
    repository_id = positive(policy["repository_id"])
    owner = _owner(policy["owner"])
    broker = _broker(policy["broker"])
    workflow = _workflow(policy["workflow"])
    if broker is not None and (broker["user_id"] == owner["user_id"] or
            broker["login"].casefold() == owner["login"].casefold()):
        raise Refused("broker principal must be distinct from owner bypass identity")
    if workflow is not None and workflow["repository_id"] != repository_id:
        raise Refused("workflow repository identity differs from target")
    expected = _rulesets(owner, workflow) if broker is not None and workflow is not None else None
    if policy["rulesets"] != expected:
        raise Refused("target policy rulesets do not derive from exact identities")
    expected_guarantees = desired_target_policy(
        policy["repository"], repository_id=repository_id, owner=owner, broker=broker, workflow=workflow
    )["guarantees"]
    if policy["guarantees"] != expected_guarantees:
        raise Refused("target guarantee classification refused")


def validate_target_observation(observation):
    fields(observation, "schema repository repository_id observed_by visibility repository_settings principal workflow rulesets effective_rules classic_branch_protection")
    if observation["schema"] != "aide.github-target-observation.v1":
        raise Refused("target observation schema refused")
    repository_name(observation["repository"])
    positive(observation["repository_id"])
    observed_by = observation["observed_by"]
    fields(observed_by, "login user_id type repository_permission")
    _login(observed_by["login"])
    positive(observed_by["user_id"])
    if observed_by["type"] != "User" or observed_by["repository_permission"] not in ("read", "triage", "write", "maintain", "admin"):
        raise Refused("target observer identity refused")
    visibility = observation["visibility"]
    fields(visibility, "bypass_actors_complete effective_rules_complete rulesets_complete workflows_complete")
    if any(type(value) is not bool for value in visibility.values()):
        raise Refused("target observation visibility must be explicit booleans")
    if not isinstance(observation["repository_settings"], dict) or set(observation["repository_settings"]) != set(REPOSITORY_SETTINGS):
        raise Refused("target repository settings shape refused")
    if any(type(value) is not bool for value in observation["repository_settings"].values()):
        raise Refused("target repository settings must be booleans")
    principal = observation["principal"]
    if principal is not None:
        _broker(principal)
    workflow = observation["workflow"]
    if workflow is not None:
        _workflow(workflow)
    rulesets = observation["rulesets"]
    if not isinstance(rulesets, list) or len(rulesets) > 16:
        raise Refused("target ruleset observation bounds refused")
    ids, roles = set(), set()
    for record in rulesets:
        fields(record, "body id role source source_type")
        rule_id = positive(record["id"])
        role = text_value(record["role"], 64)
        if not re.fullmatch(r"[a-z][a-z0-9_]*", role):
            raise Refused("target ruleset role refused")
        if rule_id in ids or role in roles or record["source_type"] != "Repository" or record["source"] != observation["repository"]:
            raise Refused("target ruleset identity or source refused")
        if not isinstance(record["body"], dict):
            raise Refused("target ruleset body refused")
        _bounded_json(record["body"])
        ids.add(rule_id)
        roles.add(role)
    effective = observation["effective_rules"]
    fields(effective, "status target_ref rules")
    if effective["status"] != "observed" or effective["target_ref"] != TARGET_REF:
        raise Refused("effective target rules observation refused")
    if not isinstance(effective["rules"], list) or len(effective["rules"]) > 128:
        raise Refused("effective target rules bounds refused")
    for rule in effective["rules"]:
        if not isinstance(rule, dict):
            raise Refused("effective target rule body refused")
        _bounded_json(rule)
    protection = observation["classic_branch_protection"]
    fields(protection, "body status target_ref")
    if protection["target_ref"] != TARGET_REF or protection["status"] not in ("absent", "present"):
        raise Refused("classic branch protection observation refused")
    if protection["status"] == "absent":
        if protection["body"] is not None:
            raise Refused("absent classic protection cannot carry a body")
    elif not isinstance(protection["body"], dict):
        raise Refused("present classic protection body required")
    else:
        _bounded_json(protection["body"])


def target_policy_review_plan(policy, observation):
    """Return a non-mutating exact review plan; never perform or authorize it."""
    validate_target_policy(policy)
    validate_target_observation(observation)
    blockers = []
    if observation["repository"] != policy["repository"]:
        blockers.append("repository_identity_mismatch")
    if observation["repository_id"] != policy["repository_id"]:
        blockers.append("repository_id_mismatch")
    if observation["observed_by"] != {
            "login": policy["owner"]["login"], "user_id": policy["owner"]["user_id"],
            "type": "User", "repository_permission": "admin"}:
        blockers.append("owner_admin_observer_unresolved")
    for name, complete in sorted(observation["visibility"].items()):
        if not complete:
            blockers.append("incomplete_visibility:" + name)
    if policy["broker"] is None:
        blockers.append("broker_principal_unresolved")
    elif observation["principal"] != policy["broker"]:
        blockers.append("broker_principal_mismatch")
    if policy["workflow"] is None:
        blockers.append("workflow_check_identity_unresolved")
    elif observation["workflow"] != policy["workflow"]:
        blockers.append("workflow_check_identity_mismatch")

    desired_by_role = {item["role"]: item["body"] for item in policy["rulesets"] or []}
    observed_by_role = {item["role"]: item for item in observation["rulesets"]}
    unexpected = sorted(set(observed_by_role) - set(desired_by_role))
    if unexpected:
        blockers.append("unexpected_rulesets:" + ",".join(unexpected))
    for role in sorted(set(observed_by_role) & set(desired_by_role)):
        if observed_by_role[role]["body"] != desired_by_role[role]:
            blockers.append("ruleset_drift:" + role)
    expected_effective = sorted(
        (observed_by_role[role]["body"] for role in observed_by_role), key=canonical)
    observed_effective = sorted(observation["effective_rules"]["rules"], key=canonical)
    if observed_effective != expected_effective:
        blockers.append("effective_rules_drift")
    if observation["classic_branch_protection"]["status"] != "absent":
        blockers.append("classic_branch_protection_requires_review")

    operations = []
    if not blockers:
        if observation["repository_settings"] != policy["repository_settings"]:
            operations.append({
                "method": "PATCH",
                "path": "/repos/" + policy["repository"],
                "body": policy["repository_settings"],
            })
        for role in sorted(set(desired_by_role) - set(observed_by_role)):
            operations.append({
                "method": "POST",
                "path": "/repos/" + policy["repository"] + "/rulesets",
                "role": role,
                "body": desired_by_role[role],
            })
    result = {
        "schema": "aide.github-target-policy-review-plan.v1",
        "mode": "review_only",
        "repository": policy["repository"],
        "policy_digest": digest(policy),
        "observation_digest": digest(observation),
        "status": "blocked" if blockers else ("already_current" if not operations else "ready_for_review"),
        "blockers": blockers,
        "operations": operations,
        "required_reviews": [
            "target_policy_and_bypass",
            "restricted_principal_and_permissions",
            "workflow_and_check_provenance",
            "exact_operation_bytes",
        ],
        "apply_authorized": False,
        "network_calls": "none",
        "settings_mutated": False,
        "workflow_installed": False,
        "hosted_effects_run": False,
    }
    result["plan_digest"] = digest(result)
    return result


def canonical_policy_bytes(value):
    """Expose deterministic review bytes without adding a writer or sender."""
    return (canonical(value) + "\n").encode("utf-8")
