# Source-bound Lite dev integration observation

- Accepted source/effect subject: `aaa53fa5d201f9082e522c73470c47287119ea58`,
  tree `085b9b5b1e28229400358e98c5e8379c30b29c53`, with the exact
  independent ACCEPT recorded separately.
- Evidence-only review closeout: `e0636ddbc0e4c22e6ca15b034ee75908177447ce`,
  tree `20ec4e885e2778e696722072f890bcf5564ca60f`.
- `dev` before: `2aaee82e96d275d83501785a073f6ba73c7b6594`.
- Local `dev` integrated by `git merge --ff-only` to `e0636ddb`. The accepted
  subject is an ancestor; no conflict resolution or source substitution
  occurred.
- Remote task branch and remote `dev` were observed at the full `e0636ddb`
  identity after non-force pushes. Remote `main` remained
  `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.
- `commit check --range dev..e0636ddb` passed all 19 new commits before
  integration. The refreshed `main..dev` check still returned FAIL over 359
  commits for the ten historical messages in the existing exact owner
  decision packet; three earlier dispositions remain accepted.
- The source-bound effect manifest stayed SHA-256
  `6e7a9d4e54cedf1e6eccc000d0e4073a14552586baca302c9444ce6f7b855aa0`.
  The stable ZIP and tar remained SHA-256 `a762c816295a90e09db97ce7e56443272ce19fd5aa581ffccdb6081e1a75836a`
  and `a8e7bd38114e4761257ca0c4514985c39cf651ff4d2ae79d8ed12b86ed9b869f`.
- No main promotion, tag, publication, downloaded asset or target deployment
  occurred. The D runner had no active job after integration.

This is an observed source/evidence integration, not a new release-effect
verdict. The ten narrow historical owner decisions are a separate main gate.
