"""Explicit Python derived-library data; no image or loader effects."""
from __future__ import annotations
from dataclasses import dataclass, replace
import hashlib
import io
import json
import re
import zipfile

from .state import Refused

MAX_MEMBERS = 1024
MAX_MEMBER_BYTES = 2 * 1024 * 1024
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_ARCHIVE_BYTES = 18 * 1024 * 1024
PTH_BYTES = b"python314.zip\n.\n"
BOOTSTRAP_MEMBERS = frozenset({
    "encodings/__init__.py", "encodings/aliases.py", "encodings/utf_8.py", "codecs.py",
    "json/__init__.py", "json/decoder.py", "json/encoder.py", "json/scanner.py",
    "os.py", "io.py", "ntpath.py", "stat.py",
})



def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise Refused("literal SHA256 required")
    return value


def _integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise Refused("explicit bounded integer required")
    return value


def _member_path(value):
    if not isinstance(value, str) or not value.endswith(".py") or len(value) > 160:
        raise Refused("bounded literal Python source member required")
    parts = value.split("/")
    if len(parts) > 12:
        raise Refused("library member depth exceeds bound")
    for part in parts:
        base = part.split(".", 1)[0].upper()
        if (not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,79}", part) or part.endswith(".") or
                base in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(r"(?:COM|LPT)[1-9]", base) or
                part.lower() in {"site-packages", "__pycache__", "sitecustomize.py", "usercustomize.py"}):
            raise Refused("non-device source member without ambient site hooks required")
    return value


@dataclass(frozen=True)
class Member:
    path: str
    size: int
    sha256: str


@dataclass(frozen=True)
class LibrarySpec:
    members: tuple[Member, ...]
    source_bytes: int
    archive_bytes: int
    fingerprint: str

    @classmethod
    def read(cls, value):
        if (type(value) is not dict or set(value) != {"schema", "members", "source_bytes", "archive_bytes"} or
                value["schema"] != "aide.host.python-library.v1"):
            raise Refused("exact known Python library specification required")
        source_limit = _integer(value["source_bytes"], 1, MAX_SOURCE_BYTES)
        archive_limit = _integer(value["archive_bytes"], source_limit, MAX_ARCHIVE_BYTES)
        rows = value["members"]
        if type(rows) is not list or not 1 <= len(rows) <= MAX_MEMBERS:
            raise Refused("finite nonempty library member list required")
        members, names, directories, total = [], {}, {}, 0
        for row in rows:
            if type(row) is not dict or set(row) != {"path", "size", "sha256"}:
                raise Refused("exact library member fields required")
            path = _member_path(row["path"]); folded = path.casefold()
            if folded in names: raise Refused("duplicate or case-aliased library member")
            names[folded] = path
            parts = path.split("/")
            for i in range(1, len(parts)):
                directory = "/".join(parts[:i]); key = directory.casefold()
                if key in directories and directories[key] != directory:
                    raise Refused("case-aliased library directory")
                directories[key] = directory
            size = _integer(row["size"], 0, MAX_MEMBER_BYTES); total += size
            members.append(Member(path, size, _digest(row["sha256"])))
        predicted = total + 22 + sum(76 + 2 * len(row.path) for row in members)
        if names.keys() & directories.keys() or total > source_limit or predicted > archive_limit:
            raise Refused("library path collision or aggregate byte bound exceeded")
        if not BOOTSTRAP_MEMBERS <= set(names.values()):
            raise Refused("explicit codec/JSON bootstrap members are missing")
        result = cls(tuple(sorted(members, key=lambda row: row.path)), source_limit, archive_limit, "")
        canonical = json.dumps(result.to_value(), sort_keys=True, separators=(",", ":")).encode()
        return replace(result, fingerprint=hashlib.sha256(canonical).hexdigest())

    def to_value(self):
        return {"schema": "aide.host.python-library.v1", "source_bytes": self.source_bytes,
                "archive_bytes": self.archive_bytes,
                "members": [{"path": row.path, "size": row.size, "sha256": row.sha256} for row in self.members]}

    def validate(self):
        try:
            if LibrarySpec.read(self.to_value()) != self: raise Refused("typed library admission differs from its immutable value")
        except (AttributeError, TypeError, ValueError) as error:
            raise Refused("complete immutable library admission required") from error
        return self


@dataclass(frozen=True)
class DerivedFile:
    path: str
    contents: bytes
    producer_sha256: str

    def __post_init__(self):
        if (self.path not in ("python314.zip", "python314._pth") or type(self.contents) is not bytes or
                not 0 < len(self.contents) <= MAX_ARCHIVE_BYTES):
            raise Refused("one bounded known derived Python file required")
        _digest(self.producer_sha256)
        if self.path == "python314._pth" and self.contents != PTH_BYTES:
            raise Refused("fixed isolated Python path payload required")

    @property
    def sha256(self):
        return hashlib.sha256(self.contents).hexdigest()

    def declaration(self):
        return {"kind": "generated_bytes", "path": self.path, "size": len(self.contents),
                "sha256": self.sha256, "producer_sha256": self.producer_sha256}


@dataclass(frozen=True)
class LibraryBundle:
    spec: LibrarySpec
    files: tuple[DerivedFile, ...]

    def manifest(self):
        return {"schema": "aide.host.python-derived-library.v1", "producer_sha256": self.spec.fingerprint,
                "members": self.spec.to_value()["members"], "files": [row.declaration() for row in self.files],
                "format": "ZIP_STORED/fixed-1980-epoch/ASCII-names/no-extras-or-comments/no-ZIP64",
                "tool_runtime_qualified": False}


def build_stdlib(spec, inputs):
    """Derive inert archive bytes; metadata admission does not prove import behavior."""
    if not isinstance(spec, LibrarySpec) or type(inputs) is not dict:
        raise Refused("typed library admission and exact source bytes required")
    spec.validate()
    if set(inputs) != {row.path for row in spec.members}:
        raise Refused("library input set differs from admission")
    frozen = []
    for row in spec.members:
        try: data = inputs[row.path]
        except KeyError as error: raise Refused("library input set changed while freezing") from error
        if type(data) is not bytes or len(data) != row.size or hashlib.sha256(data).hexdigest() != row.sha256:
            raise Refused("library source length or digest changed")
        frozen.append((row, data))
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED, allowZip64=False) as archive:
        for row, data in frozen:
            info = zipfile.ZipInfo(row.path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED; info.create_system = 0
            info.create_version = 20; info.extract_version = 20
            info.external_attr = 0o100444 << 16; info.internal_attr = 0
            info.extra = b""; info.comment = b""
            archive.writestr(info, data)
    data = output.getvalue()
    predicted = sum(row.size + 76 + 2 * len(row.path) for row in spec.members) + 22
    if len(data) != predicted or len(data) > spec.archive_bytes:
        raise Refused("derived library exceeds exact admitted ZIP structure")
    return LibraryBundle(spec, (DerivedFile("python314.zip", data, spec.fingerprint),
                                DerivedFile("python314._pth", PTH_BYTES, spec.fingerprint)))
