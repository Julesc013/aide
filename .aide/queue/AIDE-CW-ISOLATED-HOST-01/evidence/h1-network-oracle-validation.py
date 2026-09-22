"""Exercise the exact native connect oracle on owned ordinary-process loopback sockets."""
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import time
import unittest

IMAGE = None
EXPECTED = None


class NativeNetworkOracleTests(unittest.TestCase):
    def invoke(self, port):
        self.assertEqual(hashlib.sha256(IMAGE.read_bytes()).hexdigest(), EXPECTED)
        started = time.monotonic()
        result = subprocess.run([str(IMAGE), "127.0.0.1", str(port)], capture_output=True, timeout=7)
        self.assertLess(time.monotonic() - started, 6.5)
        self.assertEqual(result.stderr, b"")
        self.assertLess(len(result.stdout), 256)
        value = json.loads(result.stdout)
        self.assertEqual(set(value), {"network_error", "diagnostic_status", "missing_capability"})
        self.assertIs(type(value["diagnostic_status"]), int)
        self.assertIs(type(value["missing_capability"]), int)
        self.assertEqual(value["diagnostic_status"], 0)
        self.assertEqual(value["missing_capability"], 0)
        self.assertIs(type(value["network_error"]), int)
        return result.returncode, value["network_error"]

    def test_noncanonical_or_nonliteral_address_refuses_before_connect(self):
        for address in ("localhost", "127.1", "127.000.0.1", "127.0.0.1 ", "::1", "300.1.2.3"):
            with self.subTest(address=address):
                self.assertEqual(hashlib.sha256(IMAGE.read_bytes()).hexdigest(), EXPECTED)
                result = subprocess.run([str(IMAGE), address, "9"], capture_output=True, timeout=1)
                self.assertEqual((result.returncode, result.stdout, result.stderr), (70, b"", b""))

    def test_connect_completion_is_success_only_with_actual_owned_listener_accept(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            listener.settimeout(1)
            self.assertEqual(self.invoke(listener.getsockname()[1]), (0, 0))
            peer, address = listener.accept()
            peer.close()
            self.assertEqual(address[0], "127.0.0.1")

    def test_completed_connection_refusal_is_not_misreported_as_access_denial(self):
        with socket.socket() as reserved:
            # Keep the port bound by this test, without listen, so no foreign
            # process can turn the intended refusal into an unrelated service.
            reserved.bind(("127.0.0.1", 0))
            self.assertEqual(self.invoke(reserved.getsockname()[1]), (74, 10061))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: h1-network-oracle-validation.py <exact-native-image> <sha256>")
    IMAGE, EXPECTED = Path(sys.argv[1]), sys.argv[2]
    unittest.main(argv=[sys.argv[0]], verbosity=2)
