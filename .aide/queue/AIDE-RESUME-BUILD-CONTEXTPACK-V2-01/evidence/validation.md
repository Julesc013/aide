# Validation

Commands run:

```bash
git diff --check
git diff --cached --check
py -3 .aide/scripts/aide_lite.py context-pack-v2 status
py -3 .aide/scripts/aide_lite.py context-pack-v2 project
py -3 .aide/scripts/aide_lite.py context-pack-v2 validate
py -3 .aide/scripts/aide_lite.py reference-id validate
py -3 .aide/scripts/aide_lite.py event-record validate
py -3 .aide/scripts/aide_lite.py evidence-packet validate
py -3 .aide/scripts/aide_lite.py workunit validate
py -3 .aide/scripts/aide_lite.py worker-run validate
py -3 .aide/scripts/aide_lite.py test-job validate
py -3 .aide/scripts/aide_lite.py capability-manifest validate
py -3 .aide/scripts/aide_lite.py conformance-profile validate
py -3 .aide/scripts/aide_lite.py conformance-result validate
```

Results:

- diff checks: passed; `git diff --check` emitted only a queue-index CRLF normalization warning.
- ContextPack v2 status/project/validate: `PASS_WITH_WARNINGS`
- ReferenceID validate: `PASS_WITH_WARNINGS`
- EventRecord validate: `PASS_WITH_WARNINGS`
- EvidencePacket validate: `PASS`
- WorkUnit validate: `PASS`
- WorkerRun validate: `PASS`
- TestJob validate: `PASS`
- CapabilityManifest validate: `PASS_WITH_WARNINGS`
- ConformanceProfile validate: `PASS_WITH_WARNINGS`
- ConformanceResult validate: `PASS_WITH_WARNINGS`

Broad validation and task evidence inspection are recorded after the task-local
evidence files are materialized.

Final task inspection:

```bash
py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-RESUME-BUILD-CONTEXTPACK-V2-01
py -3 .aide/scripts/aide_lite.py validate
```

Results:

- task inspect: `classification: complete`, `missing_evidence: 0`
- task evidence: no missing files
- broad AIDE validation: `PASS`
