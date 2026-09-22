"""Fixed-origin HTTPS observations; protected host/credential installation absent.

Only trusted controller code may supply host.assert_current(plan, "observe")
and host.credential(plan, "observe"), a context manager yielding Credential.
Both are bounded local operations. No configuration or worker input constructs
that host. The containing registered child remains the final process/time bound.
"""
from contextlib import contextmanager
from dataclasses import dataclass, field
import math
import os
import queue
import re
import socket
import ssl
import threading
import time
from urllib.parse import unquote, urlsplit

from .common import Refused, canonical, parse_json
from .github_api import ORIGIN, VERSION, MAX_BODY, repository_name
from .github_http_framing import response
from .pr_observation import validate_plan


@dataclass(frozen=True)
class Credential:
    token: str = field(repr=False)
    expires_at: float


def _finite(value):
    return type(value) in (int, float) and math.isfinite(value)


class _Exchange:
    def __init__(self, client, timeout):
        self.client = client
        self.until = min(client.until, client.monotonic() + timeout)
        self.credential_expiry = None
        self.stopped, self.done = threading.Event(), threading.Event()
        self.lock, self.sockets = threading.Lock(), []

    def guard(self):
        now, tick = self.client.now(), self.client.monotonic()
        if (self.stopped.is_set() or not _finite(now) or not _finite(tick) or
                now >= self.client.deadline or not self.client.started <= tick < self.until or
                (self.credential_expiry is not None and now >= self.credential_expiry)):
            raise Refused("GitHub HTTPS observation lease expired or was revoked")
        if self.client.host is None:
            raise Refused("protected GitHub observation host is unavailable")
        self.client.host.assert_current(parse_json(self.client.plan_bytes), "observe")
        # A local qualification check can itself consume the remaining interval.
        now, tick = self.client.now(), self.client.monotonic()
        if (not _finite(now) or not _finite(tick) or now >= self.client.deadline or
                not self.client.started <= tick < self.until or
                (self.credential_expiry is not None and now >= self.credential_expiry)):
            raise Refused("GitHub HTTPS qualification exceeded its lease")

    def adopt(self, sock):
        with self.lock:
            self.sockets.append(sock)
            if self.stopped.is_set():
                sock.close()
        self.guard()

    def abort(self):
        self.stopped.set()
        with self.lock:
            for sock in self.sockets:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except (OSError, ValueError):
                    pass
                try:
                    sock.close()
                except OSError:
                    pass

    def monitor(self):
        while not self.done.wait(0.02):
            try:
                self.guard()
            except Exception:
                self.abort()
                return

    def remaining(self):
        self.guard()
        return max(0.001, self.until - self.client.monotonic())

    @contextmanager
    def watching(self):
        self.guard()
        monitor = threading.Thread(target=self.monitor, daemon=True)
        monitor.start()
        try:
            yield self
        finally:
            self.done.set()
            self.abort()
            monitor.join(0.1)


class GitHubHTTP:
    """Single-use observation lifetime, fixed GET origin and bounded wire budget.

    DNS runs in a daemon which can only report addresses, never connect or use
    credentials. A timed-out query cannot cause a later TCP request. Host hooks
    must be bounded and safe to call concurrently from the qualification monitor.
    The production constructor accepts no endpoint, resolver or trust override.
    """
    def __init__(self, plan, *, deadline, host=None, now=time.time, monotonic=time.monotonic):
        validate_plan(plan)
        repository_name(plan["repository"])
        self.plan_bytes = canonical(plan)
        self.prefix = "/repos/" + plan["repository"]
        self.host, self.now, self.monotonic = host, now, monotonic
        current, self.started = now(), monotonic()
        if (not _finite(deadline) or not _finite(current) or not _finite(self.started) or
                not 0 < deadline - current <= 120):
            raise Refused("GitHub HTTPS needs a fresh finite observation deadline")
        self.deadline, self.until = deadline, self.started + deadline - current
        self.calls, self.bytes = 0, 0
        self.lock = threading.Lock()

    def _context(self):
        if any(name in os.environ for name in ("SSL_CERT_FILE", "SSL_CERT_DIR", "SSLKEYLOGFILE")):
            raise Refused("GitHub TLS environment override refused")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_default_certs(ssl.Purpose.SERVER_AUTH)
        return context

    def _resolve(self):
        return socket.getaddrinfo("api.github.com", 443, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)

    def _connect(self, sock, address):
        sock.connect(address)

    def _address(self, exchange):
        result = queue.Queue(maxsize=1)
        def resolve():
            try:
                addresses = self._resolve()
                if not isinstance(addresses, list) or not 1 <= len(addresses) <= 32:
                    addresses = None
            except Exception:
                addresses = None
            result.put_nowait(addresses)
        threading.Thread(target=resolve, daemon=True).start()
        while True:
            exchange.guard()
            try:
                addresses = result.get(timeout=min(0.02, exchange.remaining()))
                break
            except queue.Empty:
                pass
        if not addresses:
            raise Refused("GitHub bounded DNS observation failed")
        family, kind, protocol, canonical_name, address = addresses[0]
        if (family not in (socket.AF_INET, socket.AF_INET6) or kind != socket.SOCK_STREAM or
                protocol != socket.IPPROTO_TCP or not isinstance(address, tuple) or
                len(address) != (2 if family == socket.AF_INET else 4) or address[1] != 443):
            raise Refused("GitHub resolver address refused")
        socket.inet_pton(family, address[0])
        return family, address

    def _request_path(self, url, headers):
        if (not isinstance(url, str) or len(url) > 2100 or not url.startswith(ORIGIN + "/") or
                any(ord(c) < 33 or ord(c) > 126 or c in "\\#" for c in url)):
            raise Refused("GitHub HTTPS origin or path refused")
        parsed = urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != "api.github.com" or parsed.fragment:
            raise Refused("GitHub HTTPS origin refused")
        path = parsed.path
        decoded = unquote(path)
        if ((path != "/user" and path != self.prefix and not path.startswith(self.prefix + "/")) or
                any(part in (".", "..", "") for part in decoded[1:].split("/")) or
                any(ord(c) < 32 or c in "\\:#?" for c in decoded)):
            raise Refused("GitHub HTTPS endpoint outside admitted repository")
        if headers != {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": VERSION}:
            raise Refused("GitHub HTTPS request headers must be transport-owned")
        return path + ("?" + parsed.query if parsed.query else "")

    def _account(self, count):
        self.bytes += count
        if self.bytes > 8 * MAX_BODY:
            raise Refused("GitHub HTTPS cumulative wire budget exhausted")

    def _exchange(self, url, path, timeout, maximum):
        with _Exchange(self, timeout).watching() as exchange:
            context = self._context()
            if (context.verify_mode != ssl.CERT_REQUIRED or context.check_hostname is not True or
                    context.minimum_version < ssl.TLSVersion.TLSv1_2 or context.keylog_filename is not None):
                raise Refused("GitHub HTTPS verified TLS policy required")
            exchange.guard()
            family, address = self._address(exchange)
            exchange.guard()
            raw = socket.socket(family, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            exchange.adopt(raw)
            raw.settimeout(exchange.remaining())
            self._connect(raw, address)
            exchange.guard()
            secured = context.wrap_socket(raw, server_hostname="api.github.com", do_handshake_on_connect=False)
            exchange.adopt(secured)
            secured.settimeout(exchange.remaining())
            exchange.guard()
            secured.do_handshake()
            exchange.guard()
            # No credential is acquired or sent before certificate/hostname proof.
            with self.host.credential(parse_json(self.plan_bytes), "observe") as credential:
                if (not isinstance(credential, Credential) or not isinstance(credential.token, str) or
                        not re.fullmatch(r"[A-Za-z0-9_]{16,512}", credential.token) or
                        not _finite(credential.expires_at) or not 0 < credential.expires_at - self.now() <= 3600):
                    raise Refused("GitHub protected credential lease refused")
                exchange.credential_expiry = credential.expires_at
                exchange.guard()
                request = ("GET " + path + " HTTP/1.1\r\nHost: api.github.com\r\n"
                    "Accept: application/vnd.github+json\r\nX-GitHub-Api-Version: " + VERSION + "\r\n"
                    "User-Agent: aide-integration-broker\r\nAccept-Encoding: identity\r\n"
                    "Connection: close\r\nAuthorization: Bearer " + credential.token + "\r\n\r\n")
                secured.settimeout(exchange.remaining())
                exchange.guard()
                secured.sendall(request.encode("ascii"))
                exchange.guard()
                value = response(secured, url, guard=exchange.guard, account=self._account,
                                 maximum=maximum, token=credential.token)
                exchange.guard()
            exchange.guard()
            return value

    def read(self, url, *, headers, timeout, max_bytes):
        if not self.lock.acquire(blocking=False):
            raise Refused("concurrent GitHub HTTPS use refused")
        failed, value = False, None
        try:
            # Account even invalid/refused attempts before any transport effect.
            self.calls += 1
            if (self.calls > 96 or self.bytes >= 8 * MAX_BODY or not _finite(timeout) or
                    not 0 < timeout <= 10 or type(max_bytes) is not int or not 1 <= max_bytes <= MAX_BODY):
                raise Refused("GitHub HTTPS request budget refused")
            path = self._request_path(url, headers)
            value = self._exchange(url, path, timeout, max_bytes)
        except Exception:
            failed = True
        finally:
            self.lock.release()
        # Raise outside the catch: no underlying response, TLS or host exception
        # becomes printable exception context containing reflected credentials.
        if failed:
            raise Refused("GitHub HTTPS exchange refused; no retry or inferred absence")
        return value
