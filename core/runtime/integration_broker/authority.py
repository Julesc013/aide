"""Finite delegated issuance from externally protected controller observations."""
from pathlib import Path
import json
import math
import sqlite3
import time

from . import capsule
from .common import Refused, fields, identity, digest, canonical, object_json, require_path, bounded_bytes
from .service import validate_authority
from .preparation import directory_lease
from core.runtime.continuous_worker.contract import file_hash, read_activation
from core.runtime.continuous_worker.locking import supervisor_lock


def read_delegation(path, approved_sha256):
    """The approval pin is supplied by the external operator, never the worker."""
    path = require_path(str(path))
    identity(approved_sha256)
    if file_hash(path) != approved_sha256:
        raise Refused("external delegation bytes changed")
    value = object_json(path)
    fields(value, "schema repository target_ref actor expires_at max_requests task_ids activation broker_root repository_root")
    if value["schema"] != "aide.broker.delegation.v1":
        raise Refused("unknown external delegation schema")
    fields(value["activation"], "path sha256")
    identity(value["activation"]["sha256"])
    if (type(value["expires_at"]) not in (int, float) or not math.isfinite(value["expires_at"]) or
            type(value["max_requests"]) is not int or not 1 <= value["max_requests"] <= 2):
        raise Refused("external delegation requires finite bounds")
    tasks = value["task_ids"]
    if (not isinstance(tasks, list) or not 1 <= len(tasks) <= 2 or
            any(not isinstance(task, str) or not task for task in tasks) or len(set(tasks)) != len(tasks)):
        raise Refused("external delegation needs a unique finite task set")
    for name in ("broker_root", "repository_root"):
        require_path(value[name])
    return value


class Issuer:
    """Source implementation with a closed operational host seam.

    Only a separately implemented qualified controller/store host can supply
    qualification.assert_current(). There is no config-loaded plugin or CLI
    shortcut, and absent qualification refuses issuance before ledger effects.
    Fixture implementations are not proof of an operational host boundary.
    """
    def __init__(self, delegation_path, approved_sha256, *, qualification=None, now=time.time):
        self.path, self.pin = require_path(str(delegation_path)), approved_sha256
        self.delegation = read_delegation(self.path, self.pin)
        self.qualification, self.now = qualification, now

    def issue(self, frozen):
        delegation = read_delegation(self.path, self.pin)
        if delegation != self.delegation:
            raise Refused("external delegation identity changed")
        if self.qualification is None:
            raise Refused("protected controller/store host is not implemented or qualified")
        activation_ref = delegation["activation"]
        activation = read_activation(require_path(activation_ref["path"]), activation_ref["sha256"])
        if activation["schema"] != "aide.continuous-worker.activation.v1":
            raise Refused("delegated issuer requires frozen coordinator v1")
        fields(frozen, "schema task repository base base_tree allowed_paths admission_digest candidate verification")
        if frozen["schema"] != "aide.broker.authority-request.v1":
            raise Refused("unknown frozen issuance request")
        specs = {spec["id"]: spec for spec in activation["tasks"]}
        if (set(delegation["task_ids"]) - set(specs) or frozen["task"] not in delegation["task_ids"] or
                frozen["repository"] != delegation["repository"]):
            raise Refused("frozen task is outside finite external delegation")
        spec = specs[frozen["task"]]
        if (self.now() >= min(delegation["expires_at"], activation["expires_at"]) or
                delegation["expires_at"] > activation["expires_at"] or
                delegation["max_requests"] > activation["limits"]["max_attempts"]):
            raise Refused("external delegation exceeds current programme bounds")
        authority = {"schema": "aide.broker.authority.v1", "repository": delegation["repository"],
                     "target_ref": delegation["target_ref"], "actor": delegation["actor"],
                     "base": frozen["base"], "base_tree": frozen["base_tree"],
                     "expires_at": delegation["expires_at"], "max_requests": delegation["max_requests"],
                     "required_checks": ["test." + str(i) for i in range(len(spec["test_commands"]))],
                     "admission_digest": spec["source_sha256"], "review_digest": digest(frozen["verification"]),
                     "allowed_paths": spec["allowed_paths"]}
        validate_authority(authority)
        root = require_path(delegation["broker_root"])
        # The host must authenticate its current identity, actual ACL/process
        # boundary, store objects and source pins. A boolean receipt is not enough.
        self.qualification.assert_current(delegation, activation)
        evidence = capsule.validate(frozen, activation, spec, activation["integration"]["exchange_root"])
        binding = {"delegation_sha256": self.pin, "activation_sha256": activation_ref["sha256"],
                   "capsule_digest": evidence["capsule_digest"], "authority": authority}
        key = digest(frozen)
        with directory_lease(root), supervisor_lock(root):
            self.qualification.assert_current(delegation, activation)
            if self.now() >= authority["expires_at"] or file_hash(self.path) != self.pin:
                raise Refused("external delegation expired or changed before issuance")
            for name in ("issuer.sqlite3", "issuer.sqlite3-wal", "issuer.sqlite3-shm"):
                require_path(str(root / name))
            connection = sqlite3.connect(root / "issuer.sqlite3", isolation_level=None, timeout=10)
            try:
                connection.execute("PRAGMA journal_mode=WAL")
                connection.execute("PRAGMA synchronous=FULL")
                if connection.execute("PRAGMA user_version").fetchone()[0] not in (0, 1):
                    raise Refused("unknown issuer ledger schema")
                connection.executescript("""
                    CREATE TABLE IF NOT EXISTS issuances(
                        request TEXT PRIMARY KEY, task TEXT UNIQUE NOT NULL,
                        delegation TEXT NOT NULL, binding TEXT NOT NULL);
                    PRAGMA user_version=1;
                """)
                connection.execute("BEGIN IMMEDIATE")
                existing = connection.execute("SELECT binding FROM issuances WHERE request=?", (key,)).fetchone()
                if existing:
                    if existing[0] != canonical(binding):
                        raise Refused("issued evidence or authority changed")
                else:
                    if connection.execute("SELECT COUNT(*) FROM issuances").fetchone()[0] >= delegation["max_requests"]:
                        raise Refused("external issuance budget exhausted")
                    try:
                        connection.execute("INSERT INTO issuances VALUES(?,?,?,?)",
                                           (key, frozen["task"], self.pin, canonical(binding)))
                    except sqlite3.IntegrityError as error:
                        raise Refused("task already received another exact authority") from error
                connection.execute("COMMIT")
            finally:
                if connection.in_transaction:
                    connection.execute("ROLLBACK")
                connection.close()
        return {"schema": "aide.broker.authority-observation.v1", "request_digest": key,
                "status": "authorized", "authority": authority}
