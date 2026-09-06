"""Finite HTTP/1.1 framing for authenticated, single-exchange GitHub reads."""
import re

from .common import Refused
from .github_api import Response, safe_json

MAX_HEADERS = 64 * 1024
MAX_LINE = 8192


class Wire:
    def __init__(self, sock, guard, account):
        self.sock, self.guard, self.account = sock, guard, account
        self.buffer = bytearray()

    def receive(self):
        self.guard()
        part = self.sock.recv(8192)
        self.guard()
        self.account(len(part))
        if not part:
            raise Refused("GitHub response was truncated")
        self.buffer.extend(part)

    def line(self, maximum=MAX_LINE):
        while True:
            at = self.buffer.find(b"\r\n")
            if at >= 0:
                if at + 2 > maximum:
                    raise Refused("GitHub response line exceeds budget")
                value = bytes(self.buffer[:at])
                del self.buffer[:at + 2]
                if b"\r" in value or b"\n" in value:
                    raise Refused("GitHub response line ending refused")
                return value
            if len(self.buffer) >= maximum:
                raise Refused("GitHub response line exceeds budget")
            self.receive()

    def exact(self, count):
        result = bytearray()
        while len(result) < count:
            if not self.buffer:
                self.receive()
            size = min(count - len(result), len(self.buffer))
            result.extend(self.buffer[:size])
            del self.buffer[:size]
        return bytes(result)


def _headers(wire):
    status = wire.line()
    if not re.fullmatch(rb"HTTP/1\.1 [0-9]{3} [\x20-\x7e]{0,100}", status):
        raise Refused("GitHub HTTP status line refused")
    code = int(status[9:12])
    if code not in (200, 404):
        raise Refused("GitHub HTTP request failed; no redirect or retry")
    consumed, headers, seen = len(status) + 2, [], set()
    while True:
        line = wire.line(min(MAX_LINE, MAX_HEADERS - consumed))
        consumed += len(line) + 2
        if not line:
            return code, tuple(headers), dict((k.lower(), v) for k, v in headers)
        if len(headers) >= 64 or b":" not in line:
            raise Refused("GitHub response header count or syntax refused")
        name, value = line.split(b":", 1)
        if (not re.fullmatch(rb"[!#$%&'*+.^_`|~0-9A-Za-z-]{1,80}", name) or
                any(c < 32 or c > 126 for c in value) or name.lower() in seen):
            raise Refused("GitHub response header is invalid or duplicated")
        seen.add(name.lower())
        headers.append((name.decode("ascii"), value.decode("ascii").strip(" ")))


def _body(wire, headers, maximum):
    length, transfer = headers.get("content-length"), headers.get("transfer-encoding")
    if headers.get("content-encoding", "identity") != "identity" or (length is not None and transfer is not None):
        raise Refused("GitHub response encoding or conflicting framing refused")
    if length is not None:
        if not re.fullmatch(r"0|[1-9][0-9]{0,9}", length) or int(length) > maximum:
            raise Refused("GitHub Content-Length exceeds budget or is invalid")
        return wire.exact(int(length))
    if transfer != "chunked":
        raise Refused("GitHub response needs explicit bounded framing")
    result = bytearray()
    # Bound even zero-sized data chunks / chunk overhead independently of bytes.
    for _ in range(4096):
        size = wire.line(32)
        if not re.fullmatch(rb"[0-9A-Fa-f]{1,8}", size):
            raise Refused("GitHub chunk framing refused")
        count = int(size, 16)
        if count == 0:
            if wire.line(2):
                raise Refused("GitHub chunk trailers refused")
            return bytes(result)
        if len(result) + count > maximum:
            raise Refused("GitHub chunked body exceeds budget")
        result.extend(wire.exact(count))
        if wire.exact(2) != b"\r\n":
            raise Refused("GitHub chunk terminator refused")
    raise Refused("GitHub chunk count exceeds budget")


def response(sock, url, *, guard, account, maximum, token):
    wire = Wire(sock, guard, account)
    code, pairs, headers = _headers(wire)
    if headers.get("content-type", "").split(";", 1)[0].strip() != "application/json":
        raise Refused("GitHub response media type refused")
    if any(token in value or token in key for key, value in pairs):
        raise Refused("GitHub credential reflection refused")
    body = _body(wire, headers, maximum)
    if wire.buffer:
        raise Refused("GitHub response contains bytes beyond declared framing")
    if token.encode("ascii") in body:
        raise Refused("GitHub credential reflection refused")
    # Also reject JSON-escaped reflection before Reads exposes decoded strings.
    value = safe_json(body)
    def inspect(item):
        if isinstance(item, str) and token in item:
            raise Refused("GitHub credential reflection refused")
        if isinstance(item, dict):
            for key, child in item.items():
                inspect(key)
                inspect(child)
        elif isinstance(item, list):
            for child in item:
                inspect(child)
    inspect(value)
    guard()
    return Response(url, code, pairs, body)
