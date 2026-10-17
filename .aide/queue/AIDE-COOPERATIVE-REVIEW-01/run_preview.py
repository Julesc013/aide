"""Reuse the qualified preview owner for this child's fixed integration base."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
path = Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
spec = importlib.util.spec_from_file_location('cooperative_preview_owner', path)
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '2194eb6b73ac055bd4c173d1a12ffcf1833f833d'
if __name__ == '__main__':
    owner.main()
