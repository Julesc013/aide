# Validation Results

Acceptance input checks:

- Repair 05 check task inspect: PASS, `missing_evidence: 0`.
- Repair 05 check report: `PASS_WITH_WARNINGS`, `material_finding_count: 0`.
- Current seam validation: `PASS_WITH_WARNINGS`, 42 records.
- Current conformance results: `PASS_WITH_WARNINGS`, 23/23 expectations passed.
- Current portability result: `PASS`, required output sets equal, output hashes equal, absolute path leak count 0.
- Current demo result: `PASS_WITH_WARNINGS`, source mutation count 0, forbidden operation count 0.
- Fixture manifest: 43 fixtures.
- Dominium status: clean, `main...origin/main [behind 24]`.

Final checks before commit:

- `py -3 .aide/scripts/aide_lite.py task inspect --task-id AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`: PASS, `missing_evidence: 0`.
- `py -3 .aide/scripts/aide_lite.py task evidence --task-id AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`: PASS, no missing evidence.
- `git diff --check`: PASS.
- `py -3 .aide/scripts/aide_lite.py validate`: PASS.
- JSON parse scan over acceptance JSON: PASS, 1 file parsed.
- Secret-like scan over acceptance surfaces: PASS, zero hits.
- `git -C C:\Projects\Dominium\dominium status --short --branch`: PASS, no dirty Dominium paths; checkout remains `main...origin/main [behind 24]`.

Post-commit validation still required:

- `py -3 .aide/scripts/aide_lite.py commit check --latest`.
