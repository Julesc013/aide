"""Finite AMD64 PE dependency metadata reader; never loads or executes an image.

The supported subset refuses bound imports and non-RVA delay descriptors. Parsed
metadata is not loader qualification; exact bytes and system bindings stay required.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
import re
import struct

from .state import Refused

MAX_PE_BYTES = 16 * 1024 * 1024
MAX_IMAGE_BYTES = 512 * 1024 * 1024
MAX_IMPORTS = 2048
MAX_EXPORTS = 16384
MAX_DELAY_SYMBOLS = 16384


def dll_name(value):
    if (not isinstance(value, str) or not 5 <= len(value) <= 259 or
            not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*\.dll", value, re.IGNORECASE) or
            value.split(".", 1)[0].upper() in {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}):
        raise Refused("literal bounded non-device DLL basename required")
    return value.lower()


@dataclass(frozen=True, order=True)
class Forwarder:
    module: str
    symbol: str


@dataclass(frozen=True)
class PeInfo:
    sha256: str
    machine: str
    is_dll: bool
    imports: tuple[str, ...]
    delay_imports: tuple[str, ...]
    forwarders: tuple[Forwarder, ...]

    @property
    def dependencies(self):
        return tuple(sorted(set(self.imports) | set(self.delay_imports) | {row.module for row in self.forwarders}))


class _Reader:
    def __init__(self, data):
        if type(data) is not bytes or not 64 <= len(data) <= MAX_PE_BYTES or data[:2] != b"MZ":
            raise Refused("bounded immutable PE bytes required")
        self.data = data
        pe = self.unpack("<I", 60)[0]
        if pe < 64 or self.slice(pe, 4) != b"PE\0\0":
            raise Refused("valid bounded PE header required")
        machine, count = self.unpack("<HH", pe + 4)
        optional_size, characteristics = self.unpack("<HH", pe + 20)
        if machine != 0x8664 or not 1 <= count <= 96 or not characteristics & 2:
            raise Refused("bounded executable AMD64 image required")
        self.is_dll = bool(characteristics & 0x2000)
        optional = pe + 24
        if not 112 <= optional_size <= 240 or (optional_size - 112) % 8 or self.unpack("<H", optional)[0] != 0x20b:
            raise Refused("supported PE32+ optional header required")
        self.slice(optional, optional_size)
        image_size, headers = self.unpack("<II", optional + 56)
        directory_count = self.unpack("<I", optional + 108)[0]
        table_end = optional + optional_size + count * 40
        if (not table_end <= headers <= len(data) or not headers < image_size <= MAX_IMAGE_BYTES or
                directory_count > 16 or 112 + 8 * directory_count > optional_size):
            raise Refused("bounded image/header/directory extents required")
        self.headers, self.image_size = headers, image_size
        self.directories = tuple(self.unpack("<II", optional + 112 + i * 8) for i in range(directory_count))
        self.sections = []
        raw_ranges, virtual_ranges = [], []
        for i in range(count):
            virtual, address, raw, pointer = self.unpack("<IIII", optional + optional_size + i * 40 + 8)
            extent = max(virtual, raw)
            if not extent or address < headers or address + extent > image_size:
                raise Refused("bounded non-header section RVA required")
            if any(address < end and start < address + extent for start, end in virtual_ranges):
                raise Refused("overlapping virtual sections refused")
            virtual_ranges.append((address, address + extent))
            if raw:
                if pointer < headers or pointer + raw > len(data):
                    raise Refused("bounded non-header raw section required")
                if any(pointer < end and start < pointer + raw for start, end in raw_ranges):
                    raise Refused("overlapping raw sections refused")
                raw_ranges.append((pointer, pointer + raw))
            self.sections.append((address, raw, pointer))
        self.virtual_sections = tuple(virtual_ranges)
        self.delay_symbols = 0

    def slice(self, offset, size):
        if not 0 <= offset <= len(self.data) or not 0 <= size <= len(self.data) - offset:
            raise Refused("PE field escapes immutable file bytes")
        return self.data[offset:offset + size]

    def unpack(self, pattern, offset):
        return struct.unpack(pattern, self.slice(offset, struct.calcsize(pattern)))

    def offset(self, rva, size):
        if not 0 <= rva < self.image_size or not 0 < size <= self.image_size - rva:
            raise Refused("bounded nonempty RVA extent required")
        matches = ([rva] if rva + size <= self.headers else [])
        matches += [pointer + rva - address for address, raw, pointer in self.sections
                    if address <= rva and rva - address + size <= raw]
        if len(matches) != 1:
            raise Refused("RVA is not uniquely mapped to file bytes")
        self.slice(matches[0], size)
        return matches[0]

    def image_bytes(self, rva, size):
        """Bounded initial mapped bytes, including a section's zero-filled tail.

        Only IAT/handle metadata uses this view. Descriptors, names and lookup
        entries must stay file-backed; no virtual address is dereferenced.
        """
        if not 0 <= rva < self.image_size or not 0 < size <= min(self.image_size - rva, (MAX_DELAY_SYMBOLS + 1) * 8):
            raise Refused("bounded mapped table extent required")
        if rva + size <= self.headers: return self.slice(rva, size)
        matches = [i for i, (start, end) in enumerate(self.virtual_sections) if start <= rva and rva + size <= end]
        if len(matches) != 1: raise Refused("mapped table crosses a gap or section extent")
        address, raw, pointer = self.sections[matches[0]]
        backed = min(size, max(0, raw - (rva - address)))
        prefix = self.slice(pointer + rva - address, backed) if backed else b""
        return prefix + b"\0" * (size - backed)

    def delay_descriptor(self, row):
        if row[0] != 1 or row[7]:
            raise Refused("only unbound RVA delay imports are admitted")
        if not row[3] or not row[4]:
            raise Refused("explicit delay IAT and file-backed lookup required")
        count = 0
        while True:
            slot = self.unpack("<Q", self.offset(row[4] + count * 8, 8))[0]
            if not slot: break
            if self.delay_symbols >= MAX_DELAY_SYMBOLS:
                raise Refused("aggregate delay-symbol bound exceeded")
            self.delay_symbols += 1; count += 1
            if slot & (1 << 63):
                if (slot & ((1 << 63) - 1)) > 0xffff:
                    raise Refused("delay ordinal has reserved bits")
            else:
                if slot > 0xffffffff: raise Refused("delay name RVA exceeds supported width")
                self.offset(slot, 2)
                self.string(slot + 2, bound=512)
        length = (count + 1) * 8
        iat = self.image_bytes(row[3], length)
        if iat[-8:] != b"\0" * 8: raise Refused("delay IAT lacks its bounded terminator")
        if row[2]: self.image_bytes(row[2], 8)
        if row[5]:
            # Timestamp0 leaves this optional table unused. Validate its complete
            # initialized extent, but never follow its raw function addresses.
            bound = self.slice(self.offset(row[5], length), length)
            if bound[-8:] != b"\0" * 8: raise Refused("optional delay table lacks its terminator")
        if row[6]:
            unload = self.slice(self.offset(row[6], length), length)
            if unload != iat: raise Refused("delay unload table differs from the original IAT")
        return row[1]

    def directory(self, index):
        rva, size = self.directories[index] if index < len(self.directories) else (0, 0)
        if bool(rva) != bool(size):
            raise Refused("incomplete PE directory extent")
        if rva: self.offset(rva, size)
        return rva, size

    def string(self, rva, *, bound=260, enclosing=None):
        offset = self.offset(rva, 1)
        ends = ([self.headers] if rva < self.headers else [])
        ends += [address + raw for address, raw, _ in self.sections if address <= rva < address + raw]
        if len(ends) != 1: raise Refused("name has no unique bounded file span")
        limit = min(bound, ends[0] - rva)
        if enclosing is not None:
            if not enclosing[0] <= rva < enclosing[1]: raise Refused("forwarder escapes export directory")
            limit = min(limit, enclosing[1] - rva)
        end = self.data.find(b"\0", offset, offset + limit)
        if end <= offset: raise Refused("empty, unterminated or oversized PE name")
        value = self.data[offset:end]
        if not re.fullmatch(rb"[\x21-\x7e]+", value): raise Refused("literal printable ASCII PE name required")
        return value.decode("ascii")

    def imports(self, *, delayed=False):
        index, width = (13, 32) if delayed else (1, 20)
        rva, size = self.directory(index)
        if not rva: return ()
        if size < width or size > width * (MAX_IMPORTS + 1):
            raise Refused("bounded import descriptor table required")
        names = set()
        for i in range(min(size // width, MAX_IMPORTS + 1)):
            row = self.unpack("<" + "I" * (width // 4), self.offset(rva + i * width, width))
            if not any(row): return tuple(sorted(names))
            if i == MAX_IMPORTS: raise Refused("import count exceeds bound")
            if delayed:
                name_rva = self.delay_descriptor(row)
            else:
                if row[1]: raise Refused("bound import timestamps refused")
                name_rva, thunk = row[3], row[4]
                if row[0]: self.offset(row[0], 8)
                if not thunk: raise Refused("nonempty import address table required")
                self.offset(thunk, 8)
            name = dll_name(self.string(name_rva))
            if name in names: raise Refused("duplicate or case-aliased import descriptor")
            names.add(name)
        raise Refused("import table has no bounded terminator")

    def forwarders(self):
        rva, size = self.directory(0)
        if not rva: return ()
        if size < 40: raise Refused("complete export header required")
        row = self.unpack("<IIHHIIIIIII", self.offset(rva, 40))
        count, names, functions, name_table, ordinals = row[6:11]
        if count > MAX_EXPORTS or names > count:
            raise Refused("bounded export counts required")
        if names:
            self.offset(name_table, names * 4); self.offset(ordinals, names * 2)
            for i in range(names):
                name_rva = self.unpack("<I", self.offset(name_table + i * 4, 4))[0]
                self.string(name_rva, bound=512)
                ordinal = self.unpack("<H", self.offset(ordinals + i * 2, 2))[0]
                if ordinal >= count: raise Refused("export ordinal escapes function table")
        if count: self.offset(functions, count * 4)
        result = set()
        for i in range(count):
            target = self.unpack("<I", self.offset(functions + i * 4, 4))[0]
            if target >= self.image_size: raise Refused("export target escapes image")
            if rva <= target < rva + size:
                value = self.string(target, enclosing=(rva, rva + size))
                if value.count(".") != 1: raise Refused("one literal DLL/export forwarder separator required")
                module, symbol = value.split(".")
                if not re.fullmatch(r"(?:[A-Za-z_?$@][A-Za-z0-9_?$@]*|#[1-9][0-9]{0,9})", symbol):
                    raise Refused("bounded literal forwarder symbol required")
                result.add(Forwarder(dll_name(module + ".dll"), symbol))
        return tuple(sorted(result))


def read_pe(data):
    """Read a deliberately bounded PE subset; no filesystem, loader or callbacks."""
    reader = _Reader(data)
    if reader.directory(11) != (0, 0):
        raise Refused("bound import directory is outside this reader's admitted subset")
    return PeInfo(hashlib.sha256(data).hexdigest(), "amd64", reader.is_dll,
                  reader.imports(), reader.imports(delayed=True), reader.forwarders())
