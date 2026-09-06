"""One-stage broker reconciliation; provider dispatch requires an internal adapter.

No adapter is installed by configuration or the CLI. Scripted adapters exercise
this orchestration, but do not qualify a protected host or remote server.
"""
from contextlib import closing
import hashlib
import json
import math
import re

from .common import Refused, OID, canonical, digest, identity, parse_json
from .effect_boundary import prepared_candidate
from .pr_observation import ObservationStore, validate_plan

MUTATIONS = frozenset({"publish_objects", "create_branch", "create_pr", "merge"})
MAX_OBSERVATION = 1024 * 1024


def commit_object(tree, base, actor, message):
    """Deterministic literal commit object; no hooks, identity config or signing.

    The fixed epoch is serialization metadata, not an observation of wall time.
    The protected plan must pin the resulting object and reviewed message.
    """
    identity(tree, OID)
    identity(base, OID)
    if not isinstance(actor, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", actor):
        raise Refused("canonical broker actor required")
    if (not isinstance(message, str) or not message.strip() or not message.endswith("\n") or
            "\x00" in message or "\r" in message):
        raise Refused("literal reviewed commit message required")
    raw = (f"tree {tree}\nparent {base}\nauthor {actor} <{actor}@aide.invalid> 0 +0000\n"
           f"committer {actor} <{actor}@aide.invalid> 0 +0000\n\n{message}").encode("utf-8")
    if len(raw) > 64 * 1024:
        raise Refused("candidate commit byte budget exceeded")
    oid = hashlib.sha1(b"commit " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    return oid, raw


class StagedTransport:
    """Internal typed seam; each provider mutation has its own durable intent.

    An adapter must supply assert_current(broker, request, plan, purpose),
    observe(plan) -> bounded JSON bytes and dispatch(operation, plan, prepared).
    A real implementation must authenticate and completely observe provider
    facts, enforce bounded execution and recheck its actual protected-host and
    target contract. Implementing these methods with no-ops proves nothing.
    """
    def __init__(self, plan, commit_bytes, *, adapter=None, checkpoint=None):
        validate_plan(plan)
        self._plan_json = canonical(plan)
        if type(commit_bytes) is not bytes or len(commit_bytes) > 64 * 1024:
            raise Refused("literal bounded commit bytes required")
        try:
            message = commit_bytes.decode("utf-8").split("\n\n", 1)[1]
        except (UnicodeError, IndexError) as error:
            raise Refused("invalid canonical candidate commit") from error
        oid, expected = commit_object(plan["candidate_tree"], plan["base"], plan["actor"], message)
        if oid != plan["candidate_commit"] or commit_bytes != expected:
            raise Refused("candidate commit differs from fixed plan")
        self._commit_bytes = commit_bytes
        self.adapter = adapter
        self.checkpoint = checkpoint or (lambda phase: None)

    @property
    def plan(self):
        return json.loads(self._plan_json)

    def validate(self, broker, request):
        manifest, _ = broker.validate_request(request)
        plan = self.plan
        if (plan["request_digest"] != digest(request) or
                any(plan[k] != broker.authority[k] for k in ("repository", "actor", "target_ref", "base")) or
                plan["candidate_tree"] != manifest["candidate_tree"] or
                plan["expires_at"] > broker.authority["expires_at"] or
                {check["name"] for check in plan["checks"]} != set(broker.authority["required_checks"])):
            raise Refused("staged transport plan differs from admitted request")
        self._qualified(broker, request, "observe")
        return plan

    def _qualified(self, broker, request, purpose):
        if self.adapter is None:
            raise Refused("qualified provider adapter is not installed")
        # This is an internal host API, never a caller-supplied boolean or CLI
        # module name. Credentials and controller/store isolation are external.
        self.adapter.assert_current(broker, json.loads(canonical(request)), self.plan, purpose)

    def _read(self, broker, request, store):
        self._qualified(broker, request, "observe")
        store.observation_attempt(self.plan)
        raw = self.adapter.observe(self.plan)
        if type(raw) is not bytes or len(raw) > MAX_OBSERVATION:
            raise Refused("provider observation byte budget or type")
        observation = parse_json(raw)
        self._qualified(broker, request, "observe")
        stage = store.observe(self.plan, observation)
        if stage == "integrated":
            self._integrated(broker, request, observation)
        return stage, observation

    def _integrated(self, broker, request, observation):
        plan = self.plan
        receipt = {"schema": "aide.broker.integration-receipt.v1",
                   "request_digest": digest(request), "repository": plan["repository"],
                   "target_ref": plan["target_ref"], "actor": plan["actor"], "base": plan["base"],
                   "candidate_tree": plan["candidate_tree"], "integrated_tree": plan["candidate_tree"],
                   "integrated_commit": observation["pull"]["merge_commit"],
                   "required_checks_digest": digest(broker.authority["required_checks"])}
        manifest, _ = broker.validate_request(request)
        broker.checked_receipt(receipt, digest(request), manifest)
        broker.ledger.integrated(digest(request), receipt)
        return receipt

    def observe(self, broker, request):
        self.validate(broker, request)
        with closing(ObservationStore(broker.root)) as store:
            row = store.db.execute("SELECT 1 FROM plans WHERE request=?", (digest(request),)).fetchone()
            if row is None:
                return {"status": "pending", "receipt": None}
            stage, observation = self._read(broker, request, store)
            if stage == "integrated":
                return {"status": "integrated", "receipt": self._integrated(broker, request, observation)}
        return {"status": "pending", "receipt": None}

    def advance(self, broker, request):
        """At most one new stage dispatch; missing replies only permit observation."""
        self.validate(broker, request)
        with closing(ObservationStore(broker.root)) as store:
            store.reserve(self.plan)
            stage, _ = self._read(broker, request, store)
            if stage not in MUTATIONS:
                return
            with prepared_candidate(broker, request) as prepared:
                # Observe again after acquiring the generation/target writer
                # lease. The final server mutation must still enforce its own
                # atomic predicate; this fresh observation is not CAS.
                stage, observation = self._read(broker, request, store)
                if stage not in MUTATIONS:
                    return
                self._qualified(broker, request, stage)
                oid = broker.git.run(prepared["directory"], "hash-object", "-t", "commit", "-w", "--stdin",
                                     data=self._commit_bytes).decode().strip()
                if (oid != self.plan["candidate_commit"] or
                        broker.git.run(prepared["directory"], "cat-file", "commit", oid) != self._commit_bytes):
                    raise Refused("materialized candidate commit differs from fixed bytes")
                broker.guard()
                broker.ledger.intent(digest(request))
                if not store.intent(self.plan, observation, stage, now=broker.now()):
                    return
                self.checkpoint("intent:" + stage)
                self._qualified(broker, request, stage)
                broker.guard()
                now = broker.now()
                if (type(now) not in (int, float) or not math.isfinite(now) or
                        now >= min(self.plan["expires_at"], broker.authority["expires_at"])):
                    raise Refused("stage dispatch authority or plan expired")
                # The adapter receives only leased prepared inputs and an exact
                # immutable plan projection. It must not accept mutation targets
                # or credentials from worker-produced text.
                inputs = dict(prepared, commit_bytes=self._commit_bytes)
                self.adapter.dispatch(stage, self.plan, inputs)
                self.checkpoint("dispatched:" + stage)
