"""One offline Mini lifecycle qualification within the existing managed job."""
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import uuid
import zipfile

from core.execution.managed_workspace import current_context, digest, file_digest, ordinary
from core.runtime.continuous_worker.windows_job import WindowsJobHost, sanitized_environment

TASK = Path(__file__).resolve().parent
ROOT = TASK.parents[2]


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def main():
    context = current_context(ROOT)
    acquisition = json.loads((TASK / "evidence/acquisition-result.json").read_text())
    recipe = json.loads((TASK / "evidence/dependency-recipe.json").read_text())
    scratch, output = map(Path, (os.environ["AIDE_JOB_TMP"], os.environ["AIDE_JOB_OUTPUT"]))
    deps = scratch / "mini-dependencies"
    deps.mkdir()
    assert acquisition["status"] == "PASS" and acquisition["collection_retirement_verified"]
    assert acquisition["unpacked_bytes"] == 15336396 and acquisition["archive_members"] == 833
    assert acquisition["job_id"] == "67a60fa03cfc4ddd9483e7fa86c190e6"
    assert Path(acquisition["retained"]) == Path(
        "D:/Projects/AIDE/.aide.local/execution/retained") / acquisition["job_id"]
    expanded, count, seen = 0, 0, set()
    for wheel in acquisition["wheels"]:
        source = Path(acquisition["retained"]) / "output" / wheel["filename"]
        assert ordinary(source).st_size == wheel["bytes"]
        for parent in source.parents:
            ordinary(parent, directory=True)
        assert file_digest(source) == wheel["sha256"]
        with zipfile.ZipFile(source) as archive:
            for member in archive.infolist():
                parts = PurePosixPath(member.filename).parts
                assert parts and not member.filename.startswith("/")
                assert all(re.fullmatch(r"[A-Za-z0-9_.-]+", p) and p not in (".", "..") for p in parts)
                assert not any(p.endswith(".data") for p in parts)
                assert not stat.S_ISLNK(member.external_attr >> 16) and not member.flag_bits & 1
                expanded += member.file_size
                count += 1
                assert expanded <= 24 * 1024 * 1024 and count <= 4000
                destination = deps.joinpath(*parts)
                assert destination.resolve().is_relative_to(deps.resolve())
                if member.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    assert member.filename.casefold() not in seen
                    seen.add(member.filename.casefold())
                    data = archive.read(member)
                    assert hashlib.sha256(data).hexdigest() == recipe["files"][member.filename]
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with destination.open("xb") as stream:
                        stream.write(data)
    assert expanded == 15336396 and count == 833
    assert {p.relative_to(deps).as_posix(): file_digest(p)
            for p in deps.rglob("*") if p.is_file()} == recipe["files"]
    user = scratch / "fixture-user"
    user.mkdir()
    environment = sanitized_environment()
    environment.update(USERPROFILE=str(user), APPDATA=str(user), LOCALAPPDATA=str(user),
                       PYTHONUSERBASE=str(user), PYTHONDONTWRITEBYTECODE="1")
    source_commit = context["job"]["source_commit"]
    stages = []
    host = WindowsJobHost()
    scenarios = ("disabled", "missing", "changed", "version", "distribution", "bounds",
                 "preloaded", "duplicate", "success", "malformed", "step",
                 "environment_failure", "interrupt", "resume", "cancel")
    interrupted = None
    for scenario in scenarios:
        stage = output / scenario
        stage.mkdir()
        project = scratch / (scenario + "-project")
        if scenario == "resume":
            project = scratch / "interrupt-project"
            before_resume = {p.relative_to(interrupted).as_posix(): file_digest(p)
                             for p in interrupted.rglob("*") if p.is_file()}
        else:
            project.mkdir()
            (project / "arithmetic.py").write_text("def add(a, b):\n    return a - b\n", encoding="utf-8")
            (project / "notes.txt").write_text("Preserve project customization.\n", encoding="utf-8")
        job_id = uuid.uuid4().hex
        argv = [sys.executable, "-I", "-B", str(ROOT / "core/execution/tests/test_mini_worker.py"),
                scenario, str(deps), str(TASK / "evidence/dependency-recipe.json"),
                str(project), str(stage), source_commit]
        launch = {"scenario": scenario, "status": "PREPARED", "job_id": job_id,
                  "argv": argv, "cwd": str(project), "timeout": 25,
                  "output_limit": 131072, "memory_limit": 512 * 1024 * 1024,
                  "process_limit": 3}
        write(stage / "launch.json", launch)
        write(output / "active-stage.json", launch)

        def checkpoint(value):
            launch.update(status="INCOMPLETE", checkpoint=value)
            write(stage / "launch.json", launch)

        def observed(value):
            with (stage / "observations.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps(value) + "\n")

        result = None
        row = {"scenario": scenario, "job_id": job_id, "result": None}
        try:
            result = host.run(
                argv, cwd=project, input_bytes=b"", output_dir=stage / "process",
                job_id=job_id, timeout=25, output_limit=131072,
                memory_limit=512 * 1024 * 1024, process_limit=3,
                cancelled=lambda: scenario == "cancel" and (stage / "cancel-ready").is_file(),
                checkpoint=checkpoint, observed=observed, environment=environment)
            row["result"] = result
        except BaseException as exc:
            row["error_type"] = type(exc).__name__
            raise
        finally:
            launch.update(status="TERMINAL" if result else "UNCERTAIN", result=result)
            write(stage / "launch.json", launch)
            stages.append(row)
            write(output / "stages.json", stages)
        # Retain actual bounded postimages before scratch retirement or continuation.
        assert result["quiescent"], scenario
        postimages = stage / "postimages"
        postimages.mkdir()
        row["postimage_sha256"] = {}
        for name in ("arithmetic.py", "notes.txt"):
            assert ordinary(project / name).st_size <= 4096
            data = (project / name).read_bytes()
            (postimages / name).write_bytes(data)
            row["postimage_sha256"][name] = hashlib.sha256(data).hexdigest()
        write(output / "stages.json", stages)
        if scenario == "cancel":
            assert result["reason"] == "cancelled"
            receipt = json.loads((stage / "cancel/attempt.json").read_text())
            assert receipt["status"] == "INCOMPLETE" and not receipt["accepted"]
            assert (stage / "cancel/trajectory.json").is_file()
            assert (project / "arithmetic.py").read_text() == "def add(a, b):\n    return a + b\n"
            assert host.reconcile(job_id)["quiescent"]
            row["partial_effect_preserved"] = True
        else:
            assert result["exit_code"] == 0, scenario
            counts = json.loads((stage / "test-result.json").read_text())
            assert counts["tests_run"] == 1 and not any(counts[k] for k in ("failures", "errors", "skips"))
        if scenario == "interrupt":
            interrupted = stage / "interrupt"
        if scenario == "resume":
            assert {p.relative_to(interrupted).as_posix(): file_digest(p)
                    for p in interrupted.rglob("*") if p.is_file()} == before_resume
            row["prior_evidence_unchanged"] = True
        write(output / "stages.json", stages)
        print(json.dumps({"scenario": scenario, "result": "PASS", "job_id": job_id}), flush=True)
    assert not list(user.iterdir()), "ambient user configuration was touched"
    assert {p.relative_to(deps).as_posix(): file_digest(p)
            for p in deps.rglob("*") if p.is_file()} == recipe["files"]
    write(output / "fixture-result.json", {
        "status": "PASS", "scenarios": len(stages), "source_commit": source_commit,
        "recipe_sha256": digest(recipe), "real_model_requests": 0,
        "actual_upstream_default_agent": True, "fixture_only": True,
        "candidate_automatically_accepted": False, "network_calls": 0,
        "global_installation": False, "filesystem_read_isolation_qualified": False})
    write(output / "active-stage.json", {"status": "TERMINAL", "result": "PASS"})


if __name__ == "__main__":
    main()

