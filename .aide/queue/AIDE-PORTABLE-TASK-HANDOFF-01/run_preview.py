"""Bind the existing preview owner and preserve the qualified portable bytes."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import json
from pathlib import Path

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

owner = load('handoff_preview_owner', Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py'))
owner.BASE = '19e237cde0864ca56169a14a7bf8ded5180d6def'
inventory = load('handoff_preview_inventory', Path('.aide/queue/AIDE-DAILY-PACK-REFRESH-01/pack_inventory.py'))
expected = json.loads(Path('.aide/queue/AIDE-PORTABLE-TASK-HANDOFF-01/evidence/attempt-02-delivered-result.json').read_text(encoding='utf-8'))['after_sha256s']

def verify_pack():
    observed = {name: entry['sha256'] for name, entry in inventory.observe()['files'].items()}
    assert len(observed) == 864 and observed == expected

if __name__ == '__main__':
    verify_pack()
    owner.main()
    verify_pack()
