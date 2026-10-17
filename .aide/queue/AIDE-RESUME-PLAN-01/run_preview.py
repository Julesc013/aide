"""Use the existing preview owner with this child's exact integration base."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('resume_preview_owner',
    Path('.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py'))
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '716ec1fd0ad6fb2d3875417c4db7b867a7b393fe'
if __name__ == '__main__':
    owner.main()
