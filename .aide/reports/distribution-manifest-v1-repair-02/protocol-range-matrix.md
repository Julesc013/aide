# Protocol Range Matrix

- {'case_id': 'valid-current-1x', 'expected_valid': True, 'observed_valid': True, 'observed_refusal_codes': [], 'passed': True}
- {'case_id': 'valid-lower-0-9-max-1x', 'expected_valid': True, 'observed_valid': True, 'observed_refusal_codes': [], 'passed': True}
- {'case_id': 'future-max-2x', 'expected_valid': False, 'observed_valid': False, 'observed_refusal_codes': ['distribution.unsupported_protocol_range'], 'passed': True}
- {'case_id': 'future-max-2-0-0', 'expected_valid': False, 'observed_valid': False, 'observed_refusal_codes': ['distribution.unsupported_protocol_range'], 'passed': True}
- {'case_id': 'future-min-2-0-0', 'expected_valid': False, 'observed_valid': False, 'observed_refusal_codes': ['distribution.unsupported_protocol_range'], 'passed': True}
- {'case_id': 'inverted-max-0-9', 'expected_valid': False, 'observed_valid': False, 'observed_refusal_codes': ['distribution.unsupported_protocol_range'], 'passed': True}
- {'case_id': 'component-future-max-2x', 'expected_valid': False, 'observed_valid': False, 'observed_refusal_codes': ['distribution.unsupported_protocol_range'], 'passed': True}
