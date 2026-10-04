"""Run pinned child-exit recovery checks inside one managed D job."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import sys


def main() -> None:
    if len(sys.argv) != 3:
        raise ValueError("expected exact release ZIP path and SHA-256")
    archive = Path(sys.argv[1]).resolve(strict=True)
    archive_sha = sys.argv[2]
    root = Path(__file__).resolve().parent
    temp = Path(os.environ["AIDE_JOB_TMP"])
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    source = root / "forced_restart_base.py"
    spec = importlib.util.spec_from_file_location("aide_forced_restart_pinned", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("pinned restart canary cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.ZIP = archive
    module.ZIP_SHA = archive_sha
    out = temp / "run-forced-restart"
    sys.argv = [str(source), "--out", str(out)]
    try:
        module.main()
    finally:
        if out.exists():
            for path in out.glob("*.json"):
                shutil.copy2(path, retained / path.name)
            failure = out / "failure.txt"
            if failure.is_file():
                shutil.copy2(failure, retained / failure.name)


if __name__ == "__main__":
    main()
