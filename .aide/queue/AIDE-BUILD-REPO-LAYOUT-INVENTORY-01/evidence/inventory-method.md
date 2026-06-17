# Inventory Method

## Live Commands Used For Facts

```powershell
git status --short --branch
git log -1 --oneline
git ls-files .aide
git ls-files core
Get-ChildItem -Force .aide -Directory
Get-ChildItem -Force core -Directory
Get-ChildItem -Force .aide/reports -Directory
Get-ChildItem -Force .aide/reports -File
rg ".aide/reports/[A-Za-z0-9_.-]+-(check|accept|acceptance)"
py -3 .aide/scripts/aide_lite.py repo status
py -3 .aide/scripts/aide_lite.py roots status
py -3 .aide/scripts/aide_lite.py refactor map-status
```

## Key Facts

- Repo status reports 5,136 files, 0 unknown classifications, 943 generated
  files, 2,687 evidence files, and 608 orphan candidates.
- Root status reports 22 roots, 3 mixed roots, 19 unknown or review-required
  roots, 15 high-risk roots, and no-apply root plans.
- Refactor map status reports 0 move entries, 20 salvage entries, 0 aliases,
  and 40 reference rewrite candidates.
- `.aide/reports` has 102 top-level report files and 52 report directories.
- Report directories use mixed lifecycle suffixes: 14 `-check`, 6 `-accept`,
  and 6 `-acceptance` directories.
- Hardcoded flat check/accept report path references appear in 156 files with
  365 matches across code, docs, queue evidence, and planning logs.

## Boundary

The reports use observed filesystem and helper-command facts. They do not make
deletion, movement, rewrite, alias, or rationalization decisions.
