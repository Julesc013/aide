"""Real bounded child-process bridge fixtures; no provider credentials or network."""
from contextlib import closing
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import test_continuous_worker_pr_observation as staged_cases
from core.runtime.integration_broker.common import Refused, canonical, digest
from core.runtime.integration_broker.bridge_store import BridgeStore
from core.runtime.integration_broker.pr_observation import ObservationStore
from core.runtime.integration_broker.registered_bridge import RegisteredBridge
from core.runtime.integration_broker.staged_transport import StagedTransport
from core.runtime.continuous_worker.locking import supervisor_lock


FIXTURE_BRIDGE = r"""
import base64, hashlib, json, pathlib, sys, time, zlib
root=pathlib.Path.cwd()
request=json.load(sys.stdin)
plan=request['plan']; op=request['operation']
starts_path=root/'fixture-starts.json'
starts=json.loads(starts_path.read_text()) if starts_path.exists() else []
starts.append({'call_id':request['call_id'],'operation':op})
starts_path.write_text(json.dumps(starts))
mode=(root/'mode').read_text() if (root/'mode').exists() else ''
if mode=='hang' or mode=='hang:'+op: time.sleep(20)
if mode=='flood':
    sys.stdout.write('x'*2097152); sys.stdout.flush(); time.sleep(20)
if mode=='malformed':
    print('{}'); sys.exit(0)
state_path=root/'fixture-service.json'
state=json.loads(state_path.read_text()) if state_path.exists() else {'stage':'publish_objects','effects':[]}
if op!='observe':
    assert op==state['stage']
    prepared=request['prepared']; raw=base64.b64decode(prepared['commit_bytes'])
    assert hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==plan['candidate_commit']
    path=pathlib.Path(prepared['directory'])/'objects'/plan['candidate_commit'][:2]/plan['candidate_commit'][2:]
    assert zlib.decompress(path.read_bytes())==b'commit '+str(len(raw)).encode()+b'\0'+raw
    assert raw.startswith(('tree '+plan['candidate_tree']+'\nparent '+plan['base']+'\n').encode())
    state['effects'].append(op)
    stages=['publish_objects','create_branch','create_pr','merge','integrated']
    state['stage']=stages[stages.index(op)+1]
    state_path.write_text(json.dumps(state))
    if mode=='lose:'+op: sys.exit(9)
    result={'status':'submitted'}
else:
    result={'schema':'aide.broker.pr-observation.v1','request_digest':plan['request_digest'],
      'repository':plan['repository'],'actor':plan['actor'],'target_commit':plan['base'],
      'candidate':{'commit':plan['candidate_commit'],'tree':plan['candidate_tree'],'parents':[plan['base']]},
      'branch':{'ref':plan['branch_ref'],'commit':plan['candidate_commit']},
      'pull':{'number':8,'state':'open','draft':False,'base':plan['base'],'base_ref':plan['target_ref'],
        'base_repository':plan['repository'],'head':plan['candidate_commit'],'head_ref':plan['branch_ref'],
        'head_repository':plan['repository'],'author':plan['actor'],'merge_commit':None,
        'merge_tree':None,'merge_parents':None,'integrated_ancestor':None},
      'checks_complete':True,'checks':[dict(c,head_commit=plan['candidate_commit'],status='completed',conclusion='success') for c in plan['checks']],
      'policy_digest':plan['policy_digest'],'merge_contract_sha256':plan['merge_contract_sha256']}
    if state['stage']=='publish_objects': result['candidate']=result['branch']=result['pull']=None
    elif state['stage']=='create_branch': result['branch']=result['pull']=None
    elif state['stage']=='create_pr': result['pull']=None
    elif state['stage']=='integrated':
        result['pull'].update(state='merged',merge_commit='9'*40,merge_tree=plan['candidate_tree'],
          merge_parents=[plan['base'],plan['candidate_commit']],integrated_ancestor=True)
        result['target_commit']='9'*40
response={'schema':'aide.broker.bridge-response.v1','call_id':request['call_id'],
          'request_digest':request['request_digest'],'operation':op,'result':result}
if mode=='wrong-id': response['call_id']='0'*32
print(json.dumps(response))
"""


class FixtureQualification:
    """Permissive local test seam; does not establish host isolation."""
    def __init__(self):
        self.allowed = True

    def assert_current(self, *args):
        if not self.allowed:
            raise Refused("fixture qualification revoked")


@unittest.skipUnless(os.name == "nt" and shutil.which("git"), "requires real Windows owned process host")
class RegisteredBridgeTests(unittest.TestCase):
    def fixture(self, **overrides):
        case = staged_cases.StagedBrokerTests(methodName="runTest")
        helper, plan, commit, _, _, broker = case.fixture()
        self.addCleanup(case.doCleanups)
        code = helper.root / "bridge-code"
        code.mkdir()
        script = code / "bridge.py"
        script.write_text(FIXTURE_BRIDGE, encoding="utf-8", newline="\n")
        executable = Path(sys.executable)
        limits = {"timeout_seconds": 3, "output_bytes": 1048576, "memory_bytes": 268435456,
                  "processes": 2, "max_calls": 20, "max_io_bytes": 67108864, "minimum_free_bytes": 67108864}
        limits.update(overrides)
        config = {"schema": "aide.broker.bridge.v1", "plan_digest": digest(plan),
                  "argv": [str(executable), "-I", "-B", str(script)],
                  "inputs": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (executable, script)},
                  "cwd": str(code), "limits": limits}
        path = helper.root / "bridge-registration.json"
        path.write_text(canonical(config), encoding="utf-8")
        pin = hashlib.sha256(path.read_bytes()).hexdigest()
        qualification = FixtureQualification()
        bridge = RegisteredBridge(path, pin, plan, qualifier=qualification)
        broker.transport = StagedTransport(plan, commit, adapter=bridge)
        return helper, plan, commit, broker, bridge, qualification, code

    def calls(self, helper):
        with closing(sqlite3.connect(helper.state / "provider-bridge.sqlite3")) as db:
            db.row_factory = sqlite3.Row
            return [dict(row) for row in db.execute("SELECT * FROM calls ORDER BY rowid")]

    def test_registered_child_reads_real_commit_objects_and_finishes_all_stages(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        for _ in range(4):
            broker.reconcile(helper.request)
        self.assertEqual(broker.query(helper.request)["status"], "integrated")
        state = json.loads((code / "fixture-service.json").read_text())
        self.assertEqual(state["effects"], ["publish_objects", "create_branch", "create_pr", "merge"])
        for row in self.calls(helper):
            self.assertEqual(row["stage"], "returned")
            receipt = json.loads(row["result"])
            self.assertTrue(receipt["job"]["quiescent"])
            folder = helper.state / ("provider-call-" + row["id"]) / "streams"
            for name, expected in receipt["hashes"].items():
                self.assertEqual(hashlib.sha256((folder / name).read_bytes()).hexdigest(), expected)
        self.assertEqual(len(self.calls(helper)), 13)

    def test_missing_qualification_and_unpinned_script_refuse_before_child(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        bridge.qualifier = None
        with self.assertRaisesRegex(Refused, "qualification is absent"):
            broker.reconcile(helper.request)
        bridge.qualifier = qualifier
        (code / "bridge.py").write_text(FIXTURE_BRIDGE + "\n# changed\n", encoding="utf-8")
        with self.assertRaisesRegex(Refused, "source drift"):
            broker.reconcile(helper.request)
        self.assertFalse((helper.state / "provider-bridge.sqlite3").exists())
        self.assertEqual(list(helper.state.glob("provider-call-*")), [])

    def test_failed_call_reservation_prevents_directory_and_child(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        with patch.object(BridgeStore, "reserve", side_effect=OSError("call intent refused")):
            with self.assertRaisesRegex(OSError, "call intent refused"):
                broker.reconcile(helper.request)
        self.assertEqual(list(helper.state.glob("provider-call-*")), [])
        self.assertFalse((code / "fixture-service.json").exists())

    def test_timeout_output_limit_and_unrelated_response_remain_uncertain(self):
        for mode in ("hang", "flood", "wrong-id", "malformed"):
            with self.subTest(mode=mode):
                helper, plan, commit, broker, bridge, qualifier, code = self.fixture(timeout_seconds=.15 if mode == "hang" else 3)
                (code / "mode").write_text(mode)
                with self.assertRaises(Refused):
                    broker.reconcile(helper.request)
                rows = self.calls(helper)
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["stage"], "uncertain")
                result = json.loads(rows[0]["result"])
                self.assertTrue(result["quiescence"]["quiescent"])
                expected = "timeout" if mode == "hang" else ("output_limit_or_io_error" if mode == "flood" else "exited")
                self.assertEqual(result["job"]["reason"], expected)
                self.assertFalse((code / "fixture-service.json").exists())

    def test_source_and_deadline_rechecked_immediately_before_creation(self):
        for kind in ("source", "deadline"):
            with self.subTest(kind=kind):
                helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
                def checkpoint(phase):
                    if phase != "before_create":
                        return
                    if kind == "source":
                        (code / "bridge.py").write_text(FIXTURE_BRIDGE + "\n# drift\n", encoding="utf-8")
                    elif broker.ledger.get(digest(helper.request))["stage"] == "apply_intent":
                        broker.now = lambda: 2001
                bridge.checkpoint = checkpoint
                with self.assertRaises(Refused):
                    broker.reconcile(helper.request)
                self.assertFalse((code / "fixture-service.json").exists())
                rows = self.calls(helper)
                self.assertEqual(rows[-1]["stage"], "uncertain")
                self.assertEqual(sum(row["operation"] != "observe" for row in rows), kind == "deadline")
                starts = json.loads((code / "fixture-starts.json").read_text()) if (code / "fixture-starts.json").exists() else []
                self.assertEqual([entry["operation"] for entry in starts], ["observe", "observe"] if kind == "deadline" else [])

    def test_inflight_qualification_and_expiry_stop_owned_mutation_child(self):
        for kind in ("qualification", "deadline"):
            with self.subTest(kind=kind):
                helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
                (code / "mode").write_text("hang:publish_objects")
                timers = []
                def checkpoint(phase):
                    if phase == "resumed" and broker.ledger.get(digest(helper.request))["stage"] == "apply_intent":
                        def revoke():
                            if kind == "qualification":
                                qualifier.allowed = False
                            else:
                                broker.now = lambda: 2001
                        timer = threading.Timer(.1, revoke)
                        timers.append(timer)
                        timer.start()
                bridge.checkpoint = checkpoint
                with self.assertRaises(Refused):
                    broker.reconcile(helper.request)
                for timer in timers:
                    timer.join(2)
                row = self.calls(helper)[-1]
                self.assertEqual(row["stage"], "uncertain")
                result = json.loads(row["result"])
                self.assertTrue(result["quiescence"]["quiescent"])
                self.assertEqual(result["job"]["reason"], "cancelled")
                self.assertFalse((code / "fixture-service.json").exists())

    def test_lost_mutation_reply_advances_later_stage_without_repeating(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        (code / "mode").write_text("lose:publish_objects")
        with self.assertRaises(Refused):
            broker.reconcile(helper.request)
        (code / "mode").write_text("")
        broker.reconcile(helper.request)
        state = json.loads((code / "fixture-service.json").read_text())
        self.assertEqual(state["effects"], ["publish_objects", "create_branch"])
        rows = self.calls(helper)
        self.assertEqual(sum(row["operation"] == "publish_objects" for row in rows), 1)
        self.assertEqual(next(row for row in rows if row["operation"] == "publish_objects")["stage"], "uncertain")

    def test_read_attempt_tokens_cannot_be_reused_or_fabricated(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        broker.prepare(helper.request)
        bridge.assert_current(broker, helper.request, plan, "observe")
        with closing(ObservationStore(helper.state)) as store:
            store.reserve(plan)
            attempt = store.observation_attempt(plan)
        bridge.observe(plan, attempt=attempt)
        for value in (attempt, True, attempt + 100):
            with self.subTest(attempt=value), self.assertRaises(Refused):
                bridge.observe(plan, attempt=value)
        self.assertEqual(len(self.calls(helper)), 1)

    def test_call_and_retained_io_budgets_refuse_before_more_children(self):
        for limits in ({"max_calls": 1}, {"max_io_bytes": 1}):
            with self.subTest(limits=limits):
                helper, plan, commit, broker, bridge, qualifier, code = self.fixture(**limits)
                with self.assertRaisesRegex(Refused, "budget exhausted"):
                    broker.reconcile(helper.request)
                self.assertEqual(len(self.calls(helper)), 1 if "max_calls" in limits else 0)
                self.assertFalse((code / "fixture-service.json").exists())

    def test_provider_lock_does_not_alias_supervisor_and_blocks_a_second_provider(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        with supervisor_lock(helper.state):
            with supervisor_lock(helper.state, scope="provider-bridge"):
                with self.assertRaisesRegex(Refused, "another supervisor"):
                    with supervisor_lock(helper.state, scope="provider-bridge"):
                        self.fail("duplicate provider lock")
        with self.assertRaisesRegex(Refused, "unknown owned lock"):
            with supervisor_lock(helper.state, scope="../escape"):
                self.fail("unsafe lock scope")

    def test_actual_supervisor_death_fences_exact_job_and_never_replays_mutation(self):
        helper, plan, commit, broker, bridge, qualifier, code = self.fixture()
        (code / "mode").write_text("hang:publish_objects")
        config = helper.root / "supervisor-fixture.json"
        config.write_text(json.dumps({"state": str(helper.state), "exchange": str(helper.exchange), "repo": str(helper.repo),
                         "git": str(helper.git.executable), "git_sha": helper.git.sha256,
                         "authority": helper.authority, "request": helper.request,
                         "registration": str(bridge.path), "registration_sha": bridge.pin,
                         "plan": plan, "commit": commit.decode()}), encoding="utf-8")
        script = r"""
import json, os, sys
from pathlib import Path
from core.runtime.integration_broker.common import Git, digest
from core.runtime.integration_broker.service import Broker
from core.runtime.integration_broker.staged_transport import StagedTransport
from core.runtime.integration_broker.registered_bridge import RegisteredBridge
c=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
class FixtureQualification:
    def assert_current(self,*args): pass
bridge=RegisteredBridge(c['registration'],c['registration_sha'],c['plan'],qualifier=FixtureQualification())
broker=Broker(c['state'],c['exchange'],c['repo'],Git(c['git'],c['git_sha']),c['authority'],
              transport=StagedTransport(c['plan'],c['commit'].encode(),adapter=bridge),now=lambda:1000)
def checkpoint(phase):
    if phase=='resumed' and broker.ledger.get(digest(c['request']))['stage']=='apply_intent': os._exit(72)
bridge.checkpoint=checkpoint
broker.reconcile(c['request'])
"""
        result = subprocess.run([sys.executable, "-B", "-c", script, str(config)], cwd=ROOT,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        self.assertEqual(result.returncode, 72, result.stdout.decode(errors="replace"))
        (code / "mode").write_text("")
        self.assertEqual(broker.reconcile(helper.request)["status"], "pending")
        mutation = [row for row in self.calls(helper) if row["operation"] == "publish_objects"]
        self.assertEqual(len(mutation), 1)
        self.assertEqual(mutation[0]["stage"], "uncertain")
        self.assertTrue(json.loads(mutation[0]["result"])["recovery"]["quiescent"])
        self.assertFalse((code / "fixture-service.json").exists())


if __name__ == "__main__":
    unittest.main()
