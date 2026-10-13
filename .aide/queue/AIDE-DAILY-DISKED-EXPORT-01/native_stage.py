"""Fixed offline native qualification stages; never execute a WorkUnit command."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib
import importlib.metadata
import json
from pathlib import Path
import unittest


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    deps, project, output = map(Path, sys.argv[1:4])
    stage = sys.argv[4]
    sys.path.insert(0, str(deps))
    sys.path.insert(0, str(project / 'spec/tools'))
    for module_name in ('yaml', 'jsonschema', 'attrs', 'referencing', 'rpds', 'typing_extensions'):
        module = importlib.import_module(module_name)
        assert Path(module.__file__).resolve().is_relative_to(deps.resolve())
    expected = json.loads((Path(__file__).parent / 'evidence/acquisition-result.json').read_text())
    versions = {}
    for wheel in expected['wheels']:
        distribution = importlib.metadata.distribution(wheel['name'])
        assert distribution.version == wheel['version']
        assert Path(distribution.locate_file('')).resolve() == deps.resolve()
        versions[wheel['name']] = distribution.version
    import specctl as native
    assert Path(native.__file__).resolve() == (project / 'spec/tools/specctl.py').resolve()
    if stage == 'tests':
        suite = unittest.defaultTestLoader.discover(str(project / 'spec/tools/tests'))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        counts = {'tests_run': result.testsRun, 'failures': len(result.failures),
                  'errors': len(result.errors), 'skips': len(result.skipped),
                  'skipped_cases': [{'test': case.id(), 'reason': reason} for case, reason in result.skipped],
                  'dependency_versions': versions}
        (output / 'native-test-counts.json').write_text(json.dumps(counts) + '\n', encoding='utf-8')
        return 0 if result.wasSuccessful() else 1
    if stage == 'cli':
        return native.main(sys.argv[5:])
    if stage == 'stop-after-export':
        assert native.main(['context', '--work', 'DE-W000', '--output',
                            str(output / 'context'), '--byte-budget', '180000']) == 0
        assert native.main(['aide-export', '--work', 'DE-W000', '--output',
                            str(output / 'selected')]) == 0
        record = output / 'selected/DE-W000.json'
        context = output / 'context/manifest.json'
        assert sorted(p.name for p in record.parent.iterdir()) == ['DE-W000.json']
        handoff = {'schema': 'aide.task-local-native-qualification.v1',
                   'work_id': 'DE-W000', 'completed_effect': 'selected_export',
                   'export_sha256': sha(record), 'context_sha256': sha(context),
                   'next_stage': 'verify_existing_context_and_export',
                   'authorizes_implementation': False, 'stop_kind': 'controlled_process_exit_75'}
        (output / 'fixture-handoff.json').write_text(json.dumps(handoff, indent=2) + '\n', encoding='utf-8')
        return 75
    if stage == 'resume':
        handoff = json.loads((output / 'fixture-handoff.json').read_text())
        record_path = output / 'selected/DE-W000.json'
        assert handoff['work_id'] == 'DE-W000' and handoff['completed_effect'] == 'selected_export'
        assert sha(record_path) == handoff['export_sha256']
        assert sha(output / 'context/manifest.json') == handoff['context_sha256']
        assert native.main(['verify-context', str(output / 'context')]) == 0
        record = native.read_json(record_path)
        assert record['metadata']['id'] == record['spec']['task_id'] == 'DE-W000'
        assert not record['spec']['authorizes_implementation']
        assert record['status']['result'] == 'NOT_RUN' and record['status']['phase'] == 'planned'
        result = {'work_id': 'DE-W000', 'status': 'PASS_BOUNDED_PROCESS_CONTINUITY',
                  'completed_export_repeated': False, 'export_sha256': sha(record_path),
                  'arbitrary_interruption_qualified': False, 'native_target_activated': False}
        (output / 'fixture-resume.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        return 0
    raise ValueError('Unknown fixed native qualification stage')


if __name__ == '__main__':
    raise SystemExit(main())
