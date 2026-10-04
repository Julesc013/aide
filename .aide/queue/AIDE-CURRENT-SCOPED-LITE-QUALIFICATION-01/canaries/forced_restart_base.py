"""Force a real child-process exit at delivered Lite lifecycle effect boundaries."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(os.environ["AIDE_JOB_TMP"])
ZIP = Path(r"D:\Projects\AIDE\aide\.aide\release\dist\aide-lite-pack-v0.zip")
ZIP_SHA = "af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff"
HELPER = Path(__file__).resolve().parent / "lifecycle_helper.py"
HELPER_SHA = "3f3140807520b1481181c34e95e06273e2774698cf2d384e42b5b6214f58a181"
MANAGED = ".aide/prompts/compact-task.md"
EXIT = 77


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def helper():
    if sha(HELPER) != HELPER_SHA:
        raise AssertionError("prior extractor helper changed")
    spec = importlib.util.spec_from_file_location("aide_forced_restart_helper", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def child(kind: str, pack: Path, target: Path, digest: str, marker: Path) -> None:
    h = helper()
    module = h.load_delivered(pack)

    def die(boundary: str) -> None:
        marker.write_text(boundary + "\n", encoding="utf-8")
        os._exit(EXIT)

    if kind == "import-receipt":
        original = module.portable_import_write_exact

        def write(root, rel, body, expected, backup=None):
            result = original(root, rel, body, expected, backup)
            if rel == module.PORTABLE_IMPORT_RECEIPT_PATH:
                die(kind)
            return result

        module.portable_import_write_exact = write
        module.apply_import_pack(pack, target, expected_plan_digest=digest)
    elif kind == "repair-file":
        original = module.atomic_create_bytes_no_clobber

        def create(path, body):
            result = original(path, body)
            if Path(path) == target / MANAGED:
                die(kind)
            return result

        module.atomic_create_bytes_no_clobber = create
        module.apply_portable_owned_repair(pack, target, MANAGED, expected_plan_digest=digest)
    elif kind == "removal-receipt":
        original = module.windows_unlink_exact_portable_file

        def unlink(path, expected, *args, **kwargs):
            result = original(path, expected, *args, **kwargs)
            if Path(path) == target / module.PORTABLE_IMPORT_RECEIPT_PATH:
                die(kind)
            return result

        module.windows_unlink_exact_portable_file = unlink
        module.apply_portable_removal(target, digest)
    else:
        raise ValueError(kind)
    raise AssertionError(f"{kind} did not exit at its selected boundary")


def record_child(out: Path, kind: str, pack: Path, target: Path, digest: str) -> dict:
    marker = out / f"{kind}.marker"
    argv = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--child", kind,
            "--pack", str(pack), "--target", str(target), "--digest", digest, "--marker", str(marker)]
    result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    log = out / f"{kind}.child.json"
    log.write_text(json.dumps({"argv": argv, "exit_code": result.returncode,
        "stdout": result.stdout, "stderr": result.stderr}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if result.returncode != EXIT or not marker.is_file() or marker.read_text("utf-8") != kind + "\n":
        raise AssertionError(f"{kind} did not terminate at selected effect boundary; see {log}")
    return {"kind": kind, "exit_code": result.returncode, "log_sha256": sha(log), "marker_sha256": sha(marker)}


def normal(rec, label: str, script: Path, root: Path, *args: str, exits=(0,)) -> str:
    argv = [sys.executable, "-I", "-B", str(script), "--repo-root", str(root), *args]
    result = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    log = rec / f"{label}.json"
    log.write_text(json.dumps({"argv": argv, "exit_code": result.returncode, "stdout": result.stdout,
        "stderr": result.stderr}, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if result.returncode not in exits:
        raise AssertionError(f"{label} exit {result.returncode}; see {log}")
    return result.stdout


def run(out: Path) -> None:
    if os.name != "nt" or out.parent != ROOT or not out.name.startswith("run-") or out.exists():
        raise ValueError("use a new run-* child of the external scratch directory on Windows")
    if sha(ZIP) != ZIP_SHA:
        raise AssertionError("current delivered ZIP changed")
    h = helper()
    out.mkdir()
    try:
        members = h.extract_zip(ZIP, out / "candidate")
        pack = out / "candidate" / h.PACK_NAME
        module = h.load_delivered(pack)
        cli = pack / "files/.aide/scripts/aide_lite.py"
        observed = []

        target = out / "fresh-import"
        target.mkdir()
        authored = b"# Existing project guidance\r\n"
        (target / "AGENTS.md").write_bytes(authored)
        (target / "project-owned.txt").write_bytes(b"keep me\r\n")
        args = ("import-pack", "--pack", str(pack), "--target", str(target), "--mode", "safe")
        preview = normal(out, "import-preview", cli, pack, *args, "--dry-run")
        digest = h.field(preview, "plan_digest")
        observed.append(record_child(out, "import-receipt", pack, target, digest))
        if not (target / module.PORTABLE_IMPORT_INTENT_PATH).is_file():
            raise AssertionError("abrupt import lost intent")
        pending = normal(out, "import-pending", cli, pack, *args, "--dry-run", exits=(0, 3))
        if h.field(pending, "status") != "RECOVERY_REQUIRED":
            raise AssertionError("abrupt import not classified as pending")
        resumed = normal(out, "import-resume", cli, pack, *args, "--expect-plan", digest)
        if h.field(resumed, "status") != "RECOVERED":
            raise AssertionError("abrupt import did not reconcile completed effect")
        if (target / module.PORTABLE_IMPORT_INTENT_PATH).exists() or not (target / "AGENTS.md").read_bytes().startswith(authored):
            raise AssertionError("abrupt import changed authored guidance or retained intent")
        if (target / "project-owned.txt").read_bytes() != b"keep me\r\n":
            raise AssertionError("abrupt import changed project-owned file")

        repair = out / "repair"
        h.install(h.Recorder(out), "repair-install", pack, repair)
        (repair / MANAGED).unlink()
        repair_args = ("repair-owned-file", "--pack", str(pack), "--target", str(repair), "--path", MANAGED)
        preview = normal(out, "repair-preview", cli, pack, *repair_args, "--dry-run")
        repair_digest = h.field(preview, "plan_digest")
        observed.append(record_child(out, "repair-file", pack, repair, repair_digest))
        pending = normal(out, "repair-pending", cli, pack, *repair_args, "--dry-run", exits=(0, 3))
        if h.field(pending, "status") != "RECOVERY_REQUIRED":
            raise AssertionError("abrupt repair not pending")
        resumed = normal(out, "repair-resume", cli, pack, *repair_args, "--expect-plan", repair_digest)
        if h.field(resumed, "status") != "RECOVERED" or (repair / module.PORTABLE_REPAIR_INTENT_PATH).exists():
            raise AssertionError("abrupt repair did not reconcile exact file")
        if sha(repair / MANAGED) != sha(pack / "files" / MANAGED):
            raise AssertionError("repaired file differs from delivered payload")

        removal = out / "removal"
        removal.mkdir()
        (removal / "AGENTS.md").write_bytes(authored)
        (removal / "project-owned.txt").write_bytes(b"keep me\r\n")
        h.install(h.Recorder(out), "removal-install", pack, removal)
        removal_receipt = module.load_portable_import_receipt(removal)
        expected_agents = module.portable_agents_section_postimage(
            (removal / "AGENTS.md").read_bytes(),
            removal_receipt["managed"]["AGENTS.md"]["installed_digest"])
        if expected_agents is None or not expected_agents.startswith(authored):
            raise AssertionError("authored AGENTS removal oracle is invalid")
        project_digest = sha(removal / "project-owned.txt")
        removal_cli = removal / ".aide/scripts/aide_lite.py"
        plan = json.loads(normal(out, "removal-preview", removal_cli, removal,
            "plan-removal", "--target", str(removal), "--json"))
        observed.append(record_child(out, "removal-receipt", pack, removal, plan["plan_digest"]))
        if not (removal / module.PORTABLE_REMOVAL_INTENT_PATH).is_file() or (removal / module.PORTABLE_IMPORT_RECEIPT_PATH).exists():
            raise AssertionError("abrupt removal did not retain intent after receipt retirement")
        runner = cli
        recovered = json.loads(normal(out, "removal-resume", runner, removal,
            "apply-removal", "--target", str(removal), "--expect-plan", plan["plan_digest"], "--json"))
        if recovered["status"] != "DETACHED_RECOVERED":
            raise AssertionError(f"abrupt removal recovery: {recovered['status']}")
        h.assert_detached(removal, set(removal_receipt["managed"]), module,
            unknown={"project-owned.txt": project_digest}, authored_agents=expected_agents)
        if (removal / "project-owned.txt").read_bytes() != b"keep me\r\n":
            raise AssertionError("abrupt removal changed project-owned bytes")

        result = {"status": "PASS", "zip_sha256": ZIP_SHA, "cli_sha256": sha(cli),
            "helper_sha256": HELPER_SHA, "script_sha256": sha(Path(__file__)),
            "member_count": len(members), "forced_exits": observed,
            "import": "RECOVERED", "repair": "RECOVERED", "removal": "DETACHED_RECOVERED",
            "synthetic_successor_is_published": False}
        path = out / "summary.json"
        path.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "PASS", "summary": str(path), "sha256": sha(path)}, sort_keys=True))
    except BaseException:
        (out / "failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    parser.add_argument("--child", choices=("import-receipt", "repair-file", "removal-receipt"))
    parser.add_argument("--pack", type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--digest")
    parser.add_argument("--marker", type=Path)
    args = parser.parse_args()
    if args.child:
        child(args.child, args.pack, args.target, args.digest, args.marker)
    elif args.out:
        run(args.out.resolve())
    else:
        parser.error("--out or --child is required")


if __name__ == "__main__":
    main()
