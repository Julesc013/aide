"""Exact PR/check observations and durable intents; no network dispatcher is installed."""
import math
import json
import re
import sqlite3
from contextlib import contextmanager

from .common import Refused, OID, fields, identity, canonical, digest, require_path


def validate_plan(plan):
    fields(plan, "schema request_digest repository actor target_ref base candidate_commit candidate_tree branch_ref checks policy_digest merge_contract_sha256 expires_at max_observations")
    if plan["schema"] != "aide.broker.pr-plan.v1" or plan["target_ref"] != "refs/heads/dev":
        raise Refused("unknown PR plan or protected target")
    identity(plan["request_digest"])
    for name in ("base", "candidate_commit", "candidate_tree"):
        identity(plan[name], OID)
    if (not isinstance(plan["repository"], str) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", plan["repository"]) or
            not isinstance(plan["actor"], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}", plan["actor"])):
        raise Refused("explicit repository and actor required")
    if plan["branch_ref"] != "refs/heads/task/aide-cw-" + plan["request_digest"]:
        raise Refused("PR branch must bind the full request identity")
    identity(plan["policy_digest"])
    if plan["merge_contract_sha256"] is not None:
        identity(plan["merge_contract_sha256"])
    if (type(plan["expires_at"]) not in (int, float) or not math.isfinite(plan["expires_at"]) or
            type(plan["max_observations"]) is not int or not 1 <= plan["max_observations"] <= 128):
        raise Refused("finite PR observation bounds required")
    checks = plan["checks"]
    if not isinstance(checks, list) or not 1 <= len(checks) <= 32:
        raise Refused("finite explicit hosted checks required")
    names = set()
    for check in checks:
        fields(check, "name app_id workflow_sha")
        if (not isinstance(check["name"], str) or not check["name"] or len(check["name"]) > 200 or
                check["name"] in names or type(check["app_id"]) is not int or check["app_id"] <= 0):
            raise Refused("invalid or duplicate required check identity")
        identity(check["workflow_sha"], OID)
        names.add(check["name"])


def decision(plan, observation):
    """Validate normalized authenticated provider facts, without inferring CAS.

    A qualified provider adapter must supply complete fresh observations. This
    parser does not authenticate a service or qualify an exact-base contract.
    """
    validate_plan(plan)
    fields(observation, "schema request_digest repository actor target_commit candidate branch pull checks_complete checks policy_digest merge_contract_sha256")
    if observation["schema"] != "aide.broker.pr-observation.v1" or any(
            observation[k] != plan[k] for k in ("request_digest", "repository", "actor")):
        raise Refused("provider observation belongs to another request or actor")
    identity(observation["target_commit"], OID)
    candidate = observation["candidate"]
    if candidate is not None:
        fields(candidate, "commit tree parents")
        if candidate != {"commit": plan["candidate_commit"], "tree": plan["candidate_tree"], "parents": [plan["base"]]}:
            raise Refused("provider candidate commit/tree/parent mismatch")
    branch = observation["branch"]
    if branch is not None:
        fields(branch, "ref commit")
        if branch != {"ref": plan["branch_ref"], "commit": plan["candidate_commit"]} or candidate is None:
            raise Refused("provider branch is foreign or candidate is unavailable")
    pull = observation["pull"]
    if pull is not None:
        fields(pull, "number state draft base base_ref base_repository head head_ref head_repository author merge_commit merge_tree merge_parents integrated_ancestor")
        if (type(pull["number"]) is not int or pull["number"] <= 0 or type(pull["draft"]) is not bool or
                pull["state"] not in ("open", "closed", "merged") or
                any(pull[k] != v for k, v in {"base": plan["base"], "base_ref": plan["target_ref"],
                    "base_repository": plan["repository"], "head": plan["candidate_commit"],
                    "head_ref": plan["branch_ref"], "head_repository": plan["repository"],
                    "author": plan["actor"]}.items()) or candidate is None):
            raise Refused("provider PR does not bind exact admitted base/head/actor")
        if pull["state"] == "merged":
            identity(pull["merge_commit"], OID)
            if (pull["merge_tree"] != plan["candidate_tree"] or
                    pull["merge_parents"] != [plan["base"], plan["candidate_commit"]] or
                    pull["integrated_ancestor"] is not True or pull["draft"]):
                raise Refused("provider merge lacks exact tree/parents and target ancestry")
        elif any(pull[k] is not None for k in ("merge_commit", "merge_tree", "merge_parents", "integrated_ancestor")):
            raise Refused("unmerged PR carries fabricated integration evidence")
    if type(observation["checks_complete"]) is not bool or not isinstance(observation["checks"], list) or len(observation["checks"]) > 128:
        raise Refused("invalid or unbounded check observation")
    observed, required = {}, {check["name"]: check for check in plan["checks"]}
    for check in observation["checks"]:
        fields(check, "name app_id workflow_sha head_commit status conclusion")
        name = check["name"]
        if (not isinstance(name, str) or not name or name in observed or
                type(check["app_id"]) is not int or check["app_id"] <= 0 or
                check["status"] not in ("queued", "in_progress", "completed") or
                check["conclusion"] not in (None, "success", "failure", "neutral", "cancelled", "skipped", "timed_out", "action_required", "stale")):
            raise Refused("ambiguous hosted check observations")
        identity(check["workflow_sha"], OID)
        identity(check["head_commit"], OID)
        observed[name] = check
        if name in required:
            if (any(check[k] != required[name][k] for k in ("app_id", "workflow_sha")) or
                    check["head_commit"] != plan["candidate_commit"]):
                raise Refused("required check came from another application/workflow/head")
    passed = observation["checks_complete"] and all(name in observed and
        observed[name]["status"] == "completed" and observed[name]["conclusion"] == "success" for name in required)
    if pull is not None and pull["state"] == "merged":
        if not passed:
            raise Refused("merged observation lacks complete passing required checks")
        return "integrated"
    if observation["target_commit"] != plan["base"]:
        raise Refused("remote target base moved; a pre-read is not compare-and-swap")
    if candidate is None:
        return "publish_objects"
    if branch is None:
        if pull is not None:
            raise Refused("unmerged PR lost its exact request branch")
        return "create_branch"
    if pull is None:
        return "create_pr"
    if pull["state"] == "closed" or pull["draft"]:
        return "blocked_pr"
    if not passed:
        return "wait_checks"
    # These pins are claims from the separately qualified adapter, not a local
    # proof of server atomicity. No dispatcher exists in this source increment.
    if (plan["merge_contract_sha256"] is None or observation["merge_contract_sha256"] != plan["merge_contract_sha256"] or
            observation["policy_digest"] != plan["policy_digest"]):
        return "qualify_target"
    return "merge"


class ObservationStore:
    """Finite request/target reservation and write-ahead transport-stage intents."""
    def __init__(self, root):
        root = require_path(str(root))
        for name in ("pr-observations.sqlite3", "pr-observations.sqlite3-wal", "pr-observations.sqlite3-shm"):
            require_path(str(root / name))
        self.db = sqlite3.connect(root / "pr-observations.sqlite3", isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        if self.db.execute("PRAGMA user_version").fetchone()[0] not in (0, 1):
            self.db.close()
            raise Refused("unknown PR observation ledger schema")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS plans(request TEXT PRIMARY KEY, repository TEXT NOT NULL,
                target TEXT NOT NULL, plan TEXT NOT NULL, stage TEXT NOT NULL, latest TEXT);
            CREATE UNIQUE INDEX IF NOT EXISTS one_writer ON plans(repository,target) WHERE stage != 'integrated';
            CREATE TABLE IF NOT EXISTS observations(sequence INTEGER PRIMARY KEY, request TEXT NOT NULL, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS intents(request TEXT NOT NULL, operation TEXT NOT NULL, observation TEXT NOT NULL,
                PRIMARY KEY(request,operation));
            PRAGMA user_version=1;
        """)

    def close(self):
        self.db.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def _plan(self, plan):
        row = self.db.execute("SELECT * FROM plans WHERE request=?", (plan["request_digest"],)).fetchone()
        if row is None or row["plan"] != canonical(plan):
            raise Refused("PR plan is not the exact durable reservation")
        return row

    def reserve(self, plan):
        validate_plan(plan)
        with self.transaction():
            if self.db.execute("SELECT 1 FROM plans WHERE request=?", (plan["request_digest"],)).fetchone():
                self._plan(plan)
                return False
            if self.db.execute("SELECT COUNT(*) FROM plans").fetchone()[0] >= 2:
                raise Refused("finite PR request budget exhausted")
            try:
                self.db.execute("INSERT INTO plans VALUES(?,?,?,?,'reserved',NULL)",
                                (plan["request_digest"], plan["repository"], plan["target_ref"], canonical(plan)))
            except sqlite3.IntegrityError as error:
                raise Refused("remote target writer already reserved") from error
        return True

    def observe(self, plan, observation):
        next_step = decision(plan, observation)
        key = plan["request_digest"]
        with self.transaction():
            row = self._plan(plan)
            previous_pull = json.loads(row["latest"])["pull"] if row["latest"] else None
            if previous_pull is not None and (observation["pull"] is None or
                    previous_pull["number"] != observation["pull"]["number"]):
                raise Refused("request cannot transfer or discard its observed PR identity")
            if next_step == "integrated" and not self.db.execute(
                    "SELECT 1 FROM intents WHERE request=? AND operation='merge'", (key,)).fetchone():
                raise Refused("integration observation has no durable merge intent")
            if row["stage"] == "integrated":
                if (next_step != "integrated" or
                        json.loads(row["latest"])["pull"] != observation["pull"]):
                    raise Refused("integrated PR evidence cannot regress or change")
            if self.db.execute("SELECT COUNT(*) FROM observations WHERE request=?", (key,)).fetchone()[0] >= plan["max_observations"]:
                raise Refused("finite PR observation budget exhausted")
            body = canonical(observation)
            self.db.execute("INSERT INTO observations(request,body) VALUES(?,?)", (key, body))
            self.db.execute("UPDATE plans SET stage=?,latest=? WHERE request=?", (next_step, body, key))
        return next_step

    def intent(self, plan, observation, operation, *, now):
        if operation not in ("publish_objects", "create_branch", "create_pr", "merge") or decision(plan, observation) != operation:
            raise Refused("mutation does not follow exact provider observations")
        if type(now) not in (int, float) or not math.isfinite(now) or now >= plan["expires_at"]:
            raise Refused("PR mutation authority expired")
        with self.transaction():
            row = self._plan(plan)
            if row["latest"] != canonical(observation) or row["stage"] != operation:
                raise Refused("mutation does not bind the latest durable observation")
            if self.db.execute("SELECT 1 FROM intents WHERE request=? AND operation=?", (plan["request_digest"], operation)).fetchone():
                return False
            self.db.execute("INSERT INTO intents VALUES(?,?,?)", (plan["request_digest"], operation, digest(observation)))
        return True
