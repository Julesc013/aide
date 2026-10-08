"""One no-model capability probe for an independently admitted changed backend.

Only initialize and config/read are permitted. All client state and fixtures
belong to the existing managed job's temporary lease. No thread, sandboxed
command or model is started; implicit Windows provisioning is not admitted.
"""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import threading
import time

BACKEND = Path(r'C:\Users\Jules\.vscode\extensions\openai.chatgpt-26.1002.51308-win32-x64\bin\windows-x86_64\codex.exe')
BACKEND_SHA = 'd83cc3582592e307df008411f02f61a93fb93580b53dc173608a63202d97bbe4'
FEATURES = ('apps', 'plugins', 'remote_plugin', 'hooks', 'browser_use',
            'browser_use_external', 'computer_use', 'in_app_browser', 'multi_agent')


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')


def main():
    output = Path(os.environ['AIDE_JOB_OUTPUT'])
    temporary = Path(os.environ['AIDE_JOB_TMP'])
    identity = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
        raise ctypes.WinError()
    if identity.value != 'BLACKGLASS-WIN1\\CodexSandboxOffline':
        raise RuntimeError('expected unchanged restricted managed worker')
    with BACKEND.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != BACKEND_SHA:
            raise RuntimeError('changed backend subject; no substitution')
    home, candidate, excluded = (temporary / name for name in ('isolated-client', 'candidate', 'excluded'))
    for path in (home, candidate, excluded):
        path.mkdir()
    marker = excluded / 'fixture.txt'
    marker.write_bytes(b'AIDE harmless excluded fixture\n')
    allowed = candidate / 'allowed.txt'
    (home / 'config.toml').write_bytes(b'')
    profile = 'aide_updated_backend_probe'
    rules = {':root': 'deny', ':minimal': 'read', str(Path(sys.executable).parent): 'read',
             str(BACKEND.parent): 'read', str(candidate): 'write', str(excluded): 'deny',
             str(home): 'deny', str(candidate / '.git'): 'deny',
             str(candidate / '.codex'): 'deny', str(candidate / '.aide.local'): 'deny'}
    options = {'default_permissions': profile, 'approval_policy': 'never',
               'web_search': 'disabled', 'windows.sandbox': 'elevated',
               'history.persistence': 'none', 'log_dir': str(home / 'logs'),
               'sqlite_home': str(home / 'state'),
               'permissions.' + profile + '.filesystem': rules,
               'permissions.' + profile + '.network.enabled': False}
    options.update({'features.' + feature: False for feature in FEATURES})
    render = lambda value: ('{' + ','.join(json.dumps(k) + '=' + json.dumps(v) for k, v in value.items()) + '}'
                            if isinstance(value, dict) else json.dumps(value))
    argv = [str(BACKEND), '-C', str(candidate)]
    for key, value in options.items():
        argv += ['-c', key + '=' + render(value)]
    argv += ['app-server']
    result = {'schema': 'aide.changed-backend.no-model-probe.v1', 'status': 'FAIL',
              'backend_sha256': BACKEND_SHA, 'windows_identity': identity.value,
              'job_id': os.environ['AIDE_JOB_ID'], 'requested_model_turns': 0,
              'profile': {'name': profile, 'filesystem': rules, 'network_enabled': False},
              'client_state_destination': str(home), 'credentials_copied': False,
              'real_account_qualified': False, 'whole_session_contained': False,
              'actual_model_editing_qualified': False, 'responses': []}
    process = None
    messages = queue.Queue(maxsize=32)
    raw_stdout, raw_stderr = bytearray(), bytearray()
    faults = []

    def read_stdout():
        try:
            while line := process.stdout.readline(65537):
                raw = line.encode('utf-8')
                if len(raw) > 49152 or len(raw_stdout) + len(raw) > 49152:
                    raise RuntimeError('stdout bound exceeded')
                raw_stdout.extend(raw)
                messages.put_nowait(json.loads(line))
        except Exception as error:
            faults.append(type(error).__name__ + ': ' + str(error))

    def read_stderr():
        try:
            while raw := process.stderr.read(1024):
                raw = raw.encode('utf-8')
                if len(raw_stderr) + len(raw) > 16384:
                    raise RuntimeError('stderr bound exceeded')
                raw_stderr.extend(raw)
        except Exception as error:
            faults.append(type(error).__name__ + ': ' + str(error))

    def rpc(identifier, method, params):
        if method not in ('initialize', 'config/read'):
            raise RuntimeError('RPC not admitted')
        request = {'id': identifier, 'method': method, 'params': params}
        result['responses'].append({'request': request})
        process.stdin.write(json.dumps(request) + '\n')
        process.stdin.flush()
        deadline = time.monotonic() + 25
        while time.monotonic() < deadline:
            if faults:
                raise RuntimeError(faults[0])
            try:
                message = messages.get(timeout=.2)
            except queue.Empty:
                if process.poll() is not None:
                    raise RuntimeError('owned backend exited before response')
                continue
            if message.get('id') == identifier:
                result['responses'][-1]['response'] = message
                return message
        raise TimeoutError(method)

    readers = []
    failed = None
    try:
        environment = dict(os.environ, CODEX_HOME=str(home), PYTHONDONTWRITEBYTECODE='1')
        # Isolated empty config has no account or MCP transport. No thread/start,
        # command/exec, setupStart, model or global configuration RPC.
        process = subprocess.Popen(argv, cwd=candidate, env=environment,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
        readers = [threading.Thread(target=read_stdout, daemon=True), threading.Thread(target=read_stderr, daemon=True)]
        for reader in readers:
            reader.start()
        response = rpc(1, 'initialize', {'clientInfo': {'name': 'aide_changed_backend_probe', 'version': '1'},
                    'capabilities': {'experimentalApi': True}})
        if 'error' in response:
            raise RuntimeError('initialize refused')
        result['user_agent'] = response['result']['userAgent']
        if '0.162.0-alpha.2' not in result['user_agent']:
            raise RuntimeError('backend version mismatch')
        process.stdin.write('{"method":"initialized"}\n')
        process.stdin.flush()
        response = rpc(2, 'config/read', {'includeLayers': False})
        if 'error' in response:
            raise RuntimeError('configuration refused')
        effective = response['result']['config']
        selected = effective.get('permissions', {}).get(profile, {})
        filesystem = selected.get('filesystem')
        if filesystem != rules and filesystem != {**rules, 'glob_scan_max_depth': None}:
            raise RuntimeError('effective filesystem differs')
        if (effective.get('default_permissions') != profile or effective.get('sandbox_mode') is not None
                or effective.get('approval_policy') != 'never'
                or effective.get('windows', {}).get('sandbox') != 'elevated'
                or selected.get('network', {}).get('enabled') is not False
                or any(effective.get('features', {}).get(f) is not False for f in FEATURES)
                or effective.get('mcp_servers', {})):
            raise RuntimeError('effective security differs')
        # Keep only the exact security selection in the curated result.
        result['responses'][-1]['response'] = {'id': 2, 'security_matched': True}
        result['effective_security'] = {k: effective.get(k) for k in
                                        ('default_permissions', 'approval_policy', 'windows', 'web_search')}
        result['effective_profile'] = selected
        result['effective_features'] = {f: effective.get('features', {}).get(f) for f in FEATURES}
        result['configuration_checks_passed'] = True
        result['requested_threads'] = 0
        result['requested_sandboxed_commands'] = 0
        result['native_filesystem_boundary_exercised'] = False
        result['status'] = 'PASS_CONFIGURATION_DECODED_NATIVE_NOT_EXERCISED'
    except Exception as error:
        failed = error
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        # Evidence precedes teardown. A failed close/wait cannot erase the
        # actual refusal or the bounded bytes already read from the backend.
        result['teardown_errors'] = []
        def checkpoint():
            (output / 'backend-stdout.log').write_bytes(raw_stdout)
            (output / 'backend-stderr.log').write_bytes(raw_stderr)
            save(output / 'changed-backend-probe.json', result)
        checkpoint()
        if process is not None:
            try:
                process.stdin.close()
            except Exception as error:
                result['teardown_errors'].append('stdin.close: ' + type(error).__name__)
            try:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as error:
                result['teardown_errors'].append('owned wait: ' + type(error).__name__)
                checkpoint()
            for reader in readers:
                reader.join(timeout=2)
            result['backend_exit'] = process.returncode
            result['readers_quiescent'] = all(not reader.is_alive() for reader in readers)
        result['fixture_unchanged'] = marker.read_bytes() == b'AIDE harmless excluded fixture\n'
        result['reader_faults'] = faults
        checkpoint()
        print(json.dumps({k: result.get(k) for k in ('status', 'command_exit', 'command_checks', 'error')}), flush=True)
        if (faults or result['teardown_errors'] or not result.get('readers_quiescent', False)
                or not result['fixture_unchanged']):
            raise RuntimeError('reader/fixture custody failed; preserve original result')
    if failed:
        raise failed


if __name__ == '__main__':
    main()
