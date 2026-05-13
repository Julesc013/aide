# GitHub Advisory Report

Q35 adds report-only GitHub protection and CI advisory support.

Expected generated outputs:

- `.aide/github/github-advisory.json`
- `.aide/github/github-advisory.md`
- `.aide/github/branch-protection-plan.json`
- `.aide/github/branch-protection-plan.md`
- `.aide/github/ci-advisory.json`
- `.aide/github/ci-advisory.md`
- `.aide/github/latest-github-status.md`

Boundary:

- GitHub API mutation: false
- workflow file written: false
- workflow installation: false
- branch mutation: false
- tag creation: false
- release publishing: false
- provider/model/network calls: false

Latest command result:

- `github advisory`: PASS.
- `github validate`: PASS.
- findings: 1 advisory finding, for missing GitHub protection application; this
  is expected because Q35 is report-only and does not apply settings.
