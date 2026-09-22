"""Bounded preparation generations with kernel-bound Windows directory ownership."""
from contextlib import contextmanager
import ctypes
from ctypes import wintypes
import os

from .common import Refused, require_path


class UnicodeString(ctypes.Structure):
    _fields_ = [("Length", wintypes.USHORT), ("MaximumLength", wintypes.USHORT),
                ("Buffer", wintypes.LPWSTR)]


class ObjectAttributes(ctypes.Structure):
    _fields_ = [("Length", wintypes.ULONG), ("RootDirectory", wintypes.HANDLE),
                ("ObjectName", ctypes.POINTER(UnicodeString)), ("Attributes", wintypes.ULONG),
                ("SecurityDescriptor", ctypes.c_void_p), ("SecurityQualityOfService", ctypes.c_void_p)]


class IoStatus(ctypes.Structure):
    _fields_ = [("Status", ctypes.c_void_p), ("Information", ctypes.c_size_t)]


class FileInformation(ctypes.Structure):
    _fields_ = [("Attributes", wintypes.DWORD), ("Creation", wintypes.FILETIME),
                ("Access", wintypes.FILETIME), ("Write", wintypes.FILETIME),
                ("Volume", wintypes.DWORD), ("SizeHigh", wintypes.DWORD),
                ("SizeLow", wintypes.DWORD), ("Links", wintypes.DWORD),
                ("IndexHigh", wintypes.DWORD), ("IndexLow", wintypes.DWORD)]


@contextmanager
def directory_lease(path, *, create=False):
    """Hold directory-list access without delete sharing; atomically create new directories.

    This object lease is not a credential or child-file isolation boundary.
    No uncertain generation is ever cleaned up automatically.
    """
    path = require_path(str(path))
    if os.name != "nt" or str(path).startswith("\\\\"):
        raise Refused("preparation ownership requires a local Windows volume")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                  ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
    kernel.CreateFileW.restype = wintypes.HANDLE
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel.CloseHandle.restype = wintypes.BOOL
    kernel.GetFileInformationByHandle.argtypes = [wintypes.HANDLE, ctypes.POINTER(FileInformation)]
    kernel.GetFileInformationByHandle.restype = wintypes.BOOL
    if create:
        # NtCreateFile FILE_CREATE + FILE_DIRECTORY_FILE returns the exclusively
        # created object handle atomically; no CreateDirectory/open ownership gap.
        native = ctypes.WinDLL("ntdll")
        native.NtCreateFile.argtypes = [ctypes.POINTER(wintypes.HANDLE), wintypes.DWORD,
            ctypes.POINTER(ObjectAttributes), ctypes.POINTER(IoStatus), ctypes.c_void_p,
            wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, ctypes.c_void_p, wintypes.ULONG]
        native.NtCreateFile.restype = wintypes.LONG
        text = "\\??\\" + str(path)
        buffer = ctypes.create_unicode_buffer(text)
        name = UnicodeString(len(text.encode("utf-16-le")), len(text.encode("utf-16-le")) + 2,
                             ctypes.cast(buffer, wintypes.LPWSTR))
        attributes = ObjectAttributes(ctypes.sizeof(ObjectAttributes), None, ctypes.pointer(name), 0x40, None, None)
        handle, status = wintypes.HANDLE(), IoStatus()
        result = native.NtCreateFile(ctypes.byref(handle), 0x100081, ctypes.byref(attributes),
                                     ctypes.byref(status), None, 0x10, 3, 2, 0x21, None, 0)
        if result < 0:
            raise Refused("exclusive directory creation refused: " + hex(result & 0xffffffff))
    else:
        # Metadata-only access does not enforce Windows delete sharing. Directory
        # listing access enforces sharing without requiring DELETE sharing by Git.
        handle = kernel.CreateFileW(str(path), 0x81, 3, None, 3, 0x02000000, None)
        if handle == wintypes.HANDLE(-1).value:
            raise Refused("cannot lease preparation directory object")
    try:
        info = FileInformation()
        if not kernel.GetFileInformationByHandle(handle, ctypes.byref(info)):
            raise Refused("cannot observe leased directory identity")
        yield {"volume": info.Volume, "file_id": (info.IndexHigh << 32) | info.IndexLow}
    finally:
        kernel.CloseHandle(handle)
