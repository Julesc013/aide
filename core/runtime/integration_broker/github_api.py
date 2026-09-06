"""Bounded GitHub REST reads; the injected reader owns TLS/auth and no redirects."""
from dataclasses import dataclass
import math
import re
import time
from urllib.parse import urlencode, urlsplit, parse_qsl, unquote

from .common import Refused, parse_json

ORIGIN = "https://api.github.com"
VERSION = "2026-03-10"
MAX_BODY = 1024 * 1024
ABSENT = object()


def object_value(value):
    if not isinstance(value, dict):
        raise Refused("GitHub object required")
    return value


def positive(value):
    if type(value) is not int or not 1 <= value <= 2**63 - 1:
        raise Refused("GitHub positive integer identity required")
    return value


def text_value(value, maximum=240):
    if (not isinstance(value, str) or not 1 <= len(value) <= maximum or
            any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise Refused("GitHub bounded text required")
    return value


def repository_name(value):
    value = text_value(value)
    if (not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value) or
            any(part in (".", "..") for part in value.split("/"))):
        raise Refused("GitHub repository path refused")
    return value


def safe_json(raw):
    try:
        value = parse_json(raw)
        remaining = 50000
        def visit(item, depth):
            nonlocal remaining
            remaining -= 1
            if remaining < 0 or depth > 32:
                raise Refused("GitHub JSON structural budget exceeded")
            if isinstance(item, float) and not math.isfinite(item):
                raise Refused("GitHub non-finite JSON refused")
            children = item.values() if isinstance(item, dict) else item if isinstance(item, list) else ()
            for child in children:
                visit(child, depth + 1)
        visit(value, 0)
        return value
    except RecursionError as error:
        raise Refused("GitHub JSON nesting refused") from error


@dataclass(frozen=True)
class Response:
    url: str
    status: int
    headers: tuple
    body: bytes


class Reads:
    """One observation's finite GET budget, consumed before each reader call.

    read(url, headers=..., timeout=..., max_bytes=...) must return a Response,
    bound response allocation while streaming, authenticate api.github.com and
    never redirect or retry. Fixture readers cannot prove those host guarantees.
    The registered parent bridge separately bounds/kills the complete child.
    """
    def __init__(self, repository, read, *, deadline, now=time.time, monotonic=time.monotonic, max_calls=96, max_bytes=8 * MAX_BODY):
        self.repository = repository_name(repository)
        self.prefix = "/repos/" + self.repository
        if (type(deadline) not in (int, float) or not math.isfinite(deadline) or
                type(max_calls) is not int or not 1 <= max_calls <= 96 or
                type(max_bytes) is not int or not 1 <= max_bytes <= 8 * MAX_BODY or not callable(read)):
            raise Refused("GitHub read bounds required")
        current = now()
        if type(current) not in (int, float) or not math.isfinite(current) or not 0 < deadline - current <= 120:
            raise Refused("GitHub observation needs a fresh deadline within 120 seconds")
        self.monotonic, self.started = monotonic, monotonic()
        self.read, self.deadline, self.now = read, deadline, now
        self.max_calls, self.max_bytes = max_calls, max_bytes
        self.calls, self.bytes = 0, 0

    def _request(self, path, *, missing=False):
        if (not isinstance(path, str) or len(path) > 2048 or
                (path != "/user" and path != self.prefix and not path.startswith(self.prefix + "/")) or
                any(c in path for c in ("\\", "#", "\r", "\n")) or "/../" in path):
            raise Refused("GitHub endpoint outside admitted repository")
        decoded_path = unquote(path.split("?", 1)[0])
        if (any(part in (".", "..", "") for part in decoded_path[1:].split("/")) or
                any(ord(c) < 32 or c in "\\\\:#?" for c in decoded_path)):
            raise Refused("GitHub encoded endpoint path refused")
        current, elapsed = self.now(), self.monotonic() - self.started
        if (type(current) not in (int, float) or not math.isfinite(current) or current >= self.deadline or
                not math.isfinite(elapsed) or not 0 <= elapsed < 120):
            raise Refused("GitHub observation deadline expired")
        available = min(MAX_BODY, self.max_bytes - self.bytes)
        if self.calls >= self.max_calls or available <= 0:
            raise Refused("GitHub read budget exhausted")
        self.calls += 1
        url = ORIGIN + path
        response = self.read(url, headers={"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": VERSION},
                             timeout=min(10, self.deadline - current, 120 - elapsed), max_bytes=available)
        if (not isinstance(response, Response) or response.url != url or type(response.status) is not int or
                not isinstance(response.body, bytes) or len(response.body) > available or
                not isinstance(response.headers, tuple) or len(response.headers) > 64):
            raise Refused("GitHub response identity or byte budget refused")
        self.bytes += len(response.body)
        current, elapsed = self.now(), self.monotonic() - self.started
        if (type(current) not in (int, float) or not math.isfinite(current) or current >= self.deadline or
                not math.isfinite(elapsed) or not 0 <= elapsed < 120):
            raise Refused("GitHub response arrived after deadline")
        headers = {}
        for pair in response.headers:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise Refused("GitHub header shape refused")
            name, value = pair
            name = text_value(name, 80).lower()
            if name in headers:
                raise Refused("GitHub duplicate header refused")
            headers[name] = text_value(value, 8192)
        if response.status == 404 and missing:
            return ABSENT, headers
        if response.status != 200 or headers.get("content-type", "").split(";", 1)[0].strip() != "application/json":
            raise Refused("GitHub read failed; no retry or inferred absence")
        return safe_json(response.body), headers

    def get(self, path, *, missing=False):
        value, headers = self._request(path, missing=missing)
        if "link" in headers:
            raise Refused("unexpected pagination on GitHub object endpoint")
        return None if value is ABSENT else object_value(value)

    def pages(self, path, key, *, query=None, maximum=128):
        if type(maximum) is not int or not 1 <= maximum <= 128:
            raise Refused("GitHub collection bound refused")
        query = dict(query or {})
        if set(query) & {"page", "per_page"}:
            raise Refused("GitHub pagination is reader-owned")
        result, total, identities = [], None, set()
        # Two pages cover the frozen 128-record ceiling; no unbounded Link loop.
        for page in (1, 2):
            suffix = urlencode({**query, "per_page": 100, "page": page})
            value, headers = self._request(path + "?" + suffix)
            if key is None:
                items = value
            else:
                value = object_value(value)
                count = value.get("total_count")
                if type(count) is not int or not 0 <= count <= maximum or (total is not None and count != total):
                    raise Refused("GitHub total count changed or exceeds budget")
                total, items = count, value.get(key)
            if not isinstance(items, list) or len(items) > 100 or len(result) + len(items) > maximum:
                raise Refused("GitHub page exceeds collection budget")
            for item in items:
                item = object_value(item)
                number = positive(item.get("id"))
                if number in identities:
                    raise Refused("GitHub duplicate record across pages")
                identities.add(number)
            result.extend(items)
            links = {}
            for entry in headers.get("link", "").split(","):
                if not entry:
                    continue
                match = re.fullmatch(r'\s*<([^<>]+)>; rel="(next|prev|first|last)"\s*', entry)
                if not match or match[2] in links:
                    raise Refused("GitHub pagination Link refused")
                link = urlsplit(match[1])
                pairs = parse_qsl(link.query, keep_blank_values=True)
                parameters = dict(pairs)
                number = parameters.pop("page", "")
                if (link.scheme != "https" or link.netloc != "api.github.com" or link.path != path or
                        link.fragment or len(pairs) != len(dict(pairs)) or number not in ("1", "2") or
                        parameters != {**{k: str(v) for k, v in query.items()}, "per_page": "100"}):
                    raise Refused("GitHub pagination Link endpoint or parameters refused")
                links[match[2]] = int(number)
            if "next" not in links:
                if total is not None and len(result) != total:
                    raise Refused("GitHub collection is truncated")
                if key is None and len(items) == 100:
                    raise Refused("GitHub list completeness is ambiguous")
                return result
            if links["next"] != page + 1 or len(items) != 100 or page == 2:
                raise Refused("GitHub pagination next path or budget refused")
        raise Refused("GitHub pagination incomplete")
