"""Request-bound local foundation. Production transport is deliberately absent."""
from __future__ import annotations

import json
import math
import re
import time
import uuid

from .common import (Refused, OID, fields, identity, require_path, beneath, digest)
from .candidate import read_candidate, verify_changes, materialize
from .ledger import Ledger
from .preparation import directory_lease
from core.runtime.continuous_worker.locking import supervisor_lock


def validate_authority(authority):
    fields(authority, "schema repository target_ref actor base base_tree expires_at max_requests required_checks admission_digest review_digest allowed_paths")
    if authority["schema"] != "aide.broker.authority.v1":
        raise Refused("unknown broker authority")
    if not isinstance(authority["repository"], str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", authority["repository"]):
        raise Refused("invalid repository identity")
    if authority["target_ref"] != "refs/heads/dev":
        raise Refused("only exact dev integration is admitted")
    if not isinstance(authority["actor"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", authority["actor"]):
        raise Refused("explicit integration actor required")
    for field in ("base", "base_tree"):
        identity(authority[field], OID)
    for field in ("admission_digest", "review_digest"):
        identity(authority[field])
    if type(authority["expires_at"]) not in (int, float) or not math.isfinite(authority["expires_at"]):
        raise Refused("finite authority expiry required")
    if type(authority["max_requests"]) is not int or not 1 <= authority["max_requests"] <= 2:
        raise Refused("finite broker transaction limit required")
    checks = authority["required_checks"]
    if not isinstance(checks, list) or not checks or any(not isinstance(c, str) or not c for c in checks) or len(set(checks)) != len(checks):
        raise Refused("explicit unique required checks required")
    from .common import allowed_paths
    allowed_paths(authority["allowed_paths"])


class Broker:
    def __init__(self, root, exchange, repository_root, git, authority, *, transport=None, now=time.time, checkpoint=None):
        # Transport injection is an internal test seam, never a config/CLI plugin.
        validate_authority(authority)
        self.root, self.exchange, self.repository_root = (
            require_path(str(p)) for p in (root, exchange, repository_root))
        roots = (self.root, self.exchange, self.repository_root)
        if any(beneath(a, b) or beneath(b, a) for i, a in enumerate(roots) for b in roots[i + 1:]):
            raise Refused("broker, handoff and repository roots must be separate")
        self.git, self.authority, self.transport, self.now = git, json.loads(json.dumps(authority)), transport, now
        self.ledger = Ledger(self.root)
        self.checkpoint = checkpoint or (lambda phase: None)

    def close(self):
        self.ledger.close()

    def validate_request(self, request):
        fields(request, "schema task authority_digest admission_digest candidate verification")
        if request["schema"] != "aide.broker.request.v1":
            raise Refused("unknown integration request schema")
        if not isinstance(request["task"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}", request["task"]):
            raise Refused("invalid task identifier")
        if request["authority_digest"] != digest(self.authority) or request["admission_digest"] != self.authority["admission_digest"]:
            raise Refused("request authority/admission mismatch")
        manifest, blobs = read_candidate(self.exchange, request["candidate"])
        if any(manifest[k] != self.authority[k] for k in ("repository", "base", "base_tree", "allowed_paths")):
            raise Refused("candidate does not match finite authority")
        verification = request["verification"]
        fields(verification, "coding_session assurance_session assurance_passed subject_tree checks")
        if digest(verification) != self.authority["review_digest"]:
            raise Refused("reviewed evidence digest mismatch")
        for field in ("coding_session", "assurance_session"):
            try:
                if str(uuid.UUID(verification[field])) != verification[field]:
                    raise ValueError()
            except (ValueError, TypeError, AttributeError):
                raise Refused("canonical review session UUID required") from None
        if verification["coding_session"] == verification["assurance_session"] or verification["assurance_passed"] is not True:
            raise Refused("fresh passing assurance required")
        if verification["subject_tree"] != manifest["candidate_tree"]:
            raise Refused("assurance is bound to another candidate")
        checks = verification["checks"]
        if not isinstance(checks, list):
            raise Refused("invalid check evidence")
        names = []
        for check in checks:
            fields(check, "name result artifact_sha256")
            identity(check["artifact_sha256"])
            if check["result"] != "PASS" or not isinstance(check["name"], str):
                raise Refused("required check has not passed")
            names.append(check["name"])
        if len(set(names)) != len(names) or set(names) != set(self.authority["required_checks"]):
            raise Refused("required check set mismatch")
        return manifest, blobs

    def authority_observation(self, frozen):
        """Observe pre-issued protected authority; never manufacture review approval."""
        fields(frozen, "schema task repository base base_tree allowed_paths admission_digest candidate verification")
        if frozen["schema"] != "aide.broker.authority-request.v1":
            raise Refused("unknown frozen authority request")
        if any(frozen[k] != self.authority[k] for k in
               ("repository", "base", "base_tree", "allowed_paths", "admission_digest")):
            raise Refused("frozen request differs from externally issued authority")
        request = {"schema": "aide.broker.request.v1", "task": frozen["task"],
                   "authority_digest": digest(self.authority), "admission_digest": frozen["admission_digest"],
                   "candidate": frozen["candidate"], "verification": frozen["verification"]}
        self.validate_request(request)
        self.guard()
        return {"schema": "aide.broker.authority-observation.v1", "request_digest": digest(frozen),
                "status": "authorized", "authority": self.authority}

    def guard(self):
        if self.now() >= self.authority["expires_at"]:
            raise Refused("integration authority expired")
        target = self.git.run(self.repository_root, "rev-parse", "--verify",
                              self.authority["target_ref"]).decode().strip()
        if target != self.authority["base"]:
            raise Refused("integration target base moved")

    def prepare(self, request):
        # A crash releases the kernel lock. Recovery allocates a fresh generation;
        # old objects remain retained and can never become deletion authority.
        with directory_lease(self.root), supervisor_lock(self.root):
            manifest, blobs = self.validate_request(request)
            self.guard()
            self.git.validate_store(self.repository_root, manifest["base"])
            base_tree, base_files = self.git.tree(self.repository_root, manifest["base"])
            if base_tree != manifest["base_tree"]:
                raise Refused("base tree mismatch")
            verify_changes(manifest, base_files)
            self.ledger.reserve(request, manifest, self.authority)
            key = digest(request)
            self.checkpoint("reserved")
            if self.ledger.get(key)["stage"] == "reserved":
                generation = uuid.uuid4().hex
                self.ledger.allocate_preparation(key, generation)
                self.checkpoint("preparation_intent")
                folder = self.root / generation
                with directory_lease(folder, create=True) as owned:
                    self.checkpoint("directory_created")
                    tree = materialize(self.git, folder, manifest, blobs,
                                       base_repository=self.repository_root)
                    self.checkpoint("materialized")
                    self.guard()
                    self.ledger.prepared(key, tree, generation=generation, directory_identity=owned)
            return self.query(request, observe=False)

    def checked_receipt(self, value, key, manifest):
        fields(value, "schema request_digest repository target_ref actor base candidate_tree integrated_commit integrated_tree required_checks_digest")
        expected = {"schema": "aide.broker.integration-receipt.v1", "request_digest": key,
                    "repository": self.authority["repository"], "target_ref": self.authority["target_ref"],
                    "actor": self.authority["actor"], "base": manifest["base"],
                    "candidate_tree": manifest["candidate_tree"], "integrated_tree": manifest["candidate_tree"],
                    "required_checks_digest": digest(self.authority["required_checks"])}
        if any(value[k] != v for k, v in expected.items()):
            raise Refused("integration receipt does not match exact request")
        identity(value["integrated_commit"], OID)
        return value

    def query(self, request, *, observe=True):
        manifest, _ = self.validate_request(request)
        key = digest(request)
        row = self.ledger.get(key)
        if row and (row["request"] != json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                    or row["manifest"] != json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
                    or row["authority"] != digest(self.authority)):
            raise Refused("durable reservation mismatch")
        if row and row["stage"] == "apply_intent" and observe and self.transport is not None:
            observation = self.transport.observe(request)
            fields(observation, "status receipt")
            if observation["status"] == "integrated":
                receipt = self.checked_receipt(observation["receipt"], key, manifest)
                self.ledger.integrated(key, receipt)
                row = self.ledger.get(key)
            elif observation["status"] not in ("absent", "pending", "refused"):
                raise Refused("invalid integration observation")
            # Absent after intent is still uncertain; never grants replay authority.
        receipt = None
        if row and row["stage"] == "integrated":
            receipt = self.checked_receipt(json.loads(row["receipt"]), key, manifest)
        return {"schema": "aide.broker.observation.v1", "request_digest": key,
                "status": "integrated" if receipt else ("pending" if row else "absent"),
                "stage": row["stage"] if row else "unreserved", "receipt": receipt,
                "receipt_sha256": digest(receipt) if receipt else None}

    def apply(self, request):
        self.validate_request(request)
        if self.transport is None:
            raise Refused("production integration transport is not implemented or qualified")
        existing = self.ledger.get(digest(request))
        if existing and existing["stage"] in ("apply_intent", "integrated"):
            return self.query(request)
        self.prepare(request)
        self.guard()
        if self.ledger.intent(digest(request)):
            # A thrown/lost response leaves the durable intent; apply is never replayed.
            self.transport.apply(request)
        return self.query(request)

    def reconcile(self, request):
        """Re-enter only the broker ledger, never repeat an uncertain transport.

        Reserved/prepared requests can finish local preparation. Durable
        apply_intent requests are observed only by apply's existing guard.
        """
        return self.apply(request)
