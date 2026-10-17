# First runner review: REQUEST_CHANGES

/root/review_disked_continuation reviewed map9df4ff03 and the three source templates.
All pins matched; application and60 assertions stayed unchanged. Required fix:
addSubTest must journal failure/error under the parent method ID because unittest
does not route those failures through addFailure/addError. Successful subtests must
not produce whole-method passes. The narrow override is added in the next subject.
No allocations2-4 ran under this rejected runner.
