"""Run the pinned Windows lifecycle canary inside one managed D job."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import shutil
import sys


def main() -> None:
    root = Path(__file__).resolve().parent
    temp = Path(os.environ["AIDE_JOB_TMP"])
    retained = Path(os.environ["AIDE_JOB_OUTPUT"])
    source = root / "lifecycle_canary_base.py"
    spec = importlib.util.spec_from_file_location("aide_lifecycle_pinned", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("pinned lifecycle canary cannot load")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PREP = temp
    module.ZIP = Path(sys.argv[1]).resolve(strict=True)
    module.ZIP_SHA = sys.argv[2]
    module.HELPER = root / "lifecycle_helper.py"
    module.HELPER_SHA = sys.argv[3]
    out = temp / "run-lifecycle"
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
