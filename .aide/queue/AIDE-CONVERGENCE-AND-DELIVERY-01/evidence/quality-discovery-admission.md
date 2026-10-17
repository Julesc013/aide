# Explain recorded quality and reuse evidence

Child: AIDE-QUALITY-DISCOVERY-01. Base dev/main:
33a377743d86f59fd63a042096063d664e200468. This bounded P6 contribution follows
the existing campaign delegation and useful-extensibility amendment. It does not
wait for optional desktop delivery or pending DiskEd ownership.

## Objective and existing owner

Extend `.aide/scripts/aide_lite.py quality explain-file` with an additive JSON
projection and useful human output from the existing Q38 ledger. Show recorded
owner, docs, likely tests, dependencies and matching reuse candidates, explaining
why each was selected. Limit displayed relations, disclose omitted counts, and
state that report freshness and semantic dependency coverage are unverified.
Persist the already computed reuse_report as an optional field in the existing
ledger; old ledgers remain valid and report reuse as unindexed. Both existing
ledger schemas describe this additive optional field. Do not parse truncated
Markdown or reconstruct source relationships during an explanation.
No new index, semantic graph, source scan, test selector or task authority.
Preserve legacy fields and exit behavior for valid/missing records. Malformed or
oversized reports must fail clearly without generating reports or reading source.
Empty heuristic results mean not found, never known absent. Similarity does not
authorize extraction, refactoring or deletion. Source revision is attribution,
not a claim of current bytes. This is a read-only advisory projection.

## Bounded paths

- This admission and `.aide/queue/AIDE-QUALITY-DISCOVERY-01/**`.
- `.aide/scripts/aide_lite.py`, `.aide/scripts/tests/test_q38_file_quality.py`.
- `docs/reference/file-quality-ledger.md`.
- `.aide/quality/file-quality-ledger.schema.json` and
  `.aide/reports/file-quality-ledger.schema.json` (optional reuse_report only).
- `.aide/queue/index.yaml`, parent ExecPlan.md/status.yaml.
- Four `.aide/intake/latest-*` files, `.aide/context/latest-task-packet.md`.
- PLANS.md, IMPLEMENT.md, DOCUMENTATION.md.
- Existing four `.aide/reports/capability-*` ledger/binding/status outputs.
- Derived `.aide/export/aide-lite-pack-v0/**` and existing export reports only
  through the existing exporter, reflecting this changed portable payload.
- Six existing `.aide/changelog/` preview outputs through their existing owner.

No policy, global configuration, host dispatch, provider, target repository,
daemon, storage-root, branch protection, public release, tag or immutable archive
change. No regeneration of live Q37/Q38 reports merely to make this feature green.
Existing report inputs stay preserved; unknown freshness remains visible.

## Verification and effects

Preserve original Q37/Q38 tests. Add focused fixture assertions for useful owner,
test and helper lookup; deterministic JSON; equivalent human meaning; not-found
versus unindexed; malformed/oversized input; bounded output and unchanged files.
Include two same-name helpers with different behavior to keep heuristic limits
explicit. Check actual CLI output against an existing report without rewriting it.

At most three sequential managed allocations: focused tests; changed export and
delivered fixture checks; promotion preview. Use existing managed_workspace and
approved D execution roots/config61162891870315aa1a0adc94ded55e2b9a65224c948c23c26c823005bbbaca90,
unchanged limits and authoritative admission. Freeze exact source/input manifests
and independently review each effect before execution. No automatic job retries;
failure consumes allocation and is retained. Collect, hash and retire owned scratch
and reservations. Routine read-only doctor/validate/diff/commit checks remain
proportionate; generate packet before refreshing capability bindings.

Independent source and integration review precedes qualified dev/main fast-forward
and nonforce pushes. Main requires affected package evidence, not a new release.
Keep Lite1.0.0 frozen. Local-only task/aide-quality-discovery-01 may be created from
the exact base after admission, helper/ref/dispatch checks in the sole checkout.
Only four intake files and this admission are pre-branch owned changes. Retire
only this local branch after verified integration. Other refs are untouched.

The lexical intake classifier reports release/split-required because the prompt
mentions future integration/release exclusions. This packet separates source,
managed qualification and later exact Git effects; it admits no publication.
Stop for changed ownership, unsafe effects or a failed applicable gate. Preserve
prior evidence and continue independent work when optional hosts remain unavailable.
