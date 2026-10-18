"""Read-only evidence checks and the existing fixed promotion preview."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
import os
from pathlib import Path
import subprocess

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
TASK = ROOT / ".aide/queue/AIDE-MINI-WORKER-01"
BASE = "fcaa9e1e2230cf1fc14cfa5edde05cad0ce27971"
from core.execution.managed_workspace import content_digest, file_digest, load_config


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


owner = load("mini_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
owner.BASE = BASE


def check_records():
    ev = TASK / "evidence"
    records = []
    for name, expected in (("acquisition-attempt-01.json", 1),
                           ("acquisition-repair-attempt-02.json", 0),
                           ("fixture-attempt-03.json", 0)):
        record = json.loads((ev / name).read_text())
        assert record["phase"] == "retired" and record["result"]["exit_code"] == expected
        assert record["result"]["quiescent"] and record["scratch_absent"] and record["reservation_released"]
        for part, sha in record["collected_manifest"].items():
            assert content_digest(Path(record["retained"]) / part) == sha
        _, roots, _ = load_config(ROOT / ".aide.local/execution.json")
        assert not (roots["scratch"] / record["job_id"]).exists()
        records.append(record)
    fixture = records[-1]
    output = Path(fixture["retained"]) / "output"
    stages = json.loads((output / "stages.json").read_text())
    assert len(stages) == 15
    for row in stages:
        stage = output / row["scenario"]
        assert row["result"]["quiescent"]
        launch = json.loads((stage / "launch.json").read_text())
        assert launch["job_id"] == row["job_id"] == row["result"]["job_id"]
        assert launch["status"] == "TERMINAL"
        observations = [json.loads(line) for line in (stage / "observations.jsonl").read_text().splitlines()]
        assert observations[-1]["stage"] == "quiescent"
        for name, sha in row["postimage_sha256"].items():
            assert file_digest(stage / "postimages" / name) == sha
        assert (stage / "postimages/notes.txt").read_text() == "Preserve project customization.\n"
        changed = row["scenario"] in ("success", "interrupt", "resume", "cancel")
        expected = "def add(a, b):\n    return a " + ("+" if changed else "-") + " b\n"
        assert (stage / "postimages/arithmetic.py").read_text() == expected
        if row["scenario"] == "cancel":
            assert row["result"]["reason"] == "cancelled" and row["partial_effect_preserved"]
            receipt = json.loads((stage / "cancel/attempt.json").read_text())
            assert receipt["status"] == "INCOMPLETE" and not receipt["accepted"]
        else:
            counts = json.loads((stage / "test-result.json").read_text())
            assert counts["tests_run"] == 1 and not any(counts[k] for k in ("errors", "failures", "skips"))
        if row["scenario"] == "resume":
            assert row["prior_evidence_unchanged"]
    for name in ("success", "interrupt", "resume"):
        receipt = json.loads((output / name / name / "attempt.json").read_text())
        assert receipt["identity"]["source_revision"] == fixture["job"]["source_commit"]
        assert not receipt["accepted"] and receipt["model_usage"] is None
        assert file_digest(output / name / name / "trajectory.json") == receipt["trajectory_sha256"]
    assert (output / "success/candidate.patch").is_file()
    source = json.loads((ev / "fixture-source.json").read_text())
    for name in ("core/execution/mini_worker.py", "core/execution/tests/test_mini_worker.py",
                 ".aide/queue/AIDE-MINI-WORKER-01/qualify_worker.py",
                 ".aide/queue/AIDE-MINI-WORKER-01/evidence/dependency-recipe.json"):
        assert file_digest(ROOT / name) == source["files"][name]
    inventory = json.loads((ROOT / ".aide/queue/AIDE-CAMPAIGN-CURRENT-STATE-01/evidence/immutable-inventory.json").read_text())
    for group in inventory.values():
        for name, sha in group.items():
            assert file_digest(ROOT / name) == sha
    pack = ROOT / ".aide/export/aide-lite-pack-v0"
    assert {p.relative_to(ROOT).as_posix() for p in pack.rglob("*") if p.is_file()} == set(inventory["pack"])
    return {"fixture_scenarios": 15, "original_failure_preserved": True,
            "jobs_verified": len(records), "pack_files_unchanged": len(inventory["pack"]),
            "release_files_unchanged": len(inventory["release"]),
            "worker_peak_bytes": fixture["peaks"]["memory_bytes"],
            "scratch_peak_bytes": fixture["peaks"]["scratch_bytes"]}


def main():
    assert sys.argv[1:] in (["generate"], ["verify"])
    evidence = check_records()
    if sys.argv[1:] == ["verify"]:
        print(json.dumps({"result": "PASS", **evidence, "preview": owner.verify()}, indent=2))
        return
    # Passive import must not load the optional harness or provider packages.
    import core.execution.mini_worker
    assert not any(n.split(".", 1)[0] in ("minisweagent", "pydantic", "litellm", "openai")
                   for n in sys.modules)
    output = Path(os.environ["AIDE_JOB_OUTPUT"])
    for label, args in (("doctor", ["doctor"]), ("validation", ["validate"]),
                        ("pack-status", ["pack-status"])):
        with (output / (label + ".log")).open("xb") as stream:
            result = subprocess.run([sys.executable, "-B", ".aide/scripts/aide_lite.py", *args],
                                    stdin=subprocess.DEVNULL, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=120)
        assert result.returncode == 0, label
    assert check_records() == evidence
    owner.main()
    result = {"result": "PASS", **evidence, "passive_import": "no_optional_SDK",
              "real_model_requests": 0, "whole_task_usage": "unknown",
              "preview": owner.verify()}
    (output / "qualification.json").write_text(json.dumps(result, indent=2) + "\n",
                                               encoding="utf-8", newline="\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

