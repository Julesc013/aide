from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
import sys

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.providers import contracts, registry, status  # noqa: E402


class ProviderContractTests(unittest.TestCase):
    def make_repo(self) -> Path:
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for rel in [
            ".aide/profile.yaml",
            ".aide/queue/index.yaml",
            registry.PROVIDER_POLICY_PATH,
            registry.PROVIDER_CATALOG_PATH,
            registry.CAPABILITY_MATRIX_PATH,
            registry.ADAPTER_CONTRACT_PATH,
            registry.PROVIDER_STATUS_PATH,
        ]:
            source = REPO_ROOT / rel
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
        return root

    def test_dataclass_contract_shape(self) -> None:
        provider = contracts.ProviderMetadata(
            provider_id="deterministic_tools",
            display_name="Deterministic Tools",
            adapter_class=contracts.AdapterClass.DETERMINISTIC_TOOL.value,
            provider_class=contracts.ProviderClass.DETERMINISTIC.value,
            privacy_class=contracts.PrivacyClass.LOCAL.value,
            credentials_required=False,
            credentials_location="none",
            live_calls_allowed_in_q20=False,
            status="metadata_only",
        )
        self.assertEqual(provider.provider_id, "deterministic_tools")
        self.assertFalse(provider.live_calls_allowed_in_q20)

    def test_catalog_loading_and_required_families(self) -> None:
        providers = registry.load_provider_catalog(self.make_repo())
        ids = {provider.provider_id for provider in providers}
        self.assertGreaterEqual(len(providers), 13)
        self.assertIn("deterministic_tools", ids)
        self.assertIn("human", ids)
        self.assertIn("openai", ids)
        self.assertTrue(all(provider.live_calls_allowed_in_q20 is False for provider in providers))

    def test_capability_matrix_anchors(self) -> None:
        dimensions = registry.capability_dimensions(self.make_repo())
        self.assertIn("deterministic_transform", dimensions)
        self.assertIn("frontier_review", dimensions)
        self.assertIn("unavailable", dimensions)

    def test_validation_detects_no_secrets_and_disabled_calls(self) -> None:
        result = registry.validate_provider_files(self.make_repo())
        self.assertEqual(result["result"], "PASS", result)
        self.assertEqual(result["errors"], [])

    def test_status_summary_contains_no_credentials_or_raw_bodies(self) -> None:
        data = status.build_provider_status(self.make_repo())
        serialized = json.dumps(data, sort_keys=True)
        self.assertFalse(data["live_provider_calls"])
        self.assertFalse(data["live_model_calls"])
        self.assertFalse(data["network_calls"])
        self.assertFalse(data["credentials_configured"])
        self.assertNotIn("raw_prompt_body", serialized)
        self.assertNotIn("raw_response_body", serialized)
        self.assertNotIn("sk-", serialized)

    def test_status_distinguishes_local_remote_human_and_deterministic(self) -> None:
        data = status.build_provider_status(self.make_repo())
        self.assertIn("deterministic_tools", data["deterministic_provider_ids"])
        self.assertIn("human", data["human_provider_ids"])
        self.assertIn("local_ollama", data["local_provider_ids"])
        self.assertIn("openai", data["remote_provider_ids"])
        self.assertIn("openrouter", data["aggregator_provider_ids"])

    def test_write_status_reports(self) -> None:
        root = self.make_repo()
        json_path, md_path, data = status.write_provider_status_files(root)
        self.assertTrue(json_path.exists())
        self.assertTrue(md_path.exists())
        parsed = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(parsed["schema_version"], status.SCHEMA_VERSION)
        self.assertIn("## Boundary", md_path.read_text(encoding="utf-8"))
        self.assertEqual(data["validation"]["result"], "PASS")

    def test_offline_probe_makes_no_live_call_claims(self) -> None:
        probe = status.offline_probe(self.make_repo())
        self.assertFalse(probe["live_provider_calls"])
        self.assertFalse(probe["live_model_calls"])
        self.assertFalse(probe["network_calls"])
        self.assertFalse(probe["provider_probe_calls"])


if __name__ == "__main__":
    unittest.main()
