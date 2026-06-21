"""Thin entry point for the repair-check side-effect boundary evidence."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).with_name("check_repaired_seam.py")), run_name="__main__")
