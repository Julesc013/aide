from __future__ import annotations

import json
import tempfile
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path


from core.gateway import gateway_status, server  # noqa: E402


class GatewaySkeletonTests(unittest.TestCase):
    def write_text(self, root: Path, rel_path: str, text: str) -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")

    def write_json(self, root: Path, rel_path: str, data: dict[str, object]) -> None:
        self.write_text(root, rel_path, json.dumps(data, indent=2, sort_keys=True) + "\n")

    def write_gateway_fixture(self, root: Path, prepared: bool) -> None:
        # Keep these tests focused on Gateway payload behavior. Running the full
        # AIDE Lite report/eval pipeline here makes the suite depend on unrelated
        # long-running golden tasks and has caused validation timeouts.
        self.write_text(root, ".gitignore", ".aide.local/\n.aide.local/**\n")
        self.write_text(
            root,
            ".aide/profile.yaml",
            "schema_version: aide.profile.v0\npolicy_id: aide-profile\nstatus: active\n",
        )
        self.write_text(root, ".aide/queue/index.yaml", "schema_version: aide.queue-index.v0\nitems: []\n")

        text_files = {
            ".aide/policies/gateway.yaml": (
                "schema_version: aide.gateway-policy.v0\n"
                "policy_id: gateway-skeleton\n"
                "status: active\n"
                "local_skeleton\n"
                "report_only\n"
            ),
            ".aide/policies/provider-adapters.yaml": "schema_version: aide.provider-adapters.v0\nstatus: active\n",
            ".aide/providers/provider-catalog.yaml": "schema_version: aide.provider-catalog.v0\nproviders: []\n",
            ".aide/policies/token-budget.yaml": "schema_version: aide.token-budget.v0\nstatus: active\n",
            ".aide/prompts/compact-task.md": "# Compact Task\n",
            ".aide/policies/verification.yaml": "schema_version: aide.verification.v0\nstatus: active\n",
            ".aide/prompts/evidence-review.md": "# Evidence Review\n",
            ".aide/policies/token-ledger.yaml": "schema_version: aide.token-ledger.v0\nstatus: active\n",
            ".aide/policies/evals.yaml": "schema_version: aide.evals.v0\nstatus: active\n",
            ".aide/evals/golden-tasks/catalog.yaml": "schema_version: aide.golden-tasks.v0\ntasks: []\n",
            ".aide/policies/controller.yaml": "schema_version: aide.controller.v0\nstatus: active\n",
            ".aide/controller/latest-outcome-report.md": "# Outcome\n",
            ".aide/controller/latest-recommendations.md": "# Recommendations\n",
            ".aide/policies/routing.yaml": "schema_version: aide.routing.v0\nquality_gates: []\n",
            ".aide/policies/cache.yaml": "schema_version: aide.cache.v0\nstatus: active\n",
            ".aide/policies/local-state.yaml": "schema_version: aide.local-state.v0\nstatus: active\n",
            ".aide/gateway/endpoints.yaml": "schema_version: aide.gateway-endpoints.v0\nendpoints: []\n",
            ".aide/gateway/lifecycle.yaml": "schema_version: aide.gateway-lifecycle.v0\nstatus: active\n",
            ".aide/gateway/security-boundary.md": "# Security Boundary\n",
            ".aide/context/latest-task-packet.md": "# Task Packet\n",
            ".aide/context/latest-context-packet.md": "# Context Packet\n",
            ".aide/context/latest-review-packet.md": "# Review Packet\n",
            ".aide/reports/token-ledger.jsonl": "",
            gateway_status.TOKEN_SUMMARY_PATH: "# Token Summary\n",
            gateway_status.VERIFICATION_REPORT_PATH: "# Verification\n\nresult: PASS\n",
        }
        for rel_path, text in text_files.items():
            self.write_text(root, rel_path, text)

        for rel_path in [
            ".aide/context/repo-map.json",
            ".aide/context/test-map.json",
            ".aide/context/context-index.json",
        ]:
            self.write_json(root, rel_path, {"schema_version": rel_path, "result": "PASS"})

        self.write_json(
            root,
            gateway_status.PROVIDER_STATUS_JSON_PATH,
            {
                "schema_version": "aide.provider-status.v0",
                "provider_family_count": 0,
                "validation": {"result": "PASS"},
                "live_provider_calls": False,
                "live_model_calls": False,
                "network_calls": False,
                "credentials_configured": False,
            },
        )

        if not prepared:
            return

        self.write_json(
            root,
            gateway_status.ROUTE_DECISION_JSON_PATH,
            {
                "schema_version": "aide.route-decision.v0",
                "route_id": "test",
                "task_class": "bounded_code_patch",
                "risk_class": "low",
                "route_class": "no_model_tool",
                "fallback_route_class": "human_review",
                "blocked": False,
                "quality_gate_status": "PASS",
                "token_budget_status": "within_budget",
                "evidence_sources": [],
                "required_checks": [],
                "notes": ["fixture_only"],
            },
        )
        self.write_text(root, gateway_status.ROUTE_DECISION_MD_PATH, "# Route Decision\n")
        self.write_json(
            root,
            gateway_status.GOLDEN_RUN_JSON_PATH,
            {"schema_version": "aide.golden-run.v0", "result": "PASS", "tasks": []},
        )
        self.write_json(
            root,
            gateway_status.CACHE_KEYS_JSON_PATH,
            {
                "schema_version": "aide.cache-keys.v0",
                "contents_inline": False,
                "keys": {},
                "local_state_boundary": {"local_state_ignored": True},
            },
        )

    def make_repo(self, prepared: bool = True) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        self.write_gateway_fixture(root, prepared=prepared)
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
        (root / gateway_status.ROUTE_DECISION_JSON_PATH).unlink(missing_ok=True)
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
