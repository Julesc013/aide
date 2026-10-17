"""Reuse the qualified preview owner for this child's fixed integration base."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
path = Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
spec = importlib.util.spec_from_file_location('engineering_preview_owner', path)
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '239558e8a9edd9bc49772d9e3a6876cf35e1c9c5'
if __name__ == '__main__':
    owner.main()
