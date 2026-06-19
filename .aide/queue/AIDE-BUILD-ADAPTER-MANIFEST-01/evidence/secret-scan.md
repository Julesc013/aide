# Secret Scan

Secret-like scan result: passed with no value-shaped matches.

Scope:

- `.aide/queue/AIDE-BUILD-ADAPTER-MANIFEST-01/**`
- `.aide/reports/adapter-manifest/**`
- `.aide/queue/index.yaml`
- `PLANS.md`
- `IMPLEMENT.md`

Command:

```text
rg -n --hidden --glob '!*.git/*' --glob '!*.pyc' "(?i)(api[_-]?key\s*[:=]\s*[^\s`]+|secret\s*[:=]\s*[^\s`]+|password\s*[:=]\s*[^\s`]+|private[_-]?key\s*[:=]\s*[^\s`]+|bearer\s+[A-Za-z0-9._-]{20,}|sk-[A-Za-z0-9]{20,})" .aide/queue/AIDE-BUILD-ADAPTER-MANIFEST-01 .aide/reports/adapter-manifest PLANS.md IMPLEMENT.md .aide/queue/index.yaml
```

The earlier broad scan pattern was too loose and matched historical task
identifiers in `.aide/queue/index.yaml`; the value-shaped scan above returned
no matches.
