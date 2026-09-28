"""One delivered-byte, child-exit mid-removal check under the AIDE runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
HELPER = ROOT / "lifecycle_helper.py"
EXIT = 77


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def helper():
    spec = importlib.util.spec_from_file_location("aide_mid_removal_helper", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def child(pack: Path, target: Path, digest: str, marker: Path) -> None:
    module = helper().load_delivered(pack)
    managed = set(module.load_portable_import_receipt(target)["managed"])
    original = module.windows_unlink_exact_portable_file

    def unlink(path, expected, *args, **kwargs):
        result = original(path, expected, *args, **kwargs)
        rel = Path(path).relative_to(target).as_posix()
        if rel in managed and rel not in {"AGENTS.md", module.PORTABLE_REMOVAL_RUNNER_PATH}:
            marker.write_text(rel + "\n", encoding="utf-8")
            os._exit(EXIT)
        return result

    module.windows_unlink_exact_portable_file = unlink
    module.apply_portable_removal(target, digest)
    raise AssertionError("selected first managed-file removal did not occur")


def run(archive: Path, expected: str) -> None:
    temp = Path(os.environ["AIDE_JOB_TMP"])
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    out = temp / "mid-removal"
    if out.exists() or sha(archive) != expected:
        raise ValueError("new scratch and exact release ZIP required")
    out.mkdir()
    try:
        h = helper()
        members = h.extract_zip(archive, out / "extract")
        pack = out / "extract" / h.PACK_NAME
        module = h.load_delivered(pack)
        target = out / "brownfield"
        target.mkdir()
        authored = b"# Existing project guidance\r\n"
        (target / "AGENTS.md").write_bytes(authored)
        (target / "project-owned.txt").write_bytes(b"keep me\r\n")
        project_digest = sha(target / "project-owned.txt")
        rec = h.Recorder(out)
        h.install(rec, "install", pack, target)
        receipt = module.load_portable_import_receipt(target)
        expected_agents = module.portable_agents_section_postimage(
            (target / "AGENTS.md").read_bytes(), receipt["managed"]["AGENTS.md"]["installed_digest"])
        assert expected_agents is not None and expected_agents.startswith(authored)
        plan = h.plan_removal(rec, "plan", target)
        digest = plan["plan_digest"]
        marker = out / "child.marker"
        argv = [sys.executable, "-I", "-B", str(Path(__file__).resolve()), "--child",
                str(pack), str(target), digest, str(marker)]
        child_result = subprocess.run(argv, capture_output=True, text=True, timeout=180)
        if child_result.returncode != EXIT or not marker.is_file():
            raise AssertionError("child did not exit after an owned-file removal: " + child_result.stderr[-500:])
        first = marker.read_text(encoding="utf-8").strip()
        if first not in receipt["managed"] or (target / first).exists():
            raise AssertionError("recorded first removal is not an absent owned file")
        if not (target / module.PORTABLE_REMOVAL_INTENT_PATH).is_file() or not (target / module.PORTABLE_IMPORT_RECEIPT_PATH).is_file():
            raise AssertionError("mid-removal exit lost intent or receipt")
        if (target / "project-owned.txt").read_bytes() != b"keep me\r\n":
            raise AssertionError("mid-removal exit changed project-owned bytes")
        cli = pack / "files/.aide/scripts/aide_lite.py"
        resumed = rec.run("resume", cli, pack, "apply-removal", "--target", str(target),
                          "--expect-plan", digest, "--json")
        result = json.loads(resumed.stdout)
        if result["status"] != "DETACHED":
            raise AssertionError("mid-removal resume did not detach: " + result["status"])
        h.assert_detached(target, set(receipt["managed"]), module,
                          unknown={"project-owned.txt": project_digest},
                          authored_agents=expected_agents)
        summary = {"status": "PASS", "asset_sha256": expected, "member_count": len(members),
                   "child_exit": child_result.returncode, "first_removed": first,
                   "intent_and_receipt_retained_after_exit": True, "resume": result["status"],
                   "project_owned_preserved": True, "authored_agents_preserved": True}
        (retained / "mid-removal-summary.json").write_text(
            json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(summary, sort_keys=True))
    except BaseException:
        (retained / "mid-removal-failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise


if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[1] == "--child":
        child(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], Path(sys.argv[5]))
    elif len(sys.argv) == 3:
        run(Path(sys.argv[1]), sys.argv[2])
    else:
        raise SystemExit("exact ZIP and SHA, or --child pack target plan marker required")
