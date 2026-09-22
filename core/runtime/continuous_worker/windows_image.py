"""Bounded private image admission and retained preparation; no installed host factory."""
from __future__ import annotations
from contextlib import ExitStack, closing
import ctypes as C
from ctypes import wintypes as W
from dataclasses import dataclass, replace
import hashlib
import json
import math
import os
from pathlib import Path, PureWindowsPath
import re
import time

from . import windows_security_objects as native
from .state import Refused
from .windows_python_image import DerivedFile, MAX_ARCHIVE_BYTES, PTH_BYTES

CHUNK = 65536


def _integer(value, lower, upper, name):
    if type(value) is not int or not lower <= value <= upper:
        raise Refused(f"bounded integer {name} required")
    return value


def _digest(value):
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise Refused("literal SHA256 required")
    return value


def _identity(value):
    if (not isinstance(value, dict) or set(value) != {"volume", "file_id"} or
            type(value["volume"]) is not int or not 0 < value["volume"] < 2**64 or
            not isinstance(value["file_id"], str) or not re.fullmatch(r"[0-9a-f]{32}", value["file_id"]) or
            value["file_id"] == "0" * 32):
        raise Refused("exact native volume and object identity required")
    return value["volume"], value["file_id"]


def relative_path(value):
    if not isinstance(value, str) or not value or len(value) > 160 or "\\" in value:
        raise Refused("bounded slash-separated image path required")
    parts = value.split("/")
    if len(parts) > 12:
        raise Refused("image directory depth exceeds bound")
    for part in parts:
        native.literal_component(part)
    return tuple(parts)


def _utf16_units(value):
    try:
        return len(value.encode("utf-16-le")) // 2
    except UnicodeEncodeError as error:
        raise Refused("well-formed Unicode Windows path required") from error


def _root(value):
    if not isinstance(value, str) or _utf16_units(value) > 180:
        raise Refused("bounded absolute private-image root required")
    path = PureWindowsPath(value)
    if (not path.is_absolute() or not re.fullmatch(r"[A-Za-z]:", path.drive) or
            str(path) != value or any(part in (".", "..") for part in path.parts) or
            any(c in value[2:] for c in (":", "\x00"))):
        raise Refused("canonical local image root required")
    for part in path.parts[1:]:
        # NT object names and Win32 journal paths must have one spelling. Keep
        # legitimate internal spaces/Unicode, but refuse Win32-normalized names.
        device = part.split(".", 1)[0].rstrip(" ").upper().translate(str.maketrans("¹²³", "123"))
        if (part.endswith((".", " ")) or re.search(r'[<>"|?*\x00-\x1f]', part) or
                device in {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$", "CLOCK$"} or
                re.fullmatch(r"(?:COM|LPT)[1-9]", device)):
            raise Refused("ambiguous Windows root component refused")
    return path


@dataclass(frozen=True)
class ImageLimits:
    entries: int
    file_bytes: int
    total_bytes: int
    seconds: int

    def __post_init__(self):
        _integer(self.entries, 1, 2048, "entry count")
        _integer(self.file_bytes, 1, 512 * 1024 * 1024, "file bytes")
        _integer(self.total_bytes, self.file_bytes, 768 * 1024 * 1024, "total bytes")
        _integer(self.seconds, 1, 300, "preparation seconds")


@dataclass(frozen=True)
class ImageFile:
    path: str
    source: str
    size: int
    sha256: str
    source_identity: tuple[int, str]


@dataclass(frozen=True)
class GeneratedImageFile:
    path: str
    size: int
    sha256: str
    producer_sha256: str


def _image_files(rows, limits, source, output, schema):
    if type(rows) is not list or not 1 <= len(rows) <= limits.entries:
        raise Refused("bounded nonempty image files required")
    files, names, directories, sources, source_directories, total = [], {}, {}, set(), {}, 0
    for row in rows:
        if type(row) is not dict:
            raise Refused("known exact image file required")
        kind = "source_file" if schema.endswith(".v1") else row.get("kind")
        fields = {"path", "source", "size", "sha256", "source_identity"} if kind == "source_file" else {"path", "size", "sha256", "producer_sha256"}
        if schema.endswith(".v2"): fields.add("kind")
        if kind not in ("source_file", "generated_bytes") or set(row) != fields:
            raise Refused("explicit known source-file or generated-byte fields required")
        parts = relative_path(row["path"]); path = "/".join(parts); key = path.casefold()
        if key in names or _utf16_units(str(output.joinpath(*parts))) > 240:
            raise Refused("image path alias or materialized path bound exceeded")
        size = _integer(row["size"], 0, limits.file_bytes, "declared file size")
        digest = _digest(row["sha256"])
        components_to_record = [(parts, directories)]
        if kind == "source_file":
            origin = relative_path(row["source"]); source_name = "/".join(origin)
            if source_name.casefold() in sources or _utf16_units(str(source.joinpath(*origin))) > 240:
                raise Refused("source alias or materialized path bound exceeded")
            sources.add(source_name.casefold()); components_to_record.append((origin, source_directories))
            entry = ImageFile(path, source_name, size, digest, _identity(row["source_identity"]))
        else:
            if path not in ("python314.zip", "python314._pth") or not 0 < size <= MAX_ARCHIVE_BYTES:
                raise Refused("one bounded exact derived Python path required")
            if path == "python314._pth" and (size != len(PTH_BYTES) or digest != hashlib.sha256(PTH_BYTES).hexdigest()):
                raise Refused("fixed isolated Python path declaration required")
            entry = GeneratedImageFile(path, size, digest, _digest(row["producer_sha256"]))
        for components, registered in components_to_record:
            for i in range(1, len(components)):
                directory = "/".join(components[:i]); folded = directory.casefold()
                if folded in registered and registered[folded] != directory:
                    raise Refused("case-aliased image or source directory")
                registered[folded] = directory
        names[key] = path; total += size; files.append(entry)
    if (names.keys() & directories.keys() or sources & source_directories.keys() or
            len(names) + len(directories) > limits.entries or total > limits.total_bytes):
        raise Refused("file/directory collision or aggregate image limit exceeded")
    return tuple(sorted(files, key=lambda row: row.path))


@dataclass(frozen=True)
class ImagePlan:
    generation: str
    input_root: str
    input_identity: tuple[int, str]
    output_root: str
    parent_identity: tuple[int, str]
    user_sid: str
    package_sid: str
    entrypoint: str
    limits: ImageLimits
    files: tuple[ImageFile | GeneratedImageFile, ...]
    fingerprint: str
    schema: str = "aide.host.private-image.v1"

    @classmethod
    def read(cls, value):
        fields = {"schema", "generation", "input_root", "input_identity", "output_root", "parent_identity",
                  "user_sid", "package_sid", "entrypoint", "limits", "files"}
        if not isinstance(value, dict) or set(value) != fields or value["schema"] not in ("aide.host.private-image.v1", "aide.host.private-image.v2"):
            raise Refused("known exact private-image plan required")
        generation = value["generation"]
        if not isinstance(generation, str) or not re.fullmatch(r"[0-9a-f]{32}", generation):
            raise Refused("literal private-image generation required")
        source, output = _root(value["input_root"]), _root(value["output_root"])
        if output.name != "image-" + generation or source == output or source in output.parents or output in source.parents:
            raise Refused("separate input and uniquely named output image required")
        limits = value["limits"]
        if not isinstance(limits, dict) or set(limits) != {"entries", "file_bytes", "total_bytes", "seconds"}:
            raise Refused("explicit private-image limits required")
        limits = ImageLimits(**limits)
        user, package = native.sid_text(value["user_sid"]), native.sid_text(value["package_sid"])
        if not re.fullmatch(r"S-1-15-2-(?:[0-9]+-){6}[0-9]+", package):
            raise Refused("one specific package SID required")
        files = _image_files(value["files"], limits, source, output, value["schema"])
        entrypoint = "/".join(relative_path(value["entrypoint"]))
        if entrypoint not in {row.path for row in files if isinstance(row, ImageFile)} or not entrypoint.lower().endswith(".exe"):
            raise Refused("exact declared executable entrypoint required")
        result = cls(generation, str(source), _identity(value["input_identity"]), str(output),
                   _identity(value["parent_identity"]), user, package, entrypoint, limits,
                   files, "", value["schema"])
        canonical = json.dumps(result.to_value(), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
        return replace(result, fingerprint=hashlib.sha256(canonical).hexdigest())

    def to_value(self):
        identity = lambda pair: {"volume": pair[0], "file_id": pair[1]}
        def file_value(row):
            if isinstance(row, GeneratedImageFile):
                return {"kind": "generated_bytes", "path": row.path, "size": row.size,
                        "sha256": row.sha256, "producer_sha256": row.producer_sha256}
            value = {"path": row.path, "source": row.source, "size": row.size,
                     "sha256": row.sha256, "source_identity": identity(row.source_identity)}
            if self.schema.endswith(".v2"): value["kind"] = "source_file"
            return value
        return {"schema": self.schema, "generation": self.generation,
                "input_root": self.input_root, "input_identity": identity(self.input_identity),
                "output_root": self.output_root, "parent_identity": identity(self.parent_identity),
                "user_sid": self.user_sid, "package_sid": self.package_sid, "entrypoint": self.entrypoint,
                "limits": {key: getattr(self.limits, key) for key in ("entries", "file_bytes", "total_bytes", "seconds")},
                "files": [file_value(row) for row in self.files]}

    def validate(self):
        try:
            if ImagePlan.read(self.to_value()) != self:
                raise Refused("typed image plan differs from its validated immutable value")
        except (AttributeError, TypeError, ValueError, IndexError) as error:
            raise Refused("complete immutable image admission required") from error
        return self

    @property
    def reservation(self):
        return str(PureWindowsPath(self.output_root).parent / ("image-" + self.generation + ".intent.jsonl"))


class _STANDARD(C.Structure):
    _fields_ = [("allocation", C.c_longlong), ("size", C.c_longlong), ("links", W.DWORD),
                ("delete_pending", C.c_ubyte), ("directory", C.c_ubyte)]


def _file_size(handle):
    value = _STANDARD()
    native._check(native.get_identity(handle, 1, C.byref(value), C.sizeof(value)))
    if value.links != 1 or value.delete_pending or value.directory or value.size < 0:
        raise Refused("one ordinary stable source file required")
    return value.size


def _normalized_nt_name(handle):
    get_name = native.bind(native.K, "GetFinalPathNameByHandleW", [W.HANDLE, W.LPWSTR, W.DWORD, W.DWORD], W.DWORD)
    buffer = C.create_unicode_buffer(4096)
    length = get_name(handle, buffer, len(buffer), 2)  # NORMALIZED | VOLUME_NAME_NT.
    value = buffer.value
    if (not 0 < length < len(buffer) or _utf16_units(value) != length or
            not re.fullmatch(r"\\Device\\HarddiskVolume[1-9][0-9]{0,9}(?:\\.*)?", value) or
            str(PureWindowsPath(value)) != value):
        raise Refused("bounded normalized native directory name required")
    return value


def _separate_roots(source, parent, output):
    origin = PureWindowsPath(source.canonical_name)
    destination = PureWindowsPath(parent.canonical_name) / PureWindowsPath(output).name
    if (source.expected == parent.expected or origin == destination or
            origin in destination.parents or destination in origin.parents):
        raise Refused("held source and image objects overlap")


def _reserve_journal(path, parent, guard):
    """CREATE_NEW relative to the held parent; the CRT adopts that exact handle."""
    import msvcrt
    value = PureWindowsPath(path)
    if value.parent != PureWindowsPath(parent.path):
        raise Refused("journal must be relative to its held parent")
    native.literal_component(value.name); parent.check()
    try:
        handle = native._open(value.name, parent.handle, directory=False, create=True, share=0, guard=guard)
    except (Refused, OSError) as error:
        raise Refused("image reservation unavailable; retain without replay") from error
    try:
        descriptor = msvcrt.open_osfhandle(handle.value, os.O_WRONLY | os.O_BINARY | os.O_NOINHERIT)
    except BaseException:
        native.close(handle)
        raise
    try:
        return os.fdopen(descriptor, "wb", buffering=0)
    except BaseException:
        os.close(descriptor)
        raise


def _create_image_root(path, user, *, guard, parent):
    value = PureWindowsPath(path)
    if value.parent != PureWindowsPath(parent.path):
        raise Refused("image must be relative to its held parent")
    native.literal_component(value.name); parent.check()
    handle = native._open(value.name, parent.handle, directory=True, create=True,
                          security=native.descriptor(user, directory=True), guard=guard)
    try:
        return native.OwnedObject(handle, value.name, parent, str(value), True, user,
                                  native._identity(handle), guard=guard)
    except BaseException:
        native.close(handle)
        raise


class SourceDirectory:
    """Read-only no-reparse lease; its existing objects are never granted or deleted."""
    def __init__(self, path, expected, guard):
        self.path, self.expected, self.guard = path, expected, guard
        self.native_name = native.native_path(path)
        self.handle = native._open(self.native_name, None, directory=True, create=False,
                                   read_only_source=True, guard=guard)
        try:
            self.check()
            self.canonical_name = _normalized_nt_name(self.handle)
            if self.canonical_name.casefold() != self.native_name.casefold():
                raise Refused("source or parent alias differs from its held normalized name")
            self.check()
        except Exception:
            self.close()
            raise

    @property
    def closed(self):
        return self.handle is None

    def check(self):
        self.guard()
        if self.handle is None or tuple(native._identity(self.handle)[key] for key in ("volume", "file_id")) != self.expected:
            raise Refused("protected source or parent object changed")
        if native.native_path(self.path).casefold() != self.native_name.casefold():
            raise Refused("literal drive mapping changed from its held directory")

    def close(self):
        if self.handle is not None:
            native.close(self.handle); self.handle = None

    def chunks(self, entry):
        self.check()
        handles, parent = [], self.handle
        try:
            parts = relative_path(entry.source)
            for i, part in enumerate(parts):
                handle = native._open(part, parent, directory=i < len(parts) - 1, create=False,
                                      read_only_source=True, guard=self.guard)
                handles.append(handle); parent = handle
            expected = tuple(native._identity(parent)[key] for key in ("volume", "file_id"))
            if expected != entry.source_identity or _file_size(parent) != entry.size:
                raise Refused("source file identity or size differs from admission")
            read_file = native.bind(native.K, "ReadFile", [W.HANDLE, C.c_void_p, W.DWORD, C.POINTER(W.DWORD), C.c_void_p], W.BOOL)
            remaining = entry.size
            while remaining:
                self.check(); self.guard()
                length = min(CHUNK, remaining); block, count = C.create_string_buffer(length), W.DWORD()
                native._check(read_file(parent, block, length, C.byref(count), None))
                if count.value != length:
                    raise Refused("protected source returned an incomplete chunk")
                remaining -= length
                yield block.raw
            self.check()
            if tuple(native._identity(parent)[key] for key in ("volume", "file_id")) != expected or _file_size(parent) != entry.size:
                raise Refused("protected source changed during copy")
        finally:
            for handle in reversed(handles): native.close(handle)


@dataclass
class PreparedImage:
    plan: ImagePlan
    objects: tuple
    observations: tuple
    closed: bool = False
    leases: object = None

    def check(self):
        if self.closed or tuple(obj.observe() for obj in self.objects) != self.observations:
            raise Refused("prepared image object or descriptor changed")
        return self.observations

    def close(self):
        for obj in reversed(self.objects): obj.close()
        if self.leases is not None: self.leases.close()
        self.closed = True


def _generated_inputs(plan, generated):
    if type(generated) is not tuple:
        raise Refused("immutable explicit generated-file tuple required")
    expected = {row.path: row for row in plan.files if isinstance(row, GeneratedImageFile)}
    if len(generated) != len(expected):
        raise Refused("generated-byte input set differs from image admission")
    result = {}
    for item in generated:
        if type(item) is not DerivedFile:
            raise Refused("typed immutable derived bytes required")
        # Reconstruct to refuse a forged/mutated typed value before any native
        # lease or reservation. The admission's producer and digest are authority.
        current = DerivedFile(item.path, item.contents, item.producer_sha256)
        entry = expected.get(current.path)
        if (entry is None or current.path in result or len(current.contents) != entry.size or
                current.sha256 != entry.sha256 or current.producer_sha256 != entry.producer_sha256):
            raise Refused("generated bytes differ from admitted path, size, digest or producer")
        result[current.path] = current.contents
    return result


def _generated_chunks(data):
    for offset in range(0, len(data), CHUNK):
        yield data[offset:offset + CHUNK]


def prepare_image(plan, *, guard, clock=time.monotonic, generated=()):
    """Prepare admitted bytes only; tool/DLL/runtime qualification remains separate.

    Local synchronous I/O gets checks before/after operations. A qualified outer
    owned process must still enforce the wall limit if a kernel call stalls.
    """
    if not isinstance(plan, ImagePlan) or not callable(guard):
        raise Refused("trusted typed image plan and current controller guard required")
    plan.validate()
    preparing = True
    started = clock()
    if type(started) not in (int, float) or not math.isfinite(started):
        raise Refused("finite monotonic image clock required")
    deadline = started + plan.limits.seconds
    def current():
        guard()
        now = clock()
        if type(now) not in (int, float) or not math.isfinite(now) or (now < started or (preparing and now >= deadline)):
            raise Refused("private-image preparation deadline expired or regressed")
    current()
    generated_bytes = _generated_inputs(plan, generated)
    current()
    objects, transferred = [], False
    with ExitStack() as stack:
        source = SourceDirectory(plan.input_root, plan.input_identity, current); stack.callback(source.close)
        parent = SourceDirectory(str(PureWindowsPath(plan.output_root).parent), plan.parent_identity, current); stack.callback(parent.close)
        def live():
            current(); source.check(); parent.check()
        live()
        _separate_roots(source, parent, plan.output_root)
        # Identity and the held parent authorize the actual relative creations;
        # canonical names support overlap refusal, not a DOS namespace lease.
        journal = _reserve_journal(plan.reservation, parent, live)
        stack.callback(journal.close)
        def append(value):
            raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
            if len(raw) > 4 * 1024 * 1024 or journal.write(raw) != len(raw):
                raise Refused("bounded durable image journal write required")
            os.fsync(journal.fileno())
        append({"schema": "aide.host.image-intent.v1", "generation": plan.generation,
                "plan_sha256": plan.fingerprint, "output_root": plan.output_root, "cleanup": "retain_only"})
        try:
            live()
            root = _create_image_root(plan.output_root, plan.user_sid, guard=live, parent=parent); objects.append(root)
            directories = {(): root}
            for entry in plan.files:
                live(); parts = relative_path(entry.path)
                for i in range(1, len(parts)):
                    prefix = parts[:i]
                    if prefix not in directories:
                        obj = directories[prefix[:-1]].child(prefix[-1], directory=True)
                        directories[prefix] = obj; objects.append(obj)
                obj = directories[parts[:-1]].child(parts[-1]); objects.append(obj)
                stream = (_generated_chunks(generated_bytes[entry.path]) if isinstance(entry, GeneratedImageFile)
                          else source.chunks(entry))
                with closing(stream) as chunks:
                    obj.write_stream(chunks, size=entry.size, sha256=entry.sha256,
                                     limit=plan.limits.file_bytes, deadline=deadline, clock=clock)
            for obj in reversed(objects): obj.seal()
            # Package access begins only once every byte copy completed.
            for obj in objects: obj.grant(plan.package_sid, mode="read")
            observations = tuple(obj.observe() for obj in objects)
            live()
            append({"phase": "prepared_bytes", "plan_sha256": plan.fingerprint,
                    "objects": observations, "tool_runtime_qualified": False, "cleanup": "retain_only"})
            # The durable flush and final observations also consume the deadline.
            live()
            result = PreparedImage(plan, tuple(objects), observations)
            result.check()
            journal.close()
            live()
            preparing = False
            result.leases = stack.pop_all()
            transferred = True
            return result
        except Exception:
            # A failure record is best effort only. The durable initial intent
            # already makes unknown/interrupted preparation ineligible to replay.
            try: append({"phase": "failed_or_uncertain", "cleanup": "retain_only"})
            except Exception: pass
            raise
        finally:
            if not transferred:
                for obj in reversed(objects): obj.close()
