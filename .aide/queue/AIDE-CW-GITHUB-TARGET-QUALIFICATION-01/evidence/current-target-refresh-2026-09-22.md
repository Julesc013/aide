# Current GitHub Target Refresh

Observation date: 2026-09-22
API version: `2026-03-10`
Execution identity: `BLACKGLASS-WIN1\Jules`
Authenticated account: `Julesc013` (`User`, id `30209022`)
Repository: `Julesc013/aide` (id `1192621212`, public)

## Current Facts

- `main`: `aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3`.
- `dev`: `c6fdc754844cf7d42302218ce08307a7e05dcb61`.
- Observer repository permission: `admin`.
- Repository rulesets: none.
- Effective rules for `dev`: none.
- Classic `dev` protection: HTTP 404, `Branch not protected`.
- Actions workflows: zero.
- Merge commits: enabled.
- Squash merges: enabled.
- Rebase merges: enabled.
- Auto merge: disabled.
- Delete branch on merge: disabled.
- Restricted broker principal: unresolved.
- Required workflow/check app identity: unresolved.

## Read-Only Endpoints

- `GET /repos/Julesc013/aide`
- `GET /repos/Julesc013/aide/rulesets`
- `GET /repos/Julesc013/aide/rules/branches/dev`
- `GET /repos/Julesc013/aide/branches/dev/protection`
- `GET /repos/Julesc013/aide/actions/workflows`
- `GET /repos/Julesc013/aide/collaborators/Julesc013/permission`
- `GET /repos/Julesc013/aide/git/ref/heads/main`
- `GET /repos/Julesc013/aide/git/ref/heads/dev`

No setting, workflow, credential, branch, pull request, merge, ruleset, tag, or
release mutation was performed.

## Documentation Basis

- GitHub's synchronous merge endpoint documents `sha` as the required matching
  PR head and HTTP 409 for a mismatch:
  `https://docs.github.com/en/rest/pulls/pulls#merge-a-pull-request`.
- Ruleset required checks support strict base freshness and an optional exact
  integration id:
  `https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset`.
- Restrict updates permits matching-ref creation but limits later updates to
  bypass actors:
  `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`.

These sources define supported mechanisms. They do not prove that AIDE's
currently absent controls are installed or that future hosted races will pass.
