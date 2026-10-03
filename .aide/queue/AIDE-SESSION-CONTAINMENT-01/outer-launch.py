"""Render task-local CLI overrides without changing global settings or starting AI.

This prepared command profile cannot constrain app-server filesystem APIs.
The current client must constrain/omit those routes before qualification.
"""
from pathlib import Path
import hashlib
import json
import re
import tomllib

TASK = Path(__file__).resolve().parent
CODEX = Path(r'C:\Users\Jules\.codex\packages\standalone\releases\0.145.0-x86_64-pc-windows-msvc\bin\codex.exe')
EXPECTED = '83751f15cb6a0a7b97df67752c001e3fe1c20e18ffbfec3ff63567296205eb6c'

def render(value):
    if isinstance(value,bool): return str(value).lower()
    if isinstance(value,str): return json.dumps(value)
    if isinstance(value,dict): return '{'+','.join(json.dumps(k)+'='+render(v) for k,v in value.items())+'}'
    raise ValueError('unsupported task-local override')

def arguments():
    if hashlib.sha256(CODEX.read_bytes()).hexdigest()!=EXPECTED:
        raise RuntimeError('installed reviewed client changed')
    cfg=tomllib.loads((TASK/'outer-launch.toml').read_text(encoding='utf-8'))
    args=[str(CODEX),'-C',str(TASK.parents[2])]
    for key,value in cfg.items():
        args+=['-c',key+'='+render(value)]
    # Preserve server declarations but disable each for this proposed session.
    home=Path(r'C:\Users\Jules\.codex\config.toml')
    base=tomllib.loads(home.read_text(encoding='utf-8'))
    if base.get('sandbox_mode') is not None or 'sandbox_workspace_write' in base:
        raise RuntimeError('legacy sandbox settings override profiles; require exact reconciliation')
    for name in base.get('mcp_servers',{}):
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*',name):
            raise RuntimeError('MCP name cannot be safely expressed as a dotted CLI override')
        args+=['-c','mcp_servers.'+name+'.enabled=false']
    return args

if __name__=='__main__':
    print(json.dumps({'status':'PREPARED_NOT_WHOLE_SESSION_QUALIFIED',
        'argv':arguments(),'automatic_model_invocation':False,
        'required_host_action':'Enable client filesystem restrictions for shell and editor tools, and omit independently unrestricted integrations before starting the next contained task.'},indent=2))
