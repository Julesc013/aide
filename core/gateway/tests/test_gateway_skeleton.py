from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite"] = aide_lite
assert SPEC.loader is not None
SPEC.loader.exec_module(aide_lite)

from core.gateway import gateway_status, server  # noqa: E402


class GatewaySkeletonTests(unittest.TestCase):
    def make_repo(self, prepared: bool = True) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        aide_lite._write_minimal_repo(root)
        if prepared:
            aide_lite.run_context(root)
            aide_lite.write_task_packet(root, "Implement Q19 Gateway Architecture and Skeleton")
            aide_lite.adapt_agents(root)
            verification = aide_lite.build_verification_report(root, task_packet_path=aide_lite.LATEST_PACKET_PATH)
            aide_lite.write_verification_report(root, aide_lite.LATEST_VERIFICATION_REPORT_PATH, verification)
            aide_lite.write_review_packet(root)
            aide_lite.write_golden_run_reports(root, aide_lite.run_golden_tasks(root))
            records = aide_lite.build_ledger_scan_records(root)
            aide_lite.write_ledger_records(root, records)
            aide_lite.write_token_savings_summary(root, records, [])
            decision = aide_lite.build_route_decision(root)
            aide_lite.write_route_decision(root, decision)
            aide_lite.write_cache_report(root)
        return root

    def test_status_helpers_load_policy_and_summarize_artifacts(self) -> None:
        root = self.make_repo()
        data = gateway_status.build_gateway_status(root)
        self.assertEqual(data["service"], "aide-gateway-skeleton")
        self.assertFalse(data["provider_calls_enabled"])
        self.assertFalse(data["model_calls_enabled"])
        self.assertFalse(data["outbound_network_enabled"])
        self.assertEqual(data["policy"]["path"], ".aide/policies/gateway.yaml")
        self.assertIn("token_survival", data["readiness"])
        self.assertIn("route", data["signals"])
        self.assertNotIn("print('hello')", json.dumps(data))
        self.assertNotIn("raw_prompt_body", json.dumps(data))

    def test_status_helpers_report_missing_artifacts(self) -> None:
        root = self.make_repo(prepared=False)
        (root / aide_lite.ROUTE_DECISION_JSON_PATH).unlink(missing_ok=True)
        status = gateway_status.status_payload(root)
        self.assertFalse(status["route_decision_present"])
        route_payload = gateway_status.route_explain_payload(root)
        self.assertEqual(route_payload["status"], "warning")

    def test_endpoint_payload_shapes(self) -> None:
        root = self.make_repo()
        expected = {
            "/health": "ok",
            "/status": "ok",
            "/route/explain": "ok",
            "/summaries": "ok",
            "/version": "ok",
        }
        for endpoint, status in expected.items():
            with self.subTest(endpoint=endpoint):
                code, payload = gateway_status.endpoint_payload(endpoint, root)
                self.assertEqual(code, 200)
                self.assertEqual(payload["status"], status)
                serialized = json.dumps(payload)
                self.assertNotIn("raw_prompt_body", serialized)
                self.assertNotIn("raw_response_body", serialized)
                self.assertNotIn("SHOULD_NOT_APPEAR", serialized)

    def test_unknown_endpoint_returns_safe_404(self) -> None:
        code, payload = gateway_status.endpoint_payload("/not-real", self.make_repo())
        self.assertEqual(code, 404)
        self.assertEqual(payload["status"], "not_found")
        self.assertIn("/health", payload["allowed_endpoints"])

    def test_write_gateway_status_reports(self) -> None:
        root = self.make_repo()
        json_path, md_path, data = gateway_status.write_gateway_status_files(root)
        self.assertTrue(json_path.exists())
        self.assertTrue(md_path.exists())
        parsed = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["schema_version"], gateway_status.SCHEMA_VERSION)
        self.assertIn("## Readiness", md_path.read_text(encoding="utf-8"))
        self.assertEqual(data["signals"]["golden_task_status"], "PASS")

    def test_server_handler_is_localhost_testable(self) -> None:
        root = self.make_repo()
        handler = server.make_handler(root)
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        try:
            self.assertIn(httpd.server_address[0], {"127.0.0.1", "localhost"})
        finally:
            httpd.server_close()

    def test_server_rejects_external_bind(self) -> None:
        with self.assertRaisesRegex(ValueError, "localhost"):
            server.serve(self.make_repo(), host="0.0.0.0", port=0)

    def test_post_and_provider_proxy_are_not_supported(self) -> None:
        code, payload = gateway_status.endpoint_payload("/v1/chat/completions", self.make_repo())
        self.assertEqual(code, 404)
        self.assertFalse(payload.get("provider_calls_enabled", False))
        self.assertFalse(payload.get("model_calls_enabled", False))

    def test_gateway_smoke_passes(self) -> None:
        smoke = gateway_status.smoke_gateway(self.make_repo())
        self.assertEqual(smoke["result"], "PASS")
        self.assertEqual(smoke["not_found_status_code"], 404)
        self.assertFalse(smoke["provider_calls_enabled"])
        self.assertFalse(smoke["model_calls_enabled"])


if __name__ == "__main__":
    unittest.main()
