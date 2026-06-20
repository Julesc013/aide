# Secret-Like Scan

Bounded scan:

```text
rg -n --hidden -S "(sk-[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |OPENSSH |EC |DSA |)?PRIVATE KEY-----|AKIA[0-9A-Z]{16})" .aide/protocol/aide-dominium-readonly-seam-v0.schema.json core/interop/dominium .aide/scripts/tests/test_aide_dominium_readonly_seam.py .aide/fixtures/dominium-readonly-seam .aide/interop/dominium .aide/reports/dominium-readonly-seam-v0 .aide/queue/AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01
```

Result: PASS. No strict secret-like matches were found.
