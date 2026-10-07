"""Affected regression qualification in the existing bounded managed job."""
import contextlib, hashlib, importlib.util, io, json, os, sys, unittest
from pathlib import Path
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / ".aide/scripts/tests"))
import test_q27_commit_recovery as q27
import test_q34_changelog_release as q34
import test_efficiency_wait as wait_tests
from types import SimpleNamespace
lite = q27.aide_lite
class PublicGitFixture:
 def __init__(self, *args, **kwargs):
  if args or set(kwargs) - {"prefix", "dir"}: raise ValueError("unsupported public fixture arguments")
  if kwargs.get("dir") and Path(kwargs["dir"]).resolve() != Path(os.environ["AIDE_JOB_TMP"]).resolve():
   raise ValueError("public fixture parent differs from admitted temp")
  self.context = lite.public_archive_fixture("aide-public-release-test-")
  self.name = self.context.__enter__()
  self.closed = False
 def __enter__(self): return self.name
 def __exit__(self, *exc): self.cleanup()
 def cleanup(self):
  if not self.closed:
   self.closed = True
   self.context.__exit__(None, None, None)
# Module-local factories only. No assertions or global tempfile behavior change.
q27.tempfile = SimpleNamespace(TemporaryDirectory=PublicGitFixture)
q34.tempfile = SimpleNamespace(TemporaryDirectory=PublicGitFixture)
wait_tests.tempfile = SimpleNamespace(TemporaryDirectory=PublicGitFixture)
selected = [
 "test_q27_commit_recovery", "test_q34_changelog_release",
 "test_managed_workspace.ManagedWorkspaceTests.test_codex_adapter_uses_existing_owner_with_bound_ephemeral_readonly_turn",
 "test_managed_workspace.ManagedWorkspaceTests.test_codex_model_permission_and_turn_budget_refuse_before_allocation",
 "test_managed_workspace.ManagedWorkspaceTests.test_codex_paid_routes_and_override_fields_refuse_without_fallback",
 "test_managed_workspace.ManagedWorkspaceTests.test_codex_unchanged_request_refuses_before_second_allocation",
 "test_managed_workspace.ManagedWorkspaceTests.test_codex_failed_host_retains_request_identity_before_retry",
 "test_managed_workspace.ManagedWorkspaceTests.test_paused_dispatch_refuses_before_allocation_and_is_durable",
 "test_efficiency_wait.EfficiencyWaitTests.test_terminal_is_bounded_repeatable_and_read_only",
 "test_efficiency_wait.EfficiencyWaitTests.test_unchanged_wait_emits_only_terminal_view",
]
suite = unittest.defaultTestLoader.loadTestsFromNames(selected)
result = unittest.TextTestRunner(verbosity=1).run(suite)
packet_path = REPO / ".aide/queue/AIDE-STABLE-LITE-RELEASE-EFFECT-01/evidence/historical-current-proposed-registry.json"
packet = json.loads(packet_path.read_text(encoding="utf-8-sig"))
records = []
for record in packet["records"]:
 oid = record["commit"]
 items = lite.git_commit_messages_for_range(REPO, oid + "^.." + oid)
 found = [item for item in items if item[0] == oid]
 assert len(found) == 1
 message = found[0][2]
 checks = lite.validate_commit_message_text(message)
 assert lite.canonical_commit_message_sha256(message) == record["message_sha256"]
 assert [c.message for c in checks if c.severity == "FAIL"] == record["failed_checks"]
 assert lite.historical_message_is_presentation_only(message, checks), oid
 assert lite.commit_is_within_historical_boundary(REPO, oid, lite.historical_presentation_boundary(REPO)), oid
 view = io.StringIO()
 with contextlib.redirect_stdout(view):
  code = lite.main(["commit", "check", "--range", oid + "^.." + oid])
 assert code == 0 and ("- " + oid[:7] + " PRESENTATION_ADVISORY") in view.getvalue(), view.getvalue()
 records.append({"commit": oid, "tree": record["tree"], "parents": record["parents"],
                 "message_sha256": record["message_sha256"], "original_failed_checks": record["failed_checks"],
                 "classification": "PRESENTATION_ADVISORY", "strict_result": "FAIL"})
summary = {"schema": "aide.reasonable-automation-qualification.v1", "test_count": result.testsRun,
           "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
           "historical_records": records, "individual_owner_decisions_created": 0,
           "packet_sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
           "history_rewritten": False, "model_requests": 0,
           "evidence_semantics": "message syntax only; substantive evidence remains independently required"}
output = Path(os.environ["AIDE_JOB_OUTPUT"]) / "qualification.json"
output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"test_count": result.testsRun, "successful": result.wasSuccessful(), "historical_advisories": len(records), "summary": str(output)}))
sys.exit(0 if result.wasSuccessful() and not result.skipped else 1)
