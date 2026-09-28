# Current-byte lifecycle, restart and context qualification, 2026-09-28

Frozen source `b74923195d0ba006c8af012dc14f9f692545d421`, tree
`3c2d077ee6b164a5175784ac68c000f3e736b666`, used current ZIP SHA-256
`af8bf103353d72eacbbf1f2f28cea8cef1f11ea0d942872c57f76aee9725a7ff`.
No local release bytes or delivered CLI source changed during these jobs.

The Windows lifecycle canary ran as D job
`27289a03567046028ab33271faca3296`, manifest SHA-256
`616655af0f7e25f1bdd333bda0d4d8fb6f3ad8ce24134c1a927c301a2655e26e`.
Its 31 expected command outcomes passed on 834 ZIP members. Actual owned-file
repair applied, rival bytes were preserved, repair restart returned RECOVERED,
synthetic-successor rollback returned ROLLED_BACK, fresh and brownfield removal
returned DETACHED, and changed brownfield ownership returned PARTIAL_REMOVAL.
The synthetic successor was a fixture, not a published release. Retained
`summary.json` SHA-256
`bf69acc628c9af82694ed92c810ff039e5aed603cb03bc82da81ee54969fd295`;
job receipt SHA-256
`3b32be9d85914fcc00ffc37b3fa9fbdcfa952faae96356bd35bb610f0138679d`.
Peak scratch 30,548,066 bytes, peak memory 238,772,224 bytes; 33 retained
output files total 4,095,605 bytes. Scratch retired and reservation released.

The forced-process-exit canary ran as D job
`0f34675be5df45b59c5607aca29d7e63`, manifest SHA-256
`e312127b49fc6c19a8db95e0ce7cf96f236f94227a9396da5e1d8f0252e6da00`.
Three child effects exited deliberately at code 77. Fresh CLI reconciled
import and repair as RECOVERED and removal as DETACHED_RECOVERED. The adapted
ignored local oracle SHA-256 was
`2dd3b0f8b12a7bc382a71747019ce61ba7938e72b832d1a96d2e807b3e2b005b`;
the unmodified external original remains retained. Summary SHA-256
`7275f805c212f63917fdb94cd554a576ee775b01ca47be356f4518cbdef5177e`;
job receipt SHA-256
`52ed76ba4cb9c7638f0fd80dbb66e503a6e6696346d0a07955bac1031cd82b09`.
Peak scratch 13,974,703 bytes, peak memory 260,509,696 bytes; 16 retained
output files total 1,059,529 bytes. Scratch retired and reservation released.

The context/evidence canary ran as D job
`c45db84982fb43179233b77c97f38e61`, manifest SHA-256
`2658e1bb0c3ffdf5d73bdf45fcd3041410b1fb4454efd32fe6a086e3f5960fc3`.
The child exited zero. Fresh and Git brownfield imports preserved the
project-owned file; installed `context`, `pack --task` and `verify --evidence`
all exited zero behind a Python socket guard. Both produced compact context
and task packets from the installed CLI. Verify returned WARN/zero errors:
15 fresh warnings (11 absent optional report references, one absent managed
adapter, two absent cache reports, one no-Git diff scope), and 18 brownfield
warnings (same 11+1+2, four uncommitted fixture paths). This guard does not
observe native networking in child processes, so OS-level offline evidence
remains open. Retained `summary.json` SHA-256
`b77a2da92a6e9f7d8659b9c1fe2c681e7ffb19ed4f5231ba1f31609edbe8dfb1`.

The context runner initially returned REFUSED only at scratch retirement:
Windows Git loose object files in the disposable brownfield target were
readonly. The durable active record already contained child exit zero and
collected output/log digests. Exact owned scratch path, 3,458 ordinary entries,
the one expected nested `.git`, retained digests and absence of links/hardlinks
were checked before clearing readonly attributes on 991 files, without deleting
anything manually. AIDE `job recover` then observed the owned job quiescent,
verified retained custody, retired scratch and released the reservation.
Preflight receipt SHA-256
`e981a8062763bb988fa957fa82da06f41f7d6458707741dede4050adb270136f`;
final retained job receipt SHA-256
`462709907b9f42b7a2184ab24890bed3de9f7d8659b9c1fe2c681e7ffb19ed4f`.

The bounded runner repair was then exercised on the same logical task branch.
The full managed-workspace suite ran in D job
`d6669a3a771b45a1b7e437da1e9de4ea`: **27 tests passed** in 21.107 seconds;
child exit zero, peak scratch 4,716 bytes, peak memory 211,726,336 bytes,
scratch retired and reservation released. Manifest SHA-256
`2bed88be75ea4f3993e0242d4dbab17b152677f981d8886ab334fe91c38ecd80`;
retained receipt SHA-256
`1bfd7aba8b8e46c564b09ab149e6fe6f5ba784026f98c941eb21bdd248492022`.
The regression includes a readonly disposable Git-shaped object and required
retained output custody.

A second D job `d93c4a00bf5348f1b38e0fbd109b68e2` created a real disposable
Git repository beneath the job temp root. It observed three loose objects, all
readonly. The runner cleared exactly three attributes, retained the unique
result, retired scratch and released its reservation. Child exit zero, peak
scratch 27,211 bytes, peak memory 92,672,000 bytes. Manifest SHA-256
`ca9efc4ce5c9f11a3cbc87b89dd0ce91273f1957703280d689137d26a851571c`;
result SHA-256
`5a4bb118646788dab8b72880a605093ca4c2b65c148bdb54bfa327de47eea931`;
retained receipt SHA-256
`42ec9d3756d67149df7a908ab7a836f6b7afed4263e2d9a10562d41efdc9c55c`.
The two jobs shared the configured D control root and did not overlap.

After checking the staged diff, the existing success-case process identity
assertion was restored to its original test as well as retained in the new
regression. The final test-file revision ran in D job
`76d445d90e3b4cdeb785c299cb8fd25a`: **27 tests passed** in 21.302 seconds,
child exit zero, peak scratch 4,716 bytes, peak memory 212,873,216 bytes,
scratch retired and reservation released. Final manifest SHA-256
`3e2830bc64a3c0db7449454642be22ba37a5af71028061ced13274105befe73d`;
retained receipt SHA-256
`a59b9fe09074dd5e369c7c247fa8b3b2bc389662099d66681bf9666450989891`.
This final rerun supersedes the earlier suite result for the test-file revision.
