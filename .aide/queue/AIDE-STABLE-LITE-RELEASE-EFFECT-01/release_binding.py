"""Read-only consistency check for the held current local release evidence.

This checks bindings, not the authenticity of a review or permission to publish.
It never executes a release, changes a gate, or refreshes missing evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


SCHEMA = "aide.stable-release-local-binding.v1"
ASSET_NAMES = {"aide-lite-v1.0.0.zip", "aide-lite-v1.0.0.tar.gz",
               "aide-lite-v1.0.0.manifest.json", "aide-lite-v1.0.0.SHA256SUMS.txt"}
EVIDENCE_ROLES = {"source67", "build_effect", "build", "case0", "remaining7", "coverage",
                  "replay", "delivered41"}
GATES = {"outer_client", "historical_messages", "live_model_permission",
         "matched_efficiency", "final_release_acceptance", "runtime_promotion",
         "publication_and_download_verification", "wider_cleanup"}
HISTORY_BASE = "aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3"


class Refusal(ValueError):
    pass


def require(condition: object, message: str) -> None:
    if not condition:
        raise Refusal(message)


def _unique(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict:
    result = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique)
    require(isinstance(result, dict), f"JSON object required: {path.name}")
    return result


def bound_path(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and "\\" not in relative and ":" not in relative,
            "portable relative path required")
    parts = PurePosixPath(relative)
    require(relative and not parts.is_absolute() and ".." not in parts.parts,
            "path escapes qualification root")
    path = root / relative
    require(path.resolve().is_relative_to(root.resolve()), "resolved path escapes root")
    require(path.is_file(), f"bound file missing: {relative}")
    return path


def read_bound(root: Path, record: dict) -> Path:
    require(isinstance(record, dict), "bound file record required")
    path = bound_path(root, record["path"])
    require(re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is not None,
            "SHA-256 identity required")
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    require(digest == record["sha256"], f"bound bytes changed: {record['path']}")
    if "size_bytes" in record:
        require(path.stat().st_size == record["size_bytes"], "bound file size changed")
    return path


def _review(root: Path, entry: dict) -> None:
    review = load_json(read_bound(root, entry["review"]))
    require(review.get("verdict") in {"ACCEPT", "ACCEPT_WITH_NOTES"},
            "qualified recorded review required")
    require(review.get("blocking_findings") == [], "review has unresolved findings")
    subjects = [review.get(k) for k in
                ("result_sha256", "subject_sha256", "subject_result_sha256")]
    require(entry["sha256"] in subjects, "review covers another result")
    notes = review.get("notes", [])
    if isinstance(notes, str):
        require("allnotesnonblocking/disposed" in "".join(notes.lower().split()),
                "recorded note disposition missing")
    else:
        require(isinstance(notes, list), "review notes malformed")
        for note in notes:
            require(isinstance(note, dict), "review note malformed")
            if "blocking" in note:
                require(note["blocking"] is False, "review note is blocking or contradictory")
            if "classification" in note:
                require(note["classification"] == "nonblocking_disposed",
                        "review note classification is unresolved or contradictory")
            require(
                    (note.get("classification") == "nonblocking_disposed" or
                     (note.get("blocking") is False and bool(note.get("disposition")))),
                    "recorded note remains unresolved")


def qualify(root: Path, packet: dict) -> dict:
    require(packet.get("schema_version") == SCHEMA, "not a current local binding packet")
    require(packet.get("state") == "HELD_EXTERNAL_GATES", "packet erased held posture")
    require(packet.get("publication_authorized") is False and
            packet.get("effect_executable") is False, "local evidence cannot admit publication")
    require(packet.get("version") == "1.0.0" and packet.get("tag") == "aide-lite-v1.0.0",
            "release identity changed")
    require(packet.get("historical_release_check_base") == HISTORY_BASE,
            "historical range was silently shortened")
    require(set(packet["external_gates"]) == GATES and
            all(v == "PENDING_SEPARATE_PROOF_OR_AUTHORITY"
                for v in packet["external_gates"].values()), "external gate omitted or waived")
    require(packet.get("prospective_tag_source") is None,
            "future tag source requires its own frozen effect acceptance")
    require(packet.get("limits") == {"whole_session_contained": False,
                                    "read_isolation": "unqualified",
                                    "hard_global_disk_quota": False,
                                    "total_cost_reduction_proven": False},
            "unsupported environment or efficiency claim")

    assets = packet["assets"]
    require(set(assets) == ASSET_NAMES, "four exact assets required")
    for name, record in assets.items():
        require(record["path"] == f".aide/release/stable/{name}", "unexpected asset path")
        read_bound(root, record)
    asset_hashes = {name: record["sha256"] for name, record in assets.items()}
    manifest = load_json(bound_path(root, assets["aide-lite-v1.0.0.manifest.json"]["path"]))
    identity = manifest["identity"]
    require(identity["version"] == packet["version"] and identity["tag"] == packet["tag"],
            "archive manifest identity differs")
    require(identity["source_commit"] == packet["pack_source"]["commit"] and
            identity["source_tree"] == packet["pack_source"]["tree"], "pack provenance differs")
    for role, name in [("zip", "aide-lite-v1.0.0.zip"), ("tar_gz", "aide-lite-v1.0.0.tar.gz")]:
        require(manifest["archives"][role] == assets[name], "archive declaration differs")
    sums = bound_path(root, assets["aide-lite-v1.0.0.SHA256SUMS.txt"]["path"]).read_text(encoding="utf-8")
    entries = [line.split() for line in sums.splitlines() if line.strip()]
    require(len(entries) == 3 and {pair[1]: pair[0] for pair in entries} ==
            {name: sha for name, sha in asset_hashes.items() if not name.endswith(".txt")},
            "published checksum list differs")

    evidence = packet["evidence"]
    require(set(evidence) == EVIDENCE_ROLES, "complete local evidence roles required")
    docs = {}
    for role, entry in evidence.items():
        docs[role] = load_json(read_bound(root, entry))
        if role not in {"source67", "build_effect"}:
            _review(root, entry)
    source = docs["source67"]
    require(source["status"] == "PASS", "affected source proof failed")
    require(source["source_inputs"] == packet["operative_inputs"] and
            len(packet["operative_inputs"]) == 10, "source proof input set differs")
    for path, sha in packet["operative_inputs"].items():
        read_bound(root, {"path": path, "sha256": sha})
    for key, count in [("admission_tests", 5), ("public_fixture_tests", 8),
                       ("release_tests", 36), ("capability_tests", 18)]:
        group = source[key]
        require(all(group.get(k) == v for k, v in
                    {"run": count, "errors": 0, "failures": 0, "skips": 0}.items()),
                f"source proof incomplete: {key}")
    require(source["export-pack_exit_code"] == 0 and source["validate_exit_code"] == 0,
            "source export/validation failed")
    build = docs["build"]
    require(build["build_exit"] == 0 and build["validate_exit"] == 0 and
            build["effect_sha256"] == evidence["build_effect"]["sha256"] and
            docs["build_effect"]["source67_proof_sha256"] == evidence["source67"]["sha256"] and
            build["all10_source67_operative_inputs_reused"] is True,
            "build does not bind source proof")
    require(build["assets"] == {name: {"bytes": record["size_bytes"], "sha256": record["sha256"]}
                                for name, record in assets.items()}, "build used other assets")
    require(build["archive_file_members"] == 852 and build["archive_checksum_entries"] == 849 and
            build["zip_tar_payload_identical"] is True, "archive build proof incomplete")

    for role, indices in [("case0", [0]), ("remaining7", list(range(1, 8)))]:
        result = docs[role]
        qualification = result["qualification"]
        require(qualification["status"] == "PASS" and qualification["case_indices"] == indices,
                f"original case coverage differs: {role}")
        require(qualification["asset"]["assets"] == asset_hashes, "consumer used another archive")
        require(result["native_command_exit"] == 0 and result["worker_native_exit"] == 0 and
                result["scratch_pending_reservation_absent"] is True, "consumer not closed")
    coverage = docs["coverage"]
    require(coverage["current_byte_zip_sha256"] == asset_hashes["aide-lite-v1.0.0.zip"] and
            coverage["current_byte_tar_sha256"] == asset_hashes["aide-lite-v1.0.0.tar.gz"],
            "coverage binds other assets")
    require(coverage["first_result_sha256"] == evidence["case0"]["sha256"] and
            coverage["rest_result_sha256"] == evidence["remaining7"]["sha256"],
            "coverage binds other jobs")
    require(coverage["form_count"] == 38 and coverage["output_observations"] == 39 and
            coverage["job_form_observations"] == 12 and coverage["total_unique_output_records"] == 51,
            "declared coverage incomplete")
    require(len(coverage["forms"]) == 38 and
            {form["form"] for form in coverage["forms"]} == set(identity["public_cli_forms"]),
            "public form set differs")
    replay = docs["replay"]
    require(replay["status"] == "PASS" and replay["qualification"]["replay_unchanged"] is True and
            replay["qualification"]["asset"]["assets"] == asset_hashes and
            replay["scratch_retired_reservation_released"] is True, "replay proof incomplete")
    delivered = docs["delivered41"]
    proof = delivered["proof"]
    require(delivered["status"] == "PASS" and proof["tests_qualified"] == 41 and
            proof["archives"] == {"zip": asset_hashes["aide-lite-v1.0.0.zip"],
                                  "tar": asset_hashes["aide-lite-v1.0.0.tar.gz"]},
            "delivered qualification differs")
    require(len(proof["explicit_fixture_overlays"]) == 10 and
            packet["delivered_test_scope"] == "41 original tests with ten explicit fixture-data overlays; no bare-archive or unaugmented CURRENT claim",
            "delivered fixture qualification was erased")
    require([s["tests_expected"] for s in proof["suites"]] == [18, 23] and
            all(s["exit_code"] == 0 and s["count_verified"] is True and
                s["skip_marker_absent"] is True for s in proof["suites"]) and
            delivered["scratch_retired_reservation_released"] is True,
            "delivered suites incomplete or unretired")
    return {"status": "PASS_LOCAL_BINDINGS_HELD", "publication_authorized": False,
            "effect_executable": False, "evidence_roles": sorted(EVIDENCE_ROLES),
            "consumer_cases": 8, "public_forms": 38, "distinct_records": 51,
            "delivered_tests_with_explicit_fixtures": 41,
            "external_gates": packet["external_gates"],
            "verification_scope": "Hash-bound recorded local evidence; not review authenticity, current host permissions or release admission"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--packet", required=True)
    args = parser.parse_args()
    try:
        result = qualify(args.root, load_json(bound_path(args.root, args.packet)))
    except (Refusal, KeyError, TypeError, ValueError, OSError) as exc:
        print(json.dumps({"status": "REFUSED", "reason": str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
