"""One reviewed network continuation of a proved created profile; no profile creation."""
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import socket
import subprocess
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
    ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-owned-network-effect-probe.py",
    ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-network-oracle-validation.py",
)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def observed_created_profile(owned, moniker, package, user, proof):
    """Only the externally pinned successful creation journal admits continuation."""
    from core.runtime.continuous_worker.windows_security import ProfileSpec, PreparedProfile, verify_observation
    values = {}
    for name, expected in proof.items():
        raw = (owned / name).read_bytes()
        if len(raw) > 65536 or digest(raw) != expected:
            raise RuntimeError("original created-profile proof changed or exceeds bound")
        values[name] = raw
    rows = [json.loads(row) for row in values["profile-reservation.jsonl"].splitlines()]
    receipt = json.loads(values["native-probe-receipt.json"])
    if len(rows) != 2 or not all(isinstance(row, dict) for row in rows) or not isinstance(receipt, dict):
        raise RuntimeError("complete original profile creation proof required")
    intent, created = rows
    if type(intent.get("capability_count")) is not int or intent != {"schema": "aide.host.profile-intent.v1", "moniker": moniker,
                  "expected_package_sid": package, "capability_count": 0, "cleanup": "retain_only"}:
        raise RuntimeError("original profile intent differs from admitted identity")
    if (set(created) != {"phase", "package_sid", "folder", "cleanup"} or
            created["phase"] != "created" or created["package_sid"] != package or
            created["cleanup"] != "retain_only" or not isinstance(created["folder"], str) or
            not Path(created["folder"]).is_absolute()):
        raise RuntimeError("original profile was not durably observed created")
    if (receipt.get("schema") != "aide.host.h1-native-probe.v1" or receipt.get("activation") is not False or
            receipt.get("profile") != {"moniker": moniker, "package_sid": package, "folder": created["folder"]}):
        raise RuntimeError("original profile receipt differs from created journal")
    verify_observation(receipt.get("actual_child_token"), package, user)
    return PreparedProfile(ProfileSpec(moniker, str(owned / "profile-reservation.jsonl")), package, created["folder"])


def pinned_endpoint(value):
    if not isinstance(value, dict) or set(value) != {"address", "interface_index", "interface_alias", "prefix_length", "inventory_sha256"}:
        raise RuntimeError("exact local endpoint inventory binding required")
    try:
        address = ipaddress.IPv4Address(value["address"])
        private = any(address in ipaddress.IPv4Network(net) for net in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
        if (str(address) != value["address"] or not private or type(value["interface_index"]) is not int or
                not 1 <= value["interface_index"] <= 0xffffffff or type(value["prefix_length"]) is not int or
                not 1 <= value["prefix_length"] <= 30 or not isinstance(value["interface_alias"], str) or
                not 1 <= len(value["interface_alias"]) <= 256):
            raise ValueError("unsupported literal local endpoint")
        network = ipaddress.IPv4Network((address, value["prefix_length"]), strict=False)
        if address in (network.network_address, network.broadcast_address):
            raise ValueError("network or broadcast address")
    except (TypeError, ValueError, KeyError) as error:
        raise RuntimeError("canonical private unicast IPv4 and exact interface required") from error
    path = ROOT / ".aide/queue/AIDE-CW-ISOLATED-HOST-01/evidence/h1-local-interface-inventory.json"
    raw = path.read_bytes()
    if len(raw) > 65536 or digest(raw) != value["inventory_sha256"]:
        raise RuntimeError("pinned read-only endpoint inventory changed")
    inventory = json.loads(raw)
    if not isinstance(inventory, dict) or inventory.get("schema") != "aide.host.h1-local-interface-inventory.v1" or not isinstance(inventory.get("observations"), list):
        raise RuntimeError("known read-only interface inventory required")
    rows = inventory["observations"]
    expected = {key: value[key] for key in ("address", "interface_index", "interface_alias", "prefix_length")}
    expected.update(address_state="Preferred", connection_state="Connected", skip_as_source=False)
    if (len(rows) > 256 or not all(isinstance(row, dict) for row in rows) or
            [row for row in rows if row.get("address") == value["address"] or row.get("interface_index") == value["interface_index"]] != [expected]):
        raise RuntimeError("exact unique preferred connected interface inventory required")
    return dict(value)


def observe_endpoint(image, expected, endpoint):
    # This native entry only calls read-only Windows interface APIs. No sockets,
    # files, profile, capability or network configuration effects are admitted.
    raw = Path(image).read_bytes()
    if len(raw) > 16 * 1024 * 1024 or digest(raw) != expected:
        raise RuntimeError("read-only interface image changed")
    result = subprocess.run([str(image), "--local-interface", endpoint["address"],
                             str(endpoint["interface_index"]), endpoint["interface_alias"]],
                            capture_output=True, timeout=1)
    if result.returncode != 0 or result.stderr or len(result.stdout) > 512:
        raise RuntimeError("bounded actual read-only interface observation failed")
    value = json.loads(result.stdout)
    wanted = {"address_status": 0, "adapter_status": 0, "address_match": 1, "index_match": 1,
              "alias_match": 1, "preferred": 1, "connected": 1, "prefix_length": endpoint["prefix_length"], "skip_as_source": 0}
    if not isinstance(value, dict) or value != wanted or any(type(field) is not int for field in value.values()):
        raise RuntimeError("actual interface is not the pinned preferred connected address")
    return value


def positive_control(listener, guard):
    """One ordinary connect to this exact live listener, correlated by peer port."""
    guard()
    endpoint = listener.getsockname()
    with socket.socket() as client:
        client.settimeout(1)
        client.connect(endpoint)
        peer, address = listener.accept()
        try:
            if address != client.getsockname():
                raise RuntimeError("owned positive control accepted an unrelated connection")
            control = {"endpoint": list(endpoint), "client": list(client.getsockname()), "accepted": list(address)}
        finally:
            peer.close()
    guard()
    return control


def verify_network_evidence(observed, receipt, package, endpoint):
    # A timeout is retained as a timeout. Qualification requires independent
    # Windows capability/configuration facts plus actual endpoint controls.
    if (type(observed.get("network_error")) is not int or observed["network_error"] not in (10013, 10060) or
            type(observed.get("diagnostic_status")) is not int or observed["diagnostic_status"] != 0 or
            type(observed.get("missing_capability")) is not int or observed["missing_capability"] not in (1, 2, 3) or
            receipt.get("endpoint_connection_observed") is not False):
        raise RuntimeError("complete actual calling-token network diagnosis required")
    before, after = receipt.get("loopback_configuration_before"), receipt.get("loopback_configuration_after")
    if (not isinstance(before, dict) or before != after or
            set(before) != {"package_sid", "configuration_count", "loopback_exempt"} or
            before["package_sid"] != package or before["loopback_exempt"] is not False or
            type(before["configuration_count"]) is not int or not 0 <= before["configuration_count"] <= 4096):
        raise RuntimeError("exact stable package non-exemption required")
    controls = [receipt.get("positive_control_before"), receipt.get("positive_control_after")]
    for control in controls:
        if not isinstance(control, dict) or set(control) != {"endpoint", "client", "accepted"}:
            raise RuntimeError("both actual endpoint positive controls required")
        for field in ("endpoint", "client", "accepted"):
            address = control[field]
            if (not isinstance(address, list) or len(address) != 2 or address[0] != endpoint["address"] or
                    type(address[1]) is not int or not 1 <= address[1] <= 65535):
                raise RuntimeError("exact local positive control endpoint required")
        if control["client"] != control["accepted"]:
            raise RuntimeError("positive control client and accepted peer differ")
    if controls[0]["endpoint"] != controls[1]["endpoint"]:
        raise RuntimeError("before and after controls must prove the same listener")


def run(manifest_path, approved_digest):
    # Digest binding identifies the independently reviewed effect; it is not an
    # authorization mechanism or a production worker-supplied configuration.
    raw = Path(manifest_path).read_bytes()
    if len(raw) > 65536 or digest(raw) != approved_digest:
        raise RuntimeError("reviewed H1 effect manifest digest mismatch")
    value = json.loads(raw)
    required = {"schema", "source_base", "repository", "source_files", "owned_root", "owner_sha256",
                "parent_stat", "native_volume", "moniker", "package_sid", "user_sid", "probe_sha256", "expires_at",
                "effects", "activation", "origin_proof", "endpoint"}
    if set(value) != required or value["schema"] != "aide.host.h1-owned-interface-effect.v1" or value["activation"] is not False:
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
    endpoint = pinned_endpoint(value["endpoint"])
    input_image = owned / "security-probe-interface.exe"
    image_bytes = input_image.read_bytes()
    if len(image_bytes) > 16 * 1024 * 1024 or digest(image_bytes) != value["probe_sha256"]:
        raise RuntimeError("H1 native probe input differs from reviewed build")
    effects = {"profile_creations": 0, "package_capabilities": [], "root": str(owned / "interface-probe-objects"),
               "reservation": str(owned / "interface-probe-reservation.jsonl"),
               "new_objects": ["probe.exe", "scratch", "protected-canary"],
               "package_grants": {".": "read", "probe.exe": "read", "scratch": "modify"},
               "listener": {"address": endpoint["address"], "port": 0, "count": 1, "exclusive": True},
               "ordinary_controls": 2, "read_only_interface_observations": {"max_calls": 256, "timeout_seconds": 1, "output_bytes": 512},
               "network_settings_changes": 0, "cleanup": "retain_only"}
    if value["effects"] != effects:
        raise RuntimeError("H1 effect set differs from fixed source implementation")
    sys.path.insert(0, str(ROOT))
    from core.runtime.continuous_worker.windows_security_objects import local_volume
    if local_volume(owned.drive) != value["native_volume"]:
        raise RuntimeError("H1 observed local volume changed")
    proof = value["origin_proof"]
    if not isinstance(proof, dict) or set(proof) != {"profile-reservation.jsonl", "native-probe-receipt.json"}:
        raise RuntimeError("exact prior created-profile proof required")
    observation_count = 0
    def guard():
        nonlocal observation_count
        if not time.time() < value["expires_at"] or not time.monotonic() < deadline:
            raise RuntimeError("H1 effect authority expired")
        if local_volume(owned.drive) != value["native_volume"]:
            raise RuntimeError("H1 observed local volume changed before an effect")
        if any(digest((owned / name).read_bytes()) != expected for name, expected in proof.items()):
            raise RuntimeError("original created-profile proof changed")
        current = owned.stat()
        if {"dev": current.st_dev, "ino": current.st_ino} != value["parent_stat"] or digest((owned / "owner.json").read_bytes()) != value["owner_sha256"]:
            raise RuntimeError("H1 owned parent or marker changed")
        if any(digest((ROOT / path).read_bytes()) != expected for path, expected in value["source_files"].items()):
            raise RuntimeError("H1 reviewed source changed before an effect")
        pinned_endpoint(endpoint)
        if observation_count >= 256:
            raise RuntimeError("read-only interface observation budget exhausted")
        observation_count += 1
        observe_endpoint(input_image, value["probe_sha256"], endpoint)
        if not time.time() < value["expires_at"] or not time.monotonic() < deadline:
            raise RuntimeError("H1 effect authority expired during read-only observation")
    if any((owned / name).exists() for name in ("interface-probe-reservation.jsonl", "interface-probe-objects", "interface-native-job-output", "interface-native-probe-receipt.json")):
        raise RuntimeError("H1 probe cannot replay or adopt a preexisting effect")
    sys.path.insert(0, str(ROOT))
    from core.runtime.continuous_worker.windows_security import SecurityLaunch, current_user_sid, expected_package_sid, loopback_configuration
    from core.runtime.continuous_worker.windows_security_objects import OwnedObject
    from core.runtime.continuous_worker.windows_job import WindowsJobHost
    guard()
    profile = observed_created_profile(owned, value["moniker"], value["package_sid"], value["user_sid"], proof)
    spec = profile.spec
    if current_user_sid() != value["user_sid"] or expected_package_sid(spec) != value["package_sid"]:
        raise RuntimeError("H1 controller or expected profile SID changed")
    receipt = {"schema": "aide.host.h1-owned-interface-probe.v1", "manifest_sha256": approved_digest,
               "source_files": value["source_files"], "cleanup": "retain_only", "activation": False,
               "full_private_toolchain_or_model_host": False, "result": "PENDING"}
    receipt["origin_proof"] = proof
    receipt["endpoint"] = endpoint
    receipt["profile_action"] = "use_exact_durably_created_identity_without_profile_creation"
    receipt_path = owned / "interface-native-probe-receipt.json"
    configuration_before = loopback_configuration(profile.package_sid)
    if configuration_before["loopback_exempt"] is not False:
        raise RuntimeError("owned package has a loopback exemption")
    receipt["loopback_configuration_before"] = configuration_before
    handles = []
    try:
        # The original failed probe never authorizes replay. This separately
        # reviewed continuation reserves its own one-shot object/launch effect.
        guard()
        with open(effects["reservation"], "xb", buffering=0) as intent:
            raw_intent = (json.dumps({"manifest_sha256": approved_digest, "origin_proof": proof,
                                      "profile_creations": 0, "cleanup": "retain_only"}, sort_keys=True) + "\n").encode()
            if intent.write(raw_intent) != len(raw_intent):
                raise RuntimeError("continuation intent was incomplete")
            os.fsync(intent.fileno())
        guard()
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
        guard()
        with socket.socket() as listener:
            guard()
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
            listener.bind((endpoint["address"], 0)); listener.listen(1); listener.settimeout(0.15)
            receipt["positive_control_before"] = positive_control(listener, guard)
            argv = [image.path, scratch.path, canary.path, str(os.getpid()), endpoint["address"], str(listener.getsockname()[1])]
            security = SecurityLaunch(profile, user_sid=value["user_sid"], argv=argv, cwd=scratch.path,
                                      image_sha256=value["probe_sha256"], owned_objects=tuple(handles), guard=guard)
            def cancelled():
                try:
                    security.assert_launch(argv, scratch.path)
                    return False
                except Exception:
                    return True
            result = WindowsJobHost().run(argv, cwd=scratch.path, input_bytes=b"", output_dir=owned / "interface-native-job-output",
                job_id=approved_digest[:32], timeout=10, output_limit=16384,
                memory_limit=128 * 1024 * 1024, process_limit=4,
                cancelled=cancelled, security=security)
            security.assert_launch(argv, scratch.path)
            receipt["process"], receipt["actual_child_token"] = result, security.child_observation
            try:
                peer, _ = listener.accept(); peer.close(); connected = True
            except socket.timeout:
                connected = False
            receipt["endpoint_connection_observed"] = connected
            receipt["positive_control_after"] = positive_control(listener, guard)
            receipt["loopback_configuration_after"] = loopback_configuration(profile.package_sid)
        output = (owned / "interface-native-job-output/stdout").read_bytes()
        errors = (owned / "interface-native-job-output/stderr").read_bytes()
        receipt["stdout_sha256"], receipt["stderr_sha256"] = digest(output), digest(errors)
        observed = json.loads(output)
        expected = {"scratch_error": 0, "read_error": 5, "write_error": 5,
                    "dacl_error": 5, "controller_error": 5}
        if (not isinstance(observed, dict) or set(observed) != set(expected) | {"network_error", "diagnostic_status", "missing_capability"} or
                any(type(observed[k]) is not int or observed[k] != expected[k] for k in expected) or
                result["exit_code"] != 0 or result["reason"] != "exited" or not result["quiescent"] or connected or errors):
            raise RuntimeError("actual native H1 denial observations did not pass")
        verify_network_evidence(observed, receipt, profile.package_sid, endpoint)
        receipt["network_proof"] = "calling-token missing capability, exact non-exemption, failed connection and same-listener positive controls"
        if (Path(scratch.path) / "native-created.txt").read_bytes() != b"owned-native-probe":
            raise RuntimeError("actual native H1 positive scratch proof failed")
        receipt["denials"], receipt["result"] = observed, "PASS"
    except Exception as error:
        receipt["result"], receipt["failure_type"] = "FAIL", type(error).__name__
        raise
    finally:
        receipt["read_only_interface_observations"] = observation_count
        for obj in reversed(handles):
            obj.close()
        with open(receipt_path, "xb") as target:
            target.write((json.dumps(receipt, indent=2) + "\n").encode())
            target.flush(); os.fsync(target.fileno())
    print(json.dumps({"result": receipt["result"], "receipt": str(receipt_path), "cleanup": "retain_only"}))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: h1-owned-network-effect-probe.py <reviewed-manifest> <exact-sha256>")
    run(sys.argv[1], sys.argv[2])
