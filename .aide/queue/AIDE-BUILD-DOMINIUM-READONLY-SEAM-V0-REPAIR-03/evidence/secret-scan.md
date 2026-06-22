# Secret-Like Scan

Command: `rg -n "(?i)(api[_-]?key|secret|password|token|BEGIN [A-Z ]*PRIVATE KEY)" ...`

Result: PASS_WITH_NOTES. Matches were benign references to prior `secret-scan.md` evidence filenames and the internal `ContextVar` variable name `token`; no secret material was found.
