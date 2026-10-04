"""Select existing current qualification machinery for the capability payload."""
import importlib.util
from pathlib import Path

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
worker_path = REPO / ".aide/queue/AIDE-CURRENT-SCOPED-LITE-QUALIFICATION-01/worker.py"
spec = importlib.util.spec_from_file_location("current_lite_qualification", worker_path)
worker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(worker)
# Only the accepted source-proof owner changes; existing canaries and assertions remain.
worker.TASK = TASK
if __name__ == "__main__":
    worker.main()
