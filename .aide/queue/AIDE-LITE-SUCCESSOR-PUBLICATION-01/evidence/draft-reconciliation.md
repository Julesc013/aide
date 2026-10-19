### Existing draft reconciliation

- **Completed:** local/remote dev, main and active task at9cead252; post-main fixed preview PASS; annotated1.1 tag object3ae20f881ff065254a681deba30a39209c888ee7 points to9cead252.
- **Completed:** one draft creation, ID416392381, exact title/body/tag/target, unpublished and zero assets.
- **Failed read:** GET by tag returned404. Original79 operations/streams are retained and rehashed. No upload, publication, acquisition or consumer was dispatched.
- **Observed recovery:** authenticated bounded list and GET by ID expose the same draft; gh release view also resolves it.
- **API semantics:** the [official GitHub documentation](https://docs.github.com/en/rest/releases/releases#get-a-release-by-tag-name) describes tag lookup as retrieving a published release. The [GitHub CLI upload interface](https://cli.github.com/manual/gh_release_upload) supports display labels; its observed release view resolves this existing draft.
- **Continue:** preserve release target/tag at9cead252 while a new recovery-only execution checkpoint advances the owned task branch. Reobserve the exact empty draft immediately before uploading, then perform only the unfinished effects. No completed-effect replay, retag, replacement or new native allocation.
