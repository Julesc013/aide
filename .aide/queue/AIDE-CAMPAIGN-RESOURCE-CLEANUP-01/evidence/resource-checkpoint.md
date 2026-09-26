# Resource checkpoint — 2026-09-26

Parent Goal remains active and incomplete under the owner's campaign/resource
delegation. This checkpoint does not claim stable release or bulk activation.

## Cleanup and capacity

34 inactive checkouts retired with ordinary Git worktree removal, without
force or ref deletion. Only primary dev and the reused partial-import source
checkout remain. Exact retained objects/effects are in worktree-removal-first.json,
worktree-retirement.json, worktree-retirement-third.json and
neutrality-worktree-retirement.json. Unique commits, source, dirty/unknown
material, custody and required reviews/failures remain preserved.

Measured logical bytes for the nine-, twenty-one- and one-checkout rounds plus
duplicate logs total 3,251,839,088. The first three checkouts have no logical
byte measurement. Logical bytes are not physical allocated-space recovery.
Two duplicate diagnostic logs were deleted after equality with a retained
original: duplicate-log-retirement.json. No broad C/D/E deletion.

D free before the first owned removal: 21,531,815,936 bytes. At 15:08:
C 211,551,387,648; D 73,493,364,736; E 55,903,629,312 bytes free.
Available RAM 13,146,025,984; committed 30,667,587,584 of 93,066,825,728.
Exact volumes/time: capacity-checkpoint.json. Concurrent unrelated activity
changed free space; the net increase cannot all be attributed to AIDE cleanup.
No owned test/cleanup process remains. Unrelated FacMan builds were left alone.
No new clone/checkout/bulk extraction/release archive was created for this work.

## Actual execution and limits

Continuation retired two exact old ZIP expansions after frozen Git custody,
streamed member hashes, ordinary-path and inactivity checks. Original ZIPs and
all sibling target/failure fixtures, feedback and reviews remain retained.
duplicate-consumer-extract-retirement.json records 1,662 files, 6,882,832
logical bytes, no failures, unchanged retained archives, and observed D free
73,082,650,624 → 73,091,637,248 bytes. Cumulative known logical removals are
3,258,721,920 bytes, plus the first unmeasured three checkouts. Unknown-custody
consumers remain protected. No new bulk pool or job was admitted.

No owner-approved permanent bulk pool was recovered; the precise existing
location question remains pending. No fallback or machine pool was activated.
Actual validation used only explicit tiny disposable fixtures under existing
D:/Projects/AIDE/_recovery/resource-cleanup-20260926, then retired them.
That receipt parent is not adopted as permanent bulk storage.

Actual limits: 10 GiB free disk reserve; 4 GiB RAM/commit reserves; 512 MiB
Windows Job memory; 64 KiB logs; 16 processes. Task OS scratch 8 MiB, retained
1 MiB, runtime 120s, 1,000 entries. Focused importer scratch 128 MiB, runtime
300s, 12,000 entries. Disk reservations/sampling are application controls,
not filesystem quotas; Job OS limits are distinct. Real build-tool placement
and permanent pool activation remain unqualified.

The existing execution owner enforces existing approved roots/volume IDs,
finite reservations, shared admission, exact input/process identity, bounded
logs/runtime, collection/recovery and retirement. Canonical generation outputs
also require finite reservations and are never scratch-cleanup targets. Code
monitors/waits; tests do not require repeated model polling.

## Exact review and test state

- Resource b325deeaca742aaed842235d4227e0068a050acf: independent
  ACCEPT_WITH_NOTES after recovery-final-check repair; ten affected PASS in
  13.276s. Earlier 22-case evidence retains its earlier source binding.
- Recovery fixture e87386e55eda38f35525518e8699867f9832802c: independent
  ACCEPT_WITH_NOTES; seven actual focused PASS in 25.090s, scratch
  11,654,822 bytes, Job memory 252,903,424 bytes, retired/released. Production
  flushes and full export/archive/consumer fixtures remain unchanged.
- Inspection 0302b18c724d463a5865441bb717f9733d26a1eb, tree
  ad89d8700834cad5a99edbebc068a248eca784a0: independent ACCEPT_WITH_NOTES.
  review-0302b18c.md SHA-256
  d449d1597ce408f932313b267563fb9ec73027f207dd2f3b9caa95e296c107a5.
  Its report predates the separate full Task OS result; no reviewer rerun
  is invented. Default git detect/plan and task status do not write reports;
  explicit --write-reports retains generation.
- bounded-task-status-0302-check.json: 11 PASS in 10.084s. Its legacy golden
  writers generated fifteen source projections; selective restoration is
  bound in task-os-generated-report-retirement.json.
- bounded-task-status-check.json: corrected destinations, 11 PASS in 8.554s,
  no skips; scratch 2,104 bytes, Job memory 212,393,984 bytes, logs 1,964
  bytes, retired/released, source reports unchanged. Real source context and
  original golden runners/assertions remain; only report destinations move
  into admitted scratch. Added byte/mtime equality checks the source reports.
  This precommit run records HEAD 0302b18c plus actual changed test SHA-256
  d92b2d583fb8bbd919f9eeef202211b94f499e2ac856b9863a289411050ccfa2.

## Continuation

Golden-placement e185d2898fb207e59c9eb5380fecf624a3e954ac, tree
f04b108474a3af0bf18434c4b81e83f33cacaabb, received independent
ACCEPT_WITH_NOTES; review-e185d289.md SHA-256
322e92f1d829714e71da767f2e83f4a090557fe0b97087cb7d69cae1a5ecb5a4.
The full real source context was not completely frozen in the run manifest;
retain that limit and perform final integrated qualification at its boundary.
Normally publish only the evidence-closed task checkpoint.
Primary dev remains e88b1c2ee6f3206c628f79908e430a7967e9f58c;
main remains aec53b1d3675f02e2fdd17cc718fdcff6cd4e9f3. Task publication is
not dev/main integration. After permanent placement is resolved, admit the
required importer/lifecycle suite, batch current-generator projection, qualify
delivered bytes and integrate. Native/hosted and stable-release gates stay open.
