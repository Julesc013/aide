# Secret Scan

Secret-like scan result: passed with no value-shaped matches.

Scope:

- `.aide/queue/AIDE-CHECK-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest-check/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Command:

```text
rg -n --hidden --glob '!*.git/*' --glob '!*.pyc' "(?i)(api[_-]?key\s*[:=]\s*[^\s`]+|secret\s*[:=]\s*[^\s`]+|password\s*[:=]\s*[^\s`]+|private[_-]?key\s*[:=]\s*[^\s`]+|bearer\s+[A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,})" .aide/queue/AIDE-CHECK-ADAPTER-MANIFEST-01 .aide/reports/adapter-manifest-check PLANS.md IMPLEMENT.md .aide/queue/index.yaml
```

No credential values are present or required by this blocked check.
