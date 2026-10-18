"""Qualify documentation defaults with existing tests, export and preview owners."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path.cwd()
TASK = ROOT / ".aide/queue/AIDE-LITE-SUCCESSOR-PUBLICATION-01"
EVIDENCE = TASK / "evidence"
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"])
MODULES = ["test_q31_export_pack_governance", "test_q34_changelog_release", "test_q48_github_release_draft"]
PAYLOADS = {".aide/policies/release-checklist.yaml", "docs/reference/commit-discipline.md",
            "docs/reference/git-workflow-policy.md"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(name, value):
    (OUTPUT / name).write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def checks(subject, label):
    suite = unittest.TestSuite()
    inputs = {}
    fixture_inputs = {}
    for name in MODULES:
        path = subject / ".aide/scripts/tests" / (name + ".py")
        module = load(label + "_" + name, path)
        if label == "delivered" and name == "test_q31_export_pack_governance":
            carrier = subject.parent / "import-policy.yaml"
            assert carrier.is_file()
            policy = carrier.read_bytes()
            original = module.make_source_repo
            template_path = module.aide_lite.EXPORT_IMPORT_POLICY_TEMPLATE_PATH

            def make_delivered_source(parent):
                fixture = original(parent)
                destination = fixture / template_path
                assert not destination.exists()
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(policy)
                assert destination.read_bytes() == carrier.read_bytes() == policy
                return fixture

            module.make_source_repo = make_delivered_source
            fixture_inputs["pack/import-policy.yaml"] = sha(carrier)
        suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
        inputs[path.relative_to(subject).as_posix()] = sha(path)
    assert suite.countTestCases() == 30
    with (OUTPUT / (label + "-tests.log")).open("w", encoding="utf-8") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    save(label + "-tests.json", {"tests_run": result.testsRun, "failures": len(result.failures),
         "errors": len(result.errors), "skips": len(result.skipped), "inputs": inputs,
         "fixture_inputs": fixture_inputs})
    assert result.testsRun == 30 and result.wasSuccessful() and not result.skipped
    assert all(sha(subject / path) == expected for path, expected in inputs.items())


def main():
    assert os.environ.get("AIDE_JOB_ID")
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    frozen = json.loads((EVIDENCE / "documentation-release-preimages.json").read_bytes())
    assert len(frozen) == 8 and all(sha(ROOT / path) == expected for path, expected in frozen.items())
    checks(ROOT, "source")
    preview = load("release_docs_preview", ROOT / ".aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py")
    preview.BASE = "ecff55da6db49d63c4a3718b726f96d3cd74e6e9"
    sys.argv = [str(TASK / "run_documentation_checks.py"), "generate"]
    preview.main()
    refresh = load("release_docs_export", ROOT / ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/run_refresh.py")
    inventory = EVIDENCE / "documentation-pack-inventory.json"
    before = json.loads(inventory.read_bytes())
    sys.argv = [__file__, "refresh", "--inventory", str(inventory.relative_to(ROOT)),
                "--inventory-sha256", sha(inventory)]
    refresh.main()
    pack = ROOT / refresh.PACK_REL
    after = refresh.inventory_bytes(pack)
    old = {name: row["sha256"] for name, row in before["files"].items()}
    assert set(after) == set(old) and len(after) == 875
    changed = {name for name in old if old[name] != after[name]} - refresh.EXCLUDED
    assert changed == {"files/" + path for path in PAYLOADS}, changed
    for path in PAYLOADS:
        assert (pack / "files" / path).read_bytes() == (ROOT / path).read_bytes()
    checks(pack / "files", "delivered")
    aide = load("release_docs_delivered_cli", pack / "files/.aide/scripts/aide_lite.py")
    q31 = load("release_docs_installed_fixture", ROOT / ".aide/scripts/tests/test_q31_export_pack_governance.py")
    with tempfile.TemporaryDirectory(prefix="release-docs-consumer-") as directory:
        target = Path(directory)
        q31.init_target_git(target)
        manual = {"AGENTS.md": b"Project-owned working rules.\n",
                  "TODO.md": b"Project-owned task checklist.\n",
                  "PLANS.md": b"Project-owned detailed plan.\n",
                  "ROADMAP.md": b"Project-owned direction.\n",
                  "CHANGELOG.md": b"Project-owned release history.\n"}
        for path, content in manual.items():
            (target / path).write_bytes(content)
        plan = aide.apply_import_pack(pack, target, dry_run=True, mode="safe")
        assert not plan["conflicts"]
        applied = aide.apply_import_pack(pack, target, mode="safe", expected_plan_digest=plan["plan_digest"])
        assert applied["status"] == "APPLIED" and not applied["conflicts"]
        receipt = json.loads((target / aide.PORTABLE_IMPORT_RECEIPT_PATH).read_bytes())
        assert not (target / "core").exists()
        for path, content in manual.items():
            assert content in (target / path).read_bytes(), path
        imported = {}
        for path in sorted(PAYLOADS):
            assert (target / path).read_bytes() == (ROOT / path).read_bytes()
            assert receipt["managed"][path]["installed_digest"] == sha(target / path)
            assert receipt["managed"][path]["ownership"] == "aide_portable_managed"
            imported[path] = sha(target / path)
        policy = (target / ".aide/policies/release-checklist.yaml").read_text(encoding="utf-8")
        for token in ["TODO, PLANS, ROADMAP and CHANGELOG", "without duplicated title or manual prose wrapping",
                      "human download labels", "unreconciled pre-tag documentation"]:
            assert token in policy, token
        assert (target / "docs/reference/git-workflow-policy.md").is_file()
        assert (target / ".aide/policies/release-checklist.yaml").is_file()
        guide = (target / "docs/reference/commit-discipline.md").read_text(encoding="utf-8")
        assert "(git-workflow-policy.md)" in guide
        assert "../../governance/release-policy.md" not in guide
        assert "one physical line per logical paragraph or item" in guide
        assert "wrap\nplain prose at 72-100" not in guide
        save("installed-documentation.json", {"status": "PASS", "managed_defaults": imported,
             "project_owned_documents_preserved": sorted(manual), "core_absent": True,
             "scope": "documentation and policy transfer; no automatic tag enforcement or publication"})
    verified = preview.verify()
    assert all(sha(ROOT / path) == expected for path, expected in frozen.items())
    assert refresh.inventory_bytes(pack) == after
    save("documentation-result.json", {"status": "PASS", "source_tests": 30,
         "delivered_tests": 30, "ownership_tests": 6, "pack_members": len(after),
         "changed_payloads": sorted(changed), "pack_sha256s": after,
         "preview": verified, "frozen_release_assets_unchanged": 8,
         "model_requests": 0, "whole_outcome_usage": "unknown"})
    print(json.dumps({"result": "PASS", "source": 30, "delivered": 30, "installed": "PASS",
                      "pack_members": len(after), "preview_head": verified["source_head"]}))


if __name__ == "__main__":
    main()
