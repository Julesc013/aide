# Export Pack Report

## Summary

Q21 added a deterministic portable AIDE Lite Pack exporter and generated the
current pack at:

```text
.aide/export/aide-lite-pack-v0/
```

Latest generated artifacts:

- manifest: `.aide/export/aide-lite-pack-v0/manifest.yaml`
- checksums: `.aide/export/aide-lite-pack-v0/checksums.json`
- install guide: `.aide/export/aide-lite-pack-v0/install.md`
- import policy: `.aide/export/aide-lite-pack-v0/import-policy.yaml`
- export report: `.aide/export/aide-lite-pack-v0/export-report.md`
- payload root: `.aide/export/aide-lite-pack-v0/files/`

## Manifest Result

- pack id: `aide-lite-pack-v0`
- schema: `q21.aide-lite-pack-manifest.v0`
- included files: 111
- checksums: 115
- boundary result: PASS
- raw prompt storage: false
- raw response storage: false
- local state copied: false
- provider/model calls: false
- network calls: false

## Included Classes

- AIDE Lite script and portable tests
- token/context/verifier/review/ledger/eval/controller/routing/cache/local-state/Gateway/provider/export policies
- prompt templates
- verification packet templates and policies
- starter golden tasks
- no-call router examples and route schema
- cache/local-state example docs
- local/report-only Gateway metadata and stdlib skeleton
- offline provider metadata and stdlib contract helpers
- target-neutral profile and memory templates
- managed `AGENTS.md` portable template
- reference docs and install instructions

## Excluded Classes

- source repo identity
- source repo queue history
- source repo memory
- generated context
- generated reports
- route decisions
- cache-key reports
- Gateway status reports
- provider status reports
- eval runs
- outcome ledgers
- local state
- secrets
- raw prompts
- raw responses

## Determinism Notes

The exporter sorts portable input files, writes stable JSON checksums, refuses
forbidden paths, and reports obvious secret-like content before writing the
pack. The manifest records source commit and dirty-state metadata for audit;
checksums are the authoritative integrity check for the generated pack.

## Limitations

The pack is fixture-validated only. It is not yet evidence that Eureka or
Dominium will save tokens, preserve quality, or need no local adaptation.
