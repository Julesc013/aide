"""One amended canonical-custody regression group and owned export refresh."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path.cwd()
TASK = Path(__file__).parent
OUT = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
scratch = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
os.environ["AIDE_RESOURCE_TEST_PARENT"] = str(scratch)
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))

METHODS = (
    "test_canonical_outputs_have_finite_reservations_and_no_fallback",
    "test_changelog_preview_default_needs_budgeted_canonical_custody",
    "test_canonical_volume_is_in_capacity_sampling_and_inspection",
    "test_canonical_junction_refuses_without_touching_target",
    "test_quick_canonical_overrun_fails_and_preserves_source_output",
    "test_source_generators_require_bound_canonical_output_manifests",
    "test_crash_before_final_canonical_check_cannot_recover_as_success",
    "test_crash_recovery_rechecks_canonical_volume_identity",
    "test_stable_output_has_independent_budgeted_custody",
    "test_canonical_ancestor_coverage_never_grants_parent_or_unknown_scope",
    "test_stable_release_commands_accept_only_covering_canonical_custody",
    "test_stable_canonical_junction_refuses_without_touching_target",
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, sort_keys=True, indent=2) + "\n").encode())


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


record = {"state": "started", "export_refreshed": False, "support_claimed": False,
          "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
          "production_assets_created": False, "methods": list(METHODS)}
try:
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    ownership = load("canonical_export_ownership", ROOT / ".aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py")
    prior = json.loads((TASK / "evidence/prior-export-inventory.json").read_bytes())
    save(OUT / "export-before.json", ownership.require_same(prior))
    baseline = json.loads((TASK / "evidence/baseline.json").read_bytes())["stable_assets"]
    assert all(sha(ROOT / name) == digest for name, digest in baseline.items())
    module = load("canonical_workspace_regressions", ROOT / ".aide/scripts/tests/test_managed_workspace.py")
    suite = unittest.TestSuite(module.ManagedWorkspaceTests(name) for name in METHODS)
    with (OUT / "canonical-tests.txt").open("x", encoding="utf-8", newline="\n") as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    observation = {"tests_run": result.testsRun, "passed": result.wasSuccessful(),
                   "failures": [(test.id(), text) for test, text in result.failures],
                   "errors": [(test.id(), text) for test, text in result.errors],
                   "skips": [(test.id(), reason) for test, reason in result.skipped],
                   "stream_sha256": sha(OUT / "canonical-tests.txt")}
    save(OUT / "canonical-tests.json", observation)
    record.update(state="tests_completed", tests=observation)
    save(OUT / "canonical-result.json", record)
    assert result.wasSuccessful() and result.testsRun == 12 and not result.skipped
    assert not subprocess.check_output(["git", "status", "--porcelain"]).strip()
    ownership.require_same(prior)
    old_metadata = OUT / "prior-metadata"
    old_metadata.mkdir()
    for name in sorted(ownership.EXCLUDED):
        (old_metadata / name).write_bytes((ROOT / ownership.PACK_REL / name).read_bytes())
    lite = load("canonical_export_owner", ROOT / ".aide/scripts/aide_lite.py")
    pack, report = lite.build_export_pack(ROOT)
    record.update(state="export_refreshed", export_refreshed=True, export=report)
    save(OUT / "canonical-result.json", record)
    valid, problems = lite.validate_pack_checksums(pack)
    assert valid and not problems and not lite.validate_export_pack_boundary(pack)
    assert (pack / "files/.aide/scripts/aide_lite.py").read_bytes() == lite.portable_cli_text(
        (ROOT / ".aide/scripts/aide_lite.py").read_text(encoding="utf-8")).encode("utf-8")
    assert (pack / "files/core/execution/managed_workspace.py").read_bytes() == (
        ROOT / "core/execution/managed_workspace.py").read_bytes()
    assert all(sha(ROOT / name) == digest for name, digest in baseline.items())
    assert set(p.relative_to(ROOT).as_posix() for p in (ROOT / ".aide/release/stable").iterdir()) == set(baseline)
    members = {p.relative_to(pack).as_posix(): sha(p) for p in sorted(pack.rglob("*")) if p.is_file()}
    save(OUT / "export-after.json", {"source_commit": record["source_head"], "members": members})
    record.update(state="passed", stable_assets_unchanged=len(baseline), export_files=len(members))
except BaseException as error:
    record.update(state="stopped", error_type=type(error).__name__, error=str(error))
    raise
finally:
    save(OUT / "canonical-result.json", record)
print("PASS twelve canonical-custody regressions and one owned export refresh; no production archive")
