"""Real disposable TLS denials; no live GitHub, real credentials or trust edits."""
from contextlib import contextmanager, redirect_stderr, redirect_stdout
import inspect
import io
import json
import os
from pathlib import Path
import secrets
import shutil
import socket
import ssl
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import unittest
from unittest.mock import patch
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from core.runtime.integration_broker.common import Refused
from core.runtime.integration_broker.github_api import Reads, ORIGIN, VERSION, MAX_BODY
from core.runtime.integration_broker.github_http import GitHubHTTP, Credential
from core.runtime.integration_broker.github_observation import collect
from core.runtime.integration_broker.pr_observation import decision
from test_continuous_worker_github_observation import Fixture, plan, REPO

HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": VERSION}


def packet(body=b'{"ok":true}', *, status=200, headers=()):
    pairs = [("Content-Type", "application/json"), ("Content-Length", str(len(body))), *headers]
    return (f"HTTP/1.1 {status} fixture\r\n" + "".join(k + ": " + v + "\r\n" for k, v in pairs) + "\r\n").encode() + body


class Host:
    def __init__(self):
        self.token = "synthetic_" + secrets.token_hex(24)
        self.revoked, self.leases, self.releases = False, 0, 0
        self.expiry = time.time() + 60
        self.on_lease = None

    def assert_current(self, admitted, operation):
        if admitted != plan() or operation != "observe" or self.revoked:
            raise Refused("synthetic authority refused")

    @contextmanager
    def credential(self, admitted, operation):
        self.assert_current(admitted, operation)
        self.leases += 1
        if self.on_lease:
            self.on_lease()
        try:
            yield Credential(self.token, self.expiry)
        finally:
            self.releases += 1


class Server:
    """Loopback server records only paths/counts, never request headers/tokens."""
    def __init__(self, cert, key, handler=None):
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.context.minimum_version = ssl.TLSVersion.TLSv1_2
        self.context.load_cert_chain(cert, key)
        self.handler = handler or (lambda path: packet())
        self.listener = socket.socket()
        self.listener.bind(("127.0.0.1", 0))
        self.listener.listen(16)
        self.listener.settimeout(0.05)
        self.port = self.listener.getsockname()[1]
        self.stopped, self.requested = threading.Event(), threading.Event()
        self.release, self.tls_ready = threading.Event(), threading.Event()
        self.requests, self.accepted, self.authorization_matches = [], 0, []
        self.expected_token = None
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        while not self.stopped.is_set():
            try:
                raw, _ = self.listener.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            self.accepted += 1
            try:
                raw.settimeout(1)
                with self.context.wrap_socket(raw, server_side=True) as peer:
                    self.tls_ready.set()
                    data = bytearray()
                    while not data.endswith(b"\r\n\r\n"):
                        part = peer.recv(4096)
                        if not part or len(data) + len(part) > 8192:
                            break
                        data.extend(part)
                    if not data.endswith(b"\r\n\r\n"):
                        continue
                    path = bytes(data).split(b" ", 2)[1].decode("ascii")
                    self.requests.append(path)
                    if self.expected_token:
                        self.authorization_matches.append(
                            b"Authorization: Bearer " + self.expected_token.encode() + b"\r\n" in data)
                    self.requested.set()
                    value = self.handler(path)
                    if isinstance(value, bytes):
                        peer.sendall(value)
                    elif value is not None:
                        for part in value:
                            peer.sendall(part)
            except (OSError, ValueError):
                pass
            finally:
                raw.close()

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.stopped.set()
        self.release.set()
        self.listener.close()
        self.thread.join(2)
        if self.thread.is_alive():
            raise AssertionError("owned TLS fixture did not stop")


class LocalHTTP(GitHubHTTP):
    """Fixture route exists only in tests; production constructor has no knobs."""
    def __init__(self, server, cert, host, **kwargs):
        self.server, self.cert, self.connections = server, cert, 0
        self.resolve_gate, self.resolve_done = None, threading.Event()
        super().__init__(plan(), deadline=time.time() + 60, host=host, **kwargs)

    def _context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_verify_locations(cafile=str(self.cert))
        return context

    def _resolve(self):
        if self.resolve_gate:
            self.resolve_gate.wait(2)
        self.resolve_done.set()
        return [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", ("127.0.0.1", 443))]

    def _connect(self, sock, address):
        self.connections += 1
        sock.connect((address[0], self.server.port))


class GitHubHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        executable = shutil.which("openssl") or r"C:\Program Files\Git\usr\bin\openssl.exe"
        if not Path(executable).is_file():
            raise RuntimeError("existing OpenSSL required for real TLS qualification; no silent skip")
        cls.temporary = tempfile.TemporaryDirectory(prefix="aide-broker-tls-")
        cls.root = Path(cls.temporary.name)
        cls.certificates = []
        for index, name in enumerate(("api.github.com", "wrong.invalid")):
            cert, key = cls.root / f"cert-{index}.pem", cls.root / f"key-{index}.pem"
            result = subprocess.run([executable, "req", "-x509", "-newkey", "rsa:2048", "-nodes",
                "-keyout", str(key), "-out", str(cert), "-days", "1", "-subj", "/CN=" + name,
                "-addext", "subjectAltName=DNS:" + name, "-addext", "basicConstraints=critical,CA:FALSE"],
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
            if result.returncode:
                raise RuntimeError("synthetic certificate generation failed")
            cls.certificates.append((cert, key))

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def call(self, reader, *, timeout=1, maximum=MAX_BODY, url=ORIGIN + "/user", headers=None):
        return reader.read(url, headers=HEADERS if headers is None else headers,
                           timeout=timeout, max_bytes=maximum)

    def test_real_tls_get_and_actual_raw_collector_preserve_unqualified_target(self):
        fixture, host = Fixture(), Host()
        def handler(path):
            result = fixture.read(ORIGIN + path, headers=HEADERS, timeout=1, max_bytes=MAX_BODY)
            return packet(result.body, status=result.status)
        with Server(*self.certificates[0], handler) as server:
            server.expected_token = host.token
            reader = LocalHTTP(server, self.certificates[0][0], host)
            api = Reads(REPO, reader.read, deadline=time.time() + 60)
            observed = collect(api, plan())
            self.assertEqual(decision(plan(), observed), "qualify_target")
            self.assertIsNone(observed["policy_digest"])
            self.assertGreater(len(server.requests), 12)
            self.assertEqual(reader.calls, len(server.requests))
            self.assertTrue(all(server.authorization_matches))
            self.assertEqual(host.leases, host.releases)

    def test_bad_trust_and_hostname_fail_before_credential_lease(self):
        for certificate, trusted in ((0, 1), (1, 1)):
            with self.subTest(certificate=certificate, trusted=trusted), Server(*self.certificates[certificate]) as server:
                host = Host()
                reader = LocalHTTP(server, self.certificates[trusted][0], host)
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual((host.leases, len(server.requests), reader.calls), (0, 0, 1))

    def test_absent_revoked_and_elapsed_authority_precede_tcp(self):
        for kind in ("absent", "revoked", "expired"):
            with self.subTest(kind=kind), Server(*self.certificates[0]) as server:
                host = Host()
                host.revoked = kind == "revoked"
                reader = LocalHTTP(server, self.certificates[0][0], None if kind == "absent" else host)
                if kind == "expired":
                    reader.now = lambda: reader.deadline + 1
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual((reader.connections, host.leases, reader.calls), (0, 0, 1))

    def test_expired_credential_and_revocation_at_lease_never_send_request(self):
        for kind in ("expired", "revoked"):
            with self.subTest(kind=kind), Server(*self.certificates[0]) as server:
                host = Host()
                if kind == "expired":
                    host.expiry = time.time() - 1
                else:
                    host.on_lease = lambda: setattr(host, "revoked", True)
                reader = LocalHTTP(server, self.certificates[0][0], host)
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual((host.leases, host.releases, len(server.requests)), (1, 1, 0))

    def test_qualification_rechecked_after_tls_before_credential(self):
        with Server(*self.certificates[0]) as server:
            host = Host()
            reader = LocalHTTP(server, self.certificates[0][0], host)
            original = reader._context
            def context():
                value = original()
                original_wrap = value.wrap_socket
                def wrap(*args, **kwargs):
                    secured = original_wrap(*args, **kwargs)
                    original_handshake = secured.do_handshake
                    def handshake(*args, **kwargs):
                        result = original_handshake(*args, **kwargs)
                        host.revoked = True
                        return result
                    secured.do_handshake = handshake
                    return secured
                value.wrap_socket = wrap
                return value
            reader._context = context
            with self.assertRaises(Refused):
                self.call(reader)
            self.assertEqual((host.leases, len(server.requests)), (0, 0))

    def test_redirect_and_error_status_never_retry_or_follow_location(self):
        for code in (301, 302, 307, 401, 403, 429, 500):
            with self.subTest(code=code), Server(*self.certificates[0], lambda _: packet(status=code,
                    headers=(("Location", "https://foreign.invalid/"),))) as server:
                reader = LocalHTTP(server, self.certificates[0][0], Host())
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual((reader.calls, reader.connections, len(server.requests)), (1, 1, 1))

    def test_environment_proxies_are_ignored_and_ca_keylog_overrides_refused(self):
        with Server(*self.certificates[0]) as server, patch.dict(os.environ, {
                "HTTPS_PROXY": "http://127.0.0.1:1", "HTTP_PROXY": "http://127.0.0.1:1",
                "ALL_PROXY": "http://127.0.0.1:1", "NO_PROXY": ""}):
            self.assertEqual(self.call(LocalHTTP(server, self.certificates[0][0], Host())).status, 200)
        for name in ("SSL_CERT_FILE", "SSL_CERT_DIR", "SSLKEYLOGFILE"):
            with self.subTest(name=name), patch.dict(os.environ, {name: str(self.root / "never-created")}):
                client = GitHubHTTP(plan(), deadline=time.time() + 60, host=Host())
                with patch.object(client, "_resolve", side_effect=AssertionError("DNS must not run")):
                    with self.assertRaises(Refused):
                        self.call(client)
                self.assertFalse((self.root / "never-created").exists())

    def test_fixed_origin_headers_and_path_refuse_before_connection(self):
        urls = ("http://api.github.com/user", "https://api.github.com:443/user",
                "https://api.github.com.evil.invalid/user", "https://api.github.com@evil.invalid/user",
                ORIGIN + "/repos/foreign/repo", ORIGIN + "/repos/fixture/repo/%2e%2e/user",
                ORIGIN + "/user#fragment", ORIGIN + "/user\r\nInjected:yes")
        with Server(*self.certificates[0]) as server:
            host = Host()
            reader = LocalHTTP(server, self.certificates[0][0], host)
            for url in urls:
                with self.subTest(url=url), self.assertRaises(Refused):
                    self.call(reader, url=url)
            with self.assertRaises(Refused):
                self.call(reader, headers={**HEADERS, "Authorization": "untrusted"})
            self.assertEqual((reader.connections, host.leases), (0, 0))
        self.assertEqual(set(inspect.signature(GitHubHTTP).parameters), {"plan", "deadline", "host", "now", "monotonic"})

    def test_actual_malformed_oversized_truncated_framing_refuses(self):
        malformed = (
            b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nContent-Length: 2\r\ncontent-length: 2\r\n\r\n{}",
            b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nContent-Length: 2\r\nTransfer-Encoding: chunked\r\n\r\n{}",
            b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\n\r\n{}",
            b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nContent-Length: 10\r\n\r\n{}",
            packet(headers=(("Content-Encoding", "gzip"),)),
            b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nContent-Length: 1048577\r\n\r\n",
            b"HTTP/1.1 200 ok\r\n" + b"X-Big: " + b"x" * 8192 + b"\r\n\r\n",
            b"HTTP/1.1 200 ok\r\n" + b"".join(f"X-{i}: a\r\n".encode() for i in range(65)) + b"\r\n",
            b"HTTP/1.1 200 ok\r\n" + b"".join(f"X-{i}: ".encode() + b"a" * 8000 + b"\r\n" for i in range(9)) + b"\r\n",
            b"HTTP/1.1 200 ok\nContent-Type: application/json\r\n\r\n",
        )
        for index, raw in enumerate(malformed):
            with self.subTest(index=index), Server(*self.certificates[0], lambda _, raw=raw: raw) as server:
                reader = LocalHTTP(server, self.certificates[0][0], Host())
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual(reader.connections, 1)

    def test_chunked_json_has_bounded_chunks_and_no_trailers(self):
        prefix = b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nTransfer-Encoding: chunked\r\n\r\n"
        for body, valid in ((b"1\r\n{\r\n1\r\n}\r\n0\r\n\r\n", True),
                            (b"1;extension=a\r\n{\r\n0\r\n\r\n", False),
                            (b"2\r\n{}XX0\r\n\r\n", False),
                            (b"2\r\n{}\r\n0\r\nX-Trailer: a\r\n\r\n", False),
                            (b"100001\r\n", False)):
            with self.subTest(valid=valid, size=len(body)), Server(*self.certificates[0], lambda _, body=body: prefix + body) as server:
                reader = LocalHTTP(server, self.certificates[0][0], Host())
                if valid:
                    self.assertEqual(self.call(reader).body, b"{}")
                else:
                    with self.assertRaises(Refused):
                        self.call(reader)

    def test_literal_json_escaped_and_header_secret_reflection_is_not_exposed(self):
        for kind in ("body", "escaped", "header", "exception"):
            with self.subTest(kind=kind):
                host, captured = Host(), io.StringIO()
                def handler(path):
                    if kind == "header":
                        return packet(headers=(("X-Reflection", host.token),))
                    body = json.dumps({"reflected": host.token}).encode()
                    if kind == "escaped":
                        body = b'{"reflected":"' + b"".join(f"\\u{ord(c):04x}".encode() for c in host.token) + b'"}'
                    return packet(body)
                with Server(*self.certificates[0], handler) as server:
                    reader = LocalHTTP(server, self.certificates[0][0], host)
                    if kind == "exception":
                        host.assert_current = lambda *args: (_ for _ in ()).throw(RuntimeError(host.token))
                    with redirect_stdout(captured), redirect_stderr(captured):
                        try:
                            self.call(reader)
                        except Refused as error:
                            self.assertIsNone(error.__context__)
                            captured.write("".join(traceback.format_exception(error)))
                        else:
                            self.fail("reflection was exposed")
                self.assertNotIn(host.token, captured.getvalue())
                self.assertNotIn("Authorization: Bearer", captured.getvalue())
                self.assertNotIn(host.token, repr(Credential(host.token, host.expiry)))

    def test_stalled_body_deadline_and_inflight_revocation_interrupt_owned_socket(self):
        for kind in ("deadline", "revoked", "credential_expiry"):
            with self.subTest(kind=kind), Server(*self.certificates[0]) as server:
                def handler(path):
                    yield b"HTTP/1.1 200 ok\r\nContent-Type: application/json\r\nContent-Length: 8\r\n\r\n{"
                    server.release.wait(1.5)
                server.handler = handler
                host = Host()
                reader = LocalHTTP(server, self.certificates[0][0], host)
                def revoke():
                    server.requested.wait(1)
                    time.sleep(0.05)
                    if kind == "revoked":
                        host.revoked = True
                    elif kind == "credential_expiry":
                        reader.now = lambda: host.expiry + 1
                helper = threading.Thread(target=revoke)
                helper.start()
                started = time.monotonic()
                with self.assertRaises(Refused):
                    self.call(reader, timeout=0.2 if kind == "deadline" else 1)
                elapsed = time.monotonic() - started
                server.release.set()
                helper.join(1)
                self.assertLess(elapsed, 0.7)
                self.assertEqual((reader.connections, host.leases, host.releases), (1, 1, 1))

    def test_timed_out_dns_cannot_connect_or_lease_after_late_result(self):
        with Server(*self.certificates[0]) as server:
            host = Host()
            reader = LocalHTTP(server, self.certificates[0][0], host)
            reader.resolve_gate = threading.Event()
            with self.assertRaises(Refused):
                self.call(reader, timeout=0.08)
            reader.resolve_gate.set()
            self.assertTrue(reader.resolve_done.wait(1))
            self.assertEqual((reader.connections, host.leases, server.accepted), (0, 0, 0))

    def test_qualification_rechecked_after_tcp_and_immediately_before_send(self):
        for boundary in ("connected", "credential_acquired"):
            with self.subTest(boundary=boundary), Server(*self.certificates[0]) as server:
                host = Host()
                reader = LocalHTTP(server, self.certificates[0][0], host)
                if boundary == "connected":
                    connect = reader._connect
                    def expired_connect(sock, address):
                        connect(sock, address)
                        reader.now = lambda: reader.deadline + 1
                    reader._connect = expired_connect
                else:
                    host.on_lease = lambda: setattr(reader, "now", lambda: reader.deadline + 1)
                with self.assertRaises(Refused):
                    self.call(reader)
                self.assertEqual(len(server.requests), 0)
                self.assertEqual(host.leases, 0 if boundary == "connected" else 1)

    def test_actual_stalled_tls_handshake_is_interrupted_before_credential(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            listener.settimeout(1)
            accepted, release = threading.Event(), threading.Event()
            def accept():
                with listener.accept()[0] as peer:
                    accepted.set()
                    release.wait(1)
            helper = threading.Thread(target=accept)
            helper.start()
            class Address:
                port = listener.getsockname()[1]
            host = Host()
            reader = LocalHTTP(Address(), self.certificates[0][0], host)
            started = time.monotonic()
            try:
                with self.assertRaises(Refused):
                    self.call(reader, timeout=0.15)
                self.assertTrue(accepted.is_set())
                self.assertLess(time.monotonic() - started, 0.6)
                self.assertEqual(host.leases, 0)
            finally:
                release.set()
                helper.join(1)

    def test_slow_header_drip_cannot_extend_absolute_deadline(self):
        with Server(*self.certificates[0]) as server:
            def drip(path):
                for part in (b"HTTP/1.1 200 ok\r\n", b"X-Slow: ", b"a", b"b", b"c"):
                    yield part
                    if server.release.wait(0.05):
                        return
            server.handler = drip
            reader = LocalHTTP(server, self.certificates[0][0], Host())
            started = time.monotonic()
            with self.assertRaises(Refused):
                self.call(reader, timeout=0.16)
            server.release.set()
            self.assertLess(time.monotonic() - started, 0.6)
            self.assertEqual(len(server.requests), 1)

    def test_production_context_verifies_tls_and_rejects_even_empty_overrides(self):
        names = ("SSL_CERT_FILE", "SSL_CERT_DIR", "SSLKEYLOGFILE")
        with patch.dict(os.environ, {k: v for k, v in os.environ.items() if k not in names}, clear=True):
            context = GitHubHTTP(plan(), deadline=time.time() + 60, host=Host())._context()
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)
            self.assertTrue(context.check_hostname)
            self.assertGreaterEqual(context.minimum_version, ssl.TLSVersion.TLSv1_2)
            self.assertIsNone(context.keylog_filename)
        for name in names:
            with self.subTest(name=name), patch.dict(os.environ, {name: ""}):
                client = GitHubHTTP(plan(), deadline=time.time() + 60, host=Host())
                with self.assertRaises(Refused):
                    self.call(client)

    def test_reader_rejects_concurrent_dispatch_and_exhausted_attempts(self):
        with Server(*self.certificates[0]) as server:
            reader = LocalHTTP(server, self.certificates[0][0], Host())
            reader.lock.acquire()
            try:
                with self.assertRaises(Refused):
                    self.call(reader)
            finally:
                reader.lock.release()
            reader.calls = 96
            with self.assertRaises(Refused):
                self.call(reader)
            self.assertEqual(reader.connections, 0)

    def test_wire_budget_counts_failed_responses_and_body_limit_precedes_body(self):
        with Server(*self.certificates[0], lambda _: packet(b" " * 200)) as server:
            reader = LocalHTTP(server, self.certificates[0][0], Host())
            with self.assertRaises(Refused):
                self.call(reader, maximum=100)
            self.assertGreater(reader.bytes, 0)
            reader.bytes = 8 * MAX_BODY
            with self.assertRaises(Refused):
                self.call(reader)
            self.assertEqual(reader.connections, 1)


if __name__ == "__main__":
    unittest.main()
