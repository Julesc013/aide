"""Coordinator-v1 frozen evidence and externally issued broker authority boundary."""
from pathlib import Path

from .state import Refused, canonical, digest
from .contract import registered_command
from core.runtime.integration_broker.common import Git, fields, MAX_TOTAL, parse_json
from core.runtime.integration_broker.candidate import freeze_candidate, read_candidate
from core.runtime.integration_broker.service import validate_authority


def freeze(coordinator, attempt, evidence):
    config, spec = coordinator.config, attempt["spec"]
    exchange = Path(config["integration"]["exchange_root"])
    used = sum(p.stat().st_size for p in coordinator.state.root.rglob("*") if p.is_file())
    budget = min(MAX_TOTAL, config["limits"]["max_state_bytes"] - used - 2097152)
    if budget <= 0:
        raise Refused("insufficient reserved space for frozen handoff")
    exchange.mkdir(exist_ok=True)
    registered = config["git"]
    candidate = freeze_candidate(Git(registered["argv"][0], registered["sha256"]),
                                 Path(spec["workspace"]), exchange, repository=spec["repository"],
                                 base=spec["base"], allowed=spec["allowed_paths"],
                                 checkout=evidence["literal_checkout_v1"], max_total=budget)
    manifest, _ = read_candidate(exchange, candidate)
    verification = {
        "coding_session": evidence["coding"]["session_id"],
        "assurance_session": evidence["assurance"]["session_id"],
        "assurance_passed": True, "subject_tree": manifest["candidate_tree"],
        "checks": [{"name": "test." + str(index), "result": "PASS",
                    "artifact_sha256": digest(result["artifacts"])}
                   for index, result in enumerate(evidence["tests"])],
    }
    return {"schema": "aide.broker.authority-request.v1", "task": spec["id"],
            "repository": spec["repository"], "base": spec["base"],
            "base_tree": manifest["base_tree"], "allowed_paths": spec["allowed_paths"],
            "admission_digest": spec["source_sha256"], "candidate": candidate,
            "verification": verification}


def observation(coordinator, attempt, operation, request):
    count = coordinator.state.db.execute(
        "SELECT COUNT(*) FROM effects WHERE attempt=? AND kind LIKE 'integration_observation.%'",
        (attempt["id"],)).fetchone()[0]
    if count >= coordinator.config["limits"]["max_integration_queries"]:
        raise Refused("integration observation retry limit")
    command = registered_command(coordinator.config["integration"][operation])
    output, receipt = coordinator.effect(attempt, "integration_observation." + str(count), command,
                                         coordinator.config["integration"]["cwd"], canonical(request))
    coordinator.require_success(receipt)
    return parse_json((output / "stdout").read_bytes())


def request_from_authority(value, frozen, config):
    fields(value, "schema request_digest status authority")
    if value["schema"] != "aide.broker.authority-observation.v1" or value["request_digest"] != digest(frozen):
        raise Refused("authority observation does not bind frozen evidence")
    if value["status"] in ("pending", "refused") and value["authority"] is None:
        return None
    if value["status"] != "authorized":
        raise Refused("invalid integration authority status")
    authority = value["authority"]
    validate_authority(authority)
    if any(authority[k] != frozen[k] for k in
           ("repository", "base", "base_tree", "allowed_paths", "admission_digest")):
        raise Refused("external authority differs from admitted candidate")
    if (authority["review_digest"] != digest(frozen["verification"]) or
            set(authority["required_checks"]) != {c["name"] for c in frozen["verification"]["checks"]} or
            authority["expires_at"] > config["expires_at"] or
            authority["max_requests"] > config["limits"]["max_attempts"]):
        raise Refused("external authority exceeds admitted evidence or programme bounds")
    request = {"schema": "aide.broker.request.v1", "task": frozen["task"],
               "authority_digest": digest(authority), "admission_digest": frozen["admission_digest"],
               "candidate": frozen["candidate"], "verification": frozen["verification"]}
    return {"request": request, "authority": authority}


def checked_observation(value, request, authority):
    fields(value, "schema request_digest status stage receipt receipt_sha256")
    if (value["schema"] != "aide.broker.observation.v1" or value["request_digest"] != digest(request)
            or value["status"] not in ("absent", "pending", "integrated")):
        raise Refused("broker observation does not bind exact v1 request")
    if value["status"] == "integrated":
        from core.runtime.integration_broker.service import Broker
        # Reuse the production receipt validator without creating a ledger or
        # transport; only the externally issued authority defines acceptance.
        checker = object.__new__(Broker)
        checker.authority = authority
        manifest = {"base": authority["base"], "candidate_tree": request["verification"]["subject_tree"]}
        receipt = checker.checked_receipt(value["receipt"], digest(request), manifest)
        if value["stage"] != "integrated" or value["receipt_sha256"] != digest(receipt):
            raise Refused("integration receipt digest mismatch")
    elif value["receipt"] is not None or value["receipt_sha256"] is not None:
        raise Refused("non-integrated observation carries completion evidence")
    return value


def integrate(coordinator, attempt, evidence, paused):
    frozen = evidence["frozen_handoff_v1"]
    # Restart reconciliation uses immutable exchange blobs and persisted evidence;
    # mutable worker bytes are no longer an integration input.
    manifest, _ = read_candidate(Path(coordinator.config["integration"]["exchange_root"]), frozen["candidate"])
    if manifest["candidate_tree"] != frozen["verification"]["subject_tree"]:
        raise Refused("frozen handoff no longer binds reviewed candidate")
    authorized = evidence.get("authorized_request_v1")
    if authorized is None:
        value = observation(coordinator, attempt, "authority", frozen)
        authorized = request_from_authority(value, frozen, coordinator.config)
        if authorized is None:
            raise paused()
        coordinator.state.transition(attempt["id"], "integration_pending", {"authorized_request_v1": authorized})
    request, authority = authorized["request"], authorized["authority"]
    # Revalidate persisted authority on every restart before trusting its receipt.
    expected = request_from_authority({"schema": "aide.broker.authority-observation.v1",
                                      "request_digest": digest(frozen), "status": "authorized",
                                      "authority": authority}, frozen, coordinator.config)
    if expected != authorized:
        raise Refused("persisted broker authorization drift")
    value = checked_observation(observation(coordinator, attempt, "query", request), request, authority)
    if value["status"] == "integrated":
        coordinator.state.transition(attempt["id"], "succeeded", {"integration": value})
        return
    if evidence.get("integration_dispatched_v1"):
        # Recovery belongs to the broker's request ledger. If its process died
        # before apply_intent, this may finish preparation and dispatch once;
        # after apply_intent the broker only observes and never repeats transport.
        value = checked_observation(observation(coordinator, attempt, "reconcile", request), request, authority)
        if value["status"] == "integrated":
            coordinator.state.transition(attempt["id"], "succeeded", {"integration": value})
            return
        raise paused()
    if value["status"] != "absent":
        raise paused()
    coordinator.guard(attempt["task"])
    # Intent survives a crash even before CreateProcess. An uncertain apply is
    # reconciled by query only; absence never grants automatic replay.
    coordinator.state.transition(attempt["id"], "integration_pending", {"integration_dispatched_v1": True})
    command = registered_command(coordinator.config["integration"]["apply"])
    output, receipt = coordinator.effect(attempt, "integration_apply", command,
                                         coordinator.config["integration"]["cwd"], canonical(request))
    coordinator.require_success(receipt)
    checked_observation(parse_json((output / "stdout").read_bytes()), request, authority)
    value = checked_observation(observation(coordinator, attempt, "query", request), request, authority)
    if value["status"] != "integrated":
        raise paused()
    coordinator.state.transition(attempt["id"], "succeeded", {"integration": value})
