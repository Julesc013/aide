"""Run the pinned delivered-byte canary inside one managed AIDE job."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys


def require_status(result: dict[str, object], expected: str, stage: str) -> None:
    if result.get("status") != expected:
        raise AssertionError(f"{stage}: expected {expected}, got {result.get('status')}")


def main() -> None:
    root = Path(__file__).resolve().parent
    temp = Path(os.environ["AIDE_JOB_TMP"])
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    out = temp / "run-consumer"
    source = root / "consumer_canary_base.py"
    spec = importlib.util.spec_from_file_location("aide_pinned_consumer", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("pinned consumer canary cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PREP = temp
    sys.argv = [str(source), *sys.argv[1:], "--out", str(out)]
    try:
        module.main()
        pack = out / "candidate-zip" / module.PACK_NAME
        successor = out / "synthetic-v2"
        delivered = module.delivered_module(pack)
        target = out / "partial-recovery-target"
        target.mkdir()
        authored = target / "project-owned.txt"
        authored.write_bytes(b"Keep project bytes.\r\n")

        first = delivered.apply_import_pack(pack, target, fail_after_writes=1)
        require_status(first, "INTERRUPTED", "fresh interruption")
        if first.get("recovery", {}).get("classification") != "partial":
            raise AssertionError("fresh interruption did not record partial state")
        require_status(delivered.apply_import_pack(pack, target), "RECOVERY_REQUIRED", "fresh replay guard")
        recovered = delivered.apply_import_pack(
            pack, target, expected_plan_digest=first["plan_digest"], recover_partial=True
        )
        require_status(recovered, "RECOVERED", "fresh explicit recovery")

        second = delivered.apply_import_pack(
            successor, target, predecessor_pack=pack, fail_after_writes=1
        )
        require_status(second, "INTERRUPTED", "update interruption")
        if second.get("recovery", {}).get("classification") != "partial":
            raise AssertionError("update interruption did not record partial state")
        require_status(
            delivered.apply_import_pack(successor, target, predecessor_pack=pack),
            "RECOVERY_REQUIRED", "update replay guard"
        )
        recovered_update = delivered.apply_import_pack(
            successor, target, predecessor_pack=pack,
            expected_plan_digest=second["plan_digest"], recover_partial=True
        )
        require_status(recovered_update, "RECOVERED", "update explicit recovery")
        if authored.read_bytes() != b"Keep project bytes.\r\n":
            raise AssertionError("partial recovery changed project-owned bytes")
        if (target / delivered.PORTABLE_IMPORT_INTENT_PATH).exists():
            raise AssertionError("successful recovery retained active intent")
        result = {
            "status": "PASS",
            "fresh": [first["status"], "RECOVERY_REQUIRED", recovered["status"]],
            "update": [second["status"], "RECOVERY_REQUIRED", recovered_update["status"]],
            "project_owned_sha256": hashlib.sha256(authored.read_bytes()).hexdigest(),
            "network_calls": "none",
        }
        (retained / "partial-recovery-result.json").write_text(
            json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(result, sort_keys=True))
    finally:
        if out.exists():
            for path in out.glob("*.json"):
                shutil.copy2(path, retained / path.name)
            failure = out / "failure.txt"
            if failure.is_file():
                shutil.copy2(failure, retained / failure.name)


if __name__ == "__main__":
    main()
