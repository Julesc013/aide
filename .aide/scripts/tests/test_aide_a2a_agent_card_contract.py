import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core.interop import a2a_agent_card_contract

MODULE_PATH = REPO_ROOT / ".aide/scripts/aide_lite.py"
SPEC = importlib.util.spec_from_file_location("aide_lite_a2a_agent_card_contract", MODULE_PATH)
aide_lite = importlib.util.module_from_spec(SPEC)
sys.modules["aide_lite_a2a_agent_card_contract"] = aide_lite
SPEC.loader.exec_module(aide_lite)


def copy_a2a_source_files(root: Path) -> None:
    for rel in a2a_agent_card_contract.source_artifact_paths(REPO_ROOT):
        src = REPO_ROOT / rel
        if src.exists():
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def validate_record(record: dict) -> list[str]:
    errors, _warnings = a2a_agent_card_contract.validate_a2a_agent_card_contract_with_schema(
        record,
        a2a_agent_card_contract.load_a2a_agent_card_contract_schema(REPO_ROOT),
    )
    return errors


class AIDEA2AAgentCardContractTests(unittest.TestCase):
    def test_01_valid_contract_passes_with_warnings(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        errors, warnings = a2a_agent_card_contract.validate_a2a_agent_card_contract_with_schema(record, {})
        self.assertEqual(errors, [])
        self.assertTrue(warnings)
        self.assertEqual(record["kind"], "A2AAgentCardContract")

    def test_02_stable_contract_identity(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        self.assertEqual(record["spec"]["contract_id"], "a2a-agent-card-contract-v0")
        self.assertEqual(record["spec"]["advisory_contract_ref"], "aide://interop/a2a-agent-card-contract-v0")
        self.assertFalse(record["spec"]["reference_id_kind_supported"])

    def test_03_agent_card_is_preview_only(self) -> None:
        card = a2a_agent_card_contract.build_agent_card()
        self.assertTrue(card["preview_only"])
        self.assertFalse(card["endpoint_implemented"])
        self.assertIsNone(card["url"])

    def test_04_declared_runtime_capabilities_are_false(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        for value in record["spec"]["implemented_runtime_capabilities"].values():
            self.assertFalse(value)

    def test_05_status_runtime_facts_are_false(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        for field in a2a_agent_card_contract.FALSE_RUNTIME_FIELDS:
            self.assertFalse(record["status"][field], field)

    def test_06_live_endpoint_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["live_a2a_endpoint_started"] = True
        self.assertTrue(any("live_a2a_endpoint_started" in item for item in validate_record(record)))

    def test_07_agent_registration_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["agent_registered"] = True
        self.assertTrue(any("agent_registered" in item for item in validate_record(record)))

    def test_08_task_delegation_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["task_delegation_performed"] = True
        self.assertTrue(any("task_delegation_performed" in item for item in validate_record(record)))

    def test_09_authentication_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["security"]["authentication_implemented"] = True
        self.assertTrue(any("authentication_implemented" in item for item in validate_record(record)))

    def test_10_worker_dispatch_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["worker_dispatched"] = True
        self.assertTrue(any("worker_dispatched" in item for item in validate_record(record)))

    def test_11_provider_call_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["model_or_provider_called"] = True
        self.assertTrue(any("model_or_provider_called" in item for item in validate_record(record)))

    def test_12_network_call_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["status"]["network_call_performed"] = True
        self.assertTrue(any("network_call_performed" in item for item in validate_record(record)))

    def test_13_live_url_present_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["agent_card"]["url"] = "https://example.invalid/a2a"
        self.assertTrue(any("url" in item for item in validate_record(record)))

    def test_14_security_schemes_must_be_empty(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["security"]["securitySchemes"] = {"bearer": {"type": "http"}}
        self.assertTrue(any("securitySchemes" in item for item in validate_record(record)))

    def test_15_skill_ids_validate(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        for skill in record["spec"]["skills"]:
            valid, reason = a2a_agent_card_contract.validate_skill_id(skill["id"])
            self.assertTrue(valid, reason)

    def test_16_forbidden_skill_operation_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["skills"][0]["id"] = "aide.task.dispatch"
        self.assertTrue(any("forbidden operation segment" in item for item in validate_record(record)))

    def test_17_duplicate_skill_id_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["skills"][1]["id"] = record["spec"]["skills"][0]["id"]
        self.assertTrue(any("duplicate skill id" in item for item in validate_record(record)))

    def test_18_skill_implemented_true_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["skills"][0]["implemented"] = True
        self.assertTrue(any("implemented must be false" in item for item in validate_record(record)))

    def test_19_unknown_required_capability_fails_closed(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        record["spec"]["required_aide_capabilities"].append("aide.runtime.execute")
        self.assertTrue(any("unknown required AIDE capabilities" in item for item in validate_record(record)))

    def test_20_explicit_non_capabilities_present(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        self.assertEqual(record["spec"]["explicit_non_capabilities"], a2a_agent_card_contract.EXPLICIT_NON_CAPABILITIES)
        self.assertIn("live_a2a_endpoint", record["spec"]["explicit_non_capabilities"])
        self.assertIn("task_delegation", record["spec"]["explicit_non_capabilities"])

    def test_21_static_interop_preview_consistency(self) -> None:
        preview = json.loads((REPO_ROOT / ".aide/interop/exports/a2a-agent-card.preview.json").read_text(encoding="utf-8"))
        card = a2a_agent_card_contract.build_agent_card()
        self.assertTrue(preview["preview_only"])
        self.assertFalse(preview["endpoint_implemented"])
        self.assertFalse(card["endpoint_implemented"])

    def test_22_projection_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            a2a_agent_card_contract.write_a2a_agent_card_contract_reports(root)
            first = (root / a2a_agent_card_contract.AGENT_CARD_CONTRACT_JSON).read_bytes()
            a2a_agent_card_contract.write_a2a_agent_card_contract_reports(root)
            second = (root / a2a_agent_card_contract.AGENT_CARD_CONTRACT_JSON).read_bytes()
        self.assertEqual(first, second)

    def test_23_source_interop_export_artifacts_remain_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            watched = [
                root / ".aide/interop/exports/manifest.json",
                root / ".aide/interop/exports/a2a-agent-card.preview.json",
            ]
            before = {path.as_posix(): path.read_bytes() for path in watched if path.exists()}
            report = a2a_agent_card_contract.write_a2a_agent_card_contract_reports(root)
            after = {path.as_posix(): path.read_bytes() for path in watched if path.exists()}
        self.assertEqual(before, after)
        self.assertFalse(report["source_artifacts_mutated"])

    def test_24_accepted_predecessor_reports_remain_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            watched = [
                root / ".aide/reports/interop-exports-accept/acceptance-report.json",
                root / ".aide/reports/mcp-server-contract-accept/acceptance-report.json",
            ]
            before = {path.as_posix(): path.read_bytes() for path in watched if path.exists()}
            a2a_agent_card_contract.write_a2a_agent_card_contract_reports(root)
            after = {path.as_posix(): path.read_bytes() for path in watched if path.exists()}
        self.assertEqual(before, after)

    def test_25_cli_status_project_validate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            for command in ["status", "project", "validate"]:
                with self.subTest(command=command):
                    exit_code = aide_lite.main(["--repo-root", str(root), "a2a-agent-card-contract", command])
                    self.assertEqual(exit_code, 0)
            report = json.loads((root / a2a_agent_card_contract.VALIDATION_JSON).read_text(encoding="utf-8"))
            self.assertEqual(report["validation_status"], "PASS_WITH_WARNINGS")

    def test_26_unsupported_execution_commands_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            for command in ["start", "serve", "register", "delegate", "send", "connect", "authorize"]:
                with self.subTest(command=command):
                    with self.assertRaises(SystemExit):
                        aide_lite.main(["--repo-root", str(root), "a2a-agent-card-contract", command])

    def test_27_validation_writes_json_reports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            copy_a2a_source_files(root)
            report = a2a_agent_card_contract.validate_a2a_agent_card_contract(root)
            self.assertEqual(report["validation_status"], "PASS_WITH_WARNINGS")
            self.assertTrue((root / a2a_agent_card_contract.ARTIFACT_INDEX_JSON).exists())
            self.assertTrue((root / a2a_agent_card_contract.AGENT_CARD_REPORT_JSON).exists())

    def test_28_mutating_status_combination_fails(self) -> None:
        record = a2a_agent_card_contract.build_a2a_agent_card_contract(REPO_ROOT)
        for field in ["patch_applied", "repository_target_mutated", "github_mutation_performed", "trusted"]:
            with self.subTest(field=field):
                bad = copy.deepcopy(record)
                bad["status"][field] = True
                self.assertTrue(any(field in item for item in validate_record(bad)))


if __name__ == "__main__":
    unittest.main()
