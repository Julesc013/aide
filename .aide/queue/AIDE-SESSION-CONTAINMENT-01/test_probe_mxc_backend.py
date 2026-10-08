"""Refusal classification regression; no subprocess, host setup or model."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('mxc_probe_classification', Path(__file__).with_name('probe_mxc_backend.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class NativeRefusalClassification(unittest.TestCase):
    def test_observed_early_preparation_refusal(self):
        self.assertTrue(probe.native_mxc_unavailable(1, 'Error: failed to prepare MXC sandbox: native MXC is unavailable on this executor\n'))

    def test_later_native_refusals(self):
        for message in ('native MXC is unavailable on this Windows build',
                        'this Windows build cannot enforce native MXC deny paths'):
            with self.subTest(message=message):
                self.assertTrue(probe.native_mxc_unavailable(1, message))

    def test_zero_exit_cannot_be_negative_refusal(self):
        self.assertFalse(probe.native_mxc_unavailable(0, 'native MXC is unavailable on this executor'))

    def test_generic_errors_remain_failures(self):
        self.assertFalse(probe.native_mxc_unavailable(1, 'access denied while reading configuration'))

    def test_missing_or_boolean_exit_is_not_evidence(self):
        for code in (None, True, '1'):
            with self.subTest(code=code):
                self.assertFalse(probe.native_mxc_unavailable(code, 'native MXC is unavailable on this executor'))


if __name__ == '__main__':
    unittest.main()
