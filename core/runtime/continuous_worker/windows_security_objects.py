"""Owned Windows probe objects: create-only handles, explicit grants, retain-only.

This source is not an installed host. Callers must first admit exact object paths
and effects. No API here deletes an object or adopts a pre-existing name.
"""
from __future__ import annotations
import ctypes as C
from ctypes import wintypes as W
from dataclasses import dataclass
import hashlib
import os
from pathlib import PureWindowsPath
import re

from .state import Refused

SID_PATTERN = re.compile(r"S-1-(?:[0-9]+-){1,14}[0-9]+")


def sid_text(value):
    if not isinstance(value, str) or len(value) > 180 or not SID_PATTERN.fullmatch(value):
        raise Refused("bounded literal Windows SID required")
    return value


def descriptor(user, package=None, *, mode="private", directory=False):
    user = sid_text(user)
    if mode not in ("private", "read", "modify") or (mode != "private" and package is None):
        raise Refused("explicit owned-object access mode required")
    flags = "OICI" if directory else ""
    entries = f"(A;{flags};FA;;;SY)(A;{flags};FA;;;{user})"
    if mode != "private":
        package = sid_text(package)
        if not re.fullmatch(r"S-1-15-2-(?:[0-9]+-){6}[0-9]+", package):
            raise Refused("one specific AppContainer package SID required")
        rights = "0x1200a9" if mode == "read" else "0x1301bf"
        entries += f"(A;{flags};{rights};;;{package})"
    # Only scratch objects are low-integrity writable. Protected objects remain
    # medium-integrity, with no package ACE and no inherited broad app grants.
    label = "LW" if mode == "modify" else "ME"
    return "D:P" + entries + f"S:(ML;;NW;;;{label})"


if os.name == "nt":
    K, A, N = C.WinDLL("kernel32", use_last_error=True), C.WinDLL("advapi32", use_last_error=True), C.WinDLL("ntdll")
    def bind(lib, name, args, result):
        value = getattr(lib, name)
        value.argtypes, value.restype = args, result
        return value
    class UNICODE(C.Structure):
        _fields_ = [("Length", W.USHORT), ("MaximumLength", W.USHORT), ("Buffer", W.LPWSTR)]
    class ATTRIBUTES(C.Structure):
        _fields_ = [("Length", W.ULONG), ("RootDirectory", W.HANDLE), ("ObjectName", C.POINTER(UNICODE)),
                    ("Attributes", W.ULONG), ("SecurityDescriptor", C.c_void_p), ("SecurityQualityOfService", C.c_void_p)]
    class IO_STATUS(C.Structure):
        _fields_ = [("StatusOrPointer", C.c_void_p), ("Information", C.c_size_t)]
    class FILE_ID(C.Structure):
        _fields_ = [("VolumeSerialNumber", C.c_ulonglong), ("FileId", C.c_ubyte * 16)]
    nt_create = bind(N, "NtCreateFile", [C.POINTER(W.HANDLE), W.DWORD, C.POINTER(ATTRIBUTES), C.POINTER(IO_STATUS),
        C.c_void_p, W.DWORD, W.DWORD, W.DWORD, W.DWORD, C.c_void_p, W.DWORD], W.LONG)
    query_device = bind(K, "QueryDosDeviceW", [W.LPCWSTR, W.LPWSTR, W.DWORD], W.DWORD)
    close = bind(K, "CloseHandle", [W.HANDLE], W.BOOL)
    local_free = bind(K, "LocalFree", [C.c_void_p], C.c_void_p)
    get_identity = bind(K, "GetFileInformationByHandleEx", [W.HANDLE, C.c_int, C.c_void_p, W.DWORD], W.BOOL)
    write_file = bind(K, "WriteFile", [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], W.BOOL)
    flush_file = bind(K, "FlushFileBuffers", [W.HANDLE], W.BOOL)
    sd_from_text = bind(A, "ConvertStringSecurityDescriptorToSecurityDescriptorW", [W.LPCWSTR, W.DWORD, C.POINTER(C.c_void_p), C.c_void_p], W.BOOL)
    sd_to_text = bind(A, "ConvertSecurityDescriptorToStringSecurityDescriptorW", [C.c_void_p, W.DWORD, W.DWORD, C.POINTER(W.LPWSTR), C.c_void_p], W.BOOL)
    sd_dacl = bind(A, "GetSecurityDescriptorDacl", [C.c_void_p, C.POINTER(W.BOOL), C.POINTER(C.c_void_p), C.POINTER(W.BOOL)], W.BOOL)
    sd_sacl = bind(A, "GetSecurityDescriptorSacl", [C.c_void_p, C.POINTER(W.BOOL), C.POINTER(C.c_void_p), C.POINTER(W.BOOL)], W.BOOL)
    set_security = bind(A, "SetSecurityInfo", [W.HANDLE, C.c_int, W.DWORD, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p], W.DWORD)
    get_security = bind(A, "GetSecurityInfo", [W.HANDLE, C.c_int, W.DWORD, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p, C.POINTER(C.c_void_p)], W.DWORD)


def _check(ok):
    if not ok:
        raise C.WinError(C.get_last_error())


def _windows():
    if os.name != "nt":
        raise Refused("native Windows object host required")


def local_volume(drive):
    """Observe one literal local volume mapping; never follow a DOS alias."""
    _windows()
    if not isinstance(drive, str) or not re.fullmatch(r"[A-Za-z]:", drive):
        raise Refused("one literal Windows drive required")
    value = C.create_unicode_buffer(4096)
    count = query_device(drive, value, len(value))
    if not 2 < count < len(value):
        raise Refused("bounded local Windows drive observation required")
    text = value[:count]
    # QueryDosDevice returns a MULTI_SZ. Refuse even retained prior mappings:
    # this bounded host admits one unambiguous local disk volume only.
    if not text.endswith("\x00\x00") or "\x00" in text[:-2]:
        raise Refused("ambiguous Windows drive mapping refused")
    target = text[:-2]
    if not re.fullmatch(r"\\Device\\HarddiskVolume[1-9][0-9]{0,9}", target):
        raise Refused("only an observed local native disk volume is admitted")
    return target


def native_path(path):
    if not isinstance(path, str):
        raise Refused("exact new local Windows root required")
    value = PureWindowsPath(path)
    if (len(path) > 240 or not re.fullmatch(r"[A-Za-z]:", value.drive) or
            not value.is_absolute() or any(p in (".", "..") for p in value.parts) or
            any(c in str(value)[2:] for c in (":", "\x00"))):
        raise Refused("exact new local Windows root required")
    # Bypass only the observed DOS drive alias. OBJ_DONT_REPARSE remains set
    # by _open for every actual filesystem component, including the parent.
    return local_volume(value.drive) + str(value)[2:]


def _sd(text):
    pointer = C.c_void_p()
    _check(sd_from_text(text, 1, C.byref(pointer), None))
    return pointer


def _identity(handle):
    value = FILE_ID()
    _check(get_identity(handle, 18, C.byref(value), C.sizeof(value)))
    identity = bytes(value.FileId).hex()
    if identity == "0" * 32:
        raise Refused("owned object has no stable file identity")
    return {"volume": value.VolumeSerialNumber, "file_id": identity}


def _open(name, parent, *, directory, create, security=None, share=1, guard=None):
    _windows()
    text = C.create_unicode_buffer(name)
    name_value = UNICODE(len(name.encode("utf-16-le")), len(name.encode("utf-16-le")) + 2, C.cast(text, W.LPWSTR))
    sd = _sd(security) if security else None
    attrs = ATTRIBUTES(C.sizeof(ATTRIBUTES), parent, C.pointer(name_value), 0x40 | 0x1000, sd, None)
    handle, status = W.HANDLE(), IO_STATUS()
    # No DELETE access and no delete-on-close. Read-only opens retain descriptor
    # control without FILE_WRITE_DATA, allowing an executable image section.
    access = 0x001E01FF if create else 0x001E00A9
    options = 0x20 | (0x1 if directory else 0x40)
    try:
        if guard is not None:
            guard()
        result = nt_create(C.byref(handle), access, C.byref(attrs), C.byref(status), None, 0x80,
                           share, 2 if create else 1, options, None, 0)
        if result < 0:
            raise Refused(f"owned Windows object open refused (NTSTATUS {result & 0xffffffff:08x})")
        if create and status.Information != 2:  # FILE_CREATED; never FILE_OPENED.
            close(handle)
            raise Refused("owned object was not exclusively created")
        return handle
    finally:
        if sd:
            local_free(sd)


@dataclass
class OwnedObject:
    handle: object
    name: str
    parent: "OwnedObject | None"
    path: str
    directory: bool
    user: str
    identity: dict
    sealed: bool = False
    closed: bool = False
    written: bool = False
    content_sha256: str | None = None
    guard: object = None

    @classmethod
    def create_root(cls, path, user, *, guard=None):
        _windows()
        name = native_path(path)
        value = PureWindowsPath(path)
        handle = _open(name, None, directory=True, create=True, security=descriptor(user, directory=True), guard=guard)
        try:
            return cls(handle, name, None, str(value), True, sid_text(user), _identity(handle), guard=guard)
        except Exception:
            close(handle)
            raise

    def _live(self):
        if self.guard is not None:
            self.guard()
        if self.closed or (self.parent is not None and self.parent.closed) or _identity(self.handle) != self.identity:
            raise Refused("owned object handle is unavailable or changed")

    def child(self, name, *, directory=False):
        self._live()
        if not self.directory or self.sealed or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,79}", name) or name.endswith("."):
            raise Refused("owned child must be a new literal component before sealing")
        handle = _open(name, self.handle, directory=directory, create=True, security=descriptor(self.user, directory=directory), guard=self.guard)
        try:
            return OwnedObject(handle, name, self, str(PureWindowsPath(self.path) / name), directory, self.user, _identity(handle), guard=self.guard)
        except Exception:
            close(handle)
            raise

    def write(self, data):
        self._live()
        if self.directory or self.sealed or self.written or not isinstance(data, bytes) or len(data) > 16 * 1024 * 1024:
            raise Refused("bounded owned file write required before sealing")
        self.written = True
        value, count = C.create_string_buffer(data), W.DWORD()
        _check(write_file(self.handle, value, len(data), C.byref(count), None))
        _check(count.value == len(data))
        _check(flush_file(self.handle))
        self.content_sha256 = hashlib.sha256(data).hexdigest()
        return self.content_sha256

    def seal(self):
        self._live()
        if self.sealed:
            raise Refused("owned object already sealed")
        parent = self.parent.handle if self.parent else None
        # Keep a read handle on the original object while retiring its writable
        # file object, then acquire the final no-write/no-delete sharing handle.
        middle = _open(self.name, parent, directory=self.directory, create=False, share=3, guard=self.guard)
        try:
            if _identity(middle) != self.identity:
                raise Refused("owned object name no longer binds its created handle")
            close(self.handle)
            self.handle, self.closed = middle, False
            middle = None
            final = _open(self.name, parent, directory=self.directory, create=False, share=1, guard=self.guard)
            try:
                if _identity(final) != self.identity:
                    raise Refused("owned object changed during sealing")
            except Exception:
                close(final)
                raise
            close(self.handle)
            self.handle, self.sealed = final, True
        finally:
            if middle:
                close(middle)

    def grant(self, package, *, mode):
        self._live()
        if not self.sealed:
            raise Refused("seal the exact created object before granting package access")
        text = descriptor(self.user, package, mode=mode, directory=self.directory)
        value = _sd(text)
        try:
            present, defaulted, dacl, sacl = W.BOOL(), W.BOOL(), C.c_void_p(), C.c_void_p()
            _check(sd_dacl(value, C.byref(present), C.byref(dacl), C.byref(defaulted)))
            if not present or not dacl:
                raise Refused("explicit owned object DACL required")
            _check(sd_sacl(value, C.byref(present), C.byref(sacl), C.byref(defaulted)))
            if not present or not sacl:
                raise Refused("explicit owned object mandatory label required")
            if self.guard is not None:
                self.guard()
            error = set_security(self.handle, 1, 0x80000000 | 4 | 0x10, None, None, dacl, sacl)
            if error:
                raise Refused(f"owned handle grant refused (Win32 {error})")
            return self.observe()
        finally:
            local_free(value)

    def observe(self):
        self._live()
        descriptor_value, text = C.c_void_p(), W.LPWSTR()
        error = get_security(self.handle, 1, 4 | 0x10, None, None, None, None, C.byref(descriptor_value))
        if error:
            raise Refused(f"owned handle descriptor observation refused (Win32 {error})")
        try:
            _check(sd_to_text(descriptor_value, 1, 4 | 0x10, C.byref(text), None))
            return {"path": self.path, "identity": dict(self.identity), "sddl": text.value, "sealed": self.sealed, "content_sha256": self.content_sha256}
        finally:
            if text:
                local_free(C.cast(text, C.c_void_p))
            if descriptor_value:
                local_free(descriptor_value)

    def close(self):
        if not self.closed:
            close(self.handle)
            self.closed = True
        # Retain the object. No pathname/identity check authorizes deletion.
