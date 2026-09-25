# Qualified owned repair dev effect

Before mutation, local and remote `dev` and GitHub's ref all identified
`5dfa75e632b09f732a8150376db6840bcf149ed3`. The primary dev and task
worktrees were clean; the reviewed candidate descended from current dev;
shared ref/packed-ref lock paths were absent. The effective Windows identity
was `BLACKGLASS-WIN1\Jules` and the authenticated GitHub account was
`Julesc013`.

The controller fast-forwarded local dev and used a normal, non-force
`git push origin dev`. Both `git ls-remote` and GitHub's ref endpoint then
reported `6b4007d06546fe234f96730751d94d7c540a223e`, tree
`367027251177098e55fc3633163ee7006490e6e1`. This head descends from
the exact independently reviewed local source/artifact candidate
`e4697aaa327189e6eb00742613de841aa4e4d4a8`; the intervening
`6b4007d0` commit contains only queue review/consumer evidence.

The remote effect integrates bounded owned missing-file repair source in dev. It does
not implement full repair, importer write safety, rollback, detach/removal,
native/hosted activation, main promotion, or public release.

After this dev effect, a safe-import adversarial check showed a second Windows
writer could open and alter a `tempfile.mkstemp` staging file while the first
descriptor remained open. The accepted `atomic_create_bytes_no_clobber`
helper in dev uses that same staging pattern for repair intent and payload
publication. Treat repair write safety as newly disputed and block any
release qualification until a dev-focused regression, repair, and independent
review close this risk. The earlier independent verdict remains an accurate
record of what was reviewed; it is not evidence for this newly found race.
