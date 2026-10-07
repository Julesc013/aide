"""Verify exact retained custody before accepting either finite matched result."""
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).parent / "evidence"
profile = sys.argv[1]
if profile not in ("baseline", "compact"):
    raise ValueError("unadmitted profile")

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

config = read(REPO / ".aide.local/efficiency-live-host-permission.json")
spec = importlib.util.spec_from_file_location("matched_custody_scope", REPO / "core/execution/scoped_host.py")
scoped = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scoped)
owner = scoped.load_owner(config["execution_host"], REPO)
terminal = read(EVIDENCE / ("matched-" + profile + "-result.log"))
job = read(REPO / (".aide.local/efficiency-live-host-" + profile + "-job.json"))
job_id = terminal["job_id"]
assert len(job_id) == 32 and all(c in "0123456789abcdef" for c in job_id)
root = Path(config["roots"]["retained"]) / job_id
receipt = read(root / "receipt.json")
marker = read(root / "owner.json")
assert marker == {"job_id": job_id, "manifest_digest": terminal["manifest_digest"]}
assert receipt["job"] == job and owner.digest(job) == receipt["manifest_digest"] == terminal["manifest_digest"]
assert receipt["phase"] == "retired"
assert receipt["result"] == terminal["result"]
assert receipt["result"]["exit_code"] == 0 and receipt["result"]["quiescent"]
assert not receipt["result"]["io_errors"]
assert receipt["scratch_absent"] and receipt["reservation_released"]
assert not os.path.lexists(Path(config["roots"]["scratch"]) / job_id)
assert not os.path.lexists(Path(config["roots"]["control"]) / "active.json")
for relative, expected in job["inputs"].items():
    assert owner.file_digest(REPO / relative) == expected, relative
assert owner.file_digest(Path(job["argv"][0])) == job["executable_sha256"]
for member, expected in receipt["collected_manifest"].items():
    assert member in ("output", "logs") and owner.content_digest(root / member) == expected
files = []
pending = [root]
while pending:
    directory = pending.pop()
    owner.ordinary(directory, directory=True)
    for path in directory.iterdir():
        if path.is_dir():
            owner.ordinary(path, directory=True)
            pending.append(path)
        else:
            info = owner.ordinary(path)
            assert info.st_nlink == 1
            files.append({"path": path.relative_to(root).as_posix(), "bytes": info.st_size,
                          "sha256": owner.file_digest(path)})
        assert len(pending) + len(files) <= 100
files.sort(key=lambda item: item["path"])
stream = root / "logs/stdout"
events = [json.loads(line) for line in stream.read_text(encoding="utf-8").splitlines() if line.strip()]
responses = []
tool_events = []
for event in events:
    item = event.get("item", {})
    if item.get("type") == "agent_message":
        responses.append(json.loads(item["text"]))
    elif item:
        tool_events.append(item.get("type"))
assert len(responses) == 1 and not tool_events
assert set(responses[0]) == {"verdict", "evidence", "regression", "limitation"}
spec = importlib.util.spec_from_file_location("matched_custody_cli", REPO / ".aide/scripts/aide_lite.py")
cli = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = cli
spec.loader.exec_module(cli)
usage = cli.summarize_codex_exec_usage([stream])
assert usage["completed_turns"] == 1 and usage["failed_or_incomplete_turns"] == 0
record = {
    "schema": "aide.actual-matched-model-result.v1", "profile": profile,
    "job_id": job_id, "manifest_digest": receipt["manifest_digest"],
    "receipt_sha256": owner.file_digest(root / "receipt.json"),
    "response": responses[0], "usage": usage, "tool_events": tool_events,
    "full_collection_verified": True, "files": files,
    "retained_bytes": sum(item["bytes"] for item in files), "peaks": receipt["peaks"],
    "scratch_absent": True, "reservation_released": True,
    "codex_admitted_after": owner.dispatch_state(Path(config["roots"]["control"]))["codex_admitted"],
    "requested_model": job["model"], "effort": job["effort"],
    "account": "existing_signed_in_chatgpt", "actual_model_identity": "not_reported",
    "whole_session_contained": False,
    "whole_cost": "unknown_parent_review_repair_and_host_internal_coverage",
}
target = EVIDENCE / ("matched-" + profile + ".json")
target.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8"))
print(json.dumps({"profile": profile, "job_id": job_id, "custody": "PASS",
                  "usage": usage["known_usage_totals"], "response": responses[0],
                  "record_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}, sort_keys=True))
