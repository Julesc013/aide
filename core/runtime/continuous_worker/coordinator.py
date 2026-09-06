"""Bounded resumable pipeline. External protected integration is a separate broker."""
from __future__ import annotations

import json
from contextlib import ExitStack
from pathlib import Path
import shutil
import time
import uuid

from . import codex
from .contract import changed, file_hash, read_activation, registered_command, snapshot
from .state import Refused, State, canonical, digest
from .windows_job import WindowsJobHost
from .locking import supervisor_lock


class Paused(Exception):
    pass


class Coordinator:
    def __init__(self, activation_path, approval_hash, *, host=None):
        self.path = Path(activation_path).resolve()
        self.approval = approval_hash
        self.config = read_activation(self.path, approval_hash)
        self.state = State(Path(self.config["state_root"]))
        self.state.bind(self.config)
        self.host = host or WindowsJobHost()
        with self.state.transaction():
            self.state.db.execute("INSERT OR IGNORE INTO meta VALUES('started',?)", (str(time.time()),))
        self.started = float(self.state.db.execute("SELECT value FROM meta WHERE key='started'").fetchone()[0])

    def guard(self, task=None):
        # Re-read pins at every effect boundary, not just when the programme starts.
        read_activation(self.path, self.approval)
        limits = self.config["limits"]
        if time.time() >= min(self.config["expires_at"], self.started + limits["programme_seconds"]):
            raise Refused("programme time budget exhausted")
        root = self.state.root
        used = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
        if used >= limits["max_state_bytes"] or shutil.disk_usage(root).free < limits["min_free_bytes"]:
            raise Refused("storage budget or free-space floor reached")
        if task and self.state.cancelled(task):
            raise Refused("operator cancellation")
        if self.state.mode() == "emergency-stop":
            raise Refused("emergency stop")

    def effect(self, attempt, phase, command, workspace, payload, *, worker=False):
        rows = self.state.db.execute("SELECT * FROM effects WHERE attempt=? AND kind=? ORDER BY rowid",
                                     (attempt["id"], phase)).fetchall()
        if rows:
            row = rows[-1]
            if row["status"] != "observed":
                raise Refused("uncertain process effect; reconciliation required")
            observed = json.loads(row["response"])
            if not observed.get("completed"):
                raise Refused("previous effect did not complete; retained for diagnosis")
            output = Path(json.loads(row["request"])["output"])
            if any(file_hash(output / name) != pin for name, pin in observed["artifacts"].items()):
                raise Refused("persisted process output changed")
            return output, observed["receipt"]
        self.guard(attempt["task"])
        if self.state.mode() == "pause-dispatch":
            raise Paused()
        if worker:
            count = self.state.db.execute("SELECT COUNT(*) FROM effects WHERE kind IN ('coding','assurance')").fetchone()[0]
            if count >= self.config["limits"]["max_sessions"]:
                raise Refused("worker session budget exhausted")
        job_id = uuid.uuid4().hex
        output = self.state.root / "attempts" / attempt["id"] / job_id
        request = {"job_id": job_id, "argv": command, "workspace": str(workspace),
                   "payload_sha256": digest(payload), "output": str(output)}
        limits = self.config["limits"]
        needed = len(payload.encode()) + limits["output_bytes"] + 65536
        used = sum(p.stat().st_size for p in self.state.root.rglob("*") if p.is_file())
        if len(payload.encode()) > 2097152 or used + needed > limits["max_state_bytes"]:
            raise Refused("insufficient artifact reservation or input limit exceeded")
        effect = self.state.intent(attempt["id"], phase, request)
        monitor = {"last": 0.0, "reason": ""}
        def stop_requested():
            if self.state.cancelled(attempt["task"]):
                monitor["reason"] = "operator cancellation"
                return True
            if time.monotonic() - monitor["last"] >= 2:
                monitor["last"] = time.monotonic()
                try:
                    self.guard(attempt["task"])
                except (Refused, OSError) as exc:
                    monitor["reason"] = str(exc)
                    return True
            return False
        # The durable intent precedes CreateProcess. Exceptions leave it uncertain.
        receipt = self.host.run(command, cwd=workspace, input_bytes=payload.encode(),
                                output_dir=output, job_id=job_id, timeout=limits["process_seconds"],
                                output_limit=limits["output_bytes"], memory_limit=limits["memory_bytes"],
                                process_limit=limits["max_processes"],
                                cancelled=stop_requested)
        receipt["monitor_reason"] = monitor["reason"]
        artifacts = {name: file_hash(output / name) for name in ("stdin", "stdout", "stderr")}
        self.state.observed(effect, {"completed": True, "receipt": receipt, "artifacts": artifacts})
        return output, receipt

    def verify_artifacts(self, attempt):
        records = []
        for row in self.state.db.execute("SELECT kind,request,response FROM effects WHERE attempt=?", (attempt,)):
            if row["response"] is None:
                continue
            response = json.loads(row["response"])
            if not response.get("completed"):
                continue
            output = Path(json.loads(row["request"])["output"])
            pins = response["artifacts"]
            if any(file_hash(output / name) != pin for name, pin in pins.items()):
                raise Refused("durable evidence changed after observation")
            records.append({"phase": row["kind"], "artifacts": pins})
        return records

    @staticmethod
    def require_success(receipt):
        if not receipt.get("quiescent") or receipt["exit_code"] != 0 or receipt["reason"] != "exited":
            raise Refused("owned process failed: " + receipt.get("reason", "unknown"))

    def recover(self):
        """Account for every in-flight Job; never infer completion from worker exit."""
        active = self.state.active()
        if not active:
            return
        for row in self.state.unresolved():
            request = json.loads(row["request"])
            receipt = self.host.reconcile(request["job_id"])
            if not receipt.get("quiescent"):
                raise Refused("recovery could not fence owned processes")
            self.state.observed(row["id"], {"completed": False, "recovery": receipt})
        if active["stage"] == "integration_pending":
            # Lost merge response: only query the broker; never repeat apply.
            return
        evidence = json.loads(active["evidence"])
        unresolved_results = self.state.db.execute(
            "SELECT response FROM effects WHERE attempt=?", (active["id"],)).fetchall()
        if any(not json.loads(r[0]).get("completed") for r in unresolved_results if r[0]):
            self.state.transition(active["id"], "blocked", {
                "reason": "interrupted effect reconciled; patch retained; new admission needed to retry",
                "preserved_evidence": evidence})

    def broker_query(self, attempt, request):
        # Each query is a new read-only observation; apply's outcome may still be unknown.
        queries = self.state.db.execute("SELECT COUNT(*) FROM effects WHERE attempt=? AND kind LIKE 'integration_query.%'",
                                       (attempt["id"],)).fetchone()[0]
        if queries >= self.config["limits"]["max_integration_queries"]:
            raise Refused("integration observation retry limit")
        command = registered_command(self.config["integration"]["query"])
        output, receipt = self.effect(attempt, "integration_query." + str(queries), command,
                                      self.config["integration"]["cwd"], canonical(request))
        self.require_success(receipt)
        return self.parse_broker(output, request)

    @staticmethod
    def parse_broker(output, request):
        value = json.loads((output / "stdout").read_text(encoding="utf-8"))
        if (not isinstance(value, dict) or set(value) != {"status", "request_digest", "integrated_identity", "receipt_ref"}
                or value["status"] not in ("absent", "pending", "integrated", "refused")
                or value["request_digest"] != digest(request)):
            raise Refused("broker observation does not match exact integration request")
        if value["status"] == "integrated" and (
                value["integrated_identity"] != request["subject"]["identity"] or not value["receipt_ref"]):
            raise Refused("integration lacks observed exact-content receipt")
        return value

    def pipeline(self, attempt):
        spec, ident = attempt["spec"], attempt["id"]
        self.verify_artifacts(ident)
        evidence = json.loads(self.state.db.execute("SELECT evidence FROM attempts WHERE id=?", (ident,)).fetchone()[0])
        git_command = registered_command(self.config["git"])
        workspace = Path(spec["workspace"])
        attempt_root = self.state.root / "attempts" / ident
        attempt_root.mkdir(parents=True, exist_ok=True)
        schema = attempt_root / "worker-result.schema.json"
        if not schema.exists():
            schema.write_text(canonical(codex.SCHEMA), encoding="utf-8")
        elif schema.read_text(encoding="utf-8") != canonical(codex.SCHEMA):
            raise Refused("worker schema drift")
        if "baseline" not in evidence:
            baseline = snapshot(git_command, workspace)
            if baseline["head"] != spec["base"]:
                raise Refused("moved workspace base")
            from .contract import git
            if git(git_command, workspace, "status", "--porcelain", "--untracked-files=all").strip():
                raise Refused("worker clone must initially be clean")
            self.state.transition(ident, "coding", {"baseline": baseline})
            evidence["baseline"] = baseline
        baseline = evidence["baseline"]
        if "coding" not in evidence:
            prompt = ("Implement only the admitted task in this independent clone. Do not commit, move refs, "
                      "change authority, access credentials, publish or integrate. The coordinator will run "
                      "independent tests and assurance. Allowed paths: " + canonical(spec["allowed_paths"]) +
                      "\nTask " + spec["id"] + ":\n" + spec["instructions"] +
                      "\nReturn subject_identity=" + baseline["identity"])
            command = codex.argv(registered_command(self.config["codex"]), workspace, schema,
                                 model=self.config["worker_models"]["coding"])
            output, receipt = self.effect(attempt, "coding", command, workspace, prompt, worker=True)
            self.require_success(receipt)
            result = codex.parse_events(output / "stdout", baseline["identity"])
            if result["result"]["status"] != "pass":
                raise Refused("coding worker did not pass")
            subject = snapshot(git_command, workspace)
            paths = changed(baseline, subject, spec["allowed_paths"])
            self.state.transition(ident, "testing", {"coding": result, "subject": subject, "changed_paths": paths})
            evidence |= {"coding": result, "subject": subject}
        subject = evidence["subject"]
        if snapshot(git_command, workspace)["identity"] != subject["identity"]:
            raise Refused("candidate changed after coding evidence")
        if "tests" not in evidence:
            tests = []
            for index, registered in enumerate(spec["test_commands"]):
                command = registered_command(registered)
                output, receipt = self.effect(attempt, "test." + str(index), command, workspace, "")
                self.require_success(receipt)
                if snapshot(git_command, workspace)["identity"] != subject["identity"]:
                    raise Refused("validation changed candidate files")
                tests.append({"output": str(output), "receipt": receipt,
                              "artifacts": {name: file_hash(output / name) for name in ("stdin", "stdout", "stderr")}})
            self.state.transition(ident, "assuring", {"tests": tests})
            evidence["tests"] = tests
        self.verify_artifacts(ident)
        if "assurance" not in evidence:
            prompt = ("Independently review the actual candidate diff and admitted requirements. Read-only. "
                      "Do not modify code, tests, acceptance or authority. Return pass only if no material "
                      "findings remain. Task " + spec["id"] + ": " + spec["instructions"] +
                      "\nExpected subject_identity=" + subject["identity"] +
                      "\nTest evidence references=" + canonical(evidence["tests"]))
            command = codex.argv(registered_command(self.config["codex"]), workspace, schema, assurance=True,
                                 model=self.config["worker_models"]["assurance"])
            output, receipt = self.effect(attempt, "assurance", command, workspace, prompt, worker=True)
            self.require_success(receipt)
            assurance = codex.parse_events(output / "stdout", subject["identity"])
            if assurance["session_id"] == evidence["coding"]["session_id"]:
                raise Refused("assurance reused coding context")
            if assurance["result"]["status"] != "pass" or assurance["result"]["findings"]:
                raise Refused("independent assurance has unresolved findings")
            if snapshot(git_command, workspace)["identity"] != subject["identity"]:
                raise Refused("candidate changed during assurance")
            self.state.transition(ident, "awaiting_integration", {"assurance": assurance})
            evidence["assurance"] = assurance
        artifact_manifest = self.verify_artifacts(ident)
        self.guard(attempt["task"])
        if snapshot(git_command, workspace)["identity"] != subject["identity"]:
            raise Refused("candidate moved after assurance")
        request = {"attempt": ident, "task": spec["id"], "repository": spec["repository"],
                   "admission": spec["source_sha256"], "activation": digest(self.config),
                   "base": spec["base"], "workspace": str(workspace), "subject": subject,
                   "tests": evidence["tests"], "assurance": evidence["assurance"],
                   "artifacts": [r for r in artifact_manifest if not r["phase"].startswith("integration_")]}
        stage = self.state.db.execute("SELECT stage FROM attempts WHERE id=?", (ident,)).fetchone()[0]
        observation = self.broker_query(attempt, request)
        if observation["status"] == "integrated":
            self.state.transition(ident, "succeeded", {"integration": observation})
            return
        if observation["status"] != "absent" or stage == "integration_pending":
            self.state.transition(ident, "integration_pending", {"reason": "integration outcome requires reconciliation"})
            raise Paused()
        # Persist semantic integration intent BEFORE invoking the external authority broker.
        self.state.transition(ident, "integration_pending", {"integration_request": request})
        command = registered_command(self.config["integration"]["apply"])
        output, receipt = self.effect(attempt, "integration_apply", command, self.config["integration"]["cwd"], canonical(request))
        self.require_success(receipt)
        self.parse_broker(output, request)  # response alone never closes the task
        observation = self.broker_query(attempt, request)
        if observation["status"] != "integrated":
            raise Paused()
        self.state.transition(ident, "succeeded", {"integration": observation})

    def run(self):
        with ExitStack() as locks:
            locks.enter_context(supervisor_lock(self.state.root))
            for root in sorted({t["workspace"] for t in self.config["tasks"]}):
                locks.enter_context(supervisor_lock(Path(root) / ".git"))
            return self._run_locked()

    def _run_locked(self):
        self.recover()
        while True:
            active = self.state.active()
            if active:
                spec = json.loads(self.state.db.execute("SELECT spec FROM tasks WHERE id=?", (active["task"],)).fetchone()[0])
                attempt = {"id": active["id"], "task": active["task"], "spec": spec}
            else:
                self.guard()
                attempt = self.state.claim(self.config["limits"]["max_attempts"])
            if not attempt:
                return self.state.status()
            try:
                self.pipeline(attempt)
            except Paused:
                if self.state.mode() in ("pause-dispatch", "emergency-stop"):
                    return self.state.status()
                active = self.state.active()
                if not active or active["stage"] != "integration_pending":
                    return self.state.status()
                until = time.monotonic() + 30
                while time.monotonic() < until:
                    if self.state.mode() in ("pause-dispatch", "emergency-stop"):
                        return self.state.status()
                    time.sleep(.1)
                continue
            except (Refused, OSError, ValueError, KeyError) as exc:
                active = self.state.active()
                if self.state.unresolved() or (active and active["stage"] == "integration_pending"):
                    self.state.event(attempt["id"], "uncertain", {"reason": str(exc)})
                    return self.state.status()
                stage = "cancelled" if self.state.cancelled(attempt["task"]) else "blocked"
                self.state.transition(attempt["id"], stage, {"reason": str(exc)})
                # A local blocker does not prevent another independent ready task.

