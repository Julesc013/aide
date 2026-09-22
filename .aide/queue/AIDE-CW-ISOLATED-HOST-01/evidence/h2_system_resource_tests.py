"""Injected resource tests; no native constructor, selected mapping or child."""
from dataclasses import replace
import copy
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0, str(HERE))
import h2_system_input_tests as n1
import h2_system_resource as r
import h2_system_resource_controller as c


def n1_observation():
    api=n1.FakeRead(); clock=n1.Clock()
    def hook(stage,handle):
        if stage=='open_file' and handle==11+r.NAMES.index('kernelbase.dll'):
            api.values[handle]=replace(api.values[handle],path=api.values[handle].path.replace('kernelbase.dll','KernelBase.dll'))
    api.hook=hook
    return json.loads(n1.read.ReadProbe(n1.read.ReadPlan.read(n1.value()),api,lambda:True,
                                      clock=clock.tick,wall=clock.utc).run())


def plan(): return c.plan_from_n1(n1_observation(),'2'*32,1100.0)


def transfer_value():
    p=plan(); effect='e'*64
    return {'schema':'aide.host.system-resource-transfer.v1','plan':p.value(),'effect_sha256':effect,
            'observed_paths':{row['name']:row['facts']['path'] for row in n1_observation()['files']},
            'reservation_line_sha256':r.line_sha(r.reservation_record(p,effect)),
            'intent_line_sha256s':[r.line_sha(row) for row in r.mapping_intents(p)]}


class FakeResource(n1.FakeRead):
    def __init__(self):
        super().__init__(); self.maps=[]; self.frees=[]; self.current_name=None
        self.resource_hook=lambda stage:None; self.handles=(0x10002,0x20002); self.bases=(0x30000,)
        self.native_refusal=None
    def open_file(self,parent,name):
        handle=super().open_file(parent,name)
        if name=='kernelbase.dll': self.values[handle]=replace(self.values[handle],path=self.values[handle].path.replace(name,'KernelBase.dll'))
        return handle
    def read_file(self,handle,count):
        self.hook('read',handle)
        offset=self.position.get(handle,0); self.position[handle]=offset+count
        return (bytes([handle-11])*64)[offset:offset+count]
    def executable_bases(self): self.resource_hook('bases'); return self.bases
    def map_resource(self,name):
        if len(self.opened)!=9 or self.closed: raise AssertionError('mapping outside all nine held read handles')
        self.current_name=name; self.maps.append(name); self.resource_hook('map')
        return self.handles[len(self.maps)-1]
    def mapped_name(self,address):
        self.resource_hook('mapped_name')
        name='kernelbase.dll' if self.current_name==r.API_NAMES[0] else 'ucrtbase.dll'
        return self.values[11+r.NAMES.index(name)].path
    def free_resource(self,handle):
        self.frees.append(handle); self.resource_hook('free'); return True


class TransferTests(unittest.TestCase):
    def test_exact_parent_paid_sequence_cannot_replay(self):
        t=r.Transfer.read(transfer_value()); journal=r.ParentPaidJournal(t)
        self.assertEqual(journal.reserve(t.plan.fingerprint),t.plan.fingerprint)
        for row in r.mapping_intents(t.plan): self.assertEqual(journal.intent(row),hashlib.sha256(r._canonical(row)).hexdigest())
        with self.assertRaises(r.Refused): journal.intent(r.mapping_intents(t.plan)[0])
        with self.assertRaises(r.Refused): journal.reserve(t.plan.fingerprint)
    def test_wrong_reservation_intent_or_sequence_invalidates_ticket(self):
        t=r.Transfer.read(transfer_value())
        journal=r.ParentPaidJournal(t)
        with self.assertRaises(r.Refused): journal.reserve('f'*64)
        with self.assertRaises(r.Refused): journal.reserve(t.plan.fingerprint)
        for change in ({'sequence':True},{'sequence':1},{'api_name':r.API_NAMES[1]},{'flags':0},{'plan_sha256':'f'*64}):
            journal=r.ParentPaidJournal(t); journal.reserve(t.plan.fingerprint)
            with self.assertRaises(r.Refused): journal.intent(dict(r.mapping_intents(t.plan)[0],**change))
            with self.assertRaises(r.Refused): journal.intent(r.mapping_intents(t.plan)[0])
    def test_transfer_wrong_missing_paid_lines_and_target_bounds(self):
        mutations=[lambda v:v.update(intent_line_sha256s=[]),lambda v:v.update(reservation_line_sha256='f'*64),
                   lambda v:v['intent_line_sha256s'].__setitem__(0,'f'*64),
                   lambda v:v['plan'].update(api_names=[r.API_NAMES[0]]),
                   lambda v:v['plan'].update(max_seconds=26),lambda v:v['plan'].update(files=[]),
                   lambda v:v['observed_paths'].update({'kernelbase.dll':r'\Device\HarddiskVolume4\Windows\System32\KernelBase.dll'})]
        for mutate in mutations:
            value=transfer_value(); mutate(value)
            with self.assertRaises(r.Refused): r.Transfer.read(value)
    def test_changed_frozen_transfer_and_early_intent_refuse(self):
        t=r.Transfer.read(transfer_value())
        with self.assertRaises(r.Refused): replace(t,intent_lines=('a'*64,'b'*64)).validate()
        journal=r.ParentPaidJournal(t)
        with self.assertRaises(r.Refused): journal.intent(r.mapping_intents(t.plan)[0])
        with self.assertRaises(r.Refused): journal.reserve(t.plan.fingerprint)


class ProbeTests(unittest.TestCase):
    def make(self):
        self.clock=n1.Clock(); self.api=FakeResource(); self.transfer=r.Transfer.read(transfer_value())
        self.guard=r.Deadline(self.transfer.plan.expires_at,clock=self.clock.tick,wall=self.clock.utc)
        self.probe=r.ResourceProbe(self.transfer,self.api,self.guard,clock=self.clock.tick,wall=self.clock.utc)
    def refuse(self):
        with self.assertRaises(r.Refused): self.probe.run()
        self.assertEqual(sorted(self.api.closed),sorted(self.api.opened))
        self.assertIsNotNone(self.probe.failure)
        with self.assertRaises(r.Refused): self.probe.run()
    def test_two_exact_resource_hosts_preserve_case_and_all_handles(self):
        self.make(); value=json.loads(self.probe.run()); result=value['observation']
        self.assertEqual(self.api.maps,list(r.API_NAMES)); self.assertEqual(self.api.frees,[0x10002,0x20002])
        self.assertEqual(len(self.api.closed),9); self.assertEqual(value['paid_intents_consumed'],2)
        self.assertEqual(result['mappings'][0]['mapped_path'].split('\\')[-1],'KernelBase.dll')
        self.assertFalse(result['loader_qualified']); self.assertFalse(value['operational_activation'])
        self.assertEqual(r.validate_result(r._canonical(value),self.transfer),value)
    def test_native_environment_refuses_before_file_open_or_map(self):
        self.make(); old=self.api.environment
        self.api.environment=lambda:dict(old(),native_machine=0xAA64)
        self.refuse(); self.assertEqual(self.api.opened,[]); self.assertEqual(self.api.maps,[])
    def test_unknown_backing_wrong_case_and_new_executable_origin_refuse(self):
        for kind in ('backing','case','origin','tag'):
            self.make()
            if kind=='backing': self.api.mapped_name=lambda address:r'\Device\HarddiskVolume3\Windows\System32\other.dll'
            if kind=='case': self.api.mapped_name=lambda address:self.transfer.plan.native_root+r'\KERNELBASE.DLL'
            if kind=='origin': self.api.handles=(0x10000,0x20002)
            if kind=='tag': self.api.handles=(0x10003,0x20002)
            self.refuse(); self.assertEqual(len(self.api.frees),1)
    def test_prior_executable_requires_current_base_and_is_released(self):
        self.make(); self.api.handles=(0x30000,0x20002)
        value=json.loads(self.probe.run())
        self.assertEqual(value['observation']['mappings'][0]['mapping_kind'],'prior_executable')
        self.assertEqual(self.api.frees,[0x30000,0x20002])
    def test_expiry_after_acquisition_or_release_refuses_without_repeat(self):
        for stage in ('map','free'):
            self.make(); self.api.resource_hook=lambda current:setattr(self.clock,'wall',1100.0) if current==stage else None
            self.refuse(); self.assertEqual(len(self.api.maps),1); self.assertEqual(len(self.api.frees),1)
    def test_release_failure_closes_reads_and_retains_uncertainty(self):
        self.make()
        def hook(stage):
            if stage=='free': raise OSError('synthetic release')
        self.api.resource_hook=hook; self.refuse()
        self.assertEqual(len(self.probe.session.release_failures),1); self.assertEqual(len(self.api.frees),1)
    def test_final_cleanup_and_serialization_expiry_refuse(self):
        self.make(); self.api.hook=lambda stage,handle:setattr(self.clock,'mono',126.0) if stage=='close' and handle==10 else None
        self.refuse()
        self.make(); original=r._canonical
        def serialize(value):
            data=original(value)
            if isinstance(value,dict) and value.get('schema')=='aide.host.system-resource-result.v1': self.clock.wall=1100.0
            return data
        with mock.patch.object(r,'_canonical',side_effect=serialize): self.refuse()
    def test_root_or_descriptor_drift_before_mapping_refuses(self):
        self.make()
        self.api.hook=lambda stage,handle:self.api.values.__setitem__(handle,replace(self.api.values[handle],security_sha256='f'*64)) if stage=='open_file' else None
        self.refuse(); self.assertEqual(self.api.maps,[])
    def test_child_output_bounds_and_forged_wire_results_refuse(self):
        self.make()
        with mock.patch.object(r,'MAX_OUTPUT',64): self.refuse()
        self.make(); valid=json.loads(self.probe.run())
        mutations=[lambda v:v.update(paid_intents_consumed=True),lambda v:v.update(operational_activation=True),
                   lambda v:v['observation'].update(mapping_attempts=True),lambda v:v['observation'].update(mappings=[]),
                   lambda v:v['observation'].update(api_context_qualified=True),
                   lambda v:v['observation']['mappings'][0].update(sha256='f'*64),
                   lambda v:v['observation']['mappings'][0].update(identity=[True,'a'*32]),
                   lambda v:v['observation']['files'][0].update(links=True)]
        for mutate in mutations:
            value=copy.deepcopy(valid); mutate(value)
            with self.assertRaises(r.Refused): r.validate_result(r._canonical(value),self.transfer)
    def test_native_failed_load_preserves_code_and_never_falls_back(self):
        api=r.NativeResourceApi.__new__(r.NativeResourceApi); api._load=mock.Mock(return_value=0)
        with mock.patch.object(r.obs.C,'get_last_error',return_value=126):
            with self.assertRaises(r.Refused): api.map_resource(r.API_NAMES[0])
        api._load.assert_called_once_with(r.API_NAMES[0],None,0x860)
        self.assertEqual(api.native_refusal,{'operation':'LoadLibraryExW','api_name':r.API_NAMES[0],'flags':0x860,'win32_error':126})
        with self.assertRaises(r.Refused): api.map_resource('api-ms-win-core-other-l1-1-0.dll')
        self.assertEqual(api._load.call_count,1)


def effect():
    value=n1.effect(); value['schema']='aide.host.system-resource-effect.v1'; value['source_base']=c.BASE
    value['source_files']=dict.fromkeys(c.SOURCES,'a'*64); value['source_files'][c.ARCHIVE]=c.ARCHIVE_SHA
    value['plan']=plan().value(); value['observed_paths']=transfer_value()['observed_paths']; value['effects']['selected_mappings']=2
    return value


class FakeParent(n1.FakeControl):
    def run_child(self,args,**kw):
        self.kw=kw; self.args=args; self.hook('host_enter'); kw['checkpoint']('before_create')
        if len(self.rows)!=3: raise AssertionError('all three durable rows must precede creation')
        self.dispatched+=1; self.events.append('dispatch')
        self.hook('created_suspended'); kw['checkpoint']('created_suspended')
        self.hook('resumed'); kw['checkpoint']('resumed')
        self.hook('running')
        if kw['cancelled'](): raise r.Refused('cancelled')
        self.hook('reply')
        transfer=r.Transfer.read(r.decode(kw['input_bytes'])); clock=n1.Clock(); api=FakeResource()
        guard=r.Deadline(transfer.plan.expires_at,clock=clock.tick,wall=clock.utc)
        self.bytes=r.ResourceProbe(transfer,api,guard,clock=clock.tick,wall=clock.utc).run()
        return {'exit_code':0,'reason':'exited','quiescent':True,'bytes':len(self.bytes),'io_errors':[],'job_id':kw['job_id']}


class ControllerTests(unittest.TestCase):
    def make(self):
        self.clock=n1.Clock(); self.api=FakeParent()
        self.controller=c.Controller(effect(),self.api,clock=self.clock.tick,wall=self.clock.utc)
    def test_reservation_and_both_intents_persist_before_owned_child(self):
        self.make(); value=self.controller.run(); self.assertEqual(value['result'],'PASS')
        self.assertEqual([row['schema'] for row in self.api.rows[:3]],['aide.host.system-resource-reservation.v1',
            'aide.host.system-mapping-intent.v1','aide.host.system-mapping-intent.v1'])
        self.assertEqual([row['api_name'] for row in self.api.rows[1:3]],list(r.API_NAMES))
        self.assertEqual(self.api.kw['timeout'],30); self.assertNotIn('security',self.api.kw)
        self.assertEqual(self.api.rows[3]['final_controller_status'],'pending_final_guard')
        with self.assertRaises(r.Refused): self.controller.run()
    def test_each_failed_durable_row_prevents_dispatch(self):
        for failure in range(3):
            self.make()
            def hook(stage):
                if stage=='append' and len(self.api.rows)==failure: raise OSError('synthetic durable failure')
            self.api.hook=hook
            with self.assertRaises(r.Refused): self.controller.run()
            self.assertTrue(self.api.reserved); self.assertEqual(self.api.dispatched,0)
            with self.assertRaises(r.Refused): self.controller.run()
    def test_expiry_at_each_creation_boundary_refuses(self):
        for stage,created in (('append',0),('host_enter',0),('created_suspended',1),('resumed',1),('running',1)):
            self.make(); self.api.hook=lambda current:setattr(self.clock,'wall',1100.0) if current==stage else None
            with self.assertRaises(r.Refused): self.controller.run()
            self.assertEqual(self.api.dispatched,created)
    def test_wrong_ack_restarted_intent_and_source_refusal_prevent_dispatch(self):
        self.make(); self.api.append=lambda *_:'f'*64
        with self.assertRaises(r.Refused): self.controller.run()
        self.assertEqual(self.api.dispatched,0)
        self.make(); self.api.reserved=True
        with self.assertRaises(r.Refused): self.controller.run()
        self.assertEqual(self.api.dispatched,0)
        self.make(); self.api.verify=lambda _:False
        with self.assertRaises(r.Refused): self.controller.run()
        self.assertFalse(self.api.reserved)
    def test_lost_reply_malformed_output_and_final_guard_cannot_retry(self):
        for stage in ('reply','output','parent_close'):
            self.make()
            def hook(current):
                if current==stage: raise OSError('synthetic lost reply or close')
            self.api.hook=hook
            with self.assertRaises(r.Refused): self.controller.run()
            self.assertEqual(self.api.dispatched,1)
            with self.assertRaises(r.Refused): self.controller.run()
        self.make(); self.api.output=lambda _:b'null'
        with self.assertRaises(r.Refused): self.controller.run()
    def test_effect_capacity_names_and_types_never_broaden(self):
        for mutate in (lambda v:v['effects'].update(selected_mappings=3),lambda v:v['effects'].update(ordinary_children=True),
                       lambda v:v['limits'].update(child_seconds=31),lambda v:v['plan'].update(api_names=[r.API_NAMES[0]]),
                       lambda v:v['source_files'].update({c.ARCHIVE:'f'*64})):
            value=effect(); mutate(value)
            with self.assertRaises(r.Refused): c.read_effect(value)
    def test_archived_n1_bytes_bind_derived_actual_pins_without_native_calls(self):
        raw=(c.previous.REPOSITORY/c.ARCHIVE).read_bytes(); observation=c.audited_n1(raw)
        derived=c.plan_from_n1(observation,'4'*32,1100.0)
        self.assertEqual(sum(pin.size for pin in derived.files),8306752)
        self.assertEqual(observation['files'][3]['facts']['path'].split('\\')[-1],'KernelBase.dll')
        for bad in (raw[:-1],b'bad',raw+b'x'):
            with self.assertRaises(r.Refused): c.audited_n1(bad)
        e=effect(); e['plan']=derived.value(); e['observed_paths']={row['name']:row['facts']['path'] for row in observation['files']}
        with mock.patch.object(c.previous.NativeController,'verify',return_value=None):
            parent=c.NativeParent(); parent.verify(e)
            e['plan']['files'][0]['sha256']='f'*64
            with self.assertRaises(r.Refused): parent.verify(e)


if __name__=='__main__': unittest.main(verbosity=2)
