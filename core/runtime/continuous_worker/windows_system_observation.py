"""Bounded controller-pinned Windows observations; no loader qualification.

The native backend is unconnected to worker dispatch. An owned outer process and
protected journal/controller are prerequisites for an actual admitted probe.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
import ctypes as C
from ctypes import wintypes as W
import hashlib
import json
import math
import os
import re
import sys
import time

from .state import Refused
from .windows_python_contract import MAX_API_SETS, MAX_MODULES, MAX_TOTAL_BYTES, PRIVATE_NAMES, _api_name, _digest, _identity, _name
from .windows_pe import MAX_PE_BYTES
from . import windows_security_objects as objects

RESOURCE_FLAGS = 0x800 | 0x40 | 0x20
MAX_NATIVE_CALLS = 8192
MAX_RESULT_BYTES = 2 * 1024 * 1024
MAX_EXECUTABLE_MODULES = 1024
CHUNK_BYTES = 65536
API_QUERY_MAX_PATH = 260
MAX_API_QUERY_CALLS = MAX_API_SETS + 1
MAX_RESOURCE_API_SETS = 128


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _finite(value):
    if type(value) not in (int, float): return False
    try: return math.isfinite(value)
    except OverflowError: return False


def _native_root(value):
    if type(value) is not str or not re.fullmatch(r"\\Device\\HarddiskVolume[1-9][0-9]{0,9}\\Windows\\System32", value):
        raise Refused("literal native System32 root required")
    return value


def _sid(value):
    if type(value) is not str:
        raise Refused("literal owner SID required")
    return objects.sid_text(value)


@dataclass(frozen=True)
class ObjectPin:
    name: str
    identity: tuple[int, str]
    owner_sid: str
    security_sha256: str
    size: int
    sha256: str
    links: int

    def value(self):
        return {"name": self.name, "identity": {"volume": self.identity[0], "file_id": self.identity[1]},
                "owner_sid": self.owner_sid, "security_sha256": self.security_sha256,
                "size": self.size, "sha256": self.sha256, "links": self.links}


@dataclass(frozen=True)
class ObservationPlan:
    request_id: str
    native_root: str
    root_identity: tuple[int, str]
    root_owner: str
    root_security_sha256: str
    files: tuple[ObjectPin, ...]
    api_names: tuple[str, ...]
    expires_at: float
    max_seconds: float
    fingerprint: str

    @classmethod
    def read(cls, value):
        fields = {"schema", "request_id", "root", "files", "api_names", "expires_at", "max_seconds"}
        if type(value) is not dict or set(value) != fields or value["schema"] != "aide.host.system-observation.v1":
            raise Refused("exact system observation plan required")
        request, root = value["request_id"], value["root"]
        if type(request) is not str or not re.fullmatch(r"[0-9a-f]{32}", request):
            raise Refused("literal observation request identity required")
        if type(root) is not dict or set(root) != {"path", "identity", "owner_sid", "security_sha256"}:
            raise Refused("exact native root facts required")
        root_path, root_id = _native_root(root["path"]), _identity(root["identity"])
        owner, security = _sid(root["owner_sid"]), _digest(root["security_sha256"])
        rows, names = value["files"], value["api_names"]
        if type(rows) is not list or not 1 <= len(rows) <= MAX_MODULES - 3:
            raise Refused("finite physical system object pins required")
        if type(names) is not list or len(names) > MAX_RESOURCE_API_SETS:
            raise Refused("finite API request list required")
        files, seen, identities, total = [], set(), {root_id}, 0
        for row in rows:
            if type(row) is not dict or set(row) != {"name", "identity", "owner_sid", "security_sha256", "size", "sha256", "links"}:
                raise Refused("exact physical object pin fields required")
            name, identity = _name(row["name"]), _identity(row["identity"])
            size, links = row["size"], row["links"]
            if (name in seen or name in PRIVATE_NAMES or name.startswith(("api-", "ext-")) or identity in identities or identity[0] != root_id[0] or
                    type(size) is not int or not 64 <= size <= MAX_PE_BYTES or type(links) is not int or not 1 <= links <= 1024):
                raise Refused("distinct bounded physical system file required")
            total += size
            if total > MAX_TOTAL_BYTES:
                raise Refused("system observation total bytes exceeded")
            seen.add(name); identities.add(identity)
            files.append(ObjectPin(name, identity, _sid(row["owner_sid"]), _digest(row["security_sha256"]),
                                   size, _digest(row["sha256"]), links))
        aliases = tuple(_name(name) for name in names)
        if len(set(aliases)) != len(aliases) or any(not _api_name(name) for name in aliases):
            raise Refused("distinct literal API contract requests required")
        expires, duration = value["expires_at"], value["max_seconds"]
        if not _finite(expires) or not _finite(duration) or not 0 < duration <= 120 or expires <= 0:
            raise Refused("finite observation expiry and duration required")
        result = cls(request, root_path, root_id, owner, security, tuple(sorted(files, key=lambda row: row.name)),
                     tuple(sorted(aliases)), expires, duration, "")
        return replace(result, fingerprint=hashlib.sha256(_canonical(result.value())).hexdigest())

    def value(self):
        return {"schema": "aide.host.system-observation.v1", "request_id": self.request_id,
                "root": {"path": self.native_root, "identity": {"volume": self.root_identity[0], "file_id": self.root_identity[1]},
                         "owner_sid": self.root_owner, "security_sha256": self.root_security_sha256},
                "files": [row.value() for row in self.files], "api_names": list(self.api_names),
                "expires_at": self.expires_at, "max_seconds": self.max_seconds}

    def validate(self):
        try:
            if ObservationPlan.read(self.value()) != self:
                raise Refused("observation plan differs from immutable admission")
        except (AttributeError, TypeError, ValueError, IndexError) as error:
            raise Refused("complete immutable observation plan required") from error
        return self


def _os_build(value):
    if type(value) is not str or not re.fullmatch(r"10\.0\.[0-9]{1,6}", value):
        raise Refused("exact Windows build required")
    return value


@dataclass(frozen=True)
class ApiSetQueryPlan:
    request_id: str
    os_build: str
    api_names: tuple[str, ...]
    expires_at: float
    max_seconds: float
    fingerprint: str

    @classmethod
    def read(cls, value):
        fields = {"schema", "request_id", "os_build", "api_names", "expires_at", "max_seconds"}
        if type(value) is not dict or set(value) != fields or value["schema"] != "aide.host.api-set-query.v1":
            raise Refused("exact API-set query plan required")
        request = value["request_id"]
        if type(request) is not str or not re.fullmatch(r"[0-9a-f]{32}", request):
            raise Refused("literal API-set query identity required")
        names = value["api_names"]
        if type(names) is not list or not 1 <= len(names) <= MAX_API_SETS:
            raise Refused("finite nonempty API-set query list required")
        aliases = tuple(_name(name) for name in names)
        if len(set(aliases)) != len(aliases) or any(not _api_name(name) for name in aliases):
            raise Refused("distinct literal API-set contracts required")
        expires, duration = value["expires_at"], value["max_seconds"]
        if not _finite(expires) or not _finite(duration) or not 0 < duration <= 120 or expires <= 0:
            raise Refused("finite API-set query expiry and duration required")
        result = cls(request, _os_build(value["os_build"]), tuple(sorted(aliases)), expires, duration, "")
        return replace(result, fingerprint=hashlib.sha256(_canonical(result.value())).hexdigest())

    def value(self):
        return {"schema": "aide.host.api-set-query.v1", "request_id": self.request_id,
                "os_build": self.os_build, "api_names": list(self.api_names),
                "expires_at": self.expires_at, "max_seconds": self.max_seconds}

    def validate(self):
        try:
            if ApiSetQueryPlan.read(self.value()) != self:
                raise Refused("API-set query plan differs from immutable admission")
        except (AttributeError, TypeError, ValueError, IndexError) as error:
            raise Refused("complete immutable API-set query plan required") from error
        return self


class ApiSetQuerySession:
    """One-use supported API-set host query with durable pre-call intents."""
    def __init__(self, plan, api, journal, guard, *, clock=time.monotonic, wall_clock=time.time):
        if not isinstance(plan, ApiSetQueryPlan) or not callable(guard) or not callable(clock) or not callable(wall_clock):
            raise Refused("typed API-set plan and explicit controller guard required")
        if not callable(getattr(journal, "reserve", None)) or not callable(getattr(journal, "intent", None)):
            raise Refused("protected API-set reservation and write-ahead journal required")
        if not callable(getattr(api, "os_build", None)) or not callable(getattr(api, "api_set_host", None)):
            raise Refused("supported API-set query backend required")
        self.plan, self.api, self.journal, self.guard = plan.validate(), api, journal, guard
        self.clock, self.wall_clock = clock, wall_clock
        self.consumed, self.calls, self.attempts, self.failure = False, 0, [], None
        self.start, self.wall_start, self.last = None, None, None

    def _time_check(self):
        now, wall = self.clock(), self.wall_clock()
        if (not _finite(now) or not _finite(wall) or now < self.last or wall < self.wall_start or
                now - self.start >= self.plan.max_seconds or not 0 < self.plan.expires_at - wall <= 3600):
            raise Refused("API-set query clock, expiry or duration refused")
        self.last = now

    def _check(self):
        self._time_check()
        if self.guard() is False:
            raise Refused("controller guard explicitly refused API-set query")
        self._time_check()

    def _call(self, name, *args):
        self._check()
        if self.calls >= MAX_API_QUERY_CALLS:
            raise Refused("API-set query operation budget exhausted")
        self.calls += 1
        result = getattr(self.api, name)(*args)
        self._check()
        return result

    def _query(self, name):
        intent = {"schema": "aide.host.api-set-query-intent.v1", "request_id": self.plan.request_id,
                  "plan_sha256": self.plan.fingerprint, "sequence": len(self.attempts), "api_name": name,
                  "operation": "GetApiSetModuleBaseName"}
        self.attempts.append(dict(intent))
        self._check()
        acknowledgement = _digest(self.journal.intent(dict(intent)))
        if acknowledgement != hashlib.sha256(_canonical(intent)).hexdigest():
            raise Refused("journal did not acknowledge the exact API-set query intent")
        host = self._call("api_set_host", name)
        host = _name(host)
        if _api_name(host) or host in PRIVATE_NAMES:
            raise Refused("API-set query did not return one physical system module")
        return {"api_name": name, "physical_name": host,
                "intent_acknowledgement": acknowledgement}

    def run(self):
        if self.consumed:
            raise Refused("API-set query already consumed; inspect retained state without replay")
        self.consumed = True
        self.plan.validate()
        self.start, self.wall_start = self.clock(), self.wall_clock()
        if not _finite(self.start) or not _finite(self.wall_start):
            raise Refused("finite initial API-set query clocks required")
        self.last = self.start
        try:
            self._check()
            reservation = _digest(self.journal.reserve(self.plan.fingerprint))
            if reservation != self.plan.fingerprint:
                raise Refused("journal did not reserve this exact API-set query")
            if _os_build(self._call("os_build")) != self.plan.os_build:
                raise Refused("Windows build changed before API-set query")
            queries = [self._query(name) for name in self.plan.api_names]
            self._check()
            result = {"schema": "aide.host.api-set-query-result.v1", "request_id": self.plan.request_id,
                      "plan_sha256": self.plan.fingerprint, "reservation_acknowledgement": reservation,
                      "os_build": self.plan.os_build, "queries": queries, "native_calls": self.calls,
                      "query_attempts": len(self.attempts), "api_set_query_completed": True,
                      "physical_hosts_qualified": False, "loader_qualified": False,
                      "restricted_context_qualified": False,
                      "boundary": "Supported API-set names only; physical host bytes, protected authority and restricted loader remain separate qualifications."}
            if len(_canonical(result)) > MAX_RESULT_BYTES:
                raise Refused("API-set query result exceeds output bound")
            self._check()
            output = _canonical(result)
            if len(output) > MAX_RESULT_BYTES:
                raise Refused("final API-set query result exceeds output bound")
            self._check()
            return output
        except Exception as caught:
            self.failure = {"error_type": type(caught).__name__, "native_calls": self.calls,
                            "query_attempts": len(self.attempts)}
            native = getattr(caught, "native_evidence", None)
            if type(native) is dict:
                self.failure["native_refusal"] = dict(native)
            raise Refused("API-set query refused; consumed state retained without replay") from caught


@dataclass(frozen=True)
class ObjectFacts:
    path: str
    identity: tuple[int, str]
    directory: bool
    delete_pending: bool
    size: int
    links: int
    owner_sid: str
    security_sha256: str


class ObservationSession:
    """One-use observation; journal callbacks must durably acknowledge first.

    Injectable backend/journal/guard are protected controller dependencies. Their
    mere return values do not qualify their authenticity or durability.
    """
    def __init__(self, plan, api, journal, guard, *, clock=time.monotonic, wall_clock=time.time):
        if not isinstance(plan, ObservationPlan) or not callable(guard) or not callable(clock) or not callable(wall_clock):
            raise Refused("typed plan and explicit controller guard required")
        if not callable(getattr(journal, "reserve", None)) or not callable(getattr(journal, "intent", None)):
            raise Refused("protected reservation and write-ahead journal required")
        self.plan, self.api, self.journal, self.guard = plan.validate(), api, journal, guard
        self.clock, self.wall_clock = clock, wall_clock
        self.consumed, self.calls, self.attempts = False, 0, []
        self.resources, self.release_failures, self.failure = [], [], None
        self.start, self.wall_start, self.last = None, None, None

    def _time_check(self):
        now, wall = self.clock(), self.wall_clock()
        if (not _finite(now) or not _finite(wall) or now < self.last or wall < self.wall_start or
                now - self.start >= self.plan.max_seconds or not 0 < self.plan.expires_at - wall <= 3600):
            raise Refused("system observation clock, expiry or duration refused")
        self.last = now

    def _check(self):
        self._time_check()
        if self.guard() is False:
            raise Refused("controller guard explicitly refused observation")
        # The guard itself can block or consume the remaining finite budget.
        self._time_check()

    def _call(self, name, *args, acquire=None):
        self._check()
        if self.calls >= MAX_NATIVE_CALLS:
            raise Refused("native observation operation budget exhausted")
        self.calls += 1  # Count before invoking, including failures.
        value = getattr(self.api, name)(*args)
        if acquire:
            if type(value) is not int or not 0 < value < 2**64 - 1 or (acquire, value) in self.resources:
                raise Refused("native acquisition returned no distinct known owned handle")
            # Adopt before a post-call guard failure can bypass exact cleanup.
            self.resources.append((acquire, value))
        self._check()
        return value

    def _release(self, kind, handle):
        self.resources.remove((kind, handle))  # Consume release before calling.
        try:
            if getattr(self.api, "free_resource" if kind == "mapping" else "close_file")(handle) is not True:
                raise Refused("native owned release did not acknowledge success")
        except Exception as error:
            self.release_failures.append({"kind": kind, "handle": handle, "error_type": type(error).__name__})
            raise Refused("owned release is uncertain; no retry") from error

    def _facts(self, handle, pin=None):
        facts = self._call("facts", handle)
        if type(facts) is not ObjectFacts or type(facts.identity) is not tuple or len(facts.identity) != 2:
            raise Refused("typed exact native object observations required")
        _identity({"volume": facts.identity[0], "file_id": facts.identity[1]})
        _sid(facts.owner_sid); _digest(facts.security_sha256)
        path = self.plan.native_root + ("\\" + pin.name if pin else "")
        identity = pin.identity if pin else self.plan.root_identity
        owner = pin.owner_sid if pin else self.plan.root_owner
        security = pin.security_sha256 if pin else self.plan.root_security_sha256
        if (type(facts.path) is not str or facts.path.casefold() != path.casefold() or facts.identity != identity or
                type(facts.directory) is not bool or facts.directory != (pin is None) or facts.delete_pending is not False or
                facts.owner_sid != owner or facts.security_sha256 != security or
                type(facts.size) is not int or facts.size != (pin.size if pin else 0) or
                type(facts.links) is not int or facts.links != (pin.links if pin else 1)):
            raise Refused("native object path, identity, descriptor or extent differs from admission")
        return facts

    def _hash_file(self, handle, pin):
        total, digest = 0, hashlib.sha256()
        while total < pin.size:
            count = min(CHUNK_BYTES, pin.size - total)
            block = self._call("read_file", handle, count)
            if type(block) is not bytes or not 0 < len(block) <= count:
                raise Refused("bounded complete immutable source stream required")
            digest.update(block); total += len(block)
        if self._call("read_file", handle, 1) != b"" or digest.hexdigest() != pin.sha256:
            raise Refused("system object bytes differ from exact admission")

    @staticmethod
    def _bases(value):
        if (type(value) is not tuple or not 1 <= len(value) <= MAX_EXECUTABLE_MODULES or
                any(type(v) is not int or not 0 < v < 2**64 or v & 0xffff for v in value) or len(set(value)) != len(value)):
            raise Refused("finite distinct executable module base observations required")
        return frozenset(value)

    def _mapping(self, name, root, files):
        self._facts(root)
        before = self._bases(self._call("executable_bases"))
        intent = {"schema": "aide.host.system-mapping-intent.v1", "request_id": self.plan.request_id,
                  "plan_sha256": self.plan.fingerprint, "sequence": len(self.attempts), "api_name": name,
                  "flags": RESOURCE_FLAGS}
        self.attempts.append(dict(intent))
        self._check()
        acknowledgement = _digest(self.journal.intent(dict(intent)))
        if acknowledgement != hashlib.sha256(_canonical(intent)).hexdigest():
            raise Refused("journal did not acknowledge the exact mapping intent")
        self._check()
        handle = self._call("map_resource", name, acquire="mapping")
        try:
            tag, address = handle & 3, handle & ~3
            if tag not in (0, 1, 2) or not address or address & 0xffff or (tag == 0 and address not in before):
                raise Refused("mapping tag or prior executable origin is unsupported")
            path = self._call("mapped_name", address)
            if type(path) is not str or len(path) > 1023:
                raise Refused("complete bounded mapped native path required")
            matches = [(pin, child) for pin, child in files if path.casefold() == (self.plan.native_root + "\\" + pin.name).casefold()]
            if len(matches) != 1:
                raise Refused("mapped backing object is not one held admitted system file")
            pin, child = matches[0]
            self._facts(root)
            held = self._facts(child, pin)
            if path != held.path:
                raise Refused("mapped spelling differs from the exact held native object path")
            after = self._bases(self._call("executable_bases"))
            if after != before:
                raise Refused("executable module inventory changed during resource observation")
            return {"api_name": name, "physical_name": pin.name, "identity": list(pin.identity),
                    "sha256": pin.sha256, "mapped_path": path, "mapping_kind": "prior_executable" if tag == 0 else "resource",
                    "intent_acknowledgement": acknowledgement}
        finally:
            self._release("mapping", handle)

    def run(self):
        if self.consumed:
            raise Refused("observation request already consumed; query retained state without replay")
        self.consumed = True
        self.plan.validate()
        self.start, self.wall_start = self.clock(), self.wall_clock()
        if not _finite(self.start) or not _finite(self.wall_start):
            raise Refused("finite initial observation clocks required")
        self.last = self.start
        result, error = None, None
        try:
            self._check()
            reservation = _digest(self.journal.reserve(self.plan.fingerprint))
            if reservation != self.plan.fingerprint:
                raise Refused("journal did not reserve this exact observation request")
            self._check()
            root = self._call("open_root", self.plan.native_root, acquire="file")
            self._facts(root)
            files = []
            for pin in self.plan.files:
                child = self._call("open_file", root, pin.name, acquire="file")
                self._facts(child, pin); self._hash_file(child, pin); self._facts(child, pin)
                files.append((pin, child))
            mappings = [self._mapping(name, root, files) for name in self.plan.api_names]
            self._facts(root)
            for pin, child in files: self._facts(child, pin)
            self._check()
            result = {"schema": "aide.host.system-observation-result.v1", "request_id": self.plan.request_id,
                      "plan_sha256": self.plan.fingerprint, "reservation_acknowledgement": reservation,
                      "root": self.plan.value()["root"], "files": [pin.value() for pin, _ in files], "mappings": mappings,
                      "native_calls": self.calls, "mapping_attempts": len(self.attempts),
                      "system_ownership_qualified": False, "api_context_qualified": False, "loader_qualified": False,
                      "boundary": "Exact controller-pinned observations only; protected journal/controller and actual context remain external qualifications."}
            if len(_canonical(result)) > MAX_RESULT_BYTES:
                raise Refused("system observation result exceeds output bound")
        except Exception as caught:
            error = caught
            self.failure = {"error_type": type(caught).__name__, "native_calls": self.calls, "mapping_attempts": len(self.attempts)}
        finally:
            for kind, handle in list(reversed(self.resources)):
                try: self._release(kind, handle)
                except Refused as caught:
                    if error is None: error = caught
        if error is not None:
            if self.failure is None:
                self.failure = {"error_type": type(error).__name__, "native_calls": self.calls, "mapping_attempts": len(self.attempts)}
            raise Refused("system observation refused; consumed state and release evidence retained") from error
        try:
            self._check()
            result["all_owned_handles_released"] = True
            output = _canonical(result)
            if len(output) > MAX_RESULT_BYTES:
                raise Refused("final system observation result exceeds output bound")
            self._check()
        except Exception as caught:
            self.failure = {"error_type": type(caught).__name__, "native_calls": self.calls, "mapping_attempts": len(self.attempts)}
            raise Refused("final observation is stale or incomplete; consumed state retained") from caught
        return output


class NativeApiSetQueryApi:
    """Supported API-set host query; construct only in a reviewed owned probe."""
    def __init__(self):
        if os.name != "nt" or C.sizeof(C.c_void_p) != 8:
            raise Refused("native AMD64 Windows API-set query backend required")
        try:
            self._api_query_library = C.WinDLL("api-ms-win-core-apiquery-l2-1-0.dll", use_last_error=True)
        except OSError as error:
            raise Refused("supported API-set query library unavailable") from error
        self._api_query = objects.bind(self._api_query_library, "GetApiSetModuleBaseName",
                                       [C.c_char_p, C.c_uint32, W.LPWSTR, C.POINTER(C.c_uint32)], C.c_long)

    def os_build(self):
        version = sys.getwindowsversion()
        parts = tuple(getattr(version, "platform_version", version)[:3])
        if len(parts) != 3 or any(type(part) is not int or part < 0 for part in parts):
            raise Refused("exact Windows platform build unavailable")
        return _os_build(".".join(str(part) for part in parts))

    def api_set_host(self, name):
        name = _name(name)
        if not _api_name(name):
            raise Refused("literal admitted API-set contract required")
        output, actual = C.create_unicode_buffer(API_QUERY_MAX_PATH), C.c_uint32()
        status = int(self._api_query(name.encode("ascii"), API_QUERY_MAX_PATH, output, C.byref(actual))) & 0xffffffff
        if status:
            error = Refused("supported API-set host query failed")
            error.native_evidence = {"operation": "GetApiSetModuleBaseName", "api_name": name,
                                     "hresult": "0x" + format(status, "08x")}
            raise error
        if not 2 <= actual.value <= API_QUERY_MAX_PATH or actual.value != len(output.value) + 1:
            raise Refused("API-set host output length missing or inconsistent")
        host = _name(output.value.lower())
        if _api_name(host) or host in PRIVATE_NAMES:
            raise Refused("API-set query returned no physical system module")
        return host


class NativeSystemApi:
    """Actual Windows adapter. Construct/use only under a reviewed owned probe.

    Synchronous native calls require an external owned-process deadline. This
    backend does not install, copy, grant, delete or execute a selected DLL.
    """
    def __init__(self):
        if os.name != "nt" or C.sizeof(C.c_void_p) != 8:
            raise Refused("native AMD64 Windows observation backend required")
        bind, kernel, advapi = objects.bind, objects.K, objects.A
        self._read = bind(kernel, "ReadFile", [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], W.BOOL)
        self._final = bind(kernel, "GetFinalPathNameByHandleW", [W.HANDLE, W.LPWSTR, W.DWORD, W.DWORD], W.DWORD)
        self._sid = bind(advapi, "ConvertSidToStringSidW", [C.c_void_p, C.POINTER(W.LPWSTR)], W.BOOL)
        self._load = bind(kernel, "LoadLibraryExW", [W.LPCWSTR, W.HANDLE, W.DWORD], W.HMODULE)
        self._free = bind(kernel, "FreeLibrary", [W.HMODULE], W.BOOL)
        self._mapped = bind(kernel, "K32GetMappedFileNameW", [W.HANDLE, C.c_void_p, W.LPWSTR, W.DWORD], W.DWORD)
        self._modules = bind(kernel, "K32EnumProcessModules", [W.HANDLE, C.POINTER(W.HMODULE), W.DWORD, C.POINTER(W.DWORD)], W.BOOL)
        self._process = bind(kernel, "GetCurrentProcess", [], W.HANDLE)

    def open_root(self, path):
        _native_root(path)
        return objects._open(path, None, directory=True, create=False, read_only_source=True).value

    def open_file(self, parent, name):
        _name(name)
        return objects._open(name, parent, directory=False, create=False, read_only_source=True).value

    def facts(self, handle):
        class Standard(C.Structure):
            _fields_ = [("AllocationSize", C.c_longlong), ("EndOfFile", C.c_longlong),
                        ("NumberOfLinks", W.DWORD), ("DeletePending", C.c_ubyte), ("Directory", C.c_ubyte)]
        value = Standard()
        objects._check(objects.get_identity(handle, 1, C.byref(value), C.sizeof(value)))
        if value.Directory not in (0, 1) or value.DeletePending not in (0, 1):
            raise Refused("literal native object kind required")
        path = C.create_unicode_buffer(1024)
        count = self._final(handle, path, len(path), 2)  # VOLUME_NAME_NT, normalized name.
        if not 0 < count < len(path): raise Refused("native object path missing or truncated")
        identity = objects._identity(handle)
        sd, owner, owner_text, descriptor_text = C.c_void_p(), C.c_void_p(), W.LPWSTR(), W.LPWSTR()
        status = objects.get_security(handle, 1, 1 | 4, C.byref(owner), None, None, None, C.byref(sd))
        try:
            if status or not sd or not owner: raise Refused("native owner/DACL observation unavailable")
            objects._check(self._sid(owner, C.byref(owner_text)))
            objects._check(objects.sd_to_text(sd, 1, 1 | 4, C.byref(descriptor_text), None))
            if not owner_text or not descriptor_text or len(descriptor_text.value) > 32768:
                raise Refused("bounded native descriptor observation required")
            return ObjectFacts(path.value, _identity(identity), bool(value.Directory), bool(value.DeletePending),
                               0 if value.Directory else value.EndOfFile, value.NumberOfLinks, _sid(owner_text.value),
                               hashlib.sha256(descriptor_text.value.encode("utf-8")).hexdigest())
        finally:
            for pointer in (owner_text, descriptor_text, sd):
                if pointer: objects.local_free(C.cast(pointer, C.c_void_p))

    def read_file(self, handle, count):
        if type(count) is not int or not 1 <= count <= CHUNK_BYTES:
            raise Refused("bounded native read count required")
        data, read = C.create_string_buffer(count), W.DWORD()
        objects._check(self._read(handle, data, count, C.byref(read), None))
        if read.value > count: raise Refused("native read exceeds requested span")
        return data.raw[:read.value]

    def executable_bases(self):
        values = (W.HMODULE * MAX_EXECUTABLE_MODULES)(); needed = W.DWORD()
        objects._check(self._modules(self._process(), values, C.sizeof(values), C.byref(needed)))
        if needed.value > C.sizeof(values) or needed.value % C.sizeof(W.HMODULE):
            raise Refused("executable module inventory is truncated")
        return tuple(values[:needed.value // C.sizeof(W.HMODULE)])

    def map_resource(self, name):
        if not _api_name(_name(name)): raise Refused("literal admitted API request required")
        handle = self._load(name, None, RESOURCE_FLAGS)
        if not handle: raise Refused("resource-only API mapping unavailable; no executable fallback")
        return handle

    def mapped_name(self, address):
        buffer = C.create_unicode_buffer(1024)
        count = self._mapped(self._process(), address, buffer, len(buffer))
        if not 0 < count < len(buffer): raise Refused("mapped backing path unavailable or truncated")
        return buffer.value

    def free_resource(self, handle):
        objects._check(self._free(handle))
        return True

    def close_file(self, handle):
        objects._check(objects.close(handle))
        return True
