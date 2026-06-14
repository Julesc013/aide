# Python Runner Diagnostic

- status: NON_BLOCKING_WARNING
- direct shell py -3: Python 3.14.5
- issue: nested Python-runner subprocess diagnostic resolved py -3 to Python 3.9 and failed on Path.write_text(newline=...).
- authoritative validation: .aide/reports/workunit-cli-mutation-check/behavior-results.json
- blocking: false
