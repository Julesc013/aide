# Remaining risks and limits

- Application reservations and monitoring are not filesystem disk quotas.
  Every future bulk job still needs current capacity admission, bounded
  execution and verified retirement.
- Changes in free disk space across the cleanup window include concurrent
  unrelated activity. Exact logical removed bytes and observed free-space
  readings remain separate measurements.
- The retained partial-import recovery checkout and unique source/evidence
  remain intentionally preserved; task closure is not permission to delete
  either.
- Local runner and source qualification does not prove the full AIDE stable
  release, native or hosted operation, main promotion or publication. Those
  gates remain with the parent and their own WorkUnits.
