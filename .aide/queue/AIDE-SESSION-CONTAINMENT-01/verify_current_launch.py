"""No-model configuration qualification inside the existing managed owner.

The backend's state goes into this job's existing temporary lease. This does
not exercise model apply_patch, change VS Code, or claim session containment.
"""
import ctypes
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time
import tomllib

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def filesystem_matches(actual, expected):
    """Accept only exact requested rules plus the backend's unset schema field.

    glob_scan_max_depth=None is unconfigured metadata, not another path rule.
    Non-null values and every other extra key remain a mismatch.
    """
    return actual == expected or ('glob_scan_max_depth' not in expected and
                                 actual == {**expected, 'glob_scan_max_depth': None})


def main():
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    temporary = Path(os.environ['AIDE_JOB_TMP'])
    identity = ctypes.create_unicode_buffer(256)
    count = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(count)):
        raise ctypes.WinError()
    if identity.value != 'BLACKGLASS-WIN1\\CodexSandboxOffline':
        raise RuntimeError('expected the unchanged restricted managed worker')
    spec = importlib.util.spec_from_file_location('aide_prepared_launch', TASK / 'outer-launch.py')
    launch = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(launch)
    cfg = tomllib.loads((TASK / 'outer-launch.toml').read_text(encoding='utf-8'))
    frozen = json.loads((TASK / 'evidence/current-host-launch-argv.json').read_text(encoding='utf-8'))
    executable = launch.backend()
    expected = launch.configured_arguments(executable, cfg, frozen['loaded_config_security'])
    if expected != frozen['argv']:
        raise RuntimeError('prepared argv differs from bound profile/integration selection')
    refusals = {}
    for name, value in [('legacy_mode', {'sandbox_mode': 'danger-full-access'}),
                        ('legacy_workspace', {'sandbox_workspace_write': {}}),
                        ('unsafe_mcp_name', {'mcp_servers': {'bad.name': {}}})]:
        try:
            launch.configured_arguments(executable, cfg, [value])
        except RuntimeError:
            refusals[name] = True
        else:
            raise RuntimeError('required launch refusal missing: ' + name)
    # Use the owner's allocated temp, not AppData, a drive root, or a new clone.
    home = temporary / 'codex-config-home'
    home.mkdir()
    # The real client has transport declarations. Isolated test state must
    # provide harmless valid schema fixtures without copying its credentials.
    # These disabled transports qualify enabled=false only, not user services.
    marker = temporary / 'mcp-must-not-start.txt'
    fixture_names = sorted({key for layer in frozen['loaded_config_security']
                            for key in layer.get('mcp_servers', {})})
    fixture_config = []
    for name in fixture_names:
        fixture_config.extend([
            '[mcp_servers.' + name + ']',
            'enabled = false',
            'command = ' + json.dumps(sys.executable),
            'args = ' + json.dumps(['-B', '-c',
                'import pathlib,sys; pathlib.Path(sys.argv[1]).write_bytes(b"unexpected MCP startup"); sys.exit(99)',
                str(marker)]),
        ])
    (home / 'config.toml').write_bytes(('\n'.join(fixture_config) + '\n').encode('utf-8'))
    environment = dict(os.environ, CODEX_HOME=str(home), PYTHONDONTWRITEBYTECODE='1')
    process = None
    messages = queue.Queue(maxsize=16)
    response_bytes = response_messages = 0
    errors = bytearray()
    reader_faults = []
    reader_completed = {'stdout': False, 'stderr': False}

    def read_stdout():
        nonlocal response_bytes, response_messages
        try:
            while line := process.stdout.readline(262145):
                size = len(line.encode('utf-8'))
                response_bytes += size
                response_messages += 1
                if size > 262144 or response_bytes > 524288 or response_messages > 64:
                    raise RuntimeError('backend response byte/message bound exceeded')
                messages.put_nowait(json.loads(line))
            reader_completed['stdout'] = True
        except Exception as error:
            reader_faults.append((type(error).__name__ + ': ' + str(error))[:512])

    def read_stderr():
        try:
            while chunk := process.stderr.read(1024):
                raw = chunk.encode('utf-8')
                if len(errors) + len(raw) > 16384:
                    raise RuntimeError('backend stderr exceeds 16KiB')
                errors.extend(raw)
            reader_completed['stderr'] = True
        except Exception as error:
            reader_faults.append(('stderr ' + type(error).__name__ + ': ' + str(error))[:512])

    readers = [threading.Thread(target=read_stdout, daemon=True),
               threading.Thread(target=read_stderr, daemon=True)]
    def rpc(identifier, method, params):
        # This closed list cannot start a model or dispatch a file mutation.
        if method not in ('initialize', 'config/read'):
            raise RuntimeError('qualification RPC is not admitted')
        process.stdin.write(json.dumps({'id': identifier, 'method': method, 'params': params}) + '\n')
        process.stdin.flush()
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            if reader_faults:
                raise RuntimeError(reader_faults[0])
            try:
                message = messages.get(timeout=.2)
            except queue.Empty:
                if process.poll() is not None:
                    raise RuntimeError('backend exited before its response')
                continue
            if message.get('id') == identifier:
                if 'error' in message:
                    raise RuntimeError('backend RPC refused: ' + method)
                return message['result']
        raise TimeoutError(method)

    result = {'schema': 'aide.prepared-current-launch.check.v1', 'result': 'FAIL',
        'job_id': os.environ['AIDE_JOB_ID'], 'windows_identity': identity.value,
        'model_calls': 0, 'threads_started': 0, 'turns_started': 0,
        'changes_existing_thread': False, 'whole_session_contained': False,
        'model_editing_qualified': False, 'global_configuration_changed': False,
        'client_state_destination': str(home), 'refusal_checks': refusals,
        'fixture_support': {'disabled_mcp_transport_schema_only': fixture_names,
                            'actual_user_transports_qualified': False},
        'capability_sha256': sha(TASK / 'evidence/current-host-capability.json'),
        'launch_profile_sha256': sha(TASK / 'outer-launch.toml'),
        'backend_sha256': sha(executable)}
    failed = None
    try:
        process = subprocess.Popen([*expected, 'app-server'], cwd=REPO, env=environment,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
        for reader in readers:
            reader.start()
        initialized = rpc(1, 'initialize', {'clientInfo': {
            'name': 'aide_config_only_qualification', 'version': '1'}, 'capabilities': {}})
        result['user_agent'] = initialized['userAgent']
        if '0.160.0' not in result['user_agent']:
            raise RuntimeError('resolved backend version differs from observed client')
        process.stdin.write('{"method":"initialized"}\n')
        process.stdin.flush()
        response = rpc(2, 'config/read', {'includeLayers': False})
        # Retain only security/configuration fields; never account credentials.
        effective = response['config']
        name = cfg['default_permissions']
        selected = effective.get('permissions', {}).get(name, {})
        features = effective.get('features', {})
        servers = effective.get('mcp_servers', {})
        result['effective_security'] = {key: effective.get(key) for key in
            ('default_permissions', 'approval_policy', 'web_search', 'windows')}
        result['effective_profile'] = selected
        result['effective_features'] = {key: features.get(key) for key in cfg['features']}
        result['mcp_disabled'] = {key: value.get('enabled') is False for key, value in servers.items()}
        expected_profile = cfg['permissions'][name]
        checks = {
            'selected_profile': effective.get('default_permissions') == name,
            'legacy_sandbox_absent': effective.get('sandbox_mode') is None,
            'approval_never': effective.get('approval_policy') == 'never',
            'elevated': effective.get('windows', {}).get('sandbox') == 'elevated',
            'web_disabled': effective.get('web_search') == 'disabled',
            'exact_filesystem': filesystem_matches(selected.get('filesystem'), expected_profile['filesystem']),
            'network_disabled': selected.get('network', {}).get('enabled') is False,
            'optional_routes_disabled': all(features.get(key) is False for key in cfg['features']),
            'declared_mcp_disabled': all(result['mcp_disabled'].values()) and
                all(result['mcp_disabled'].get(key) is True for layer in frozen['loaded_config_security']
                    for key in layer.get('mcp_servers', {})),
        }
        result['checks'] = checks
        if not all(checks.values()):
            raise RuntimeError('prepared configuration does not resolve exactly')
        result['result'] = 'PASS_CONFIGURATION_ONLY'
    except Exception as error:
        failed = error
        result['failure'] = type(error).__name__ + ': ' + str(error)
    finally:
        teardown_faults = []
        if process is not None:
            try:
                process.stdin.close()
            except Exception as error:
                teardown_faults.append('stdin close: ' + type(error).__name__)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                teardown_faults.append('owned backend did not retire on closed input')
                try:
                    process.terminate()
                    process.wait(timeout=5)
                except Exception as error:
                    teardown_faults.append('terminate/wait: ' + type(error).__name__)
                    try:
                        process.kill()
                        process.wait(timeout=5)
                    except Exception as error:
                        teardown_faults.append('kill/wait: ' + type(error).__name__)
            except Exception as error:
                teardown_faults.append('wait: ' + type(error).__name__)
        for reader in readers:
            if reader.ident is not None:
                try:
                    reader.join(timeout=2)
                except Exception as error:
                    teardown_faults.append('reader join: ' + type(error).__name__)
        result['owned_backend_exit'] = process.returncode if process is not None else None
        result['reader_faults'] = reader_faults
        result['reader_completed'] = reader_completed
        result['teardown_faults'] = teardown_faults
        result['response_bytes'] = response_bytes
        result['response_messages'] = response_messages
        result['unexpected_mcp_start_marker_present'] = marker.exists()
        if result['owned_backend_exit'] != 0 or reader_faults or teardown_faults or marker.exists() or not all(reader_completed.values()) or any(reader.is_alive() for reader in readers):
            result['result'] = 'FAIL'
        (output / 'backend-stderr.log').write_bytes(errors)
        (output / 'current-launch-check.json').write_bytes(
            (json.dumps(result, sort_keys=True, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({'result': result['result'], 'job_id': result['job_id'],
        'checks': result.get('checks'), 'whole_session_contained': False}), flush=True)
    if failed is not None:
        raise failed
    if result['result'] != 'PASS_CONFIGURATION_ONLY':
        raise RuntimeError('configuration qualification did not close')


if __name__ == '__main__':
    main()
