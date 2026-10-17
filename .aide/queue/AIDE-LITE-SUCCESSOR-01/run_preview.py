"""Finish the one interrupted method, then use the existing fixed preview owner."""
import sys
sys.dont_write_bytecode = True
import hashlib
import importlib.util
from pathlib import Path
import subprocess

root = Path.cwd()
spec = importlib.util.spec_from_file_location('successor_preview_owner',
    root / '.aide/queue/AIDE-DEPENDENCY-MCP-01/run_preview.py')
owner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
owner.BASE = '33ec403f0e4f17af919aa5685855f57760619e7e'


def main():
    if sys.argv[1:] == ['generate']:
        pack = root / '.aide/export/aide-lite-pack-v0'
        before = {p.relative_to(pack).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in pack.rglob('*') if p.is_file()}
        assert len(before) == 862
        bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
        subprocess.run([sys.executable, '-B', '-c', bootstrap,
                        str(Path(__file__).with_name('run_checks.py')),
                        'delivered_remaining', str(pack / 'files')],
                       check=True, timeout=90)
        after = {p.relative_to(pack).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in pack.rglob('*') if p.is_file()}
        assert after == before
    owner.main()


if __name__ == '__main__':
    main()
