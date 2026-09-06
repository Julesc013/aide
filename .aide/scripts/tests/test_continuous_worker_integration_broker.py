"""Real disposable Git handoffs and durable broker failure/recovery boundaries."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile
import threading
import unittest
import uuid
import sys

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.runtime.integration_broker.common import Refused, Git, digest, canonical, relative, MAX_FILE, parse_json
from core.runtime.integration_broker.candidate import freeze_candidate, read_candidate, tree_oid, validate_manifest, literal_checkout
from core.runtime.integration_broker.service import Broker, validate_authority
from core.runtime.integration_broker.ledger import Ledger


class ObservedTransport:
    """Internal fixture: no remote GitHub implementation is implied."""
    def __init__(self, fixture):
        self.fixture = fixture
        self.calls = 0
        self.lost_reply = False
        self.seen = False
        self.override = None

    def apply(self, request):
        self.calls += 1
        self.seen = True
        if self.lost_reply:
            raise OSError("lost response after fixture acceptance")

    def observe(self, request):
        if self.override is not None:
            return self.override
        if not self.seen:
            return {"status": "absent", "receipt": None}
        authority = self.fixture.authority
        receipt = {"schema": "aide.broker.integration-receipt.v1", "request_digest": digest(request),
                   "repository": authority["repository"], "target_ref": authority["target_ref"],
                   "actor": authority["actor"], "base": authority["base"],
                   "candidate_tree": self.fixture.manifest["candidate_tree"],
                   "integrated_commit": "f" * 40, "integrated_tree": self.fixture.manifest["candidate_tree"],
                   "required_checks_digest": digest(authority["required_checks"])}
        return {"status": "integrated", "receipt": receipt}


@unittest.skipUnless(os.name == "nt" and shutil.which("git"), "requires bounded Windows Git host")
class BrokerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="aide-broker-fixture-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo, self.exchange, self.state = [self.root / n for n in ("repo", "exchange", "state")]
        self.repo.mkdir()
        self.exchange.mkdir()
        exe = Path(shutil.which("git"))
        self.git = Git(exe, hashlib.sha256(exe.read_bytes()).hexdigest())
        self.git.run(self.repo, "init")
        self.git.run(self.repo, "config", "user.name", "Broker fixture")
        self.git.run(self.repo, "config", "user.email", "fixture@example.invalid")
        (self.repo / "src").mkdir()
        (self.repo / ".github").mkdir()
        (self.repo / ".github" / "guard").write_text("unchanged")
        (self.repo / "src" / "a.txt").write_bytes(b"old\n")
        (self.repo / "src" / "remove.bin").write_bytes(b"remove\0")
        self.git.run(self.repo, "add", ".")
        self.git.run(self.repo, "update-index", "--chmod=+x", "src/a.txt")
        self.git.run(self.repo, "commit", "-m", "fixture base")
        self.base = self.git.run(self.repo, "rev-parse", "HEAD").decode().strip()
        self.git.run(self.repo, "update-ref", "refs/heads/dev", self.base)
        self.checkout = literal_checkout(self.git, self.repo, self.base)
        (self.repo / "src" / "a.txt").write_bytes(b"changed\n")
        (self.repo / "src" / "new.bin").write_bytes(b"new\0\xff\x01")
        (self.repo / "src" / "remove.bin").unlink()
        self.ref = freeze_candidate(self.git, self.repo, self.exchange,
                                    repository="fixture/repo", base=self.base, allowed=["src"], checkout=self.checkout)
        self.manifest, _ = read_candidate(self.exchange, self.ref)
        verification = {"coding_session": str(uuid.uuid4()), "assurance_session": str(uuid.uuid4()),
                        "assurance_passed": True, "subject_tree": self.manifest["candidate_tree"],
                        "checks": [{"name": "unit", "result": "PASS", "artifact_sha256": "a" * 64}]}
        self.authority = {"schema": "aide.broker.authority.v1", "repository": "fixture/repo",
                          "target_ref": "refs/heads/dev", "actor": "fixture-broker",
                          "base": self.base, "base_tree": self.manifest["base_tree"],
                          "expires_at": 2000, "max_requests": 2, "required_checks": ["unit"],
                          "admission_digest": "b" * 64, "review_digest": digest(verification),
                          "allowed_paths": ["src"]}
        self.request = {"schema": "aide.broker.request.v1", "task": "BROKER-FIXTURE-01",
                        "authority_digest": digest(self.authority), "admission_digest": "b" * 64,
                        "candidate": self.ref, "verification": verification}
        self.transport = ObservedTransport(self)

    def broker(self, transport=None, now=1000):
        broker = Broker(self.state, self.exchange, self.repo, self.git, self.authority,
                        transport=transport, now=lambda: now)
        self.addCleanup(broker.close)
        return broker

    def test_binary_untracked_delete_and_tree_round_trip(self):
        broker = self.broker()
        result = broker.prepare(self.request)
        self.assertEqual(result["stage"], "prepared")
        candidate = self.state / broker.ledger.preparation(digest(self.request))["generation"]
        tree = self.git.run(candidate, "write-tree").decode().strip()
        self.assertEqual(tree, self.manifest["candidate_tree"])
        self.assertEqual(self.manifest["files"]["src/a.txt"]["mode"], "100755")
        names = self.git.run(candidate, "ls-tree", "-r", "--name-only", tree).decode().splitlines()
        self.assertIn("src/new.bin", names)
        self.assertNotIn("src/remove.bin", names)
        self.assertEqual(self.git.run(candidate, "show", tree + ":src/new.bin"), b"new\0\xff\x01")

    def test_handoff_no_longer_reads_mutable_worker_bytes(self):
        (self.repo / "src" / "new.bin").write_bytes(b"changed after frozen handoff")
        result = self.broker().prepare(self.request)
        self.assertEqual(result["stage"], "prepared")
        self.assertEqual(read_candidate(self.exchange, self.ref)[1][self.manifest["files"]["src/new.bin"]["sha256"]],
                         b"new\0\xff\x01")

    def test_absent_query_does_not_reserve_and_production_apply_refuses(self):
        broker = self.broker()
        self.assertEqual(broker.query(self.request)["status"], "absent")
        with self.assertRaisesRegex(Refused, "transport"):
            broker.apply(self.request)
        self.assertEqual(broker.ledger.db.execute("SELECT COUNT(*) FROM requests").fetchone()[0], 0)

    def test_corrupt_blob_refuses_before_reservation(self):
        entry = self.manifest["files"]["src/new.bin"]
        (self.exchange / self.ref["bundle"] / "blobs" / entry["sha256"]).write_bytes(b"foreign")
        broker = self.broker(self.transport)
        with self.assertRaisesRegex(Refused, "blob changed"):
            broker.apply(self.request)
        self.assertEqual(self.transport.calls, 0)
        self.assertIsNone(broker.ledger.get(digest(self.request)))

    def test_manifest_drift_and_unregistered_bundle_refuse(self):
        broker = self.broker()
        for ref in ({**self.ref, "bundle": "../repo"}, {**self.ref, "manifest_sha256": "c" * 64}):
            with self.subTest(ref=ref), self.assertRaises(Refused):
                broker.prepare({**self.request, "candidate": ref})

    def test_changed_authority_and_review_refuse(self):
        broker = self.broker(self.transport)
        for key in ("authority_digest", "admission_digest"):
            with self.subTest(key=key), self.assertRaises(Refused):
                broker.apply({**self.request, key: "c" * 64})
        changed = copy.deepcopy(self.request)
        changed["verification"]["checks"][0]["result"] = "FAIL"
        with self.assertRaisesRegex(Refused, "evidence digest"):
            broker.apply(changed)
        self.assertEqual(self.transport.calls, 0)

    def test_moved_base_refuses_before_intent(self):
        self.git.run(self.repo, "add", ".")
        self.git.run(self.repo, "commit", "-m", "moved target")
        new = self.git.run(self.repo, "rev-parse", "HEAD").decode().strip()
        self.git.run(self.repo, "update-ref", "refs/heads/dev", new)
        with self.assertRaisesRegex(Refused, "base moved"):
            self.broker(self.transport).apply(self.request)
        self.assertEqual(self.transport.calls, 0)

    def test_expiry_refuses_mutation_but_allows_lost_result_observation(self):
        broker = self.broker(self.transport)
        broker.prepare(self.request)
        broker.ledger.intent(digest(self.request))
        self.transport.seen = True
        broker.now = lambda: 2001
        self.assertEqual(broker.apply(self.request)["status"], "integrated")
        self.assertEqual(self.transport.calls, 0)
        other = {**self.request, "task": "NEW"}
        with self.assertRaisesRegex(Refused, "expired"):
            broker.apply(other)

    def test_lost_reply_restart_queries_without_repeated_apply(self):
        broker = self.broker(self.transport)
        self.transport.lost_reply = True
        with self.assertRaises(OSError):
            broker.apply(self.request)
        self.assertEqual(broker.ledger.get(digest(self.request))["stage"], "apply_intent")
        broker.close()
        resumed = self.broker(self.transport)
        result = resumed.apply(self.request)
        self.assertEqual(result["status"], "integrated")
        self.assertEqual(result["receipt_sha256"], digest(result["receipt"]))
        self.assertEqual(self.transport.calls, 1)
        self.assertEqual(resumed.apply(self.request), result)

    def test_absent_after_intent_never_authorizes_replay(self):
        broker = self.broker(self.transport)
        broker.prepare(self.request)
        broker.ledger.intent(digest(self.request))
        for _ in range(2):
            self.assertEqual(broker.apply(self.request)["status"], "pending")
        self.assertEqual(self.transport.calls, 0)

    def test_failed_intent_write_never_dispatches(self):
        broker = self.broker(self.transport)
        broker.prepare(self.request)
        broker.ledger.db.execute("CREATE TRIGGER refuse_intent BEFORE UPDATE ON requests BEGIN SELECT RAISE(ABORT,'disk refusal'); END")
        with self.assertRaises(sqlite3.DatabaseError):
            broker.apply(self.request)
        self.assertEqual(self.transport.calls, 0)

    def test_partial_preparation_retains_writer_and_refuses_another_request(self):
        broker = self.broker()
        broker.ledger.reserve(self.request, self.manifest, self.authority)
        self.assertEqual(broker.prepare(self.request)["stage"], "prepared")
        other = {**self.request, "task": "ANOTHER"}
        with self.assertRaisesRegex(Refused, "reserved"):
            broker.prepare(other)
        self.assertEqual(broker.query(self.request)["status"], "pending")

    def test_small_delta_on_base_above_full_snapshot_limit(self):
        # Trusted unchanged objects do not consume the changed-file budget.
        extra = self.repo / "unchanged"
        extra.mkdir()
        for i in range(4100):
            (extra / (str(i) + ".txt")).write_bytes(b"base object\n")
        (self.repo / "src" / "a.txt").write_bytes(b"old\n")
        (self.repo / "src" / "remove.bin").write_bytes(b"remove\0")
        (self.repo / "src" / "new.bin").unlink()
        self.git.run(self.repo, "add", "unchanged")
        self.git.run(self.repo, "commit", "-m", "large trusted base")
        base = self.git.run(self.repo, "rev-parse", "HEAD").decode().strip()
        checkout = literal_checkout(self.git, self.repo, base)
        (self.repo / "src" / "a.txt").write_bytes(b"changed\n")
        (self.repo / "src" / "remove.bin").unlink()
        (self.repo / "src" / "new.bin").write_bytes(b"new\0\xff\x01")
        ref = freeze_candidate(self.git, self.repo, self.exchange, repository="fixture/repo", base=base, allowed=["src"], checkout=checkout)
        manifest, blobs = read_candidate(self.exchange, ref)
        self.assertEqual(manifest["schema"], "aide.broker.candidate.v2")
        self.assertEqual(set(manifest["files"]), {"src/a.txt", "src/new.bin", "src/remove.bin"})
        self.assertIsNone(manifest["files"]["src/remove.bin"])
        self.assertEqual(len(blobs), 2)
        from core.runtime.integration_broker.candidate import materialize
        directory = self.root / "large-materialized"
        directory.mkdir()
        tree = materialize(self.git, directory, manifest, blobs, base_repository=self.repo)
        self.assertEqual(tree, manifest["candidate_tree"])
        self.assertEqual(self.git.run(directory, "show", tree + ":unchanged/4099.txt"), b"base object\n")

    def test_literal_checkout_refuses_crlf_transform_without_running_filters(self):
        (self.repo / "src" / "a.txt").write_bytes(b"old\r\n")
        (self.repo / "src" / "remove.bin").write_bytes(b"remove\0")
        with self.assertRaisesRegex(Refused, "literal Git blob bytes"):
            literal_checkout(self.git, self.repo, self.base)
        (self.repo / "src" / "a.txt").write_bytes(b"old\n")
        self.assertEqual(literal_checkout(self.git, self.repo, self.base), self.checkout)
        with self.assertRaisesRegex(Refused, "pre-coding"):
            freeze_candidate(self.git, self.repo, self.exchange, repository="fixture/repo", base=self.base,
                             allowed=["src"], checkout={})

    def test_corrupt_or_missing_unchanged_object_refuses_before_reservation(self):
        import zlib
        _, files = self.git.tree(self.repo, self.base)
        oid = files[".github/guard"]["oid"]
        obj = self.repo / ".git" / "objects" / oid[:2] / oid[2:]
        original = obj.read_bytes()
        broker = self.broker()
        for corrupt in (True, False):
            with self.subTest(corrupt=corrupt):
                obj.chmod(0o600)
                if corrupt:
                    obj.write_bytes(zlib.compress(b"blob 7\0corrupt"))
                else:
                    obj.unlink()
                with self.assertRaises(Refused):
                    broker.prepare(self.request)
                self.assertIsNone(broker.ledger.get(digest(self.request)))
                obj.write_bytes(original)

    def test_transitive_alternate_and_promisor_configuration_refuse(self):
        broker = self.broker()
        alternate = self.repo / ".git" / "objects" / "info" / "alternates"
        alternate.write_text(str(self.repo / ".git" / "objects") + "\n")
        with self.assertRaisesRegex(Refused, "alternate"):
            broker.prepare(self.request)
        alternate.unlink()
        self.git.run(self.repo, "config", "remote.fixture.promisor", "true")
        with self.assertRaisesRegex(Refused, "promisor"):
            broker.prepare(self.request)
        self.assertIsNone(broker.ledger.get(digest(self.request)))

    def test_delta_rejects_unchanged_path_tampering_and_redundant_deletion(self):
        from core.runtime.integration_broker.candidate import verify_changes
        base_tree, base = self.git.tree(self.repo, self.base)
        changed = copy.deepcopy(self.manifest)
        changed["files"]["missing.txt"] = None
        with self.assertRaisesRegex(Refused, "redundant"):
            verify_changes(changed, base)
        changed = copy.deepcopy(self.manifest)
        changed["candidate_tree"] = base_tree
        with self.assertRaisesRegex(Refused, "overlay tree"):
            verify_changes(changed, base)

    def test_directory_lease_refuses_substitution_and_retains_failed_generation(self):
        broker = self.broker()
        seen = []
        def checkpoint(phase):
            if phase == "directory_created":
                folder = self.state / broker.ledger.preparation(digest(self.request))["generation"]
                with self.assertRaises(OSError):
                    folder.rename(self.state / "foreign")
                seen.append(folder)
                raise OSError("stop at owned directory")
        broker.checkpoint = checkpoint
        with self.assertRaises(OSError):
            broker.prepare(self.request)
        broker.checkpoint = lambda phase: None
        self.assertEqual(broker.prepare(self.request)["stage"], "prepared")
        self.assertTrue(seen[0].is_dir())
        self.assertNotEqual(seen[0].name, broker.ledger.preparation(digest(self.request))["generation"])

    def test_real_process_death_recovers_fresh_generation_without_cleanup(self):
        config = self.root / "fixture.json"
        config.write_text(json.dumps({"authority": self.authority, "request": self.request}))
        code = """import sys,json,os,hashlib; from pathlib import Path
from core.runtime.integration_broker.service import Broker
from core.runtime.integration_broker.common import Git
root=Path(sys.argv[1]); exe=Path(sys.argv[2]); cfg=json.loads((root/'fixture.json').read_text())
b=Broker(root/'state',root/'exchange',root/'repo',Git(exe,hashlib.sha256(exe.read_bytes()).hexdigest()),cfg['authority'],now=lambda:1000,checkpoint=lambda phase: os._exit(79) if phase==sys.argv[3] else None)
b.prepare(cfg['request'])
"""
        # Each case has its own ledger and does not consume another case's budget.
        for phase in ("reserved", "preparation_intent", "directory_created", "materialized"):
            with self.subTest(phase=phase):
                self.state = self.root / ("state-" + phase)
                phase_code = code.replace("root/'state'", "root/" + repr(self.state.name))
                child = subprocess.run([sys.executable, "-B", "-c", phase_code, str(self.root), str(self.git.executable), phase],cwd=ROOT,timeout=60,capture_output=True)
                self.assertEqual(child.returncode,79,child.stderr)
                broker = self.broker()
                old = broker.ledger.preparation(digest(self.request))
                self.assertEqual(broker.prepare(self.request)["stage"], "prepared")
                if old and phase in ("directory_created", "materialized"):
                    self.assertTrue((self.state / old["generation"]).is_dir())
                    self.assertNotEqual(old["generation"], broker.ledger.preparation(digest(self.request))["generation"])

    def test_preparation_generation_budget_and_failed_intent_precede_effects(self):
        broker = self.broker()
        broker.checkpoint = lambda phase: (_ for _ in ()).throw(OSError("interrupted")) if phase == "preparation_intent" else None
        for _ in range(3):
            with self.assertRaises(OSError):
                broker.prepare(self.request)
        with self.assertRaisesRegex(Refused, "generation budget"):
            broker.prepare(self.request)
        self.assertEqual([p for p in self.state.iterdir() if p.is_dir()], [])


    def test_conflicting_or_corrupt_integration_receipt_refuses(self):
        broker = self.broker(self.transport)
        broker.prepare(self.request)
        broker.ledger.intent(digest(self.request))
        self.transport.seen = True
        good = self.transport.observe(self.request)
        for field in ("request_digest", "integrated_tree", "actor", "target_ref"):
            broken = copy.deepcopy(good)
            broken["receipt"][field] = "wrong"
            self.transport.override = broken
            with self.subTest(field=field), self.assertRaises(Refused):
                broker.query(self.request)
        self.transport.override = good
        broker.query(self.request)
        broker.ledger.db.execute("UPDATE requests SET receipt='null'")
        with self.assertRaises(Refused):
            broker.query(self.request)

    def test_concurrent_reservation_and_intent_have_one_winner(self):
        def race(call):
            barrier = threading.Barrier(2)
            results = []
            def worker():
                ledger = Ledger(self.state)
                try:
                    barrier.wait(timeout=10)
                    results.append(call(ledger))
                finally:
                    ledger.close()
            threads = [threading.Thread(target=worker) for _ in range(2)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(15)
                self.assertFalse(thread.is_alive())
            self.assertEqual(sorted(results), [False, True])
        Ledger(self.state).close()
        race(lambda ledger: ledger.reserve(self.request, self.manifest, self.authority))
        broker = self.broker()
        broker.ledger.prepared(digest(self.request), self.manifest["candidate_tree"])
        race(lambda ledger: ledger.intent(digest(self.request)))

    def test_process_death_after_durable_intent_keeps_replay_blocked(self):
        broker = self.broker(self.transport)
        broker.prepare(self.request)
        code = "from pathlib import Path; from core.runtime.integration_broker.ledger import Ledger; import os,sys; store=Ledger(Path(sys.argv[1])); assert store.intent(sys.argv[2]); os._exit(77)"
        child = subprocess.run([sys.executable, "-B", "-c", code, str(self.state), digest(self.request)],
                               cwd=ROOT, timeout=15, capture_output=True)
        self.assertEqual(child.returncode, 77, child.stderr)
        broker.close()
        resumed = self.broker(self.transport)
        self.assertEqual(resumed.apply(self.request)["stage"], "apply_intent")
        self.assertEqual(self.transport.calls, 0)

    def test_staged_index_changes_are_not_silently_reinterpreted(self):
        self.git.run(self.repo, "add", "src/a.txt")
        with self.assertRaisesRegex(Refused, "index differs"):
            freeze_candidate(self.git, self.repo, self.exchange, repository="fixture/repo",
                             base=self.base, allowed=["src"], checkout=self.checkout)

    def test_transaction_budget_includes_completed_requests(self):
        broker = self.broker(self.transport)
        for task in ("FIRST", "SECOND"):
            self.assertEqual(broker.apply({**self.request, "task": task})["status"], "integrated")
        with self.assertRaisesRegex(Refused, "transaction budget"):
            broker.apply({**self.request, "task": "THIRD"})
        self.assertEqual(self.transport.calls, 2)

    def test_linked_blob_is_refused_even_with_matching_bytes(self):
        entry = self.manifest["files"]["src/new.bin"]
        blob = self.exchange / self.ref["bundle"] / "blobs" / entry["sha256"]
        original = self.root / "original-blob"
        blob.rename(original)
        try:
            blob.symlink_to(original)
        except OSError as exc:
            self.skipTest("host does not permit disposable symlink creation: " + str(exc))
        with self.assertRaisesRegex(Refused, "symlink"):
            self.broker(self.transport).apply(self.request)
        self.assertEqual(self.transport.calls, 0)

    def test_finite_authority_refs_and_checks_are_strict(self):
        for field, value in (("target_ref", "refs/heads/main"), ("target_ref", "dev;evil"),
                             ("max_requests", 3), ("max_requests", True), ("expires_at", float("nan")),
                             ("required_checks", ["unit", "unit"]), ("actor", "")):
            with self.subTest(field=field, value=value), self.assertRaises(Refused):
                validate_authority({**self.authority, field: value})

    def test_protected_path_changes_cannot_be_frozen(self):
        (self.repo / ".github" / "guard").write_text("tamper")
        with self.assertRaisesRegex(Refused, "escaped allowed"):
            freeze_candidate(self.git, self.repo, self.exchange, repository="fixture/repo",
                             base=self.base, allowed=["src"], checkout=self.checkout)


class ContractTests(unittest.TestCase):
    def test_duplicate_json_fields_fail_closed(self):
        with self.assertRaisesRegex(Refused, "duplicate JSON"):
            parse_json(b'{"key":1,"key":2}')

    def test_path_and_ref_admission(self):
        for path in ("../a", "/a", "a\\b", "a:ads", "a/CON.txt", "a./b", ".git/config", "a//b"):
            with self.subTest(path=path), self.assertRaises(Refused):
                relative(path)

    def test_case_collisions_and_budgets(self):
        entry = {"mode": "100644", "oid": "1" * 40, "sha256": "2" * 64, "size": 0}
        for files in ({"a": entry, "A": entry}, {"a/file": entry, "A/other": entry},
                      {"a": {**entry, "size": MAX_FILE + 1}}):
            manifest = {"schema": "aide.broker.candidate.v1", "repository": "fixture/repo",
                        "base": "1" * 40, "base_tree": "2" * 40, "candidate_tree": "3" * 40,
                        "allowed_paths": ["src"], "files": files}
            with self.subTest(files=files), self.assertRaises(Refused):
                validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
