"""Verify bounded hosted capture and preserve compact, lossless result witnesses."""
import base64
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / "evidence"
LOGS = EVIDENCE / "hosted-logs.log"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    execution = json.loads((EVIDENCE / "hosted-execution.log").read_bytes())
    assert execution["state"] == "observed_terminal"
    source = execution["source_commit"]
    assert source == "9c15cc8e1566bfa199ff882cb8b7a13568225f18"
    assert execution["final_run_identity"]["conclusion"] == "success"
    assert execution["final_run_identity"]["run_attempt"] == 1
    streams = {}
    for operation in execution["operations"]:
        assert operation["state"] == "completed" and operation["exit_code"] == 0
        assert operation["reader_threads_stopped"] and not operation["drain_errors"]
        assert len(operation["streams"]) == 2
        for name, identity in operation["streams"].items():
            raw = (LOGS / name).read_bytes()
            assert identity == {"bytes": len(raw), "sha256": sha(raw)}
            streams[name] = identity
    assert len(streams) == 2 * len(execution["operations"])
    expected = {"Windows": "windows-2025-x64", "Linux": "ubuntu-24.04-x64", "Darwin": "macos-15-arm64"}
    decoded = {}
    with zipfile.ZipFile(LOGS / "037.stdout") as archive:
        assert len(archive.infolist()) <= 4096
        assert sum(item.file_size for item in archive.infolist()) <= 64 * 1024 * 1024
        for item in archive.infolist():
            if item.is_dir():
                continue
            text = archive.read(item).decode("utf-8", errors="strict")
            rows = re.findall(r"AIDE_RECEIPT_V1 (\d+)/(\d+) ([0-9a-f]{64}) ([A-Za-z0-9+/=]+)", text)
            if not rows:
                continue
            assert [int(row[0]) for row in rows] == list(range(1, len(rows) + 1))
            assert len(rows) == int(rows[0][1]) and all(row[1:3] == rows[0][1:3] for row in rows)
            packed = base64.b64decode("".join(row[3] for row in rows), validate=True)
            assert len(packed) <= 2 * 1024 * 1024 and sha(packed) == rows[0][2]
            if sha(packed) in decoded:
                continue
            with gzip.GzipFile(fileobj=io.BytesIO(packed)) as stream:
                body = stream.read(12 * 1024 * 1024 + 1)
            assert len(body) <= 12 * 1024 * 1024
            encoded = json.loads(body)
            assert 1 <= len(encoded) <= 256
            assert all(re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", name) for name in encoded)
            files = {name: base64.b64decode(value, validate=True) for name, value in encoded.items()}
            assert sum(map(len, files.values())) <= 8 * 1024 * 1024
            result = json.loads(files["result.json"])
            profile = expected[result["host"]["system"]]
            assert all((LOGS / profile / name).read_bytes() == raw for name, raw in files.items())
            index = json.loads(files["receipt-index.json"])
            assert set(index) == set(files) - {"receipt-index.json"}
            assert all(index[name] == {"bytes": len(raw), "sha256": sha(raw)} for name, raw in files.items() if name != "receipt-index.json")
            assert result["source_head"] == source
            assert result["input_sha256"] == sha((EVIDENCE / "package-inputs.json").read_bytes())
            assert result["observation_complete"] and result["native_lifecycle_pass"] and not result["support_claimed"]
            suites = {"fixtures": result["fixtures"], **result["binding_regressions"]}
            if result.get("windows_regressions"):
                suites["windows"] = result["windows_regressions"]
            assert all(value["passed"] and not value["failures"] and not value["errors"] for value in suites.values())
            current = [case for case in result["cases"] if case["subject"] == "development-export"]
            assert {case["shape"] for case in current} == {"fresh", "brownfield", "published-upgrade-fresh", "published-upgrade-brownfield"}
            assert len(current) == 4 and all(case["native_acceptance"] and case["preserved"] for case in current)
            historical = [case for case in result["cases"] if case["subject"] == "published-1.1.0"]
            assert len(historical) == 2 and all(case["preserved"] for case in historical)
            if result["host"]["system"] != "Windows":
                assert all(not case["native_acceptance"] and not case["detached"] for case in historical)
                for shape in ("fresh", "brownfield"):
                    assert files[f"published-1.1.0-{shape}-removal-apply.stderr"] == b"error: portable removal apply requires Windows anchored file handles\n"
            else:
                assert all(case["native_acceptance"] and case["detached"] for case in historical)
            destination = EVIDENCE / "hosted-results" / profile
            destination.mkdir(parents=True, exist_ok=False)
            selected = ["result.json", "receipt-index.json"] + [name for name in files if name.endswith((".result.json", ".log"))]
            copied = {}
            for name in selected:
                target = destination / (name + ".txt" if name.endswith(".log") else name)
                target.write_bytes(files[name])
                copied[target.relative_to(ROOT).as_posix()] = sha(files[name])
            decoded[sha(packed)] = {"profile": profile, "files": len(files), "raw_bytes": sum(map(len, files.values())),
                "index_sha256": sha(files["receipt-index.json"]), "copied": copied,
                "suites": {name: {"tests": value["tests_run"], "passes": value["tests_run"] - len(value["skips"]), "skips": value["skips"]} for name, value in suites.items()},
                "current_cases_passed": 4, "historical_cases": historical}
    assert {value["profile"] for value in decoded.values()} == set(expected.values()) and len(decoded) == 3
    proof = {"result": "PASS", "source_commit": source, "run_id": execution["run_id"],
        "run_url": execution["run_url"], "controller_streams": streams, "bundles": decoded,
        "original_complete_captures": "hosted-logs.log/", "support_claimed": False, "whole_model_usage": "unknown"}
    (EVIDENCE / "observation-verification.json").write_bytes((json.dumps(proof, indent=2) + "\n").encode())
    print(json.dumps({"result": "PASS", "profiles": 3, "streams": len(streams), "current_cases_passed": 12,
        "test_passes": sum(suite["passes"] for bundle in decoded.values() for suite in bundle["suites"].values()),
        "test_skips": sum(len(suite["skips"]) for bundle in decoded.values() for suite in bundle["suites"].values())}))


if __name__ == "__main__":
    main()
