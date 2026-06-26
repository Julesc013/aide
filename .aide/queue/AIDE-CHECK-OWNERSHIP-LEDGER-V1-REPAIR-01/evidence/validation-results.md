# Validation Results

- `py -3 -m compileall core/protocol .aide/scripts/tests`: exit `0`
- `py -3 -m unittest discover -s .aide/scripts/tests -p test_aide_ownership_ledger_v1.py`: exit `0`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger status`: exit `0`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger project`: exit `0`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger validate`: exit `0`
- `py -3 .aide/scripts/aide_lite.py ownership-ledger migrate-q43`: exit `0`
- `py -3 .aide/scripts/aide_lite.py project-lock validate`: exit `0`
- `py -3 .aide/scripts/aide_lite.py distribution-manifest validate`: exit `0`
- `py -3 .aide/scripts/aide_lite.py validate`: exit `0`
