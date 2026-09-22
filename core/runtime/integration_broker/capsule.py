"""Protected controller evidence capsules; input to an external delegation issuer."""
from pathlib import Path
import uuid

from .common import (Refused, fields, identity, digest, canonical, create_exact,
                     bounded_bytes, object_json, require_path, beneath)
from .candidate import read_candidate
from core.runtime.continuous_worker import codex
from core.runtime.continuous_worker.contract import changed, file_hash, registered_command


def publish(coordinator, attempt, evidence, frozen):
    """Publish observed effects only after the controller's final snapshot check."""
    phases = {"coding", "assurance"} | {"test." + str(i) for i in range(len(evidence["tests"]))}
    rows = coordinator.state.db.execute("SELECT kind,status,request,response FROM effects WHERE attempt=?",
                                        (attempt["id"],)).fetchall()
    effects = {}
    for row in rows:
        if row["kind"] in phases:
            if row["status"] != "observed" or row["response"] is None:
                raise Refused("capsule cannot publish an uncertain effect")
            from .common import parse_json
            effects[row["kind"]] = {"request": parse_json(row["request"]),
                                    "response": parse_json(row["response"])}
    if set(effects) != phases:
        raise Refused("capsule requires all independent process observations")
    capsule = {"schema": "aide.broker.controller-capsule.v1", "frozen_digest": digest(frozen),
               "activation_digest": digest(coordinator.config), "attempt": attempt["id"],
               "baseline": evidence["baseline"], "subject": evidence["subject"], "effects": effects}
    folder = require_path(str(coordinator.state.root / "authority-capsules"))
    folder.mkdir(exist_ok=True)
    path = folder / (digest(frozen) + ".json")
    raw = canonical(capsule).encode()
    if len(raw) > 16 * 1024 * 1024:
        raise Refused("controller capsule byte budget")
    coordinator.guard(attempt["task"])
    used = sum(p.stat().st_size for p in coordinator.state.root.rglob("*") if p.is_file())
    if used + len(raw) >= coordinator.config["limits"]["max_state_bytes"]:
        raise Refused("controller capsule exceeds reserved state budget")
    if path.exists():
        if bounded_bytes(path) != raw:
            raise Refused("existing controller capsule differs")
    else:
        create_exact(path, raw)
    return {"capsule_sha256": file_hash(path), "frozen_digest": digest(frozen)}


def _snapshot(value, base):
    fields(value, "head files diff_sha256 index_sha256 metadata git_changed identity")
    if value["head"] != base or not isinstance(value["files"], dict):
        raise Refused("capsule snapshot base or file map differs")
    if value["identity"] != digest({k: v for k, v in value.items() if k != "identity"}):
        raise Refused("capsule snapshot identity mismatch")
    for pin in value["files"].values():
        if pin is not None:
            identity(pin)


def validate(frozen, activation, spec, exchange, *, capsule_root=None):
    """Reparse protected observations against a separately pinned activation.

    The caller must qualify the controller/store boundary and authenticate the
    activation independently. This parser cannot establish either from hashes.
    """
    state = require_path(activation["state_root"])
    root = require_path(str(capsule_root or state / "authority-capsules"))
    if root != state / "authority-capsules":
        raise Refused("controller capsule root differs from admitted state")
    capsule = object_json(root / (digest(frozen) + ".json"))
    fields(capsule, "schema frozen_digest activation_digest attempt baseline subject effects")
    if (capsule["schema"] != "aide.broker.controller-capsule.v1" or
            capsule["frozen_digest"] != digest(frozen) or capsule["activation_digest"] != digest(activation)):
        raise Refused("controller capsule request or activation mismatch")
    attempt = capsule["attempt"]
    try:
        if not isinstance(attempt, str) or uuid.UUID(attempt).hex != attempt:
            raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise Refused("invalid controller attempt identity") from None
    if any(frozen[k] != spec[source] for k, source in
           (("task", "id"), ("repository", "repository"), ("base", "base"),
            ("allowed_paths", "allowed_paths"), ("admission_digest", "source_sha256"))):
        raise Refused("controller evidence exceeds task admission")
    manifest, _ = read_candidate(Path(exchange), frozen["candidate"])
    if (manifest["candidate_tree"] != frozen["verification"]["subject_tree"] or
            any(manifest[k] != frozen[k] for k in ("repository", "base", "base_tree", "allowed_paths"))):
        raise Refused("controller candidate differs from frozen subject")
    baseline, subject = capsule["baseline"], capsule["subject"]
    _snapshot(baseline, spec["base"])
    _snapshot(subject, spec["base"])
    changes = changed(baseline, subject, spec["allowed_paths"])
    if manifest["schema"] != "aide.broker.candidate.v2" or set(changes) != set(manifest["files"]):
        raise Refused("controller snapshot and candidate changes differ")
    for name, entry in manifest["files"].items():
        expected = None if entry is None else entry["sha256"]
        if subject["files"].get(name) != expected:
            raise Refused("controller snapshot differs from frozen bytes")
    attempt_root = state / "attempts" / attempt
    schema = require_path(str(attempt_root / "worker-result.schema.json"))
    if bounded_bytes(schema) != canonical(codex.SCHEMA).encode():
        raise Refused("controller worker result schema drift")
    effects = capsule["effects"]
    phases = {"coding", "assurance"} | {"test." + str(i) for i in range(len(spec["test_commands"]))}
    if not isinstance(effects, dict) or set(effects) != phases:
        raise Refused("controller capsule has missing or duplicate phases")
    sessions, checks, jobs = {}, [], set()
    for phase, effect in effects.items():
        fields(effect, "request response")
        request, response = effect["request"], effect["response"]
        fields(request, "job_id argv workspace payload_sha256 output")
        fields(response, "completed receipt artifacts")
        if response["completed"] is not True:
            raise Refused("controller effect was not completed")
        job = request["job_id"]
        try:
            if not isinstance(job, str) or uuid.UUID(job).hex != job or job in jobs:
                raise ValueError()
        except (ValueError, TypeError, AttributeError):
            raise Refused("invalid or reused controller job identity") from None
        jobs.add(job)
        output = require_path(request["output"])
        if output != attempt_root / job or not beneath(output, state):
            raise Refused("controller output escaped exact attempt")
        artifacts = response["artifacts"]
        fields(artifacts, "stdin stdout stderr")
        for name, pin in artifacts.items():
            identity(pin)
            if file_hash(require_path(str(output / name))) != pin:
                raise Refused("controller process artifact drift")
        if digest(bounded_bytes(output / "stdin").decode()) != request["payload_sha256"]:
            raise Refused("controller effect input digest mismatch")
        receipt = response["receipt"]
        if (not isinstance(receipt, dict) or receipt.get("exit_code") != 0 or
                type(receipt.get("exit_code")) is not int or receipt.get("quiescent") is not True or
                receipt.get("reason") != "exited" or receipt.get("job_id") != job or
                receipt.get("io_errors") != [] or receipt.get("monitor_reason", "") != ""):
            raise Refused("controller process did not pass owned completion")
        if request["workspace"] != spec["workspace"]:
            raise Refused("controller effect workspace mismatch")
        if phase in ("coding", "assurance"):
            expected = codex.argv(registered_command(activation["codex"]), Path(spec["workspace"]), schema,
                                  assurance=phase == "assurance", model=activation["worker_models"][phase])
            result = codex.parse_events(output / "stdout", baseline["identity"] if phase == "coding" else subject["identity"])
            if result["result"]["status"] != "pass" or (phase == "assurance" and result["result"]["findings"]):
                raise Refused("controller worker verdict did not pass")
            sessions[phase] = result["session_id"]
        else:
            index = int(phase.removeprefix("test."))
            expected = registered_command(spec["test_commands"][index])
            checks.append({"name": phase, "result": "PASS", "artifact_sha256": digest(artifacts)})
        if request["argv"] != expected:
            raise Refused("controller command differs from pinned role")
    verification = {"coding_session": sessions["coding"], "assurance_session": sessions["assurance"],
                    "assurance_passed": True, "subject_tree": manifest["candidate_tree"],
                    "checks": sorted(checks, key=lambda row: int(row["name"].split(".")[1]))}
    if sessions["coding"] == sessions["assurance"] or verification != frozen["verification"]:
        raise Refused("controller verification differs from frozen evidence")
    return {"capsule_digest": digest(capsule), "verification": verification, "attempt": attempt}
