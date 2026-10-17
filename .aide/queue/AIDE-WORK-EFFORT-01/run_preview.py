"""Reuse the qualified preview owner for this child's fixed integration base."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
path = Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
spec = importlib.util.spec_from_file_location('effort_preview_owner', path)
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = 'a0970badeca5b3332505a4158fcfca6b075e07e3'
if __name__ == '__main__':
    owner.main()
