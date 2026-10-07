"""Six changed draft-preview regressions; no replay of accepted history tests."""
import json
import os
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".aide/scripts/tests"))
names = ["test_draft_normalization_preserves_content_and_strictly_validates",
         "test_draft_normalization_preserves_fenced_examples",
         "test_draft_normalization_preserves_nonclosing_markers_and_indented_examples",
         "test_draft_preview_emits_exact_valid_message_and_digest",
         "test_draft_preview_does_not_invent_missing_content_or_emit_failed_message",
         "test_draft_preview_never_operates_on_history"]
suite = unittest.defaultTestLoader.loadTestsFromNames(
    ["test_q27_commit_recovery.Q27CommitRecoveryTests." + name for name in names])
result = unittest.TextTestRunner(verbosity=1).run(suite)
summary = {"tests": result.testsRun, "failures": len(result.failures),
           "errors": len(result.errors), "skips": len(result.skipped)}
(Path(os.environ["AIDE_JOB_OUTPUT"]) / "draft-result.json").write_bytes(
    (json.dumps(summary, sort_keys=True) + "\n").encode())
print(json.dumps(summary, sort_keys=True))
sys.exit(0 if result.wasSuccessful() and not result.skipped else 1)
