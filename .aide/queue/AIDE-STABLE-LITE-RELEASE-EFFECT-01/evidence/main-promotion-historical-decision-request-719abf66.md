# Main promotion historical-message decision request

The accepted release-effect candidate at `719abf66` reached remote `dev`,
but the active dev-to-main rule requires `commit check --range main..dev`.
That exact command returned **FAIL** across 337 commits: three exact owner
dispositions applied, and ten other historical commit messages remain
undispositioned. Main promotion, tag and publication are stopped.

Exact machine packet: `main-promotion-historical-decision-request-719abf66.json`, SHA-256 `faeb20c9fe2e85836e17fadcaec920220f8318b2472bc879416c7847b93b7c36`.
Full range output: approved D control root `release-commit-range-719abf66.log`, SHA-256 `67361d8efd9f176d1144df12f14218a9ee2bc69e9d4a2a4e4299aa3781eee398`.
The JSON packet pins each full commit object, tree, ordered parents,
canonical message SHA-256 and every failed checker result.

| Commit | Subject | Failed checks |
| --- | --- | ---: |
| `0e76df9e` | chore(codex): remove repository execution pins | 11 |
| `91efe815` | audit(queue): close Codex neutrality checkpoint | 12 |
| `4682413d` | chore(repo): admit hygiene and spec convergence | 11 |
| `51cbce9d` | docs(specs): adopt control-plane foundation | 11 |
| `386195af` | audit(runtime): checkpoint unique broker receipts | 12 |
| `477764b0` | audit(facman): checkpoint restartable entry evidence | 12 |
| `e3663fe1` | audit(runtime): checkpoint isolated-host evidence | 12 |
| `c4d0305e` | audit(repo): bind archive-duplicate cleanup candidate | 12 |
| `83df2b73` | fix(repo): bind cleanup review to canonical manifest | 12 |
| `02a15a67` | chore(queue): route convergence to docs integration | 12 |

## Exact owner decision needed

For each of these ten exact records, the accountable owner may accept or
reject **historical commit-message nonconformance only**. Accepting a record
does not say its original message passed, approve the code, waive a new
commit check, qualify a product profile or authorize native/hosted effects.
The earlier A/B/C decisions apply only to their own three commits.

One response can accept all ten by explicitly naming this JSON packet and
its SHA-256, or list rejected/excluded commit IDs. Silence is not acceptance.
After an actual owner response, create ten structured decision artifacts,
bind exact record/evidence hashes, obtain independent technical review of
the changed registry, and rerun the full `main..dev` range check. No
published history rewrite or broad policy exception is proposed.
