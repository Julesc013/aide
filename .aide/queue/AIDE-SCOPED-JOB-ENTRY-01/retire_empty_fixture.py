"""Retire one exact empty test fixture under its creating sandbox identity."""
import ctypes
import json
import os
from pathlib import Path
import stat
import sys

root = Path(sys.argv[1])
tmp = Path(sys.argv[2])
if (not root.is_absolute() or root.parent != tmp or '..' in root.parts
        or root.name != 'tiny-scope-fx7fg9nd'):
    raise ValueError('exact recovery fixture required')
def ordinary_directory(path):
    info = path.lstat()
    if (not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode)
            or getattr(info, 'st_file_attributes', 0) & 1024):
        raise ValueError('recovery link/non-directory preserved')
ordinary_directory(tmp)
ordinary_directory(root)
identity = ctypes.create_unicode_buffer(256); size = ctypes.c_ulong(len(identity))
if not ctypes.windll.secur32.GetUserNameExW(2, identity, ctypes.byref(size)):
    raise ctypes.WinError()
children = list(root.iterdir())
if {p.name for p in children} != {'scratch', 'retained', 'control'}:
    raise ValueError('unexpected fixture contents preserved')
for child in children:
    ordinary_directory(child)
    if list(child.iterdir()):
        raise ValueError('nonempty fixture preserved')
for child in children:
    child.rmdir()
root.rmdir()
print(json.dumps({'retired_exact_empty_fixture':str(root),
                  'windows_identity':identity.value,'directories_removed':4}))
