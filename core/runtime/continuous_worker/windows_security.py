"""Zero-capability AppContainer source seam; no installed or qualified host.

Profile/DACL effects require an independently reviewed exact effect manifest.
There is no existing-profile adoption, automatic cleanup or unrestricted fallback.
"""
from __future__ import annotations
from contextlib import contextmanager
import ctypes as C
from ctypes import wintypes as W
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re

from .state import Refused
from .windows_security_objects import OwnedObject, sid_text


@dataclass(frozen=True)
class ProfileSpec:
    moniker: str
    reservation: str

    def validate(self):
        if not isinstance(self.moniker, str) or not re.fullmatch(r"aide\.cw\.h1\.[0-9a-f]{32}", self.moniker):
            raise Refused("one exact reserved AppContainer moniker required")
        if not isinstance(self.reservation, str) or not Path(self.reservation).is_absolute() or Path(self.reservation).name != "profile-reservation.jsonl":
            raise Refused("explicit protected profile reservation path required")


if os.name == "nt":
    K, A, U, O = (C.WinDLL(name, use_last_error=True) for name in ("kernel32", "advapi32", "userenv", "ole32"))
    def bind(lib, name, args, result):
        value = getattr(lib, name)
        value.argtypes, value.restype = args, result
        return value
    class SID_ATTRIBUTES(C.Structure):
        _fields_ = [("Sid", C.c_void_p), ("Attributes", W.DWORD)]
    class CAPABILITIES(C.Structure):
        _fields_ = [("AppContainerSid", C.c_void_p), ("Capabilities", C.c_void_p), ("CapabilityCount", W.DWORD), ("Reserved", W.DWORD)]
    F = C.WinDLL("FirewallAPI.dll", use_last_error=True, winmode=0x800)
    get_loopback_config = bind(F, "NetworkIsolationGetAppContainerConfig", [C.POINTER(W.DWORD), C.POINTER(C.POINTER(SID_ATTRIBUTES))], W.DWORD)
    get_heap = bind(K, "GetProcessHeap", [], W.HANDLE)
    heap_free = bind(K, "HeapFree", [W.HANDLE, W.DWORD, C.c_void_p], W.BOOL)
    get_current = bind(K, "GetCurrentProcess", [], W.HANDLE)
    close = bind(K, "CloseHandle", [W.HANDLE], W.BOOL)
    local_free = bind(K, "LocalFree", [C.c_void_p], C.c_void_p)
    open_token = bind(A, "OpenProcessToken", [W.HANDLE, W.DWORD, C.POINTER(W.HANDLE)], W.BOOL)
    token_info = bind(A, "GetTokenInformation", [W.HANDLE, C.c_int, C.c_void_p, W.DWORD, C.POINTER(W.DWORD)], W.BOOL)
    sid_to_text = bind(A, "ConvertSidToStringSidW", [C.c_void_p, C.POINTER(W.LPWSTR)], W.BOOL)
    text_to_sid = bind(A, "ConvertStringSidToSidW", [W.LPCWSTR, C.POINTER(C.c_void_p)], W.BOOL)
    free_sid = bind(A, "FreeSid", [C.c_void_p], C.c_void_p)
    derive_sid = bind(U, "DeriveAppContainerSidFromAppContainerName", [W.LPCWSTR, C.POINTER(C.c_void_p)], W.LONG)
    create_profile = bind(U, "CreateAppContainerProfile", [W.LPCWSTR, W.LPCWSTR, W.LPCWSTR, C.c_void_p, W.DWORD, C.POINTER(C.c_void_p)], W.LONG)
    profile_folder = bind(U, "GetAppContainerFolderPath", [W.LPCWSTR, C.POINTER(W.LPWSTR)], W.LONG)
    task_free = bind(O, "CoTaskMemFree", [C.c_void_p], None)
    in_job = bind(K, "IsProcessInJob", [W.HANDLE, W.HANDLE, C.POINTER(W.BOOL)], W.BOOL)
    windows_directory = bind(K, "GetWindowsDirectoryW", [W.LPWSTR, W.UINT], W.UINT)


def _windows():
    if os.name != "nt":
        raise Refused("AppContainer source host requires Windows")


def _check(ok):
    if not ok:
        raise C.WinError(C.get_last_error())


def _sid(pointer):
    if not pointer:
        raise Refused("actual token SID is missing")
    text = W.LPWSTR()
    _check(sid_to_text(pointer, C.byref(text)))
    try:
        return sid_text(text.value)
    finally:
        local_free(C.cast(text, C.c_void_p))


def _token_buffer(token, kind):
    count = W.DWORD()
    token_info(token, kind, None, 0, C.byref(count))
    if not 1 <= count.value <= 65536:
        raise Refused("bounded token information required")
    value = C.create_string_buffer(count.value)
    _check(token_info(token, kind, value, len(value), C.byref(count)))
    if count.value > len(value):
        raise Refused("token observation grew beyond allocation")
    return value


def _token_dword(token, kind):
    value = _token_buffer(token, kind)
    if len(value) != C.sizeof(W.DWORD):
        raise Refused("actual token DWORD shape refused")
    return C.cast(value, C.POINTER(W.DWORD)).contents.value


def _token_sid(token, kind):
    value = _token_buffer(token, kind)
    if len(value) < C.sizeof(C.c_void_p):
        raise Refused("actual token SID structure is truncated")
    pointer = C.cast(value, C.POINTER(C.c_void_p)).contents.value
    # Windows returns the SID within its caller-owned token buffer. Refuse an
    # unexpected external pointer before passing it to a SID conversion API.
    if pointer is None or not C.addressof(value) <= pointer <= C.addressof(value) + len(value) - 8:
        raise Refused("actual token SID pointer is outside its bounded buffer")
    header = C.string_at(pointer, 8)
    if header[0] != 1 or header[1] > 15 or pointer + 8 + 4 * header[1] > C.addressof(value) + len(value):
        raise Refused("actual token SID exceeds its bounded buffer")
    return _sid(pointer)


def current_user_sid():
    _windows()
    token = W.HANDLE()
    _check(open_token(get_current(), 8, C.byref(token)))
    try:
        return _token_sid(token, 1)
    finally:
        close(token)


def loopback_configuration(package):
    """Read existing exemption state for one exact SID; never change policy."""
    _windows()
    package = sid_text(package)
    if not re.fullmatch(r"S-1-15-2-(?:[0-9]+-){6}[0-9]+", package):
        raise Refused("one specific package SID required for loopback observation")
    count, rows = W.DWORD(), C.POINTER(SID_ATTRIBUTES)()
    error = get_loopback_config(C.byref(count), C.byref(rows))
    try:
        if error or count.value > 4096 or (count.value and not rows):
            raise Refused("bounded actual loopback configuration unavailable")
        # Return no other installed identities. A zero count is an observed
        # empty configuration, not a missing observation or a default grant.
        exempt = any(_sid(rows[i].Sid) == package for i in range(count.value))
        return {"package_sid": package, "configuration_count": count.value, "loopback_exempt": exempt}
    finally:
        if rows:
            heap = get_heap()
            if count.value <= 4096:
                for i in range(count.value):
                    if rows[i].Sid:
                        heap_free(heap, 0, rows[i].Sid)
            heap_free(heap, 0, C.cast(rows, C.c_void_p))
        # Unknown oversized native results are refused without walking an
        # unbounded array. The isolated observer process owns residual memory.


def observe_child(process, job):
    _windows()
    token, belongs = W.HANDLE(), W.BOOL()
    _check(open_token(process, 8, C.byref(token)))
    try:
        _check(in_job(process, job, C.byref(belongs)))
        groups = _token_buffer(token, 30)
        if len(groups) < C.sizeof(W.DWORD):
            raise Refused("actual token capabilities are truncated")
        count = C.cast(groups, C.POINTER(W.DWORD)).contents.value
        if count > 64:
            raise Refused("actual token capabilities exceed bound")
        return {"appcontainer": _token_dword(token, 29), "package_sid": _token_sid(token, 31),
                "capability_count": count, "integrity_sid": _token_sid(token, 25),
                "user_sid": _token_sid(token, 1), "elevated": _token_dword(token, 20),
                "ui_access": _token_dword(token, 26), "in_owned_job": bool(belongs.value)}
    finally:
        close(token)


def verify_observation(value, package, user):
    expected = {"appcontainer": 1, "package_sid": sid_text(package), "capability_count": 0,
                "integrity_sid": "S-1-16-4096", "user_sid": sid_text(user),
                "elevated": 0, "ui_access": 0, "in_owned_job": True}
    if not isinstance(value, dict) or set(value) != set(expected):
        raise Refused("complete actual child identity required before resume")
    if any(type(value[k]) is not type(want) or value[k] != want for k, want in expected.items()):
        raise Refused("actual child is not the exact admitted zero-capability AppContainer")
    return dict(value)


def expected_package_sid(spec):
    _windows()
    spec.validate()
    pointer = C.c_void_p()
    result = derive_sid(spec.moniker, C.byref(pointer))
    if result < 0:
        raise Refused("AppContainer package SID derivation refused")
    try:
        return _sid(pointer)
    finally:
        if pointer:
            free_sid(pointer)


@dataclass(frozen=True)
class PreparedProfile:
    spec: ProfileSpec
    package_sid: str
    folder: str

    @classmethod
    def create_once(cls, spec, *, guard):
        """One explicit effect; crash/uncertainty leaves the reservation occupied."""
        _windows()
        spec.validate()
        guard()
        expected = expected_package_sid(spec)
        # Exclusive creation precedes every profile effect. Existing intent,
        # receipt or foreign file is a refusal, never a reason to create again.
        with open(spec.reservation, "xb", buffering=0) as journal:
            def append(value):
                raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode() + b"\n"
                if journal.write(raw) != len(raw):
                    raise Refused("profile reservation write was incomplete")
                os.fsync(journal.fileno())
            append({"schema": "aide.host.profile-intent.v1", "moniker": spec.moniker,
                    "expected_package_sid": expected, "capability_count": 0, "cleanup": "retain_only"})
            pointer = C.c_void_p()
            guard()
            result = create_profile(spec.moniker, spec.moniker, "AIDE owned H1 native probe", None, 0, C.byref(pointer))
            if result < 0:
                append({"phase": "creation_refused_or_uncertain", "hresult": result & 0xffffffff, "cleanup": "retain_only"})
                raise Refused("profile creation refused; existing or uncertain profile cannot be adopted")
            try:
                package = _sid(pointer)
            finally:
                if pointer:
                    free_sid(pointer)
            if package != expected:
                append({"phase": "created_identity_mismatch", "cleanup": "retain_only"})
                raise Refused("created AppContainer identity differs from reservation")
            folder = W.LPWSTR()
            result = profile_folder(package, C.byref(folder))
            if result < 0:
                append({"phase": "created_folder_unobserved", "cleanup": "retain_only"})
                raise Refused("created AppContainer folder remains uncertain")
            try:
                path = folder.value
            finally:
                if folder:
                    task_free(C.cast(folder, C.c_void_p))
            append({"phase": "created", "package_sid": package, "folder": path, "cleanup": "retain_only"})
            return cls(spec, package, path)


class SecurityLaunch:
    """Internal exact native probe launch; no worker-selected security factory."""
    def __init__(self, profile, *, user_sid, argv, cwd, image_sha256, owned_objects, guard=None):
        if not isinstance(profile, PreparedProfile) or not argv or not isinstance(owned_objects, tuple) or not owned_objects:
            raise Refused("prepared profile and exact held probe objects required")
        self.profile, self.user_sid = profile, sid_text(user_sid)
        self.guard = guard
        self.argv, self.cwd = tuple(str(x) for x in argv), str(cwd)
        self.objects = owned_objects
        self.observations = tuple(value.observe() for value in owned_objects)
        if any(not row["sealed"] for row in self.observations):
            raise Refused("probe objects must be sealed before admission")
        if self.argv[0] not in {value.path for value in owned_objects if not value.directory} or self.cwd not in {value.path for value in owned_objects if value.directory}:
            raise Refused("native probe image and cwd must belong to held owned objects")
        image = next(value for value in owned_objects if value.path == self.argv[0])
        if not isinstance(image_sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", image_sha256) or image.content_sha256 != image_sha256:
            raise Refused("native probe bytes must match the admitted source/effect image digest")
        self.image_sha256 = image_sha256
        self.child_observation = None

    def assert_launch(self, argv, cwd):
        if self.guard is not None:
            self.guard()
        if tuple(str(x) for x in argv) != self.argv or str(cwd) != self.cwd:
            raise Refused("native AppContainer launch differs from exact admitted command")
        if tuple(value.observe() for value in self.objects) != self.observations:
            raise Refused("owned probe identity or descriptor changed before launch")

    def environment(self):
        text = C.create_unicode_buffer(32768)
        count = windows_directory(text, len(text))
        if not 1 <= count < len(text):
            raise Refused("actual Windows directory unavailable")
        return {"SYSTEMROOT": text.value, "WINDIR": text.value, "TEMP": self.cwd, "TMP": self.cwd,
                "USERPROFILE": self.profile.folder, "APPDATA": self.cwd, "LOCALAPPDATA": self.cwd}

    @contextmanager
    def attributes(self):
        pointer = C.c_void_p()
        _check(text_to_sid(self.profile.package_sid, C.byref(pointer)))
        value = CAPABILITIES(pointer, None, 0, 0)
        try:
            yield ((0x20009, C.byref(value), C.sizeof(value)),)
        finally:
            local_free(pointer)

    def verify_child(self, process, job):
        self.assert_launch(self.argv, self.cwd)
        self.child_observation = verify_observation(observe_child(process, job), self.profile.package_sid, self.user_sid)
        return dict(self.child_observation)
