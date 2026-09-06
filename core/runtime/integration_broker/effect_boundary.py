"""Object-bound prepared candidate validation held across a transport effect."""
from contextlib import ExitStack, contextmanager
from types import MappingProxyType

from .common import Refused, bounded_bytes, canonical, digest, require_path, beneath
from .candidate import verify_changes
from .preparation import directory_lease
from core.runtime.continuous_worker.locking import supervisor_lock


def _configuration(git, directory):
    values = {}
    for item in git.run(directory, "config", "--local", "--no-includes", "--null", "--list").split(b"\0"):
        if not item:
            continue
        pair = item.decode("utf-8").split("\n", 1)
        if len(pair) != 2 or pair[0].lower() in values:
            raise Refused("ambiguous prepared repository configuration")
        values[pair[0].lower()] = pair[1]
    required = {"core.repositoryformatversion": "0", "core.bare": "true"}
    optional = {"core.filemode", "core.symlinks", "core.ignorecase", "core.logallrefupdates"}
    if (any(values.get(k) != v for k, v in required.items()) or
            set(values) - set(required) - optional or
            any(values[k] not in ("true", "false") for k in optional & set(values))):
        raise Refused("prepared repository configuration changed")


def _index(git, directory, expected):
    observed = {}
    for item in git.run(directory, "ls-files", "--stage", "-z").split(b"\0"):
        if not item:
            continue
        try:
            metadata, raw = item.split(b"\t", 1)
            mode, oid, stage = metadata.decode().split()
            name = raw.decode("utf-8")
        except (ValueError, UnicodeError) as error:
            raise Refused("invalid prepared index") from error
        if stage != "0" or name in observed:
            raise Refused("unmerged or duplicate prepared index")
        observed[name] = {"mode": mode, "oid": oid}
    if observed != expected:
        raise Refused("prepared index differs from frozen candidate")


@contextmanager
def prepared_candidate(broker, request):
    """Yield exact materialized inputs while retaining their directory identities.

    A qualified protected store must exclude concurrent child-file writers.
    These directory handles alone do not provide credential or file isolation.
    No request intent, remote effect or uncertain-directory cleanup occurs here.
    """
    key = digest(request)
    with ExitStack() as leases:
        leases.enter_context(directory_lease(broker.root))
        leases.enter_context(supervisor_lock(broker.root))
        manifest, blobs = broker.validate_request(request)
        row, generation = broker.ledger.get(key), broker.ledger.preparation(key)
        if (not row or row["stage"] not in ("prepared", "apply_intent") or
                row["request"] != canonical(request) or row["manifest"] != canonical(manifest) or
                row["authority"] != digest(broker.authority) or not generation or
                generation["stage"] != "prepared" or not generation["identity"]):
            raise Refused("effect requires the exact durable prepared generation")
        directory = require_path(str(broker.root / generation["generation"]))
        if directory.parent != broker.root:
            raise Refused("prepared generation escaped broker root")
        observed = leases.enter_context(directory_lease(directory))
        if canonical(observed) != generation["identity"]:
            raise Refused("prepared directory object was replaced")
        leases.enter_context(directory_lease(broker.repository_root))
        broker.guard()
        git = broker.git
        git_dir = require_path(git.run(broker.repository_root, "rev-parse", "--absolute-git-dir").decode().strip())
        if not beneath(git_dir, broker.repository_root):
            raise Refused("protected base metadata escaped repository")
        leases.enter_context(directory_lease(git_dir))
        base_objects = require_path(str(git_dir / "objects"))
        leases.enter_context(directory_lease(base_objects))
        git.validate_store(broker.repository_root, manifest["base"])
        base_tree, base_files = git.tree(broker.repository_root, manifest["base"])
        if base_tree != manifest["base_tree"]:
            raise Refused("protected base tree changed")
        verify_changes(manifest, base_files)
        _configuration(git, directory)
        objects = require_path(str(directory / "objects"))
        leases.enter_context(directory_lease(objects))
        info = require_path(str(objects / "info"))
        leases.enter_context(directory_lease(info))
        alternate = info / "alternates"
        if manifest["schema"] == "aide.broker.candidate.v2":
            expected = (str(base_objects).replace("\\", "/") + "\n").encode()
            if bounded_bytes(alternate) != expected:
                raise Refused("prepared alternate differs from protected base store")
        elif alternate.exists():
            raise Refused("complete-tree candidate acquired an alternate")
        if (info / "http-alternates").exists() or any((objects / "pack").glob("*.promisor")):
            raise Refused("prepared external object source is not admitted")
        expected_files = dict(base_files) if manifest["schema"] == "aide.broker.candidate.v2" else {}
        for name, entry in manifest["files"].items():
            if entry is None:
                expected_files.pop(name)
            else:
                expected_files[name] = {k: entry[k] for k in ("mode", "oid")}
        _index(git, directory, expected_files)
        if git.run(directory, "write-tree").decode().strip() != manifest["candidate_tree"]:
            raise Refused("prepared tree differs from frozen candidate")
        git.run(directory, "fsck", "--strict", "--no-dangling", manifest["candidate_tree"])
        for entry in manifest["files"].values():
            if entry is not None and git.run(directory, "cat-file", "blob", entry["oid"]) != blobs[entry["sha256"]]:
                raise Refused("prepared content differs from frozen bytes")
        broker.guard()
        yield MappingProxyType({"directory": directory, "request_digest": key,
                                "tree": manifest["candidate_tree"],
                                "generation": generation["generation"],
                                "directory_identity": generation["identity"]})
