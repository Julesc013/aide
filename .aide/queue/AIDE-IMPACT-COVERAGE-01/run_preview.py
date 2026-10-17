"""Bind the existing promotion-preview owner to this task's exact base."""
import importlib.util
from pathlib import Path
import sys
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('impact_preview_owner',
    Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py'))
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '36d388a72b6e6e941ca84c93387d742f85af3064'
if __name__ == '__main__':
    owner.main()
