"""Render task-local CLI overrides without changing global settings or starting AI.

The profile is prepared for the observed VS Code backend, not its live thread.
Model editing and separate filesystem/integration routes remain unqualified.
"""
from pathlib import Path
import hashlib
import json
import re
import tomllib
import stat

TASK = Path(__file__).resolve().parent
CAPABILITY = TASK / 'evidence/current-host-capability.json'
CAPABILITY_SHA256 = 'e83953ff9a581340484a92f6642c1f921f76a47f7cf1309ab9e68b744209c799'

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def ordinary(path):
    for entry in (*reversed(path.parents), path):
        info = entry.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 1024:
            raise RuntimeError('launch dependency link/reparse path refused')
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise RuntimeError('launch dependency ordinary single-link file required')

def backend():
    ordinary(CAPABILITY)
    if CAPABILITY.stat().st_size > 65536:
        raise RuntimeError('observed client capability exceeds its bounded record size')
    if sha(CAPABILITY) != CAPABILITY_SHA256:
        raise RuntimeError('observed client capability changed; requalify exact binding')
    observed = json.loads(CAPABILITY.read_text(encoding='utf-8'))
    root = Path(observed['outer_client']['extension_root'])
    for relative, digest in [('package.json', observed['outer_client']['package_sha256']),
                             (observed['outer_client']['entrypoint'], observed['outer_client']['entrypoint_sha256'])]:
        path = root / relative
        ordinary(path)
        if path.stat().st_size > 8388608:
            raise RuntimeError('observed outer client dependency exceeds its size bound')
        if sha(path) != digest:
            raise RuntimeError('observed outer client changed; requalify exact binding')
    path = Path(observed['backend']['path'])
    ordinary(path)
    if path.stat().st_size != observed['backend']['bytes'] or sha(path) != observed['backend']['sha256']:
        raise RuntimeError('installed reviewed backend changed; no automatic substitution')
    return path

def render(value):
    if isinstance(value,bool): return str(value).lower()
    if isinstance(value,str): return json.dumps(value)
    if isinstance(value,dict): return '{'+','.join(json.dumps(k)+'='+render(v) for k,v in value.items())+'}'
    raise ValueError('unsupported task-local override')

def configured_arguments(executable, cfg, loaded_configs):
    """Pure renderer; callers provide only actual loaded configuration layers."""
    args=[str(executable),'-C',str(TASK.parents[2])]
    for key,value in cfg.items():
        args+=['-c',key+'='+render(value)]
    # Legacy settings override named profiles; inspect each loaded layer.
    names = set()
    for base in loaded_configs:
        if base.get('sandbox_mode') is not None or 'sandbox_workspace_write' in base:
            raise RuntimeError('legacy sandbox settings override profiles; require exact reconciliation')
        names.update(base.get('mcp_servers', {}))
    for name in sorted(names):
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*',name):
            raise RuntimeError('MCP name cannot be safely expressed as a dotted CLI override')
        args+=['-c','mcp_servers.'+name+'.enabled=false']
    return args

def arguments():
    executable = backend()
    profile = TASK / 'outer-launch.toml'
    ordinary(profile)
    cfg = tomllib.loads(profile.read_text(encoding='utf-8'))
    loaded = []
    for path in [Path(r'C:\Users\Jules\.codex\config.toml'), TASK.parents[2] / '.codex/config.toml']:
        if path.exists():
            ordinary(path)
            loaded.append(tomllib.loads(path.read_text(encoding='utf-8')))
    return configured_arguments(executable, cfg, loaded)

if __name__=='__main__':
    print(json.dumps({'status':'PREPARED_NOT_WHOLE_SESSION_QUALIFIED',
        'argv':arguments(),'automatic_model_invocation':False,
        'client':'VS Code Codex extension 26.930.41038 / Codex 0.160.0',
        'changes_existing_thread':False,
        'required_host_action':'Select the constrained task profile in the actual client, disable uncovered integrations, then qualify model editing and one normal task. This rendered CLI does not change an existing VS Code thread.'},indent=2))
