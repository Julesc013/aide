# Remaining Risks And Gates

- The source branch mixes completed documentation with unfinished runtime work;
  candidate construction must use an explicit path closure, not a branch merge.
- The 244 imported proposed requirements and 244 acceptance designs remain
  unadopted and unrun unless later exact evidence says otherwise.
- A moving remote `dev` would require the candidate base to be refreshed and
  validation repeated before integration.
- `main` promotion is a separate hard review gate and is not authorized here.
- Tags, release assets, uploads, and public publication remain unperformed and
  require exact release review.
