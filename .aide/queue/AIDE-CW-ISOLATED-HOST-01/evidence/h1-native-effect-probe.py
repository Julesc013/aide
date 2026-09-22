"""Execute only one separately reviewed H1 profile/object probe; retain all effects."""
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
SOURCES = (
    "core/runtime/continuous_worker/windows_security.py",
    "core/runtime/continuous_worker/windows_security_objects.py",
    "core/runtime/continuous_worker/windows_job.py",
    ".aide/scripts/tests/test_continuous_worker_windows_security.py",
    ".aide/scripts/tests/test_continuous_worker_windows_security_probe.c",
    ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-native-effect-probe.py",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def run(manifest_path, approved_digest):
    # Digest binding identifies the independently reviewed effect; it is not an
    # authorization mechanism or a production worker-supplied configuration.
    raw = Path(manifest_path).read_bytes()
    if len(raw) > 65536 or digest(raw) != approved_digest:
        raise RuntimeError("reviewed H1 effect manifest digest mismatch")
    value = json.loads(raw)
    required = {"schema", "source_base", "repository", "source_files", "owned_root", "owner_sha256",
                "parent_stat", "native_volume", "moniker", "package_sid", "user_sid", "probe_sha256", "expires_at",
                "effects", "activation"}
    if set(value) != required or value["schema"] != "aide.host.h1-effect.v1" or value["activation"] is not False:
        raise RuntimeError("unknown or active H1 effect manifest")
    if Path(value["repository"]) != ROOT or set(value["source_files"]) != set(SOURCES):
        raise RuntimeError("H1 source set differs from exact reviewed programme")
    if type(value["expires_at"]) not in (int, float) or not 0 < value["expires_at"] - time.time() <= 7200:
        raise RuntimeError("H1 effect manifest needs a fresh finite expiry")
    deadline = time.monotonic() + (value["expires_at"] - time.time())
    for path, expected in value["source_files"].items():
        if digest((ROOT / path).read_bytes()) != expected:
            raise RuntimeError("H1 source changed after independent review")
    owned = Path(value["owned_root"])
    if not owned.is_absolute() or owned.name[:15] != "aide-h1-source-"[:15]:
        raise RuntimeError("exact marker-owned H1 root required")
    for path in (owned, *owned.parents):
        if path.is_symlink() or path.is_junction():
            raise RuntimeError("H1 owned root ancestry has a reparse point")
    info = owned.stat()
    if {"dev": info.st_dev, "ino": info.st_ino} != value["parent_stat"]:
        raise RuntimeError("H1 parent identity changed")
    if digest((owned / "owner.json").read_bytes()) != value["owner_sha256"]:
        raise RuntimeError("H1 ownership marker changed")
    image_bytes = (owned / "security-probe.exe").read_bytes()
    if len(image_bytes) > 16 * 1024 * 1024 or digest(image_bytes) != value["probe_sha256"]:
        raise RuntimeError("H1 native probe input differs from reviewed build")
    effects = {"profile_creations": 1, "package_capabilities": [], "root": str(owned / "probe-objects"),
               "reservation": str(owned / "profile-reservation.jsonl"),
               "new_objects": ["probe.exe", "scratch", "protected-canary"],
               "package_grants": {".": "read", "probe.exe": "read", "scratch": "modify"},
               "loopback": "one owned 127.0.0.1 listener; no exemption", "cleanup": "retain_only"}
    if value["effects"] != effects:
        raise RuntimeError("H1 effect set differs from fixed source implementation")
    sys.path.insert(0, str(ROOT))
    from core.runtime.continuous_worker.windows_security_objects import local_volume
    if local_volume(owned.drive) != value["native_volume"]:
        raise RuntimeError("H1 observed local volume changed")
    def guard():
        if not time.time() < value["expires_at"] or not time.monotonic() < deadline:
            raise RuntimeError("H1 effect authority expired")
        if local_volume(owned.drive) != value["native_volume"]:
            raise RuntimeError("H1 observed local volume changed before an effect")
        current = owned.stat()
        if {"dev": current.st_dev, "ino": current.st_ino} != value["parent_stat"] or digest((owned / "owner.json").read_bytes()) != value["owner_sha256"]:
            raise RuntimeError("H1 owned parent or marker changed")
        if any(digest((ROOT / path).read_bytes()) != expected for path, expected in value["source_files"].items()):
            raise RuntimeError("H1 reviewed source changed before an effect")
    if any((owned / name).exists() for name in ("profile-reservation.jsonl", "probe-objects", "native-job-output")):
        raise RuntimeError("H1 probe cannot replay or adopt a preexisting effect")
    sys.path.insert(0, str(ROOT))
    from core.runtime.continuous_worker.windows_security import ProfileSpec, PreparedProfile, SecurityLaunch, current_user_sid, expected_package_sid
    from core.runtime.continuous_worker.windows_security_objects import OwnedObject
    from core.runtime.continuous_worker.windows_job import WindowsJobHost
    spec = ProfileSpec(value["moniker"], effects["reservation"])
    if current_user_sid() != value["user_sid"] or expected_package_sid(spec) != value["package_sid"]:
        raise RuntimeError("H1 controller or expected profile SID changed")
    receipt = {"schema": "aide.host.h1-native-probe.v1", "manifest_sha256": approved_digest,
               "source_files": value["source_files"], "cleanup": "retain_only", "activation": False,
               "full_private_toolchain_or_model_host": False, "result": "PENDING"}
    receipt_path = owned / "native-probe-receipt.json"
    handles = []
    try:
        # This is the single separately reviewed persistent profile effect.
        profile = PreparedProfile.create_once(spec, guard=guard)
        receipt["profile"] = {"moniker": profile.spec.moniker, "package_sid": profile.package_sid, "folder": profile.folder}
        root = OwnedObject.create_root(effects["root"], value["user_sid"], guard=guard); handles.append(root)
        image = root.child("probe.exe"); handles.append(image)
        scratch = root.child("scratch", directory=True); handles.append(scratch)
        canary = root.child("protected-canary"); handles.append(canary)
        image.write(image_bytes)
        canary.write(("synthetic H1 protected canary " + value["moniker"]).encode())
        for obj in (image, scratch, canary, root):
            obj.seal()
        root.grant(profile.package_sid, mode="read")
        image.grant(profile.package_sid, mode="read")
        scratch.grant(profile.package_sid, mode="modify")
        receipt["objects"] = [obj.observe() for obj in handles]
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0)); listener.listen(1); listener.settimeout(0.15)
            argv = [image.path, scratch.path, canary.path, str(os.getpid()), str(listener.getsockname()[1])]
            security = SecurityLaunch(profile, user_sid=value["user_sid"], argv=argv, cwd=scratch.path,
                                      image_sha256=value["probe_sha256"], owned_objects=tuple(handles), guard=guard)
            def cancelled():
                try:
                    security.assert_launch(argv, scratch.path)
                    return False
                except Exception:
                    return True
            result = WindowsJobHost().run(argv, cwd=scratch.path, input_bytes=b"", output_dir=owned / "native-job-output",
                job_id=value["moniker"].rsplit(".", 1)[1], timeout=10, output_limit=16384,
                memory_limit=128 * 1024 * 1024, process_limit=4,
                cancelled=cancelled, security=security)
            security.assert_launch(argv, scratch.path)
            receipt["process"], receipt["actual_child_token"] = result, security.child_observation
            try:
                peer, _ = listener.accept(); peer.close(); connected = True
            except socket.timeout:
                connected = False
            receipt["loopback_connection_observed"] = connected
        output = (owned / "native-job-output/stdout").read_bytes()
        errors = (owned / "native-job-output/stderr").read_bytes()
        receipt["stdout_sha256"], receipt["stderr_sha256"] = digest(output), digest(errors)
        observed = json.loads(output)
        expected = {"scratch_error": 0, "read_error": 5, "write_error": 5,
                    "dacl_error": 5, "controller_error": 5, "network_error": 10013}
        if (not isinstance(observed, dict) or set(observed) != set(expected) or
                any(type(observed[k]) is not int or observed[k] != expected[k] for k in expected) or
                result["exit_code"] != 0 or result["reason"] != "exited" or not result["quiescent"] or connected or errors):
            raise RuntimeError("actual native H1 denial observations did not pass")
        if (Path(scratch.path) / "native-created.txt").read_bytes() != b"owned-native-probe":
            raise RuntimeError("actual native H1 positive scratch proof failed")
        receipt["denials"], receipt["result"] = observed, "PASS"
    except Exception as error:
        receipt["result"], receipt["failure_type"] = "FAIL", type(error).__name__
        raise
    finally:
        for obj in reversed(handles):
            obj.close()
        with open(receipt_path, "xb") as target:
            target.write((json.dumps(receipt, indent=2) + "\n").encode())
            target.flush(); os.fsync(target.fileno())
    print(json.dumps({"result": receipt["result"], "receipt": str(receipt_path), "cleanup": "retain_only"}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: h1-native-effect-probe.py <reviewed-manifest> <exact-sha256>")
    run(sys.argv[1], sys.argv[2])
