"""One finite qualification; separate processes prevent cross-subject selftest caching."""
import sys
sys.dont_write_bytecode = True
import json
import os
from pathlib import Path
import subprocess

root = Path.cwd()
task = root / '.aide/queue/AIDE-ENGINEERING-REVIEW-01'
output = Path(os.environ['AIDE_JOB_OUTPUT'])
stages = []
bootstrap = "import os,sys,tempfile,runpy; tempfile.tempdir=os.environ['AIDE_JOB_TMP']; sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
for name in ('run_checks.py', 'run_repair_pack.py'):
    result = subprocess.run([sys.executable, '-B', '-c', bootstrap, str(task / name)], cwd=root,
                            stdin=subprocess.DEVNULL, timeout=150)
    stages.append({'runner': name, 'exit_code': result.returncode})
    (output / 'repair-stages.json').write_text(json.dumps(stages, indent=2) + '\n', encoding='utf-8')
    if result.returncode:
        raise SystemExit(result.returncode)
print(json.dumps({'status': 'PASS', 'source_and_delivered_processes': 'separate', 'stages': stages}))
