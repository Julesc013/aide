"""Small independent refusal fixtures plus one real, held packet qualification."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("release_binding", HERE / "release_binding.py")
binding = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(binding)


def write_record(root, path, value):
    p = root / path
    p.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (json.dumps(value, sort_keys=True) + "\n").encode()
    p.write_bytes(data)
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def fixture(root):
    prefix = ".aide/release/stable/"
    assets = {}
    for name in ["aide-lite-v1.0.0.zip", "aide-lite-v1.0.0.tar.gz"]:
        assets[name] = write_record(root, prefix + name, name.encode())
    forms = ["form-" + str(i) for i in range(38)]
    pack = {"commit": "a" * 40, "tree": "b" * 40}
    manifest = {"identity": {"version": "1.0.0", "tag": "aide-lite-v1.0.0",
                             "source_commit": pack["commit"], "source_tree": pack["tree"],
                             "public_cli_forms": forms},
                "archives": {"zip": assets["aide-lite-v1.0.0.zip"],
                             "tar_gz": assets["aide-lite-v1.0.0.tar.gz"]}}
    assets["aide-lite-v1.0.0.manifest.json"] = write_record(root, prefix + "aide-lite-v1.0.0.manifest.json", manifest)
    sums = "".join(record["sha256"] + "  " + name + "\n" for name, record in assets.items())
    assets["aide-lite-v1.0.0.SHA256SUMS.txt"] = write_record(root, prefix + "aide-lite-v1.0.0.SHA256SUMS.txt", sums.encode())
    hashes = {name: record["sha256"] for name, record in assets.items()}
    inputs = {}
    for i in range(10):
        record = write_record(root, "operative/" + str(i), str(i).encode())
        inputs[record["path"]] = record["sha256"]
    evidence = {}

    def add(role, doc, reviewed=True):
        entry = write_record(root, "proof/" + role + ".json", doc)
        if reviewed:
            entry["review"] = write_record(root, "proof/" + role + "-review.json",
                                           {"verdict": "ACCEPT", "blocking_findings": [],
                                            "result_sha256": entry["sha256"], "notes": []})
        evidence[role] = entry

    source = {"status": "PASS", "source_inputs": inputs, "export-pack_exit_code": 0, "validate_exit_code": 0}
    for key, count in [("admission_tests", 5), ("public_fixture_tests", 8),
                       ("release_tests", 36), ("capability_tests", 18)]:
        source[key] = {"run": count, "errors": 0, "failures": 0, "skips": 0}
    add("source67", source, False)
    add("build_effect", {"source67_proof_sha256": evidence["source67"]["sha256"]}, False)
    add("build", {"build_exit": 0, "validate_exit": 0,
                  "effect_sha256": evidence["build_effect"]["sha256"],
                  "all10_source67_operative_inputs_reused": True,
                  "assets": {name: {"bytes": r["size_bytes"], "sha256": r["sha256"]} for name, r in assets.items()},
                  "archive_file_members": 852, "archive_checksum_entries": 849,
                  "zip_tar_payload_identical": True})
    for role, indices in [("case0", [0]), ("remaining7", list(range(1, 8)))]:
        add(role, {"qualification": {"status": "PASS", "case_indices": indices, "asset": {"assets": hashes}},
                   "native_command_exit": 0, "worker_native_exit": 0, "scratch_pending_reservation_absent": True})
    add("coverage", {"current_byte_zip_sha256": hashes["aide-lite-v1.0.0.zip"],
                     "current_byte_tar_sha256": hashes["aide-lite-v1.0.0.tar.gz"],
                     "first_result_sha256": evidence["case0"]["sha256"],
                     "rest_result_sha256": evidence["remaining7"]["sha256"],
                     "form_count": 38, "output_observations": 39, "job_form_observations": 12,
                     "total_unique_output_records": 51, "forms": [{"form": f} for f in forms]})
    add("replay", {"status": "PASS", "qualification": {"replay_unchanged": True, "asset": {"assets": hashes}},
                   "scratch_retired_reservation_released": True})
    add("delivered41", {"status": "PASS", "scratch_retired_reservation_released": True,
                        "proof": {"tests_qualified": 41, "archives": {"zip": hashes["aide-lite-v1.0.0.zip"], "tar": hashes["aide-lite-v1.0.0.tar.gz"]},
                                  "explicit_fixture_overlays": {str(i): "c" * 64 for i in range(10)},
                                  "suites": [{"tests_expected": n, "exit_code": 0, "count_verified": True, "skip_marker_absent": True} for n in [18, 23]]}})
    return {"schema_version": "aide.stable-release-local-binding.v1", "state": "HELD_EXTERNAL_GATES",
            "version": "1.0.0", "tag": "aide-lite-v1.0.0", "publication_authorized": False,
            "effect_executable": False, "prospective_tag_source": None,
            "historical_release_check_base": "aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3",
            "external_gates": {name: "PENDING_SEPARATE_PROOF_OR_AUTHORITY" for name in
                               ["outer_client", "historical_messages", "live_model_permission", "matched_efficiency",
                                "final_release_acceptance", "runtime_promotion", "publication_and_download_verification", "wider_cleanup"]},
            "limits": {"whole_session_contained": False, "read_isolation": "unqualified",
                       "hard_global_disk_quota": False, "total_cost_reduction_proven": False},
            "pack_source": pack, "assets": assets, "operative_inputs": inputs, "evidence": evidence,
            "delivered_test_scope": "41 original tests with ten explicit fixture-data overlays; no bare-archive or unaugmented CURRENT claim"}


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aide-release-binding-")
        self.root = Path(self.temp.name)
        self.packet = fixture(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def refuses(self):
        with self.assertRaises((binding.Refusal, KeyError, TypeError, ValueError, OSError)):
            binding.qualify(self.root, self.packet)

    def change_result(self, role, change):
        entry = self.packet["evidence"][role]
        doc = binding.load_json(self.root / entry["path"])
        change(doc)
        new = write_record(self.root, entry["path"], doc)
        review = binding.load_json(self.root / entry["review"]["path"])
        review["result_sha256"] = new["sha256"]
        new["review"] = write_record(self.root, entry["review"]["path"], review)
        self.packet["evidence"][role] = new

    def test_valid_local_bindings_remain_held(self):
        result = binding.qualify(self.root, self.packet)
        self.assertEqual(result["status"], "PASS_LOCAL_BINDINGS_HELD")
        self.assertIs(result["publication_authorized"], False)

    def test_actual_asset_tamper_refused(self):
        (self.root / self.packet["assets"]["aide-lite-v1.0.0.zip"]["path"]).write_bytes(b"changed")
        self.refuses()

    def test_missing_evidence_refused(self):
        (self.root / self.packet["evidence"]["case0"]["path"]).unlink()
        self.refuses()

    def test_different_review_subject_refused(self):
        entry = self.packet["evidence"]["case0"]
        entry["review"] = write_record(self.root, entry["review"]["path"],
                                       {"verdict": "ACCEPT", "blocking_findings": [], "result_sha256": "d" * 64, "notes": []})
        self.refuses()

    def test_unresolved_review_note_refused(self):
        entry = self.packet["evidence"]["case0"]
        review = binding.load_json(self.root / entry["review"]["path"])
        review["notes"] = [{"blocking": False, "note": "required test still pending"}]
        entry["review"] = write_record(self.root, entry["review"]["path"], review)
        self.refuses()

    def test_duplicate_consumer_case_refused(self):
        self.change_result("remaining7", lambda d: d["qualification"].update(case_indices=[1, 1, 3, 4, 5, 6, 7]))
        self.refuses()

    def test_coverage_rebind_to_other_job_refused(self):
        self.change_result("coverage", lambda d: d.update(first_result_sha256="d" * 64))
        self.refuses()

    def test_duplicate_public_form_refused(self):
        self.change_result("coverage", lambda d: d["forms"].__setitem__(0, d["forms"][1]))
        self.refuses()

    def test_unretired_replay_refused(self):
        self.change_result("replay", lambda d: d.update(scratch_retired_reservation_released=False))
        self.refuses()

    def test_erased_fixture_scope_refused(self):
        self.packet["delivered_test_scope"] = "41 bare archive tests"
        self.refuses()

    def test_shortened_historical_range_refused(self):
        self.packet["historical_release_check_base"] = "a" * 40
        self.refuses()

    def test_omitted_external_gate_refused(self):
        del self.packet["external_gates"]["live_model_permission"]
        self.refuses()

    def test_publish_ready_claim_refused(self):
        self.packet["publication_authorized"] = True
        self.refuses()

    def test_hard_quota_claim_refused(self):
        self.packet["limits"]["hard_global_disk_quota"] = True
        self.refuses()

    def test_path_escape_refused(self):
        self.packet["evidence"]["case0"]["path"] = "../outside.json"
        self.refuses()

    def test_duplicate_json_key_refused(self):
        p = self.root / "duplicates.json"
        p.write_text('{"publication_authorized": false, "publication_authorized": true}', encoding="utf-8")
        with self.assertRaises(binding.Refusal):
            binding.load_json(p)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--packet", required=True)
    parser.add_argument("--old-packet", required=True)
    args = parser.parse_args()
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(BindingTests))
    commands = []
    for path, expected in [(args.packet, 0), (args.old_packet, 1)]:
        argv = [sys.executable, "-I", "-B", str(HERE / "release_binding.py"), "--root", str(args.root), "--packet", path]
        run = subprocess.run(argv, capture_output=True)
        name = "current" if expected == 0 else "stale"
        (output / (name + ".stdout.log")).write_bytes(run.stdout)
        (output / (name + ".stderr.log")).write_bytes(run.stderr)
        parsed = json.loads(run.stdout)
        expected_status = "PASS_LOCAL_BINDINGS_HELD" if expected == 0 else "REFUSED"
        commands.append({"argv": argv, "exit_code": run.returncode, "expected_exit": expected,
                         "result": parsed, "passed": run.returncode == expected and parsed["status"] == expected_status})
    passed = result.wasSuccessful() and all(command["passed"] for command in commands)
    report = {"status": "PASS" if passed else "FAIL", "fixture_tests": result.testsRun,
              "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
              "commands": commands, "publication_authorized": False, "effect_executable": False,
              "scope": "Small refusal fixtures and actual hash-bound held local packet; no publication admission"}
    (output / "binding-qualification.json").write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ["status", "fixture_tests", "failures", "errors", "skips", "publication_authorized"]}))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
