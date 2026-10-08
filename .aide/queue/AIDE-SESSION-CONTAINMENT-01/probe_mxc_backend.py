"""One strict MXC prerequisite; no model, persistent setup or backend fallback."""
import ctypes
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading

BACKEND = Path(r'C:\Users\Jules\.vscode\extensions\openai.chatgpt-26.1002.51308-win32-x64\bin\windows-x86_64\codex.exe')
BACKEND_SHA = 'd83cc3582592e307df008411f02f61a93fb93580b53dc173608a63202d97bbe4'
FEATURES = ('apps', 'plugins', 'remote_plugin', 'hooks', 'browser_use',
            'browser_use_external', 'computer_use', 'in_app_browser', 'multi_agent', 'prefer_mxc')
ENV_KEYS = ('SYSTEMROOT', 'WINDIR', 'PATH', 'COMSPEC', 'PATHEXT', 'USERPROFILE',
            'LOCALAPPDATA', 'APPDATA', 'PROGRAMDATA', 'PROGRAMFILES', 'PROGRAMFILES(X86)',
            'PROCESSOR_ARCHITECTURE', 'NUMBER_OF_PROCESSORS', 'HOMEDRIVE', 'HOMEPATH')


def native_mxc_unavailable(exit_code, stderr):
    """Recognize exact upstream refusals; never turn any result into a PASS."""
    return (type(exit_code) is int and exit_code != 0 and
            any(s in stderr for s in ('native MXC is unavailable on this executor',
                                     'native MXC is unavailable on this Windows build',
                                     'this Windows build cannot enforce native MXC deny paths')))


def main():
    output, temporary = (Path(os.environ[k]) for k in ('AIDE_JOB_OUTPUT', 'AIDE_JOB_TMP'))
    identity = ctypes.create_unicode_buffer(256)
    size = ctypes.c_ulong(len(identity))
    if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
        raise ctypes.WinError()
    if identity.value != 'BLACKGLASS-WIN1\\CodexSandboxOffline':
        raise RuntimeError('unexpected supervisor identity')
    with BACKEND.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != BACKEND_SHA:
            raise RuntimeError('backend changed; no substitution')
    home, candidate, excluded = (temporary / n for n in ('mxc-client', 'candidate', 'excluded'))
    for p in (home, candidate, excluded):
        p.mkdir()
    marker, allowed = excluded / 'fixture.txt', candidate / 'allowed.txt'
    marker.write_bytes(b'AIDE harmless excluded fixture\n')
    (home / 'config.toml').write_bytes(b'')
    for name in ('.git', '.codex', '.aide.local'):
        (candidate / name).mkdir()
    profile = 'aide_strict_mxc_probe'
    rules = {':root': 'deny', ':minimal': 'read', str(Path(sys.executable).parent): 'read',
             str(BACKEND.parent): 'read', str(candidate): 'write', str(excluded): 'deny',
             str(home): 'deny', **{str(candidate / n): 'deny' for n in ('.git', '.codex', '.aide.local')}}
    options = {'default_permissions': profile, 'approval_policy': 'never',
               'windows.sandbox': 'mxc', 'web_search': 'disabled', 'history.persistence': 'none',
               'log_dir': str(home / 'logs'), 'sqlite_home': str(home / 'state'),
               'permissions.' + profile + '.filesystem': rules,
               'permissions.' + profile + '.network.enabled': False}
    options.update({'features.' + f: False for f in FEATURES})
    render = lambda v: ('{' + ','.join(json.dumps(k) + '=' + json.dumps(w) for k, w in v.items()) + '}'
                        if isinstance(v, dict) else json.dumps(v))
    # Only pre-existing harmless fixture bytes are touched by negative witnesses.
    code = '''import json, pathlib, subprocess, sys
allowed, denied = map(pathlib.Path, sys.argv[1:])
allowed.write_bytes(b"AIDE allowed native edit\\n")
def blocked(operation):
    try: operation()
    except PermissionError: return True
    except OSError as error:
        if error.winerror == 5: return True
        raise
    return False
child = "import pathlib,sys; p=pathlib.Path(sys.argv[1]);\\ntry: p.write_bytes(b'child escape')\\nexcept PermissionError: sys.exit(17)\\nsys.exit(19)"
r = subprocess.run([sys.executable, '-I', '-B', '-c', child, str(denied)], capture_output=True, timeout=5)
proof = {'allowed_edit': allowed.read_bytes() == b"AIDE allowed native edit\\n",
         'excluded_read': blocked(denied.read_bytes),
         'excluded_write': blocked(lambda: denied.write_bytes(b'escape')),
         'private_metadata_write': blocked(lambda: (allowed.parent/'.git'/'escape.txt').write_bytes(b'escape')),
         'child_excluded_write': r.returncode == 17 and not r.stdout and not r.stderr}
print(json.dumps(proof, sort_keys=True))
sys.exit(0 if all(proof.values()) else 23)
'''
    argv = [str(BACKEND), '-C', str(candidate)]
    for k, v in options.items():
        argv += ['-c', k + '=' + render(v)]
    argv += ['sandbox', 'windows', '--permission-profile', profile, '--include-managed-config', '--',
             sys.executable, '-I', '-B', '-c', code, str(allowed), str(marker)]
    environment = {k: v for k, v in os.environ.items() if k.upper() in ENV_KEYS}
    environment.update(CODEX_HOME=str(home), TEMP=str(home), TMP=str(home), PYTHONDONTWRITEBYTECODE='1')
    result = {'schema': 'aide.strict-mxc.prerequisite.v1', 'status': 'FAIL',
              'backend_sha256': BACKEND_SHA, 'job_id': os.environ['AIDE_JOB_ID'],
              'windows_identity': identity.value, 'requested_model_turns': 0,
              'requested_threads': 0, 'requested_commands': 1, 'sandbox': 'mxc',
              'fallback_permitted': False, 'credentials_copied': False,
              'whole_session_contained': False, 'actual_model_editing_qualified': False,
              'profile': {'name': profile, 'filesystem': rules, 'network_enabled': False}}
    buffers, faults, readers = [bytearray(), bytearray()], [], []
    process = None

    def checkpoint():
        for name, data in zip(('backend-stdout.log', 'backend-stderr.log'), buffers):
            (output / name).write_bytes(data)
        (output / 'mxc-prerequisite.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')

    def collect(pipe, buffer):
        try:
            while chunk := pipe.read(1024):
                if len(buffer) + len(chunk) > 49152:
                    raise RuntimeError('complete-output bound exceeded')
                buffer.extend(chunk)
        except Exception as e:
            faults.append(type(e).__name__ + ': ' + str(e))
            process.terminate()

    try:
        process = subprocess.Popen(argv, cwd=candidate, env=environment, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
        readers = [threading.Thread(target=collect, args=(p, b), daemon=True)
                   for p, b in zip((process.stdout, process.stderr), buffers)]
        for r in readers:
            r.start()
        process.wait(timeout=45)
        for r in readers:
            r.join(timeout=2)
        result['backend_exit'] = process.returncode
        stderr = buffers[1].decode('utf-8', errors='strict')
        if process.returncode == 0:
            proof = json.loads(buffers[0].decode('utf-8'))
            expected = ('allowed_edit', 'excluded_read', 'excluded_write', 'private_metadata_write', 'child_excluded_write')
            if set(proof) != set(expected) or any(proof[k] is not True for k in expected):
                raise RuntimeError('incomplete native witnesses')
            result.update(status='PASS_NATIVE_MXC_BOUNDARY_NO_MODEL', witnesses=proof)
        elif native_mxc_unavailable(process.returncode, stderr):
            result['status'] = 'UNAVAILABLE_NATIVE_MXC_NO_FALLBACK'
        else:
            result['status'] = 'FAIL_NATIVE_MXC_PRESERVED_NO_FALLBACK'
    except Exception as e:
        result['error'] = {'type': type(e).__name__, 'message': str(e)}
    finally:
        checkpoint()
        result['teardown_errors'] = []
        if process is not None and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=5)
            except Exception as e:
                result['teardown_errors'].append(type(e).__name__)
        for r in readers:
            r.join(timeout=2)
        result.update(backend_exit=process.returncode if process is not None else None,
                      readers_quiescent=bool(readers) and all(not r.is_alive() for r in readers),
                      reader_faults=faults,
                      fixture_unchanged=marker.read_bytes() == b'AIDE harmless excluded fixture\n',
                      allowed_edit_present=allowed.exists(),
                      private_escape_absent=not (candidate / '.git' / 'escape.txt').exists())
        if faults or result['teardown_errors'] or not result['readers_quiescent'] or not result['fixture_unchanged'] or not result['private_escape_absent']:
            result['status'] = 'FAIL_CUSTODY_PRESERVED_NO_FALLBACK'
        if result['status'] == 'UNAVAILABLE_NATIVE_MXC_NO_FALLBACK' and result['allowed_edit_present']:
            result['status'] = 'FAIL_UNEXPECTED_EFFECT_NO_FALLBACK'
        checkpoint()
        print(json.dumps({k: result.get(k) for k in ('status', 'backend_exit', 'error')}), flush=True)
    if result['status'] not in ('PASS_NATIVE_MXC_BOUNDARY_NO_MODEL', 'UNAVAILABLE_NATIVE_MXC_NO_FALLBACK'):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
