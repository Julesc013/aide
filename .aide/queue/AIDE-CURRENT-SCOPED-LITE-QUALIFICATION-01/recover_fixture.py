"""Retire one frozen public extraction fixture as its original owner; no ACL edits."""
import argparse
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import os
from pathlib import Path
import stat
import zipfile

TASK = Path(__file__).resolve().parent
REPO = TASK.parents[2]
EFFECT = TASK / "evidence/recovery-effect-46e91fbf.json"
CONTROL = Path(r"D:\Projects\AIDE\.aide.local\execution\control")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def owner_sid(path):
    api = C.WinDLL("advapi32", use_last_error=True)
    get = api.GetNamedSecurityInfoW
    get.argtypes = [W.LPWSTR, C.c_int, W.DWORD, *([C.POINTER(C.c_void_p)] * 5)]
    get.restype = W.DWORD
    sid, descriptor = C.c_void_p(), C.c_void_p()
    code = get(str(path), 1, 1, C.byref(sid), None, None, None, C.byref(descriptor))
    if code:
        raise C.WinError(code)
    value = W.LPWSTR()
    convert = api.ConvertSidToStringSidW
    convert.argtypes = [C.c_void_p, C.POINTER(W.LPWSTR)]
    convert.restype = W.BOOL
    free = C.WinDLL("kernel32").LocalFree
    free.argtypes = [C.c_void_p]
    free.restype = C.c_void_p
    try:
        if not convert(sid, C.byref(value)):
            raise C.WinError(C.get_last_error())
        return value.value
    finally:
        if value:
            free(C.cast(value, C.c_void_p))
        free(descriptor)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    effect = json.loads(EFFECT.read_text(encoding="utf-8"))
    active = CONTROL / "active.json"
    if sha(active) != effect["active_raw_sha256"]:
        raise RuntimeError("recovery lease changed")
    record = json.loads(active.read_text(encoding="utf-8"))
    if (record["job_id"] != effect["job_id"] or record["manifest_digest"] != effect["manifest_digest"]
            or record["phase"] != effect["phase_required"]
            or not record.get("reconciliation", {}).get("quiescent")):
        raise RuntimeError("recovery owner/phase changed")
    identity = C.create_unicode_buffer(256)
    size = W.ULONG(len(identity))
    if not C.windll.secur32.GetUserNameExW(2, identity, C.byref(size)):
        raise C.WinError()
    if identity.value.lower() != effect["identity_required"].lower():
        raise RuntimeError("creation identity required")
    scratch = Path(record["scratch"])
    info = scratch.lstat()
    if ([info.st_dev, info.st_ino] != effect["scratch_identity"]
            or json.loads((scratch / "owner.json").read_text()) != {
                "job_id": effect["job_id"], "manifest_digest": effect["manifest_digest"]}):
        raise RuntimeError("scratch identity changed")
    fixture = scratch / effect["owned_fixture"]
    root = fixture.lstat()
    if (not stat.S_ISDIR(root.st_mode) or root.st_file_attributes & 0x400
            or not root.st_ino or [root.st_dev, root.st_ino] != effect["fixture_identity"]):
        raise RuntimeError("invalid fixture root")
    if not fixture.resolve(strict=True).is_relative_to(scratch.resolve(strict=True) / "tmp"):
        raise RuntimeError("fixture escaped owned job")
    expected = {}
    directories = {""}
    for relative, digest in effect["archive_inputs"].items():
        archive = REPO / relative
        if sha(archive) != digest:
            raise RuntimeError("frozen public input changed")
        with zipfile.ZipFile(archive) as zipped:
            for member in zipped.infolist():
                if member.is_dir():
                    continue
                path = Path(member.filename)
                if path.is_absolute() or path.drive or ".." in path.parts:
                    raise RuntimeError("unsafe input member")
                expected.setdefault(member.filename, []).append(zipped.read(member))
                directories.update(parent.as_posix() for parent in path.parents if str(parent) != ".")
    entries = [fixture]
    pending = [fixture]
    total = 0
    digest = hashlib.sha256()
    owner = owner_sid(fixture)
    if owner != effect["owner_sid_required"]:
        print(json.dumps({"status": "OWNER_MISMATCH", "job_id": record["job_id"],
                          "fixture": effect["owned_fixture"],
                          "fixture_identity": [root.st_dev, root.st_ino],
                          "owner_sid": owner, "creation_identity": identity.value,
                          "contents_inspected": False, "apply": args.apply}, sort_keys=True), flush=True)
        raise RuntimeError("fixture is not owned by the exact creation account")
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as children:
            for item in sorted(children, key=lambda child: child.name):
                path = Path(item.path)
                entries.append(path)
                if len(entries) > effect["max_entries"]:
                    raise RuntimeError("recovery entry limit")
                info = path.lstat()
                relative = path.relative_to(fixture).as_posix()
                if (stat.S_ISLNK(info.st_mode) or info.st_file_attributes & 0x400
                        or owner_sid(path) != owner):
                    raise RuntimeError("redirected or unrelated fixture member")
                if stat.S_ISDIR(info.st_mode):
                    if relative not in directories:
                        raise RuntimeError("unknown fixture directory")
                    pending.append(path)
                    digest.update(json.dumps([relative, "directory", info.st_dev, info.st_ino]).encode())
                elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
                    total += info.st_size
                    if total > effect["bound_bytes"]:
                        raise RuntimeError("recovery byte limit")
                    data = path.read_bytes()
                    if not any(body.startswith(data) for body in expected.get(relative, [])):
                        raise RuntimeError("unknown or modified fixture bytes")
                    digest.update(json.dumps([relative, "file", info.st_dev, info.st_ino,
                                              len(data), hashlib.sha256(data).hexdigest()]).encode())
                else:
                    raise RuntimeError("shared or nonregular fixture entry")
    observation = {"status": "VERIFIED", "job_id": record["job_id"],
                   "fixture": effect["owned_fixture"], "fixture_identity": [root.st_dev, root.st_ino],
                   "owner_sid": owner, "creation_identity": identity.value,
                   "entries": len(entries), "logical_bytes": total,
                   "file_custody_digest": digest.hexdigest(), "acl_changes_by_helper": 0,
                   "apply": args.apply}
    if args.apply:
        approved = effect.get("approved_observation")
        current = {key: observation[key] for key in ("fixture_identity", "owner_sid", "entries",
                                                    "logical_bytes", "file_custody_digest")}
        if approved != current:
            raise RuntimeError("exact inspected custody is not approved for retirement")
        for path in sorted(entries, key=lambda item: len(item.parts), reverse=True):
            if path.is_dir():
                path.rmdir()
            else:
                path.unlink()
        if fixture.exists():
            raise RuntimeError("fixture retirement failed")
        observation["status"] = "RETIRED_FIXTURE"
    print(json.dumps(observation, sort_keys=True))


if __name__ == "__main__":
    main()
