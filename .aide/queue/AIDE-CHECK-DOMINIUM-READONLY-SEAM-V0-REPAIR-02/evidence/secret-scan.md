# Secret Scan

Command:

`rg -n --pcre2 "(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY|xox[baprs]-[A-Za-z0-9-]{10,})" .aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02 .aide/reports/dominium-readonly-seam-v0-repair-02-check`

Result: PASS. No credential-shaped matches were found. Exit code `1` from
`rg` means no matches for this scan.
