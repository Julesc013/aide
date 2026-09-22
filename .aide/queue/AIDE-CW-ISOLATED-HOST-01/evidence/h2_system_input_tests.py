"""Injected tests only: never construct native adapters or launch a real child."""
from contextlib import contextmanager
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import h2_system_input as read
import h2_system_input_controller as control


class Clock:
    mono = 100.0
    wall = 1000.0
    def tick(self): return self.mono
    def utc(self): return self.wall


def value():
    return {'schema': 'aide.host.system-input.v1', 'request_id': '1' * 32,
            'expires_at': 1100.0, 'system_directory': r'C:\Windows\System32',
            'native_root': r'\Device\HarddiskVolume3\Windows\System32',
            'files': [{'name': name, 'size': 64, 'sha256': hashlib.sha256(bytes([i]) * 64).hexdigest()}
                      for i, name in enumerate(read.NAMES)]}


class FakeRead:
    def __init__(self):
        self.plan = read.ReadPlan.read(value())
        self.events = []; self.opened = []; self.closed = []; self.position = {}
        self.values = {10: read.ObjectFacts(self.plan.native_root, (9, 'a' * 32), True, False,
                                          0, 1, 'S-1-5-18', 'b' * 64)}
        self.hook = lambda stage, handle: None
        self.fact_counts = {}
    def environment(self):
        self.hook('environment', 0)
        return {'system_directory': self.plan.system_directory, 'native_root': self.plan.native_root,
                'process_machine': 0, 'native_machine': 0x8664}
    def open_root(self, name):
        self.events.append('open_root'); self.opened.append(10); return 10
    def open_file(self, parent, name):
        if parent != 10: raise AssertionError('wrong parent')
        handle = 11 + read.NAMES.index(name)
        self.opened.append(handle); self.position[handle] = 0
        self.values[handle] = read.ObjectFacts(self.plan.native_root + '\\' + name,
            (9, format(handle, '032x')), False, False, 64, 2, 'S-1-5-18', 'b' * 64)
        self.hook('open_file', handle)
        return handle
    def facts(self, handle):
        self.fact_counts[handle] = self.fact_counts.get(handle, 0) + 1
        self.hook('facts', handle)
        return self.values[handle]
    def read_file(self, handle, count):
        if len(self.opened) != 9 or self.closed: raise AssertionError('read outside nine held leases')
        self.events.append('read'); self.hook('read', handle)
        if self.position[handle] == 64: return b''
        self.position[handle] = 64
        return bytes([handle - 11]) * 64
    def close_file(self, handle):
        if handle in self.closed: raise AssertionError('double close')
        self.closed.append(handle); self.hook('close', handle); return True


class ProbeTests(unittest.TestCase):
    def make(self, api=None, guard=lambda: True):
        self.clock = Clock(); self.api = api or FakeRead()
        self.probe = read.ReadProbe(read.ReadPlan.read(value()), self.api, guard,
                                   clock=self.clock.tick, wall=self.clock.utc)
        return self.probe
    def assert_refusal(self):
        with self.assertRaises(read.Refused): self.probe.run()
        self.assertEqual(sorted(self.api.closed), sorted(self.api.opened))
        self.assertIsNotNone(self.probe.failure)
        with self.assertRaises(read.Refused): self.probe.run()
    def test_exact_success_holds_every_file_through_reobservation(self):
        self.make(); result = json.loads(self.probe.run())
        self.assertEqual(result['result'], 'PASS'); self.assertEqual(len(result['files']), 8)
        self.assertEqual(self.api.closed, list(reversed(self.api.opened)))
        self.assertTrue(all(count == 2 for count in self.api.fact_counts.values()))
        self.assertTrue(all(result[key] is False for key in ('system_ownership_qualified',
            'api_context_qualified', 'loader_qualified', 'operational_activation')))
        self.assertEqual([row['facts']['links'] for row in result['files']], [2] * 8)
    def test_json_duplicate_scalar_nonfinite_and_limits(self):
        for data in (b'{"a":1,"a":2}', b'NaN', b'Infinity', b'\xff', b'[' * 3000, b'x' * (read.MAX_INPUT + 1)):
            with self.subTest(data=data[:20]), self.assertRaises(read.Refused): read.decode(data)
        for data in (b'null', b'1', b'[]', b'true'):
            with self.subTest(data=data), self.assertRaises(read.Refused): read.ReadPlan.read(read.decode(data))
    def test_exact_plan_names_and_temporal_fields(self):
        cases=[]
        for expiry in (True, float('nan'), float('inf'), 10**1000, 0):
            p=value(); p['expires_at']=expiry; cases.append(p)
        for name in ('other.dll', '../ntdll.dll', 'NTDLL.DLL', 'api-ms-win-core-path-l1-1-0.dll'):
            p=value(); p['files'][0]['name']=name; cases.append(p)
        p=value(); p['files'][0]=p['files'][1].copy(); cases.append(p)
        for size in (True, 63, read.MAX_FILE+1):
            p=value(); p['files'][0]['size']=size; cases.append(p)
        p=value(); p['system_directory']=r'C:\Windows\SysWOW64'; cases.append(p)
        for p in cases:
            with self.subTest(p=str(p)[:100]), self.assertRaises(read.Refused): read.ReadPlan.read(p)
    def test_wrong_environment_refuses_before_open(self):
        for key,item in (('native_machine',0xAA64), ('process_machine',0x8664),
                         ('native_root',r'\Device\HarddiskVolume4\Windows\System32')):
            self.make(); original=self.api.environment
            self.api.environment=lambda: dict(original(), **{key:item})
            self.assert_refusal(); self.assertEqual(self.api.opened, [])
    def test_short_oversized_nonbyte_changed_hash_and_eof(self):
        for replacement in (b'x'*63, b'x'*65, bytearray(64), b'x'*64):
            self.make(); self.api.read_file=lambda handle,count:replacement; self.assert_refusal()
        self.make(); original=self.api.read_file
        self.api.read_file=lambda handle,count: b'x' if count==1 else original(handle,count)
        self.assert_refusal()
    def test_file_facts_refuse_changed_identity_descriptor_and_path(self):
        for key,item in (('identity',(9,'e'*32)), ('owner_sid','S-1-5-19'),
                         ('security_sha256','c'*64), ('path',value()['native_root']+'\\NTDLL.DLL')):
            self.make()
            def hook(stage, handle):
                if stage=='facts' and handle==11 and self.api.fact_counts[handle]==2:
                    self.api.values[handle]=replace(self.api.values[handle], **{key:item})
            self.api.hook=hook; self.assert_refusal()
    def test_invalid_file_kind_links_volume_and_duplicate_identity(self):
        for key,item in (('directory',True),('delete_pending',True),('links',0),('links',1025),
                         ('size',65),('identity',(10,'f'*32)),('identity',(9,'a'*32))):
            self.make()
            self.api.hook=lambda stage,handle: self.api.values.__setitem__(handle,
                replace(self.api.values[handle],**{key:item})) if stage=='open_file' else None
            self.assert_refusal()
    def test_root_change_and_mapping_change_refuse(self):
        self.make()
        def hook(stage,handle):
            if stage=='facts' and handle==10 and self.api.fact_counts[handle]==2:
                self.api.values[handle]=replace(self.api.values[handle],security_sha256='d'*64)
        self.api.hook=hook; self.assert_refusal()
        self.make(); count=0; original=self.api.environment
        def env():
            nonlocal count
            count+=1; out=original()
            if count==2: out['native_root']=out['native_root'].replace('Volume3','Volume4')
            return out
        self.api.environment=env; self.assert_refusal()
    def test_all_acquired_handles_close_when_post_acquire_guard_expires(self):
        self.make()
        self.api.hook=lambda stage,handle: setattr(self.clock,'wall',1100.0) if stage=='open_file' else None
        self.assert_refusal(); self.assertEqual(self.api.closed,[11,10])
    def test_final_cleanup_freshness_and_nonfinite_initial_clock(self):
        for attr,item in (('mono',126.0),('wall',1100.0),('mono',99.0),('mono',float('nan'))):
            self.make()
            self.api.hook=lambda stage,handle: setattr(self.clock,attr,item) if stage=='close' and handle==10 else None
            self.assert_refusal()
        self.make(); self.clock.mono=float('nan'); self.assert_refusal(); self.assertEqual(self.api.opened,[])
    def test_guard_refusal_and_guard_expiry_prevent_native_dispatch(self):
        self.make(guard=lambda:False); self.assert_refusal(); self.assertEqual(self.api.opened,[])
        self.make(guard=lambda:setattr(self.clock,'wall',1100.0)); self.assert_refusal()
        self.assertEqual(self.probe.calls,0)
    def test_final_guard_revocation_refuses_after_cleanup(self):
        revoked=False
        self.make(guard=lambda:not revoked)
        def hook(stage,handle):
            nonlocal revoked
            if stage=='close' and handle==10: revoked=True
        self.api.hook=hook; self.assert_refusal()
    def test_release_failure_never_repeats_but_closes_other_handles(self):
        self.make()
        def hook(stage,handle):
            if stage=='close' and handle==15: raise OSError('injected')
        self.api.hook=hook; self.assert_refusal(); self.assertEqual(self.probe.release_failures,['OSError'])
    def test_adapter_call_and_result_bounds(self):
        self.make(); self.probe.calls=read.MAX_CALLS; self.assert_refusal(); self.assertEqual(self.api.opened,[])
        self.make()
        with mock.patch.object(read,'MAX_OUTPUT',32): self.assert_refusal()
    def test_native_facade_cannot_map_or_enumerate_executables(self):
        self.assertFalse(any(hasattr(read.ReadOnlyApi,name) for name in
            ('map_resource','free_resource','mapped_name','executable_bases','_load','_free')))
        self.assertIs(read.ReadOnlyApi.facts, read.NativeSystemApi.facts)

    def test_wire_result_rejects_missing_files_false_identity_and_overclaims(self):
        self.make(); valid=json.loads(self.probe.run())
        for mutation in (lambda v:v.update(files=[]), lambda v:v.update(root=None),
                         lambda v:v.update(calls=True), lambda v:v.update(close_attempts=True),
                         lambda v:v.update(loader_qualified=True),
                         lambda v:v['files'][0].update(sha256='f'*64),
                         lambda v:v['files'][1]['facts'].update(identity=v['files'][0]['facts']['identity']),
                         lambda v:v['files'][0]['facts'].update(links=1025)):
            candidate=json.loads(json.dumps(valid)); mutation(candidate)
            with self.assertRaises(read.Refused): read.validate_result(read._canonical(candidate), self.probe.plan)
        self.assertEqual(read.validate_result(read._canonical(valid),self.probe.plan),valid)


class NativeBindingInjectedTests(unittest.TestCase):
    def fake(self, *, machine=0x8664, process=0, path=r'C:\Windows\System32', count=None):
        api=read.ReadOnlyApi.__new__(read.ReadOnlyApi)
        def wow(handle,p,m):
            read.C.cast(p,read.C.POINTER(read.W.WORD))[0]=process
            read.C.cast(m,read.C.POINTER(read.W.WORD))[0]=machine
            return True
        def directory(buffer,length):
            buffer.value=path
            return len(path) if count is None else count
        api._wow=wow; api._directory=directory; api._process=lambda:1
        return api
    def test_architecture_requires_native_amd64_before_path_mapping(self):
        for machine,process in ((0xAA64,0),(0x8664,0x14c),(0x8664,0x8664)):
            with mock.patch.object(read.native,'native_path') as path:
                with self.assertRaises(read.Refused): self.fake(machine=machine,process=process).environment()
                path.assert_not_called()
    def test_missing_or_truncated_directory_never_uses_path_mapping(self):
        for count in (0,260,261):
            with mock.patch.object(read.native,'native_path') as path:
                with self.assertRaises(read.Refused): self.fake(count=count).environment()
                path.assert_not_called()
    def test_exact_observed_directory_passed_to_native_volume_resolver(self):
        with mock.patch.object(read.native,'native_path',return_value=value()['native_root']) as path:
            actual=self.fake().environment()
        path.assert_called_once_with(r'C:\Windows\System32')
        self.assertEqual(actual['native_machine'],0x8664)
        self.assertEqual(actual['native_root'],value()['native_root'])


def effect():
    return {'schema':'aide.host.system-input-effect.v1','source_base':control.BASE,
            'repository':str(control.REPOSITORY),'source_files':dict.fromkeys(control.SOURCES,'a'*64),
            'interpreter':{'path':control.PYTHON,'size':1000,'sha256':'a'*64},'user_sid':control.USER,
            'output_parent':{'path':control.PARENT,'identity':{'volume':9,'file_id':'a'*32},
                             'owner_marker':'owner.json','owner_sha256':'a'*64},'plan':value(),
            'limits':{'child_seconds':30,'child_memory':268435456,'child_processes':1,'output_bytes':read.MAX_OUTPUT},
            'effects':{'ordinary_children':1,'read_files':8,'selected_mappings':0,'profile_creations':0,
                       'acl_changes':0,'network_calls':0,'cleanup':'retain_only','operational_activation':False}}


class FakeControl:
    def __init__(self):
        self.events=[]; self.rows=[]; self.closed=[]; self.bytes=None
        self.hook=lambda stage:None; self.reserved=False; self.dispatched=0
    def verify(self,effect): self.hook('verify')
    @contextmanager
    def parent(self,effect,guard):
        self.check=guard
        try: yield self
        finally: self.closed.append('parent'); self.hook('parent_close')
    @contextmanager
    def reserve(self,path,parent,guard):
        if self.reserved: raise read.Refused('existing reserved attempt')
        self.hook('reserve'); self.reserved=True; self.events.append('reserve')
        try: yield self
        finally: self.closed.append('journal')
    def append(self,stream,row):
        self.hook('append'); self.rows.append(row); self.events.append('durable_intent')
        return hashlib.sha256(read._canonical(row)+b'\n').hexdigest()
    def run_child(self,args,**kw):
        self.kw=kw; self.args=args
        self.hook('host_enter'); kw['checkpoint']('before_create')
        self.dispatched+=1; self.events.append('dispatch')
        self.hook('running')
        if kw['cancelled'](): raise read.Refused('cancelled')
        self.hook('reply')
        clock=Clock(); fake=FakeRead()
        self.bytes=read.ReadProbe(read.ReadPlan.read(value()),fake,lambda:True,
                                  clock=clock.tick,wall=clock.utc).run()
        return {'exit_code':0,'reason':'exited','quiescent':True,'bytes':len(self.bytes),
                'io_errors':[],'job_id':kw['job_id']}
    def output(self,path): self.hook('output'); return self.bytes


class ControllerTests(unittest.TestCase):
    def make(self):
        self.clock=Clock(); self.api=FakeControl()
        self.controller=control.Controller(effect(),self.api,clock=self.clock.tick,wall=self.clock.utc)
    def test_durable_intent_before_exact_bounded_child_and_no_replay(self):
        self.make(); result=self.controller.run(); self.assertEqual(result['result'],'PASS')
        self.assertLess(self.api.events.index('durable_intent'),self.api.events.index('dispatch'))
        self.assertEqual(self.api.args[1:4],['-I','-S','-B'])
        self.assertEqual(self.api.kw['timeout'],30); self.assertEqual(self.api.kw['process_limit'],1)
        self.assertNotIn('security',self.api.kw)
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertEqual(self.api.dispatched,1)
    def test_bad_schema_limits_source_set_parent_refuse_before_effect(self):
        for field,item in (('source_base','b'*40),('user_sid','S-1-5-18'),('source_files',{}),
                           ('effects',{}),('limits',None),('repository','other')):
            data=effect(); data[field]=item
            with self.subTest(field=field),self.assertRaises(read.Refused): control.read_effect(data)
        data=effect(); data['limits']['child_processes']=True
        with self.assertRaises(read.Refused): control.read_effect(data)
    def test_preflight_refusal_leaves_reservation_absent(self):
        self.make(); self.api.hook=lambda stage: (_ for _ in ()).throw(read.Refused('source')) if stage=='verify' else None
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertFalse(self.api.reserved); self.assertEqual(self.api.dispatched,0)
    def test_reservation_and_durable_write_uncertainty_never_dispatch(self):
        for stage in ('reserve','append'):
            self.make()
            self.api.hook=lambda observed: (_ for _ in ()).throw(OSError('injected')) if observed==stage else None
            with self.assertRaises(read.Refused): self.controller.run()
            self.assertEqual(self.api.dispatched,0)
            with self.assertRaises(read.Refused): self.controller.run()
        self.make(); self.api.append=lambda *_:'wrong'
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertTrue(self.api.reserved); self.assertEqual(self.api.dispatched,0)
    def test_restart_existing_intent_refuses_dispatch(self):
        self.make(); self.api.reserved=True
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertEqual(self.api.dispatched,0)
    def test_expiry_after_intent_and_immediately_before_creation(self):
        for stage in ('append','host_enter'):
            self.make(); self.api.hook=lambda observed:setattr(self.clock,'wall',1100.0) if observed==stage else None
            with self.assertRaises(read.Refused): self.controller.run()
            self.assertTrue(self.api.reserved); self.assertEqual(self.api.dispatched,0)
    def test_expiry_during_owned_child_cancels_without_replay(self):
        self.make(); self.api.hook=lambda stage:setattr(self.clock,'wall',1100.0) if stage=='running' else None
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertEqual(self.api.dispatched,1); self.assertTrue(self.controller.failure['consumed'])
    def test_lost_reply_and_malformed_output_are_terminal_consumed(self):
        for stage in ('reply','output'):
            self.make(); self.api.hook=lambda observed:(_ for _ in ()).throw(OSError('injected')) if observed==stage else None
            with self.assertRaises(read.Refused): self.controller.run()
            self.assertEqual(self.api.dispatched,1)
        for data in (b'',b'null',b'{}',b'{"result":"PASS"}'):
            self.make(); self.api.output=lambda _:data
            with self.assertRaises(read.Refused): self.controller.run()
    def test_mutated_admission_and_final_cleanup_expiry_refuse(self):
        self.make(); self.controller.effect['source_files'][control.SOURCES[0]]='f'*64
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertFalse(self.api.reserved)
        self.make(); self.api.hook=lambda stage:setattr(self.clock,'wall',1100.0) if stage=='parent_close' else None
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertEqual(self.api.closed,['journal','parent'])

    def test_final_evidence_is_provisional_until_post_cleanup_guard(self):
        self.make(); self.api.hook=lambda stage:setattr(self.clock,'wall',1100.0) if stage=='parent_close' else None
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertEqual(self.api.rows[-1]['final_controller_status'],'pending_final_guard')
        self.assertNotIn('result',self.api.rows[-1])
    def test_controller_observation_bound_and_clock_refuse(self):
        self.make(); self.controller.guard_calls=4096
        with self.assertRaises(read.Refused): self.controller.run()
        self.assertFalse(self.api.reserved)
        for field,item in (('wall',1100.0),('mono',float('nan')),('mono',99.0)):
            self.make(); setattr(self.clock,field,item)
            with self.assertRaises(read.Refused): self.controller.run()
            self.assertFalse(self.api.reserved)


if __name__=='__main__': unittest.main(verbosity=2)
