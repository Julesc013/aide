# Validation Results

- `git status --short --branch`: 0 (0.135s)
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_distribution_manifest_v1.py`: 0 (52.053s)
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`: 0 (2.877s)
- `py -3 .aide/scripts/aide_lite.py install status`: 0 (1.203s)
- `py -3 .aide/scripts/aide_lite.py install validate`: 0 (1.464s)
- `py -3 .aide/scripts/aide_lite.py repair status`: 0 (1.216s)
- `py -3 .aide/scripts/aide_lite.py repair validate`: 0 (1.152s)
- `py -3 .aide/scripts/aide_lite.py upgrade status`: 0 (1.177s)
- `py -3 .aide/scripts/aide_lite.py upgrade validate`: 0 (1.433s)
- `py -3 .aide/scripts/aide_lite.py upgrade compatibility`: 0 (1.228s)
- `py -3 .aide/scripts/aide_lite.py rollback status`: 0 (1.101s)
- `py -3 .aide/scripts/aide_lite.py rollback validate`: 0 (1.22s)
- `py -3 .aide/scripts/aide_lite.py uninstall status`: 0 (1.111s)
- `py -3 .aide/scripts/aide_lite.py uninstall validate`: 0 (1.707s)
- `py -3 .aide/scripts/aide_lite.py release status`: 0 (1.107s)
- `py -3 .aide/scripts/aide_lite.py release validate`: 0 (6.553s)
- `py -3 .aide/scripts/aide_lite.py release draft-status`: 0 (1.151s)
- `py -3 .aide/scripts/aide_lite.py release draft-validate`: 0 (1.183s)
- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`: 0 (1.081s)
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DISTRIBUTION-MANIFEST-V1-01`: 0 (1.14s)
- `py -3 .aide/scripts/aide_lite.py validate`: 0 (11.724s)
- `git diff --check`: 0 (0.143s)
- `git diff --cached --check`: 0 (0.076s)

- all_commands_passed: true
- json_parse_passed: true
- path_leak_scan_passed: true
- secret_like_scan_passed: true
