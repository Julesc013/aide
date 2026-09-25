# Remaining risks, 2026-09-25

- Canonical validate/doctor fail because reviewed source changes are not yet
  reflected in the old committed export/release preview. This is an expected
  but real gate; source-only acceptance cannot be reused as artifact acceptance.
- Installed targets with an explicit target profile now override a copied
  AIDE source task ID, and target next-plan reports omit source readiness.
  Legacy repositories with no profile still use exact queue-ID fallback;
  this is not a universal ownership classifier.
- The changed profile-aware source candidate needs independent delta review.
  A later projection
  must test delivered zero- and one-item target queues and qualify replay.
- No final stable release, main promotion, tag, publication or downloaded
  consumer acceptance is established by this WorkUnit.
