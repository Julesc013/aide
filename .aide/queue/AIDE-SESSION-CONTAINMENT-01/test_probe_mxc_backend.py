"""Refusal classification regression; no subprocess, host setup or model."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('mxc_probe_classification', Path(__file__).with_name('probe_mxc_backend.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class NativeRefusalClassification(unittest.TestCase):
    def test_native_cli_workload_is_after_separator_without_windows_subcommand(self):
        command = probe.sandbox_command('codex.exe', 'candidate',
                                        {'windows.sandbox': 'mxc'}, 'strict',
                                        ['python.exe', '-I', '-B', '-c', 'pass'])
        self.assertEqual(command[command.index('sandbox') + 1], '--permission-profile')
        self.assertNotIn('windows', command)
        self.assertEqual(command[command.index('--') + 1:],
                         ['python.exe', '-I', '-B', '-c', 'pass'])
        self.assertIn('windows.sandbox="mxc"', command)

    def test_incomplete_or_mixed_executor_binding_refuses_before_launch(self):
        for options in ({'backend': str(probe.BACKEND)},
                        {'backend': str(probe.BACKEND), 'backend_sha256': 'a' * 64},
                        {'backend': str(probe.BACKEND), 'backend_sha256': 'a' * 64,
                         'expected_identity': 'GUNMETAL-WIN\\Jules', 'real_user_prerequisite': True}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                probe.executor_binding(**options)

    def test_exact_new_host_binding_preserves_legacy_identity(self):
        binding = probe.executor_binding(str(probe.BACKEND), 'a' * 64,
                                         'GUNMETAL-WIN\\Jules')
        self.assertEqual(binding, (probe.BACKEND, 'a' * 64, 'GUNMETAL-WIN\\Jules'))
        self.assertEqual(probe.executor_binding(real_user_prerequisite=True)[2],
                         'BLACKGLASS-WIN1\\Jules')

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
