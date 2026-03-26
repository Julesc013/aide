from __future__ import annotations

import json
import unittest
from pathlib import Path

from shared.core.dispatcher import dispatch_request_payload


FIXTURE_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "boot-slice"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class BootSliceRuntimeTests(unittest.TestCase):
    def assert_fixture_response(self, request_name: str, response_name: str) -> None:
        actual = dispatch_request_payload(load_fixture(request_name))
        expected = load_fixture(response_name)
        self.assertEqual(actual, expected)

    def test_success_request_matches_fixture(self) -> None:
        self.assert_fixture_response("success-request.json", "success-response.json")

    def test_unavailable_request_matches_fixture(self) -> None:
        self.assert_fixture_response("unavailable-request.json", "unavailable-response.json")

    def test_invalid_request_matches_fixture(self) -> None:
        self.assert_fixture_response("invalid-request.json", "invalid-response.json")

    def test_capability_request_matches_fixture(self) -> None:
        self.assert_fixture_response("capability-request.json", "capability-response.json")
