"""Bounded read-only custody check for one previously recorded linked worktree."""
import ctypes
import base64
import re
import hashlib
import json
import os
from pathlib import Path
import queue
import stat
import subprocess
import threading
import time

TARGET = Path("D:/Development/FacMan/repositories/universal-setup-db9c210f4a17/worktrees/task-usk-wu-006-production-publisher")
MASTER = Path("D:/Projects/Universal/universal-setup")
GIT = Path("C:/Program Files/Git/cmd/git.exe")
GIT_SHA = "da240fe9bc24895b3e04150a4990b8a6ff329ecabcd8f19684c2cc310da5ef3f"
OUTPUT = Path(os.environ["AIDE_JOB_OUTPUT"])
RAW_REMAINING = 24576


def identity():
    name = ctypes.create_unicode_buffer(256)
    length = ctypes.c_ulong(len(name))
    if not ctypes.windll.secur32.GetUserNameExW(2, name, ctypes.byref(length)):
        raise ctypes.WinError()
    if name.value != "BLACKGLASS-WIN1\\CodexSandboxOffline":
        raise ValueError("unexpected native worker identity")
    return name.value


def ordinary_directory(path):
    for part in [*reversed(path.parents), path]:
        info = part.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_file_attributes & 1024:
            raise ValueError("redirected or missing selected directory")


def git_read(root, *arguments):
    global RAW_REMAINING
    limit = min(8192, RAW_REMAINING)
    if limit == 0:
        return {"exit_code": None, "complete": False, "limit_reason": "total_raw_budget", "raw_base64": ""}
    argv = [str(GIT), "-c", "safe.directory=" + str(TARGET), "-c",
            "safe.directory=" + str(MASTER), "-c", "core.fsmonitor=false",
            "-c", "core.untrackedCache=false", "-C", str(root), *arguments]
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0",
               GIT_NO_REPLACE_OBJECTS="1")
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               env=env, creationflags=subprocess.CREATE_NO_WINDOW)
    chunks = queue.Queue(maxsize=2)
    def read():
        try:
            while True:
                chunk = process.stdout.read(1024)
                chunks.put(chunk)
                if not chunk:
                    break
        except (OSError, ValueError):
            chunks.put(b"")
    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    data = bytearray()
    deadline = time.monotonic() + 20
    complete = True
    reason = None
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                complete, reason = False, "timeout"
                break
            try:
                chunk = chunks.get(timeout=remaining)
            except queue.Empty:
                complete, reason = False, "timeout"
                break
            if not chunk:
                break
            if len(data) + len(chunk) > limit:
                data.extend(chunk[:limit - len(data)])
                complete, reason = False, "output_limit"
                break
            data.extend(chunk)
        if not complete and process.poll() is None:
            process.terminate()  # Only this exact owned Git child.
        try:
            code = process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            code = process.wait(timeout=2)
            complete, reason = False, "child_timeout"
    finally:
        process.stdout.close()
    reader.join(timeout=0.2)
    RAW_REMAINING -= len(data)
    return {"argv": argv, "exit_code": code, "complete": complete,
            "limit_reason": reason, "observed_bytes": len(data),
            "raw_sha256": hashlib.sha256(data).hexdigest(),
            "raw_base64": base64.b64encode(data).decode("ascii")}


def raw_text(record):
    return base64.b64decode(record["raw_base64"]).decode("utf-8", errors="replace")


def metadata():
    deadline = time.monotonic() + 10
    stack = [TARGET]
    result = {"entries": 0, "files": 0, "directories": 0,
              "logical_bytes": 0, "observed_unique_logical_bytes": 0,
              "shared_file_entries": 0, "redirected_entries": 0,
              "errors": 0, "complete": True, "file_contents_read": False}
    seen = set()
    while stack:
        directory = stack.pop()
        try:
            with os.scandir(directory) as entries:
                for entry in entries:
                    if result["entries"] >= 5000 or time.monotonic() >= deadline:
                        result.update(complete=False, stop="entry_or_time_limit")
                        return result
                    result["entries"] += 1
                    try:
                        info = entry.stat(follow_symlinks=False)
                        if info.st_file_attributes & 1024 or stat.S_ISLNK(info.st_mode):
                            result["redirected_entries"] += 1
                            result["complete"] = False
                        elif stat.S_ISDIR(info.st_mode):
                            result["directories"] += 1
                            stack.append(Path(entry.path))
                        elif stat.S_ISREG(info.st_mode):
                            result["files"] += 1
                            result["logical_bytes"] += info.st_size
                            key = (info.st_dev, info.st_ino)
                            if key not in seen:
                                seen.add(key)
                                result["observed_unique_logical_bytes"] += info.st_size
                            if info.st_nlink > 1:
                                result["shared_file_entries"] += 1
                        else:
                            result["errors"] += 1
                            result["complete"] = False
                    except OSError:
                        result["errors"] += 1
                        result["complete"] = False
        except OSError:
            result["errors"] += 1
            result["complete"] = False
    result["allocated_or_reclaimable_bytes"] = None
    return result


def main():
    result = {"schema": "aide.single-worktree-custody.v1",
              "worker_identity": identity(), "target": str(TARGET),
              "master": str(MASTER), "model_calls": 0,
              "target_mutations": False, "disposable_proven": False,
              "active_other_writer_coverage": "unknown", "commands": {}}
    try:
        ordinary_directory(TARGET)
        ordinary_directory(MASTER)
        if hashlib.sha256(GIT.read_bytes()).hexdigest() != GIT_SHA:
            raise ValueError("Git executable changed")
        commands = result["commands"]
        for label, root, args in [
            ("target_head_before", TARGET, ["rev-parse", "HEAD"]),
            ("master_head_before", MASTER, ["rev-parse", "HEAD"]),
            ("common", TARGET, ["rev-parse", "--path-format=absolute", "--git-common-dir"]),
            ("branch", TARGET, ["symbolic-ref", "--quiet", "HEAD"]),
            ("tracked", TARGET, ["status", "--porcelain=v1", "--untracked-files=no"]),
            ("untracked", TARGET, ["ls-files", "--others", "--exclude-standard", "-z"]),
            ("ignored", TARGET, ["ls-files", "--others", "--ignored", "--exclude-standard", "-z"]),
            ("registration", MASTER, ["worktree", "list", "--porcelain"]),
        ]:
            commands[label] = git_read(root, *args)
        head = raw_text(commands["target_head_before"]).strip()
        if commands["target_head_before"]["complete"] and commands["target_head_before"]["exit_code"] == 0 and re.fullmatch("[0-9a-f]{40}", head):
            commands["covering_refs"] = git_read(MASTER, "for-each-ref", "--contains=" + head, "--format=%(refname) %(objectname)", "refs/heads", "refs/remotes")
        else:
            commands["covering_refs"] = {"complete": False, "reason": "current_head_unknown"}
        result["metadata"] = metadata()
        for label, root in [("target_head_after", TARGET), ("master_head_after", MASTER)]:
            commands[label] = git_read(root, "rev-parse", "HEAD")
        common = commands["common"]
        result["common_matches_recorded_master"] = (
            common["complete"] and common["exit_code"] == 0
            and os.path.normcase(raw_text(common).strip())
                == os.path.normcase(str(MASTER / ".git")))
        result["heads_unchanged"] = all(
            commands[prefix + "_before"]["complete"]
            and commands[prefix + "_after"]["complete"]
            and commands[prefix + "_before"]["exit_code"] == 0
            and commands[prefix + "_after"]["exit_code"] == 0
            and raw_text(commands[prefix + "_before"]) == raw_text(commands[prefix + "_after"])
            for prefix in ["target_head", "master_head"])
        result["status"] = "OBSERVED" if result["heads_unchanged"] else "PARTIAL"
        # Paths and metadata alone never authorize cleanup or prove quiescence.
    except (OSError, ValueError) as exc:
        result.update(status="PARTIAL", reason=str(exc))
    encoded = json.dumps(result, indent=2, ensure_ascii=False).encode("utf-8")
    if len(encoded) > 60000:
        raise ValueError("result exceeds retained metadata envelope")
    (OUTPUT / "storage-custody.json").write_bytes(encoded)
    print(json.dumps({"status": result["status"], "disposable_proven": False,
                      "target_mutations": False, "retained_bytes": len(encoded)}))


if __name__ == "__main__":
    main()
