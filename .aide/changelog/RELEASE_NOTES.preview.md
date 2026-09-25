# AIDE Release Notes Preview

This is a deterministic preview only. It does not publish a release.

source_range: HEAD latest 50 commits
source_head: e215698a993d1904152c614ec84b71741f4bb086
preview_only: true

## Highlights

- Added: local customization explanation and opt-in import feedback. (98de5ee1531e)
- Added: exact historical message dispositions to the dev source ancestry. (e40aec47dd2d)
- Added: restore a missing receipt-owned file from the exact delivered pack. (49f38d12f425)
- Added: receipt-backed read-only removal planning in the delivered portable CLI. (1a25e33effc5)
- Fixed: dry-run recovery mutation and project-owned metadata payload boundary. (9b21e183d462)
- Fixed: Windows alias route into project-owned customization metadata. (2b4f5de885a5)
- Fixed: allow accountable AEST historical decisions while retaining strict raw policy results. (7a2305f51894)
- Fixed: prevent dirty-source provenance in the local combined artifact projection. (1fa02a8594fe)

## Validation Summary

- 98de5ee1531e: PASS: export/import suite ran 27 cases with zero failures.
- 9dc91654f8df: PASS: changelog preview, validate, and status; 50 commits, zero malformed.
- 8262b2fd6465: PASS: export boundary, pack-status, release validate, and draft-validate.
- 37daa862e939: PASS: first post-artifact generation changed the expected 18 records.
- 1e3a59dce7bf: PASS: 27 export/import, 18 Q47, 11 Q48, and 6 Q31 cases; two affected rechecks passed.
- 9b21e183d462: PASS: 28-case export/import suite after the recovery repair.
- 0c98e175bab9: PASS: changelog preview, validate, and status; 50 commits, zero malformed.
- 7e678f165fb4: PASS: export boundary, pack-status, release validate, draft-validate, and nine asset checks.
- 55e76dfbab3a: PASS: first postcommit generator cycle changed the expected 18 files.
- 2b4f5de885a5: PASS: focused reserved-metadata alias test after this change.

## Known Risks

- 98de5ee1531e: Conflicting managed edits still require explicit resolution; feedback is local and manually shared.
- 9dc91654f8df: Preview text is not official release notes or publication authority.
- 8262b2fd6465: This is a local artifact checkpoint; post-commit source-ancestor projection and stable release gates remain open.
- 37daa862e939: Local artifacts do not authorize main promotion, tagging, or publication.
- 1e3a59dce7bf: Queue review and dev integration remain pending; stable release and lifecycle apply are not accepted.
- 9b21e183d462: The earlier archive receipt applies only to the superseded candidate; no dev integration occurred.
- 0c98e175bab9: Preview text is not official release notes or publication authority.
- 7e678f165fb4: Local artifacts are not published and post-commit ancestry projection remains open.
- 55e76dfbab3a: Clean-tree replay and accountable dev review remain open; no public release is claimed.
- 2b4f5de885a5: The prior replacement archive is superseded; dev remains unchanged.

## Follow-up

- 98de5ee1531e: Regenerate current portable and release artifacts, qualify exact extracted bytes, then integrate the accepted slice.
- 9dc91654f8df: Generate the portable pack and local release artifacts from this committed checkpoint.
- 8262b2fd6465: Replay after commit, record final-byte evidence, and qualify a clean integration candidate.
- 37daa862e939: Replay from this committed clean tree and record the extracted-consumer receipt.
- 1e3a59dce7bf: Obtain explicit review decision for the exact candidate and integrate only if accepted.
- 9b21e183d462: Regenerate the pack and local release artifacts from this source, then qualify exact consumer bytes.
- 0c98e175bab9: Generate the replacement pack and local release artifacts from this clean checkpoint.
- 7e678f165fb4: Run and commit source-ancestor projection, then clean-tree replay and exact review packet.
- 55e76dfbab3a: Replay from this committed projection, update exact evidence, and request review of the replacement subject.
- 2b4f5de885a5: Rebuild exact portable bytes and run final source and consumer qualification.

## Warnings

- None.

## Preview Caveat

- This draft is not an official release note and does not create tags or GitHub Releases.
