"""Cooperative dependency observations in the existing coordinator ledger.

This module never dispatches, grants authority, or edits a native work record.
Participant bindings are declarations; the local caller is not authenticated.
"""
from __future__ import annotations

import json
import math
import re
import time

from .state import Refused, canonical, digest

MAX_MESSAGE = 65536
CONFIG_KEY = "dependency_configuration_v1"
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,119}")
SHA = re.compile(r"[0-9a-f]{64}")
STAGES = ("recorded", "delivered", "accepted", "returned", "adopted")
OBLIGATIONS = {"answer", "candidate", "validated", "integrated_dev", "promoted_main", "published"}


def fields(value, names):
    if not isinstance(value, dict) or set(value) != set(names.split()):
        raise Refused("unknown or missing fields")


def text(value, *, limit=4096):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or "\0" in value:
        raise Refused("invalid bounded text")


def identity(value, pattern=ID):
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise Refused("invalid identity")


def references(value):
    if not isinstance(value, list) or not 1 <= len(value) <= 32:
        raise Refused("one to 32 evidence references required")
    for ref in value:
        fields(ref, "ref sha256")
        text(ref["ref"])
        identity(ref["sha256"], SHA)


def bounded(value, limit=MAX_MESSAGE):
    try:
        raw = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
        size = len(raw.encode("utf-8"))
    except (ValueError, TypeError, UnicodeError, RecursionError) as exc:
        raise Refused("invalid JSON value") from exc
    if size > limit:
        raise Refused("message byte limit exceeded")


def decode(raw):
    if len(raw) > MAX_MESSAGE:
        raise Refused("message byte limit exceeded")

    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise Refused("duplicate JSON key")
            value[key] = item
        return value

    try:
        value = json.loads(raw, object_pairs_hook=unique)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise Refused("invalid JSON input") from exc
    bounded(value)
    return value


def configuration(value, root):
    bounded(value)
    fields(value, "schema state_root participants expires_at max_requests message_bytes")
    if value["schema"] != "aide.dependency-configuration.v1" or value["state_root"] != str(root):
        raise Refused("configuration schema or state root mismatch")
    if type(value["expires_at"]) not in (int, float) or not math.isfinite(value["expires_at"]):
        raise Refused("finite configuration expiry required")
    for name, low, high in (("max_requests", 1, 256), ("message_bytes", 1024, MAX_MESSAGE)):
        if type(value[name]) is not int or not low <= value[name] <= high:
            raise Refused("invalid configuration bound: " + name)
    participants = value["participants"]
    if not isinstance(participants, dict) or not 2 <= len(participants) <= 16:
        raise Refused("two to 16 participant bindings required")
    for name, binding in participants.items():
        identity(name)
        fields(binding, "repository owner workspace host session generation")
        for key in ("repository", "owner", "workspace", "host", "session"):
            text(binding[key])
        if type(binding["generation"]) is not int or binding["generation"] < 1:
            raise Refused("positive ownership generation required")


class Requests:
    """A bounded linked-record extension, not a scheduler or integration broker."""

    @staticmethod
    def initialize(state, config, *, now=time.time):
        configuration(config, state.root)
        if now() >= config["expires_at"]:
            raise Refused("configuration expired")
        with state.transaction():
            row = state.db.execute("SELECT value FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone()
            if row:
                if row[0] != canonical(config):
                    raise Refused("configuration changed; reconcile existing bindings first")
            else:
                state.db.execute("CREATE TABLE dependency_requests(id TEXT PRIMARY KEY, body TEXT NOT NULL, "
                                 "digest TEXT NOT NULL, stage TEXT NOT NULL, observations TEXT NOT NULL)")
                state.db.execute("INSERT INTO meta VALUES(?,?)", (CONFIG_KEY, canonical(config)))
                state.event(None, "dependency_initialized", {"configuration_sha256": digest(config)})
        return {"configuration_sha256": digest(config), "mode": "cooperative",
                "bindings": {name: digest(binding) for name, binding in config["participants"].items()}}

    def __init__(self, state, expected_config, *, now=time.time):
        self.state, self.now = state, now
        row = state.db.execute("SELECT value FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone()
        if row is None:
            raise Refused("dependency interface is not initialized")
        self.config = decode(row[0].encode())
        configuration(self.config, state.root)
        if digest(self.config) != expected_config:
            raise Refused("configuration digest mismatch")

    def guard(self):
        if self.now() >= self.config["expires_at"]:
            raise Refused("configuration expired; inspect retained records")
        if self.state.mode() != "resume":
            raise Refused("coordinator controls prohibit new dependency observations")
        row = self.state.db.execute("SELECT value FROM meta WHERE key=?", (CONFIG_KEY,)).fetchone()
        if row is None or row[0] != canonical(self.config):
            raise Refused("configuration changed")

    def actor(self, actor, expected):
        fields(actor, "participant binding_sha256")
        identity(actor["participant"])
        binding = self.config["participants"].get(actor["participant"])
        if actor["participant"] != expected or binding is None or actor["binding_sha256"] != digest(binding):
            raise Refused("wrong participant or stale binding")

    def row(self, request_id):
        identity(request_id)
        row = self.state.db.execute("SELECT * FROM dependency_requests WHERE id=?", (request_id,)).fetchone()
        if row is None:
            raise Refused("unknown dependency request")
        return row

    def submit(self, message):
        bounded(message, self.config["message_bytes"])
        fields(message, "actor request")
        body = message["request"]
        fields(body, "schema id sender recipient sender_work objective acceptance references completion")
        if body["schema"] != "aide.dependency-request.v1":
            raise Refused("unknown request schema")
        for key in ("id", "sender", "recipient"):
            identity(body[key])
        if body["sender"] == body["recipient"] or body["recipient"] not in self.config["participants"]:
            raise Refused("request needs a different registered recipient")
        self.actor(message["actor"], body["sender"])
        fields(body["sender_work"], "ref sha256")
        references([body["sender_work"]])
        for key in ("objective", "acceptance"):
            text(body[key], limit=8192)
        references(body["references"])
        obligations = body["completion"]
        if (not isinstance(obligations, list) or not obligations
                or any(not isinstance(x, str) or x not in OBLIGATIONS for x in obligations)
                or len(set(obligations)) != len(obligations)):
            raise Refused("invalid completion obligations")
        with self.state.transaction():
            self.guard()
            previous = self.state.db.execute("SELECT body FROM dependency_requests WHERE id=?", (body["id"],)).fetchone()
            if previous:
                if previous[0] != canonical(body):
                    raise Refused("request identity conflicts with another revision")
            else:
                if self.state.db.execute("SELECT COUNT(*) FROM dependency_requests").fetchone()[0] >= self.config["max_requests"]:
                    raise Refused("request allowance exhausted")
                self.state.db.execute("INSERT INTO dependency_requests VALUES(?,?,?,'recorded','{}')",
                                      (body["id"], canonical(body), digest(body)))
                self.state.event(None, "dependency_recorded", {"id": body["id"], "digest": digest(body),
                                                              "actor": message["actor"]})
        return self.inspect(body["id"])

    def observe(self, message):
        bounded(message, self.config["message_bytes"])
        fields(message, "request_id request_sha256 actor stage detail")
        stage, detail = message["stage"], message["detail"]
        if not isinstance(stage, str) or stage not in STAGES[1:]:
            raise Refused("unknown observation stage")
        with self.state.transaction():
            self.guard()
            row = self.row(message["request_id"])
            if row["digest"] != message["request_sha256"]:
                raise Refused("request revision mismatch")
            body = json.loads(row["body"])
            self.actor(message["actor"], body["sender"] if stage == "adopted" else body["recipient"])
            observations = json.loads(row["observations"])
            if stage in observations:
                if observations[stage] != message:
                    raise Refused("conflicting duplicate observation")
            else:
                if STAGES.index(stage) != STAGES.index(row["stage"]) + 1:
                    raise Refused("out-of-order observation")
                self.validate_detail(stage, detail, body, observations)
                observations[stage] = message
                self.state.db.execute("UPDATE dependency_requests SET stage=?,observations=? WHERE id=?",
                                      (stage, canonical(observations), body["id"]))
                self.state.event(None, "dependency_" + stage,
                                 {"id": body["id"], "observation_sha256": digest(message)})
        return self.inspect(message["request_id"])

    @staticmethod
    def validate_detail(stage, detail, body, observations):
        if stage == "delivered":
            fields(detail, "receipt")
            references([detail["receipt"]])
        elif stage == "accepted":
            fields(detail, "native_work evidence")
            references([detail["native_work"]])
            references(detail["evidence"])
        elif stage == "returned":
            fields(detail, "subject claims evidence")
            references([detail["subject"]])
            references(detail["evidence"])
            if not isinstance(detail["claims"], dict) or set(detail["claims"]) != set(body["completion"]):
                raise Refused("result must account for every requested completion obligation")
            if any(value not in ("PASS", "FAILED", "NOT_RUN", "UNKNOWN") for value in detail["claims"].values()):
                raise Refused("unknown completion claim")
        else:
            fields(detail, "returned_sha256 verification")
            returned = observations["returned"]
            if detail["returned_sha256"] != digest(returned):
                raise Refused("adoption does not bind the returned result")
            if any(v != "PASS" for v in returned["detail"]["claims"].values()):
                raise Refused("unmet completion obligations; adoption cannot close this request")
            references(detail["verification"])

    def inspect(self, request_id):
        row = self.row(request_id)
        body, observations = json.loads(row["body"]), json.loads(row["observations"])
        stage = row["stage"]
        owner = body["sender"] if stage in ("returned", "adopted") else body["recipient"]
        action = {"recorded": "deliver_to_registered_recipient", "delivered": "decide_native_acceptance",
                  "accepted": "perform_native_work_under_its_own_authority", "returned": "verify_result_and_record_adoption",
                  "adopted": "none_local_observation_complete"}[stage]
        claims = observations.get("returned", {}).get("detail", {}).get("claims", {})
        unmet = {key: value for key, value in claims.items() if value != "PASS"}
        if stage == "returned" and unmet:
            action = "reconcile_unmet_obligations_with_native_owner_before_successor_request"
        expired = self.now() >= self.config["expires_at"]
        return {"schema": "aide.dependency-status.v1", "mode": "cooperative", "id": body["id"],
                "request_sha256": row["digest"], "request": body, "stage": stage,
                "observations": observations, "next_owner": owner, "next_action": action,
                "unmet_obligations": unmet,
                "configuration_expired": expired, "coordinator_mode": self.state.mode(),
                "claims_independently_verified": False, "execution_authorized": False,
                "limitation": "Attributed local records only; no live host, effect or verification is inferred."}
