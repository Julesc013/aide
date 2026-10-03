"""Harmless, no-model qualification of installed ordinary app-server routes."""
import base64
import json
from pathlib import Path
import queue
import stat
import subprocess
import threading
import time

REPO = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).resolve().parent / 'evidence'
CODEX = r'C:\Users\Jules\.codex\packages\standalone\releases\0.145.0-x86_64-pc-windows-msvc\bin\codex.exe'
PYTHON = r'C:\Users\Jules\AppData\Local\Python\pythoncore-3.14-64\python.exe'

def main():
    excluded = EVIDENCE / 'outer-host-excluded-fixture.txt'
    allowed = EVIDENCE / 'outer-host-allowed-fixture.txt'
    values = [b'harmless excluded fixture', b'harmless editor write', b'allowed editor write', b'allowed shell write', b'']
    if excluded.exists() or allowed.exists():
        raise RuntimeError('unreconciled probe fixture; do not allocate replacements')
    excluded.write_bytes(values[0])
    allowed.write_bytes(b'')
    rules = {':root':'deny', ':minimal':'read', str(REPO):'read', str(excluded):'deny', str(allowed):'write'}
    inline = '{'+','.join(json.dumps(k)+'='+json.dumps(v) for k,v in rules.items())+'}'
    args = [CODEX,'app-server','--stdio','-c','default_permissions="aide_outer_probe"',
            '-c','permissions.aide_outer_probe.filesystem='+inline,
            '-c','permissions.aide_outer_probe.network.enabled=false','-c','web_search="disabled"']
    for feature in ['apps','plugins','remote_plugin','hooks','browser_use','browser_use_external','computer_use','in_app_browser','multi_agent']:
        args += ['--disable', feature]
    process = subprocess.Popen(args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                               text=True,creationflags=subprocess.CREATE_NO_WINDOW)
    messages = queue.Queue()
    errors = []
    def reader():
        for line in process.stdout:
            if len(line)>65536:
                messages.put({'oversize':True}); break
            messages.put(json.loads(line))
    def stderr():
        for line in process.stderr:
            if sum(map(len,errors))+len(line)<=4096:
                errors.append(line)
    threading.Thread(target=reader,daemon=True).start()
    threading.Thread(target=stderr,daemon=True).start()
    def rpc(identifier,method,params):
        process.stdin.write(json.dumps({'id':identifier,'method':method,'params':params})+'\n')
        process.stdin.flush()
        deadline = time.monotonic()+25
        while time.monotonic()<deadline:
            try:
                value = messages.get(timeout=.5)
            except queue.Empty:
                if process.poll() is not None:
                    raise RuntimeError('owned server exited')
                continue
            if value.get('oversize'):
                raise RuntimeError('RPC response bound exceeded')
            if value.get('id')==identifier:
                return value
        raise TimeoutError(method)
    result = {'schema':'aide.outer-host-route-observation.v1','installed_client':'0.145.0',
              'profile':{'name':'aide_outer_probe','filesystem':rules,'network_enabled':False},
              'model_turns_started':0,'threads_started':0,'global_configuration_changes':0,
              'current_outer_profile':'disabled/unrestricted','whole_session_contained':False,'responses':[]}
    try:
        direct_script = "import pathlib,sys,json\nf=pathlib.Path(sys.argv[1]);v={}\ntry: f.read_bytes()\nexcept PermissionError: v['excluded_read_denied']=True\nelse: v['excluded_read_denied']=False\ntry: f.open('r+b').close()\nexcept PermissionError: v['excluded_write_handle_denied']=True\nelse: v['excluded_write_handle_denied']=False\nprint(json.dumps(v))"
        direct = subprocess.run([CODEX,'sandbox','-P','aide_outer_probe',
            '-c','permissions.aide_outer_probe.filesystem='+inline,
            '-c','permissions.aide_outer_probe.network.enabled=false',
            '--',PYTHON,'-B','-c',direct_script,str(excluded)],capture_output=True,text=True,timeout=25)
        result['direct_sandbox']={'exit':direct.returncode,'stdout':direct.stdout,'stderr':direct.stderr}
        result['initialize'] = rpc(1,'initialize',{'clientInfo':{'name':'aide_harmless_route_qualification','version':'1'},'capabilities':{}})
        process.stdin.write('{"method":"initialized"}\n');process.stdin.flush()
        for identifier,method,params in [
            (2,'fs/readFile',{'path':str(excluded)}),
            (3,'fs/writeFile',{'path':str(excluded),'dataBase64':base64.b64encode(values[1]).decode()}),
            (4,'fs/writeFile',{'path':str(allowed),'dataBase64':base64.b64encode(values[2]).decode()})]:
            result['responses'].append({'method':method,'response':rpc(identifier,method,params)})
        result['editor_excluded_read_denied'] = 'error' in result['responses'][0]['response']
        result['editor_excluded_write_denied'] = 'error' in result['responses'][1]['response']
        result['allowed_editor_write'] = allowed.read_bytes()==values[2]
        script = "import pathlib,sys,json\nf,a=map(pathlib.Path,sys.argv[1:]); v={}\ntry: f.read_bytes()\nexcept PermissionError: v['excluded_read_denied']=True\nelse: v['excluded_read_denied']=False\ntry: f.open('r+b').close()\nexcept PermissionError: v['excluded_write_handle_denied']=True\nelse: v['excluded_write_handle_denied']=False\na.write_bytes(b'allowed shell write');v['allowed_shell_write']=True\nprint(json.dumps(v))"
        response = rpc(5,'command/exec',{'command':[PYTHON,'-B','-c',script,str(excluded),str(allowed)],'cwd':str(REPO),'timeoutMs':20000})
        result['responses'].append({'method':'command/exec','response':response})
        result['shell'] = json.loads(response['result']['stdout'])
        result['result'] = 'PARTIAL' if result['shell']['excluded_read_denied'] and result['shell']['excluded_write_handle_denied'] and result['shell']['allowed_shell_write'] else 'FAIL'
    except Exception as error:
        result['result']='FAIL';result['error_type']=type(error).__name__
        raise
    finally:
        process.stdin.close()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.terminate();process.wait(timeout=5)
        result['owned_server_exit']=process.returncode
        # Record before retirement so a teardown failure does not lose route evidence.
        report=EVIDENCE/'outer-host-route-observation.json'
        report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        for fixture in [excluded,allowed]:
            info=fixture.lstat()
            if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1 or info.st_file_attributes&1024 or fixture.read_bytes() not in values:
                raise RuntimeError('changed or linked owned fixture; preserve and reconcile')
            fixture.unlink()
        result['fixture_retirement']=not excluded.exists() and not allowed.exists()
        report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['responses','profile','initialize']},indent=2))

if __name__=='__main__':
    main()
