# Validation Commands

Commands run during build:

```powershell
py -3 -m py_compile core/protocol/update_receipt.py .aide/scripts/tests/test_aide_update_receipt_v0.py .aide/scripts/aide_lite.py
py -3 -m unittest discover -s .aide/scripts/tests -p "test_aide_update_receipt_v0.py"
py -3 .aide/scripts/aide_lite.py update-receipt status
py -3 .aide/scripts/aide_lite.py update-receipt project
py -3 .aide/scripts/aide_lite.py update-receipt validate
```

The final validation pass also includes predecessor regression checks, broad AIDE validation, queue evidence inspection, safety scans, Git diff checks, and commit policy check.
