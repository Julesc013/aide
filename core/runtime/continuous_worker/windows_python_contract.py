"""Finite named Python/system dependency data; no native or loader qualification."""
from __future__ import annotations
from dataclasses import dataclass, replace
import hashlib
import json
import re

from .state import Refused
from .windows_pe import MAX_PE_BYTES, dll_name, read_pe

MAX_MODULES = 64
MAX_TOTAL_BYTES = 256 * 1024 * 1024
MAX_API_SETS = 256
MAX_EDGES = 4096
DIRECT_SYSTEM_NAMES = frozenset({
    "advapi32.dll", "bcrypt.dll", "kernel32.dll", "version.dll", "ws2_32.dll",
    "api-ms-win-core-path-l1-1-0.dll", "api-ms-win-crt-conio-l1-1-0.dll",
    "api-ms-win-crt-convert-l1-1-0.dll", "api-ms-win-crt-environment-l1-1-0.dll",
    "api-ms-win-crt-filesystem-l1-1-0.dll", "api-ms-win-crt-heap-l1-1-0.dll",
    "api-ms-win-crt-locale-l1-1-0.dll", "api-ms-win-crt-math-l1-1-0.dll",
    "api-ms-win-crt-process-l1-1-0.dll", "api-ms-win-crt-runtime-l1-1-0.dll",
    "api-ms-win-crt-stdio-l1-1-0.dll", "api-ms-win-crt-string-l1-1-0.dll",
    "api-ms-win-crt-time-l1-1-0.dll",
})
PRIVATE_NAMES = frozenset({"python.exe", "python314.dll", "vcruntime140.dll"})


def _digest(value):
    if type(value) is not str or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise Refused("literal SHA256 required")
    return value


def _identity(value):
    if (type(value) is not dict or set(value) != {"volume", "file_id"} or
            type(value["volume"]) is not int or not 0 < value["volume"] < 2**64 or
            type(value["file_id"]) is not str or not re.fullmatch(r"[0-9a-f]{32}", value["file_id"]) or
            value["file_id"] == "0" * 32):
        raise Refused("exact native system object identity required")
    return value["volume"], value["file_id"]


def _name(value):
    name = dll_name(value)
    if name != value:
        raise Refused("canonical lower-case system declaration required")
    return name


def _api_name(value):
    return bool(re.fullmatch(r"(?:api|ext)-ms-win-[a-z0-9-]+-l[0-9]+-[0-9]+-[0-9]+\.dll", value))


@dataclass(frozen=True)
class SystemModule:
    name: str
    sha256: str
    identity: tuple[int, str]


@dataclass(frozen=True)
class ApiSetBinding:
    name: str
    hosts: tuple[str, ...]


@dataclass(frozen=True)
class SystemContract:
    os_build: str
    native_root: str
    root_identity: tuple[int, str]
    modules: tuple[SystemModule, ...]
    api_sets: tuple[ApiSetBinding, ...]
    fingerprint: str

    @classmethod
    def read(cls, value):
        fields = {"schema", "os_build", "native_root", "root_identity", "modules", "api_sets"}
        if type(value) is not dict or set(value) != fields or value["schema"] != "aide.host.python-system.v1":
            raise Refused("exact named Python system contract required")
        build, root = value["os_build"], value["native_root"]
        if type(build) is not str or not re.fullmatch(r"10\.0\.[0-9]{1,6}\.[0-9]{1,6}", build):
            raise Refused("exact bounded Windows build required")
        if type(root) is not str or not re.fullmatch(r"\\Device\\HarddiskVolume[1-9][0-9]{0,9}\\Windows\\System32", root):
            raise Refused("literal native system-root binding required")
        root_id = _identity(value["root_identity"])
        rows, mappings = value["modules"], value["api_sets"]
        if type(rows) is not list or not 1 <= len(rows) <= MAX_MODULES - len(PRIVATE_NAMES):
            raise Refused("finite named system module set required")
        if type(mappings) is not list or len(mappings) > MAX_API_SETS:
            raise Refused("finite explicit API-set host rows required")
        modules, names, identities = [], set(), {root_id}
        for row in rows:
            if type(row) is not dict or set(row) != {"name", "sha256", "identity"}:
                raise Refused("exact named system module fields required")
            name, identity = _name(row["name"]), _identity(row["identity"])
            if (name in names or name in PRIVATE_NAMES or name.startswith(("api-", "ext-")) or
                    identity in identities or identity[0] != root_id[0]):
                raise Refused("distinct physical system object on admitted volume required")
            names.add(name); identities.add(identity)
            modules.append(SystemModule(name, _digest(row["sha256"]), identity))
        api_sets, aliases = [], set()
        for row in mappings:
            if type(row) is not dict or set(row) != {"name", "hosts"}:
                raise Refused("exact API-set name and host list required")
            name, hosts = _name(row["name"]), row["hosts"]
            if not _api_name(name) or name in names or name in aliases:
                raise Refused("distinct literal API-set name required")
            if type(hosts) is not list or not 1 <= len(hosts) <= 8:
                raise Refused("bounded named API-set host list required")
            hosts = tuple(_name(host) for host in hosts)
            if len(set(hosts)) != len(hosts) or not set(hosts) <= names:
                raise Refused("API-set hosts must be distinct admitted physical system modules")
            aliases.add(name); api_sets.append(ApiSetBinding(name, tuple(sorted(hosts))))
        result = cls(build, root, root_id, tuple(sorted(modules, key=lambda row: row.name)),
                     tuple(sorted(api_sets, key=lambda row: row.name)), "")
        raw = json.dumps(result.to_value(), sort_keys=True, separators=(",", ":")).encode()
        return replace(result, fingerprint=hashlib.sha256(raw).hexdigest())

    def to_value(self):
        identity = lambda pair: {"volume": pair[0], "file_id": pair[1]}
        return {"schema": "aide.host.python-system.v1", "os_build": self.os_build,
                "native_root": self.native_root, "root_identity": identity(self.root_identity),
                "modules": [{"name": row.name, "sha256": row.sha256, "identity": identity(row.identity)} for row in self.modules],
                "api_sets": [{"name": row.name, "hosts": list(row.hosts)} for row in self.api_sets]}

    def validate(self):
        try:
            if SystemContract.read(self.to_value()) != self:
                raise Refused("typed system contract differs from immutable admission")
        except (AttributeError, TypeError, ValueError, IndexError) as error:
            raise Refused("complete immutable system contract required") from error
        return self


@dataclass(frozen=True, order=True)
class DependencyEdge:
    importer: str
    requested: str
    hosts: tuple[str, ...]


@dataclass(frozen=True)
class PythonRecipe:
    system: SystemContract
    modules: tuple[tuple[str, str], ...]
    edges: tuple[DependencyEdge, ...]
    bootstrap_modules: tuple[str, ...]
    inspected_bytes: int

    def manifest(self):
        return {"schema": "aide.host.python-recipe.v1", "system": self.system.to_value(),
                "system_sha256": self.system.fingerprint, "modules": dict(self.modules),
                "edges": [{"importer": row.importer, "requested": row.requested, "hosts": list(row.hosts)} for row in self.edges],
                "bootstrap_modules": list(self.bootstrap_modules), "inspected_bytes": self.inspected_bytes,
                "loader_qualified": False, "system_ownership_qualified": False,
                "boundary": "Pinned metadata only; protected issuer, actual API-set/loaded-module and dynamic-load observations remain required."}


def validate_python_recipe(contract, private_pins, private_inputs, system_inputs):
    """Validate immutable bytes under a controller-supplied contract, without loading."""
    if (not isinstance(contract, SystemContract) or type(private_pins) is not dict or
            type(private_inputs) is not dict or type(system_inputs) is not dict):
        raise Refused("typed system contract and exact literal input mappings required")
    contract.validate()
    system_pins = {row.name: row.sha256 for row in contract.modules}
    if set(private_pins) != PRIVATE_NAMES or set(private_inputs) != PRIVATE_NAMES or set(system_inputs) != set(system_pins):
        raise Refused("exact three-file private recipe and named system input set required")
    try: pins = {name: _digest(private_pins[name]) for name in sorted(PRIVATE_NAMES)}
    except KeyError as error: raise Refused("private pins changed while freezing") from error
    pins.update(system_pins)
    # Capture immutable bytes once before parsing. Caller dictionaries cannot
    # substitute a different module after its hash was checked.
    frozen, total = {}, 0
    for name, expected in pins.items():
        try: data = (private_inputs if name in PRIVATE_NAMES else system_inputs)[name]
        except KeyError as error: raise Refused("module input set changed while freezing") from error
        if type(data) is not bytes or not 64 <= len(data) <= MAX_PE_BYTES:
            raise Refused("bounded immutable module bytes required")
        total += len(data)
        if total > MAX_TOTAL_BYTES or hashlib.sha256(data).hexdigest() != expected:
            raise Refused("module bytes exceed total bound or differ from exact hash")
        frozen[name] = data
    metadata = {name: read_pe(data) for name, data in frozen.items()}
    for name, info in metadata.items():
        if info.is_dll != (name != "python.exe"):
            raise Refused("Python executable and named DLL characteristics differ")
    aliases = {row.name: row.hosts for row in contract.api_sets}
    edges = []
    for name, info in metadata.items():
        for dependency in info.dependencies:
            if name in PRIVATE_NAMES:
                if dependency not in PRIVATE_NAMES and dependency not in DIRECT_SYSTEM_NAMES:
                    raise Refused("private recipe requests an unadmitted direct system name")
            elif dependency in PRIVATE_NAMES:
                raise Refused("system module cannot resolve through private Python files")
            hosts = aliases.get(dependency, (dependency,))
            if any(host not in metadata for host in hosts):
                raise Refused("unresolved exact imported, delayed or forwarded module")
            edges.append(DependencyEdge(name, dependency, hosts))
            if len(edges) > MAX_EDGES:
                raise Refused("dependency edge bound exceeded")
    outgoing = {name: [] for name in metadata}
    for edge in edges: outgoing[edge.importer].extend(edge.hosts)
    reachable, pending = set(), ["python.exe"]
    while pending:
        name = pending.pop()
        if name in reachable: continue
        reachable.add(name); pending.extend(outgoing[name])
    if not PRIVATE_NAMES <= reachable:
        raise Refused("private recipe contains unreachable executable or DLL inputs")
    return PythonRecipe(contract, tuple(sorted(pins.items())), tuple(sorted(edges)), tuple(sorted(reachable)), total)
