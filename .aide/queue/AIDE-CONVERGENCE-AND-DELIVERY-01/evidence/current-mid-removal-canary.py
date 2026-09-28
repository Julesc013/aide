"""Bounded child-exit removal check for one exact delivered Lite ZIP."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import traceback
import zipfile


EXIT_AFTER_UNLINK = 77
PACK_NAME = "aide-lite-pack-v0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def delivered_module(pack: Path):
    source = pack / "files/.aide/scripts/aide_lite.py"
    spec = importlib.util.spec_from_file_location("aide_delivered_mid_removal", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("delivered CLI module missing")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def child(pack: Path, target: Path, plan_digest: str, marker: Path, exit_after: int) -> None:
    module = delivered_module(pack)
    receipt = module.load_portable_import_receipt(target)
    managed = set(receipt["managed"])
    original = module.windows_unlink_exact_portable_file
    owned_unlinks = 0

    def exit_after_owned_unlink(path, expected, *args, **kwargs):
        nonlocal owned_unlinks
        result = original(path, expected, *args, **kwargs)
        relative = Path(path).relative_to(target).as_posix()
        if relative in managed and relative not in {"AGENTS.md", module.PORTABLE_REMOVAL_RUNNER_PATH}:
            owned_unlinks += 1
            if owned_unlinks == exit_after:
                marker.write_text(json.dumps({"relative": relative, "owned_unlinks": owned_unlinks}) + "\n",
                                  encoding="utf-8")
                os._exit(EXIT_AFTER_UNLINK)
        return result

    module.windows_unlink_exact_portable_file = exit_after_owned_unlink
    module.apply_portable_removal(target, plan_digest)
    raise AssertionError("owned-file deletion point was not reached")


def delivered_cli(pack: Path, target: Path, *args: str) -> dict[str, object]:
    source = pack / "files/.aide/scripts/aide_lite.py"
    command = [sys.executable, "-I", "-B", str(source), "--repo-root", str(target), *args]
    if args[0] != "import-pack":
        command.append("--json")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=180)
    if result.returncode != 0:
        raise AssertionError(f"delivered CLI {args[0]} exited {result.returncode}: {result.stderr[-1000:]}")
    if args[0] == "import-pack":
        fields = dict(line.split(": ", 1) for line in result.stdout.splitlines() if ": " in line)
        if not fields.get("status") or not fields.get("plan_digest"):
            raise AssertionError("delivered import response lacks status or exact plan digest")
        return {"status": fields["status"], "plan_digest": fields["plan_digest"]}
    return json.loads(result.stdout)


def run(archive: Path, expected_sha256: str, exit_after: int) -> None:
    if not 1 <= exit_after <= 100:
        raise ValueError("owned-unlink ordinal must be between 1 and 100")
    scratch = Path(os.environ["AIDE_JOB_TMP"])
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    if sha256(archive) != expected_sha256:
        raise ValueError("current frozen asset digest mismatch")
    out = scratch / "current-mid-removal"
    if out.exists():
        raise ValueError("fresh job scratch required")
    out.mkdir()
    try:
        extraction = out / "extract"
        extraction.mkdir()
        with zipfile.ZipFile(archive) as bundle:
            members = bundle.infolist()
            names = [member.filename for member in members]
            if not members or len(names) != len(set(names)) or sum(member.file_size for member in members) > 512 * 1024 * 1024:
                raise ValueError("unsafe or oversized release archive")
            for member in members:
                name = member.filename
                parts = PurePosixPath(name).parts
                mode = member.external_attr >> 16
                if (not parts or parts[0] != PACK_NAME or name.startswith("/")
                        or "\\" in name or ".." in parts or stat.S_ISLNK(mode)):
                    raise ValueError("unsafe release archive member")
            bundle.extractall(extraction)
        pack = extraction / PACK_NAME
        module = delivered_module(pack)
        target = out / "brownfield"
        target.mkdir()
        authored = b"# Existing project guidance\r\n"
        project_owned = b"keep this project content\r\n"
        (target / "AGENTS.md").write_bytes(authored)
        (target / "project-owned.txt").write_bytes(project_owned)

        preview = delivered_cli(pack, target, "import-pack", "--pack", str(pack),
                                "--target", str(target), "--dry-run", "--mode", "safe")
        installed = delivered_cli(pack, target, "import-pack", "--pack", str(pack),
                                  "--target", str(target), "--mode", "safe",
                                  "--expect-plan", str(preview["plan_digest"]))
        if installed["status"] != "APPLIED":
            raise AssertionError("delivered brownfield import did not apply")
        receipt = module.load_portable_import_receipt(target)
        managed = set(receipt["managed"])
        if len(managed) <= exit_after + 2:
            raise AssertionError("insufficient receipt-owned files for requested interruption")
        expected_agents = module.portable_agents_section_postimage(
            (target / "AGENTS.md").read_bytes(), receipt["managed"]["AGENTS.md"]["installed_digest"])
        if expected_agents is None or not expected_agents.startswith(authored):
            raise AssertionError("authored AGENTS baseline cannot be recovered")
        plan = delivered_cli(pack, target, "plan-removal", "--target", str(target))
        digest = str(plan["plan_digest"])
        marker = out / "first-owned-unlink.txt"
        result = subprocess.run([sys.executable, "-I", "-B", str(Path(__file__).resolve()),
                                 "--child", str(pack), str(target), digest, str(marker), str(exit_after)],
                                capture_output=True, text=True, encoding="utf-8", timeout=180)
        if result.returncode != EXIT_AFTER_UNLINK or not marker.is_file():
            raise AssertionError(f"child did not exit after owned unlink: {result.stderr[-1000:]}")
        interruption = json.loads(marker.read_text(encoding="utf-8"))
        removed = interruption["relative"]
        if interruption["owned_unlinks"] != exit_after or removed not in managed or (target / removed).exists():
            raise AssertionError("recorded owned file was not removed")
        if (module.load_portable_removal_intent(target) is None
                or module.load_portable_import_receipt(target) is None):
            raise AssertionError("mid-removal intent or receipt was lost")
        if (target / "project-owned.txt").read_bytes() != project_owned:
            raise AssertionError("project-owned bytes changed at interruption")
        resumed = delivered_cli(pack, target, "apply-removal", "--target", str(target),
                                "--expect-plan", digest)
        if resumed["status"] != "DETACHED":
            raise AssertionError("fresh delivered CLI did not finish detach")
        if module.load_portable_removal_intent(target) is not None or module.load_portable_import_receipt(target) is not None:
            raise AssertionError("removal state remains after detach")
        for relative in managed - {"AGENTS.md"}:
            if (target / relative).exists():
                raise AssertionError(f"receipt-owned file remains: {relative}")
        if (target / "AGENTS.md").read_bytes() != expected_agents or (target / "project-owned.txt").read_bytes() != project_owned:
            raise AssertionError("authored or project-owned bytes changed after detach")
        summary = {"status": "PASS", "asset_sha256": expected_sha256,
                   "archive_members": len(members), "managed_files": len(managed),
                   "child_exit": result.returncode, "interrupted_after_owned_unlinks": exit_after,
                   "interrupted_relative": removed,
                   "intent_and_receipt_retained_after_exit": True,
                   "fresh_cli_resume": resumed["status"],
                   "authored_and_project_owned_preserved": True}
        (retained / "current-mid-removal-summary.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(summary, sort_keys=True))
    except BaseException:
        (retained / "current-mid-removal-failure.txt").write_text(
            traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    if len(sys.argv) == 7 and sys.argv[1] == "--child":
        child(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], Path(sys.argv[5]), int(sys.argv[6]))
    elif len(sys.argv) == 4:
        run(Path(sys.argv[1]), sys.argv[2], int(sys.argv[3]))
    else:
        raise SystemExit("exact ZIP, SHA and owned-unlink ordinal, or --child pack target plan marker ordinal required")
