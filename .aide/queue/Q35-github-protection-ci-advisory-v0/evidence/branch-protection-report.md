# Branch Protection Report

Q35 defines desired branch protection posture without applying it.

- `main`: canonical, protected, no force push, no deletion.
- `dev`: integration, not canonical truth, protected when present.
- `release/*`: protected release line when used.
- `hotfix/*`: urgent repair line with review and check gates.
- `gh-pages`: generated deploy branch only.

No GitHub branch protection API calls were made.
