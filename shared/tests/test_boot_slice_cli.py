from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO_ROOT / "fixtures" / "boot-slice"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class BootSliceCLITests(unittest.TestCase):
    def test_cli_smoke_matches_success_fixture(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "shared.cli",
                "--request",
                str(FIXTURE_DIR / "success-request.json"),
                "--pretty",
            ],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        actual = json.loads(completed.stdout)
        expected = load_fixture("success-response.json")
        self.assertEqual(actual, expected)
