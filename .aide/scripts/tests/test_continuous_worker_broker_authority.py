"""Finite issuer refusal/replay tests over the existing real-artifact pipeline fixture."""
import copy
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import unittest

import test_continuous_worker_pipeline as pipeline
from core.runtime.integration_broker.authority import Issuer
from core.runtime.integration_broker.common import Refused, digest


class SyntheticQualification:
    """Only a test call-count/refusal seam; never a host qualification receipt."""
    def __init__(self, refuse=False):
        self.calls = 0
        self.refuse = refuse

    def assert_current(self, delegation, activation):
        self.calls += 1
        if self.refuse:
            raise Refused("synthetic host qualification refuses")


class IssuerTests(unittest.TestCase):
    setUp = pipeline.V1PipelineTests.setUp
    tearDown = pipeline.V1PipelineTests.tearDown
    git_run = pipeline.V1PipelineTests.git_run
    write_config = pipeline.V1PipelineTests.write_config
    make_config = pipeline.V1PipelineTests.make_config
    runner = pipeline.V1PipelineTests.runner
    capsule_fixture = pipeline.V1PipelineTests.capsule_fixture

    def delegation(self):
        self.issuer_root = self.root / "issuer"
        self.issuer_root.mkdir(exist_ok=True)
        # The fixture's registered config path is owned by its existing helper.
        activation = self.path
        value = {"schema": "aide.broker.delegation.v1", "repository": self.config["tasks"][0]["repository"],
                 "target_ref": "refs/heads/dev", "actor": "fixture-issuer",
                 "expires_at": self.config["expires_at"], "max_requests": 2,
                 "task_ids": [self.config["tasks"][0]["id"]],
                 "activation": {"path": str(activation), "sha256": hashlib.sha256(activation.read_bytes()).hexdigest()},
                 "broker_root": str(self.issuer_root), "repository_root": str(self.root / "trusted-one")}
        path = self.root / "delegation.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    def test_unqualified_issuer_refuses_before_creating_ledger(self):
        path, pin = self.delegation()
        with self.assertRaisesRegex(Refused, "not implemented or qualified"):
            Issuer(path, pin).issue({})
        self.assertFalse((self.issuer_root / "issuer.sqlite3").exists())

    def test_exact_evidence_issues_once_and_restart_returns_same_authority(self):
        runner, attempt, evidence, frozen, capsule = self.capsule_fixture()
        path, pin = self.delegation()
        qualification = SyntheticQualification()
        first = Issuer(path, pin, qualification=qualification).issue(frozen)
        second = Issuer(path, pin, qualification=qualification).issue(frozen)
        self.assertEqual(first, second)
        self.assertEqual(first["authority"]["review_digest"], digest(frozen["verification"]))
        self.assertEqual(qualification.calls, 4)
        with closing(sqlite3.connect(self.issuer_root / "issuer.sqlite3")) as connection:
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM issuances").fetchone()[0], 1)
        self.assertEqual(runner.state.active()["stage"], "integration_pending")

    def test_changed_external_delegation_pin_refuses(self):
        path, pin = self.delegation()
        value = json.loads(path.read_text())
        value["max_requests"] = 200
        path.write_text(json.dumps(value))
        with self.assertRaisesRegex(Refused, "bytes changed"):
            Issuer(path, pin)
        with self.assertRaisesRegex(Refused, "finite bounds"):
            Issuer(path, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_qualification_refusal_and_wrong_task_cannot_reserve(self):
        runner, attempt, evidence, frozen, capsule = self.capsule_fixture()
        path, pin = self.delegation()
        with self.assertRaisesRegex(Refused, "qualification refuses"):
            Issuer(path, pin, qualification=SyntheticQualification(refuse=True)).issue(frozen)
        wrong = copy.deepcopy(frozen)
        wrong["task"] = "unadmitted-task"
        with self.assertRaisesRegex(Refused, "outside finite"):
            Issuer(path, pin, qualification=SyntheticQualification()).issue(wrong)
        self.assertFalse((self.issuer_root / "issuer.sqlite3").exists())

    def test_capsule_actual_output_drift_prevents_issuance(self):
        runner, attempt, evidence, frozen, capsule = self.capsule_fixture()
        record = json.loads(capsule.read_text())
        (Path(record["effects"]["assurance"]["request"]["output"]) / "stdout").write_text("forged verdict")
        path, pin = self.delegation()
        with self.assertRaisesRegex(Refused, "artifact drift"):
            Issuer(path, pin, qualification=SyntheticQualification()).issue(frozen)
        self.assertFalse((self.issuer_root / "issuer.sqlite3").exists())


if __name__ == "__main__":
    unittest.main()
