"""Reuse the qualified preview owner for this child's fixed integration base."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
path = Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
spec = importlib.util.spec_from_file_location('quality_preview_owner', path)
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '33a377743d86f59fd63a042096063d664e200468'
if __name__ == '__main__':
    owner.main()
