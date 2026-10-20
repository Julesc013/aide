"""One admitted local observation with live durable receipts and log round trip."""
import base64
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys

scratch = Path(os.environ["AIDE_JOB_TMP"]).resolve(strict=True)
output = Path(os.environ["AIDE_JOB_OUTPUT"]).resolve(strict=True)
receipts = output / "receipts"
streams = [output / ("evaluator" + suffix) for suffix in (".stdout", ".stderr")]
argv = [sys.executable, "-I", "-B", "evals/lite/lifecycle.py", "--scratch-parent", str(scratch),
        "--output", str(receipts), "--emit-log"]
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
record = {"state": "started", "argv": argv, "source_head": head, "exit_code": None}


def save():
    (output / "evaluator.command.json").write_bytes((json.dumps(record, indent=2) + "\n").encode())


save()
result = None
try:
    with streams[0].open("xb") as stdout, streams[1].open("xb") as stderr:
        result = subprocess.run(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, timeout=500)
    record.update(state="completed", exit_code=result.returncode)
except (OSError, subprocess.SubprocessError) as error:
    record.update(state="exception", error_type=type(error).__name__, error=str(error))
    raise
finally:
    record["streams"] = {p.name: {"bytes": p.stat().st_size,
                                  "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                         for p in streams if p.exists()}
    save()
if result.returncode:
    raise SystemExit(result.returncode)
data = json.loads((output / "receipts/result.json").read_bytes())
assert data["observation_complete"] and data["source_head"] == head
lines = [line.split() for line in streams[0].read_text(encoding="utf-8").splitlines()
         if line.startswith("AIDE_RECEIPT_V1 ")]
assert lines and all(len(line) == 4 and line[2] == lines[0][2] for line in lines)
assert [line[1] for line in lines] == [f"{i + 1}/{len(lines)}" for i in range(len(lines))]
packed = base64.b64decode("".join(line[3] for line in lines), validate=True)
assert len(packed) <= 2 * 1024 * 1024 and hashlib.sha256(packed).hexdigest() == lines[0][2]
with gzip.GzipFile(fileobj=io.BytesIO(packed)) as compressed:
    raw = compressed.read(12 * 1024 * 1024 + 1)
assert len(raw) <= 12 * 1024 * 1024
decoded = json.loads(raw)
actual = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in receipts.iterdir() if p.is_file()}
assert decoded == actual
(output / "transport-round-trip.json").write_bytes((json.dumps({"result": "PASS", "files": len(actual),
    "compressed_bytes": len(packed), "compressed_sha256": lines[0][2], "all_receipt_bytes_equal": True}, indent=2) + "\n").encode())
print(json.dumps({"observation_complete": True, "native_lifecycle_pass": data["native_lifecycle_pass"],
                  "support_claimed": False}), flush=True)
