Live commit `1e8889eeb6cbee55ef9f4b42f6bf5d29405b4358` is verified. Repair 02 reports 43 fixtures, 143 focused tests, 23 conformance expectations, zero source mutations, and routes exactly to `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.

The check should challenge semantics rather than merely confirm that new fields exist: the schema now has kind-specific required-field lists but several specs remain broadly typed, the operation ledger distinguishes aggregated operations from raw observations, and portability was proven using production-generated dependency copying. These need independent validation.

## Next mega check prompt

````text
# AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02
# Independent Final Verification of Registry Provenance, Public Contract,
# Fixture Replay, Conformance Evidence, Operation Observation, and Portability

Create and process `AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02`.

Use `.aide/queue/index.yaml` as canonical AIDE queue truth. Re-read live
repository state before writing anything.

This is one substantial CHECK-only task.

Independently verify that
`AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02` closes all ten remaining
material gaps from the preceding repair check, preserves closure of the other
thirteen original findings, introduces no new material regression, and retains
the offline read-only boundary.

Do not modify production seam code, schemas, tests, fixtures, generated seam
outputs, repair reports, repair evidence, historical checks, or Dominium.

Stop at `needs_review`.

If no material defect exists, recommend exactly:

`AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01`

If any bounded material defect remains, recommend exactly:

`AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03`

Do not repair defects in this task.

---

# 1. Required Baseline

Verify:

- current AIDE branch is `main`;
- AIDE worktree is clean before check outputs;
- `AIDE-ACCEPT-DOMINIUM-INTEGRATION-CHARTER-01` remains accepted;
- its evidence reports `missing_evidence: 0`;
- original seam build exists at:
  `a75635478be155ef7bc2b62de4ead3837212bbb8`,
  or the live recorded equivalent;
- original seam check exists at:
  `692b4b3469e80a67f3f2f98612ec66c86b7394e9`,
  or the live recorded equivalent;
- Repair 01 exists at:
  `30931ba1f17b1bc4d9d2b9b12ef18133831ad8fd`,
  or the live recorded equivalent;
- Repair 01 check exists at:
  `bf2b51996c7df0374942ad361ebfbae04c9c1caf`,
  or the live recorded equivalent;
- Repair 02 exists at:
  `1e8889eeb6cbee55ef9f4b42f6bf5d29405b4358`,
  or the live recorded equivalent;
- every predecessor task reports `missing_evidence: 0`;
- the original check remains `REQUEST_CHANGES` with 18 findings;
- the Repair 01 check remains `REQUEST_CHANGES` with:
  - 13 original findings closed;
  - 5 original finding rows open;
  - 10 concrete material gaps;
- Repair 02 reports `PASS` or `PASS_WITH_WARNINGS`;
- Repair 02 records exactly ten repaired-pending-check gap dispositions;
- Repair 02 recommends this check;
- no Repair 02 check, Repair 03, acceptance, supersession, or downstream
  validation-slice task already replaces this gate.

Expected Repair 02 baseline:

```text
selected Dominium inputs: 17
projected records: 42
fixtures: 43
focused tests: 143
conformance expectations: 23
source mutations: 0
forbidden operations: 0
````

Independently recompute every count.

If any baseline condition is missing, contradictory, failed, or superseded:

* stop as `BLOCKED`;
* preserve all historical evidence;
* identify the exact discrepancy;
* recommend one bounded reconciliation task;
* do not modify seam implementation.

---

# 2. Check-Only Independence

Allowed changes are limited to:

```text
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/**
.aide/reports/dominium-readonly-seam-v0-repair-02-check/**
.aide/queue/index.yaml
PLANS.md
IMPLEMENT.md
```

Do not modify:

```text
.aide/protocol/aide-dominium-readonly-seam-v0.schema.json
core/interop/dominium/**
core/protocol/**
core/interop/__init__.py
.aide/scripts/aide_lite.py
.aide/scripts/tests/test_aide_dominium_readonly_seam*.py
.aide/fixtures/dominium-readonly-seam/**
.aide/interop/dominium/**
.aide/reports/dominium-readonly-seam-v0/**
.aide/reports/dominium-readonly-seam-v0-repair-02/**
any prior task or check evidence
Dominium
```

Create independent check tools only under this task's evidence root.

For material assertions, do not import:

```text
core.interop.dominium.validation
core.interop.dominium.conformance
core.interop.dominium.fixture_replay
core.interop.dominium.bundle.portability_check
Repair 02 disposition logic
```

It is acceptable to invoke production commands to obtain candidate output.

The check must independently judge that output.

Use standard-library Python and already-installed validators only.

Do not install dependencies.

---

# 3. Historical Evidence Preservation

Verify byte or Git-tree immutability of:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-01
AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-01
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-01
AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-01
```

and their reports.

The historical sequence must remain:

```text
Build:
PASS_WITH_WARNINGS

Original independent check:
REQUEST_CHANGES
18 material findings

Repair 01:
PASS_WITH_WARNINGS

Repair 01 independent check:
REQUEST_CHANGES
10 material gaps across 5 open original finding rows

Repair 02:
PASS_WITH_WARNINGS

Repair 02 independent check:
this task
```

Do not rewrite any preceding result.

---

# 4. Required Independent Harness

Build a new independent harness equivalent to:

```text
evidence/tools/check_repair_02.py
evidence/tools/verify_registry_provenance.py
evidence/tools/verify_public_schema.py
evidence/tools/replay_all_negative_fixtures.py
evidence/tools/verify_conformance_semantics.py
evidence/tools/verify_operation_ledger.py
evidence/tools/verify_portable_dependency_closure.py
evidence/tools/verify_cross_process_determinism.py
evidence/tools/verify_dominium_immutability.py
```

Produce:

```text
evidence/independent-repair-02-check.json
evidence/ten-gap-closure.json
evidence/five-finding-closure.json
evidence/schema-negative-results.json
evidence/fixture-replay-results.json
evidence/conformance-semantic-results.json
evidence/operation-ledger-results.json
evidence/dependency-closure-results.json
evidence/portability-results.json
evidence/before-dominium-state.json
evidence/after-dominium-state.json
```

The independent harness must not use production expected-value builders to
derive both expected and observed values.

---

# 5. Exact Ten-Gap Closure Matrix

Build a matrix with exactly these ten rows:

```text
REPAIR02-GAP-01 allowed_operation_count missing
REPAIR02-GAP-02 conformance results lack required independent assertion fields
REPAIR02-GAP-03 cross-process determinism failed
REPAIR02-GAP-04 diagnostic projection disclosure incomplete
REPAIR02-GAP-05 instrumentation coverage missing
REPAIR02-GAP-06 operation ledger missing required operation families
REPAIR02-GAP-07 negative fixtures failed independent replay
REPAIR02-GAP-08 schema lacks kind-specific spec constraints
REPAIR02-GAP-09 schema lacks status constraints
REPAIR02-GAP-10 refusal projection disclosure incomplete
```

For every row record:

```text
source gap ID
original observed behavior
Repair 02 implementation
changed production files
new tests
new artifact or fixture
independent assertion
expected result
observed result
remaining limitation
disposition
```

Allowed dispositions:

```text
CLOSED
OPEN
SUPERSEDED_BY_STRONGER_CHECK
```

A superseded gap still requires a stronger passing assertion.

Do not accept `repaired_pending_independent_check` as proof.

---

# 6. Five Original Finding Rows

Independently close or keep open exactly these five original findings:

```text
diagnostics.truncation_disclosure
refusals.truncation_disclosure
schema.effectiveness
fixtures.negative_replayability
conformance.independence
```

Also rerun a regression sample for the thirteen already-closed original
findings.

At minimum resample:

```text
exact repository identity
final bundle self-digest
mixed revision
snapshot digest
singleton cardinality
dangling reference
kind-specific owner
mutation capability disguised as read-only
duplicate event sequence
native diagnostic comparison
native refusal comparison
missing HostManifest field
truthful demo timing
```

A Repair 02 change must not reopen a previously closed finding.

---

# 7. Registry Provenance — Diagnostics

Independently read the diagnostic registry bytes from pinned Dominium commit:

```text
c92b386027890c1bbf14aef6eaafe0357b7b03dd
```

Verify the diagnostic registry summary records:

```text
source registry path
source registry SHA-256
source registry Git object
source revision
native count
projected count
omitted count
selection policy
selection limit
projected IDs
selected IDs SHA-256
omitted IDs SHA-256
truncation disclosure
```

Independently recompute:

```text
source_registry_sha256
source_registry_git_object
native_count
projected_count
omitted_count
selected_ids_sha256
omitted_ids_sha256
```

Verify:

```text
source registry digest matches immutable Git object bytes
source registry digest matches the selected source snapshot entry
source registry revision equals bundle revision
projected IDs exactly match DiagnosticProjection records
projected count equals actual DiagnosticProjection count
omitted count equals native count minus projected count
selection limit is coherent
selection policy is deterministic
truncation is disclosed when omitted_count > 0
```

Test mutations with refreshed top-level bundle digests:

```text
wrong source digest
wrong Git object
wrong source revision
wrong native count
wrong projected count
wrong omitted count
wrong projected ID
wrong selected-ID digest
wrong omitted-ID digest
truncation false while omitted count is positive
unrecognized selection policy
```

Production semantic validation must reject each mutation with a stable
registry-specific error.

The public schema must reject malformed registry-summary shapes independently
where applicable.

---

# 8. Registry Provenance — Refusals

Apply the same independent checks to:

```text
contracts/refusal/refusal_code.registry.json
```

Verify the RefusalProjection IDs and fields against native source.

Test the same summary mutations.

Do not trust summary values because they were generated by production code.

The diagnostic and refusal summaries must not accidentally share digests,
counts, or selected IDs.

---

# 9. Registry Summary Canonicalization

Determine the exact canonicalization rules for:

```text
selected_ids_sha256
omitted_ids_sha256
```

Verify whether identity order is:

```text
native source order
lexicographic order
declared selection order
```

The rule must be explicit and deterministic.

Test:

```text
same set, different order
duplicate ID
empty omitted set
selection limit greater than native count
projected count inconsistent with selected IDs
```

The validator must distinguish set equality from order-sensitive contract law.

Registry provenance must be covered by the final SeamBundle self-digest.

---

# 10. Public JSON Schema — Actual Draft 2020-12 Validation

Use an already-installed Draft 2020-12 validator when available.

Do not use production semantic validation as the schema check.

First validate the committed repaired SeamBundle.

Then test invalid candidates independently.

The public schema must constrain more than key presence.

For each record kind, test:

```text
missing required field
null required field
wrong scalar type
wrong array/object type
wrong enum/const
wrong record kind for the supplied spec
cross-kind spec substitution
unknown unbounded field
```

At minimum test:

### HostManifest

```text
host_id as integer
supported_surfaces as string
registered command count as string
runtime_dispatch_available true
```

### HostCapabilitySet

```text
capabilities as object
capability missing ID
capability side_effect_class wrong type
forbidden capability implemented true
```

### WorkspaceDescriptor

```text
workspace_ref invalid ReferenceID
identity_is_file_path true
queue_status wrong type
```

### ContextDescriptor

```text
artifact_refs as string
section_count wrong type
source_revision_binding malformed
```

### ArtifactReference

```text
sha256 malformed
size_bytes negative or string
git_object malformed
identity_is_file_path true
file_path_is_locator false
```

### DiagnosticProjection

```text
diagnostic_id wrong type
severity wrong type
source_registry wrong type
```

### RefusalProjection

```text
diagnostic_codes as string
related_commands as object
recovery_action wrong type
```

### EvidenceReferenceSet

```text
evidence_refs as string
evidence_count wrong type
```

### EventEnvelope

```text
sequence zero, negative, string
event_ref invalid
event-store implementation true
```

### DominiumBridgeManifest

```text
bridge_runtime_implemented true
ownership wrong type
command_mapping missing invocation boundary
```

If the schema merely requires these keys but permits all wrong types, classify
the public contract as materially incomplete.

---

# 11. `$ref` and Kind Discrimination

Verify the selected Draft 2020-12 validator applies `$ref` siblings correctly.

Test:

```text
HostManifest record with ContextDescriptor kind
HostManifest record with ContextDescriptor spec
ContextDescriptor record with HostManifest spec
ArtifactReference item with DiagnosticProjection kind
```

Every cross-kind substitution must fail.

Do not rely on Python validator behavior if the public JSON Schema accepts it.

If compatibility with older JSON Schema implementations is intended, determine
whether `allOf` is required for portable discrimination.

---

# 12. Bounded Extension Policy

The current schema may intentionally allow selected additional properties.

Independently identify every `additionalProperties: true` location.

Classify each as:

```text
explicit extension surface
compatibility-preservation surface
unintentionally unbounded surface
```

An extension surface should use a bounded container equivalent to:

```text
extensions
x-aide-*
```

rather than arbitrary unknown fields mixed into canonical fields.

Test that a misleading field such as:

```text
authoritative: true
workbench_is_authority: true
runtime_started: true
command_invocation_implemented: true
```

cannot bypass validation merely because it is unknown.

Unknown optional metadata may remain acceptable only when it cannot change
authority, behavior, identity, security, status, or compatibility meaning.

---

# 13. Status Contract

Independently inspect top-level and record status contracts.

Verify required false-boundary facts include all live equivalents of:

```text
dominium_command_invoked
host_runtime_started
workbench_started
bridge_runtime_started
service_started
database_opened
transport_started
network_call_performed
provider_or_model_called
worker_executed
patch_transaction_applied
preview_or_apply_performed
source_repository_mutated
target_repository_mutated
branch_or_worktree_created
github_mutation_performed
release_or_promotion_performed
generated_projection_marked_canonical
```

Test:

```text
empty status
missing each required false-boundary field
true value
null value
string false
numeric zero
unknown authority-changing status field
```

Verify record-specific positive facts are permitted only where defined:

```text
record_projected
host_manifest_projected
artifact_hash_bound
event_envelope_projected
```

A positive projection fact must not silently override a false boundary.

Check whether every false-boundary property declared by schema is also required.

---

# 14. Producer and Metadata Contract

Verify producer is structurally:

```text
name
version
```

Test:

```text
producer string
missing producer name
missing producer version
empty producer object
unexpected credential field
```

Verify metadata types and constraints for:

```text
ID
schema version
protocol version
source revision
identity owner
semantic owner
authority role
freshness
compatibility
explicit non-capabilities
```

The current committed output must pass both schema and semantic checks.

---

# 15. Replay All Negative Fixtures Independently

The expected live inventory is:

```text
43 total fixtures
11 positive fixtures
32 negative fixtures
```

Independently derive these counts from disk.

Do not use production fixture inventory constants.

For every negative fixture:

1. load the serialized fixture;
2. verify its schema version;
3. verify base bundle reference;
4. independently hash the base bundle;
5. compare base digest;
6. apply serialized operations using the independent replayer;
7. independently hash the invalid payload;
8. compare invalid digest;
9. run the candidate through production validation as target under test;
10. compare expected error-code subset against observed stable codes;
11. replay a second time;
12. verify byte-identical invalid output.

Expected result:

```text
failed_count: 0
passed_count: 32
```

---

# 16. Five Previously Failing Fixtures

Verify these now emit the exact required stable codes:

```text
invalid_reference_id
  → reference.syntax

private_tool_bypass_declaration
  → command.invocation

unknown_required_capability
  → compat.required_capability

workbench_authority_overclaim
  → workbench.authority

wrong_authority_role
  → authority.role
```

Additional digest errors are acceptable.

The required semantic code must be present.

Ensure the fixture actually represents the named defect rather than a different
one that happens to fail.

---

# 17. Fixture Replayer Safety and Strictness

Independently audit the production replay engine.

Verify allowed operations are exactly:

```text
add
remove
replace
append
```

Reject:

```text
unknown op
root replacement
negative array index
noncanonical integer index
out-of-range index
replace missing object key
remove missing object key
use of "-" for remove or replace
ambiguous escaped pointer
non-string pointer
missing op
missing path
executable operation metadata
callable
module
command
shell
eval
exec
```

`remove` must not silently succeed when the target does not exist.

`replace` must require an existing target.

`add` and `append` semantics must be deterministic.

The replay engine must never access the filesystem, import modules, spawn
processes, or evaluate fixture content.

---

# 18. Conformance Result Shape

Verify every one of the 23 conformance results has:

```text
id
description
assertion_id
result
expected
observed
evidence_refs
```

Verify:

```text
assertion IDs are unique
result IDs are unique
evidence refs are non-empty for PASS
evidence refs resolve to actual assertion records
assertion sidecar contains the referenced assertion
expected and observed are not omitted
failed assertions include failure details
passed_count equals actual PASS count
NOT_RUN and NOT_PROVEN are not counted as passed
```

The results and assertion sidecar must agree byte-for-byte on:

```text
assertion ID
description
result
expected
observed
```

---

# 19. Conformance Semantic Validity

Do not accept fields alone.

Independently determine whether each of the 23 assertions actually proves its
description.

Pay particular attention to:

### Unsupported-operation refusal

It must prove unsupported CLI verbs are refused.

It must not pass merely because the recommended next-task ID has a particular
suffix.

Run actual unsupported verbs and require refusal:

```text
run
invoke
execute
apply
write
sync
push
serve
connect
dispatch
fetch
pull
checkout
branch
worktree
publish
```

### No cross-repository writes

It must use before/after repository evidence or the operation ledger.

A self-declared `dominium_file_write: false` field is insufficient alone.

### No provider/model/network activity

It must use operation-guard evidence, source/dependency review, or bounded
instrumentation.

A self-declared status field is insufficient alone.

### No mutation

It must prove actual mutation paths are absent/refused.

A forbidden-capability list alone is insufficient.

### Bounded mapping completeness

It must verify:

```text
record-kind completeness
record cardinality
registry summary provenance
reference closure
declared omission policy
```

Mere presence of ten kind names is insufficient.

### Replayable fixtures

It must use actual replay results for all 32 negative fixtures.

### Version compatibility

It must prove only the bounded compatibility claim.

A `readOldWriteCurrent: true` field alone is insufficient if no older supported
fixture or explicitly bounded compatibility rule exists.

Classify any semantically mismatched assertion as material overclaim.

---

# 20. Conformance Failure Injection

Create temporary candidates that fail one concern at a time:

```text
duplicate identity
wrong repository identity
source digest corruption
bundle digest corruption
authority overclaim
Workbench authority overclaim
invented refusal
invalid diagnostic
dangling evidence reference
event correlation mismatch
unknown required capability
network status true
worker status true
mutation capability inserted
negative fixture failure
```

For each candidate verify:

```text
the relevant assertion becomes FAILED_VALIDATION
unrelated assertions do not all collapse automatically
passed_count changes correctly
evidence remains assertion-specific
```

No aggregate fallback may mark all expectations PASS.

Call any legacy aggregate-only conformance API directly.

It must return:

```text
NOT_PROVEN
```

or equivalent, never PASS.

---

# 21. Operation Ledger Count Semantics

Independently inspect the operation ledger.

Clarify these separate concepts:

```text
operation_count
  number of aggregated operation records

observation_count
  total observed raw operation events

allowed_observation_count
  total allowed raw observations

forbidden_observation_count
  total forbidden raw observations
```

If the production names remain:

```text
allowed_operation_count
forbidden_operation_count
```

verify their documented semantics unambiguously.

Required equations:

```text
operation_count == len(operations)
observation_count == sum(operation.count for operation in operations)
observation_count == allowed_observation_count + forbidden_observation_count
```

If `allowed_operation_count` counts raw observations, then:

```text
observation_count
  ==
allowed_operation_count + forbidden_operation_count
```

must hold.

Do not incorrectly require aggregated `operation_count` to equal raw observation
counts.

Verify top-level demo counts agree with the ledger.

The reported `858` allowed observations must independently recompute from
operation entries and their `count` fields.

---

# 22. Operation Ledger Traceability

Every aggregated operation must include:

```text
family
operation
target
classification
allowed
source
observation method
count
return codes
```

Verify:

```text
count is positive integer
return codes are truthful
allowed operations do not contain forbidden verbs
forbidden operations are marked not allowed
operation ordering is deterministic
duplicate aggregate keys are absent
```

Because the ledger aggregates raw observations, require one of:

```text
complete raw observation trace
```

or:

```text
raw trace digest
raw observation count
deterministic aggregation law
bounded representative sample
```

A first-50 sample alone must not be presented as the complete trace.

---

# 23. Operation Family Coverage

Required families:

```text
git_reads
filesystem_writes
branch_worktree_ref_ops
network_attempts
provider_model_attempts
worker_dispatch
mutation_apply
```

For every family verify:

```text
coverage field exists
coverage method exists
implementation or guard exists
test exists
injection test exists where safe
evidence exists
```

A coverage value set to `true` unconditionally is not sufficient.

Independently inspect source and exercise each guard.

Classify every actual observed or injected operation into the correct family.

---

# 24. Git Command Classification

Exercise the instrumented Git runner.

Allowed forms should include bounded read-only variants of:

```text
status
rev-parse
remote get-url
branch --show-current
rev-list
show
ls-tree
```

Test unsafe variants:

```text
remote add
remote set-url
branch new-name
branch -D
fetch
pull
clone
checkout
switch
reset
merge
rebase
commit
push
worktree
tag
update-ref
unknown verb
```

Every unsafe command must:

```text
be refused before subprocess execution
be recorded as forbidden
receive the correct family
increase the forbidden count
cause demo failure when injected
```

Classify network Git operations such as:

```text
fetch
pull
clone
push
```

as network or remote-mutation attempts—not ordinary read-only Git observations.

Verify no forbidden command executes merely to prove refusal.

---

# 25. Filesystem Write Coverage

Independently verify Dominium no-write protection uses:

```text
path-aware write boundaries
before/after tracked state
before/after untracked inventory
before/after ignored inventory
HEAD
refs
index
config
selected source hashes
```

Inject a bounded attempted Dominium write through the seam's guarded write
surface.

It must be refused and recorded without changing Dominium.

AIDE output writes under authorized AIDE paths remain allowed.

Do not confuse expected AIDE report writes with Dominium writes.

---

# 26. Network, Provider, Worker, and Mutation Coverage

Under bounded instrumentation, attempt:

```text
socket creation
urllib/http request
provider/model import or invocation stub
non-Python child worker process
mutation/apply operation
```

The seam must refuse or lack these paths.

Record the family, method, and outcome.

The check itself may monkeypatch or guard these calls.

Do not make a real network request.

Coverage claims apply only to the seam process and direct child operations.

They must not claim whole-system monitoring.

---

# 27. Runtime Dependency Manifest Integrity

Independently parse:

```text
.aide/interop/dominium/runtime-dependency-manifest.json
```

Verify:

```text
dependency count
unique paths
repository-relative paths
no traversal
no absolute paths
every required file exists
every SHA-256 matches
entrypoint exists
module search root is coherent
supported Python range is explicit
manifest digest independently recomputes
```

Change one manifest entry hash in a temporary copy.

Manifest validation must fail.

Change one dependency byte.

Hash verification must fail.

Delete one required file in an isolated copy.

The CLI must fail with a clear undeclared/missing dependency result.

---

# 28. Independent Import-Graph Closure

Do not trust the production dependency list.

Use Python AST inspection to derive local imports reachable from:

```text
.aide/scripts/aide_lite.py
core/interop/dominium/**
core/protocol/envelope.py
```

Resolve local imports transitively.

Compare the independently derived local dependency set to the serialized
manifest.

Classify:

```text
manifest dependency missing
manifest dependency unused
dynamic import not declared
optional dependency not classified
```

No required local import may be absent.

Do not require all unrelated AIDE Lite modules if they are not imported along
the Dominium seam command path, but dynamic import boundaries must be explicit.

---

# 29. Manifest-Driven Portability

The independent portability check must copy files strictly from the serialized
runtime dependency manifest.

Do not call production:

```text
required_runtime_dependency_paths()
_copy_runtime_dependencies()
```

to decide what to copy.

Procedure:

1. load serialized manifest;
2. validate manifest digest;
3. validate every entry hash;
4. create empty temporary root;
5. copy exactly the declared entries;
6. verify copied hashes;
7. verify no symlinks or external references;
8. run the CLI.

If isolated execution succeeds only when production hard-coded dependency lists
are used, portability is not proven.

---

# 30. Sanitized Isolated Processes

Run portability tests with a sanitized environment:

```text
PYTHONPATH removed
PYTHONHOME removed
PYTHONNOUSERSITE=1
user-site disabled
unrelated current working directory
no parent AIDE checkout in sys.path
```

Use Python isolated mode where compatible:

```text
-I
```

or an equivalent explicit import isolation.

Run each CLI command in a fresh process, not only one process executing all
commands sequentially.

Run:

```text
status
snapshot
project
validate
diff
demo
```

against at least two separate isolated roots.

Also run one full sequence per root to detect stateful ordering defects.

All commands must succeed without importing from the original checkout.

---

# 31. Required Output Completeness

Define the exact required portable output set.

At minimum:

```text
seam-bundle.json
source-snapshot.json
projection-index.json
validation.json
conformance-results.json
conformance-assertions.json
compatibility.json
demo-result.json
fixture-manifest.json
interop seam bundle
bridge manifest
conformance expectations
runtime dependency manifest
```

Both isolated roots must produce every required file.

Do not consider two equally incomplete output dictionaries deterministic.

Verify:

```text
required output set equals actual output set
no required output missing
no undeclared portable output affects the comparison
```

---

# 32. Cross-Process Determinism

Run projections under varied but supported process conditions:

```text
different temporary AIDE roots
different current working directories
different PYTHONHASHSEED values
clean environment
fresh process per command
full-sequence process
```

Compare deterministic bytes for every required output.

Do not compare nondeterministic task-local observational evidence.

If `demo-result.json` is deterministic, prove it.

If any demo field is observational, exclude or normalize it explicitly and
document why.

No output may depend on:

```text
temporary root path
original AIDE checkout path
user home
username
current working directory
process ID
wall-clock time
hash randomization
filesystem enumeration order
```

---

# 33. Absolute Path Leak Scan

Scan:

```text
portable JSON outputs
Markdown outputs
positive fixtures
negative fixtures
CLI stdout
CLI stderr
tracebacks
dependency manifest
portability report
```

Forbidden needles include:

```text
original AIDE root
each temporary AIDE root
temporary base directory
user home
user profile directory
absolute Dominium root
current working directory
```

Portable outputs must identify source only through:

```text
repository identity
source revision
stable references
repository-relative locators
```

A local absolute Dominium path may appear only in explicitly nonportable,
task-local check evidence—not portable seam outputs.

---

# 34. Supported Python Version Claim

The runtime manifest claims:

```text
>=3.11
```

Verify:

```text
source syntax is compatible with 3.11
stdlib dependencies exist in 3.11
no higher-version-only syntax or API is used
```

Run the isolated suite on Python 3.11 when available.

If Python 3.11 is unavailable locally, record minimum-version execution as:

```text
NOT_RUN
```

and perform bounded static compatibility inspection.

Do not report minimum-version runtime proof without execution.

This may remain warning-class if current runtime succeeds and the claim is
narrowed truthfully.

---

# 35. Repair 02 Disposition Integrity

Inspect:

```text
remaining-gap-disposition.json
repair-report.json
status.yaml
test-summary.json
```

Require exactly ten gap dispositions.

For every disposition verify:

```text
source gap text matches Repair 01 check
repair summary corresponds to actual code
evidence reference exists
test exists
observed behavior matches claim
```

The five original finding rows must have an updated closure report.

Do not accept generic statements such as “repaired” without artifact-level
evidence.

---

# 36. Focused Test Review

Run:

```text
base seam suite
Repair 01 suite
Repair 02 suite
```

Expected current total:

```text
111 + 20 + 12 = 143
```

Do not require these exact counts if live tests advanced.

Independently classify tests into:

```text
semantic tests
fixture replay tests
schema tests
conformance tests
operation-ledger tests
portability tests
existence-only tests
```

Each of the ten gaps must have at least:

```text
one positive regression
one adversarial regression
```

Do not treat test count alone as proof.

---

# 37. Re-run Previous Independent Checks

Run the preserved Repair 01 independent check tools read-only against Repair 02
outputs where compatible.

Do not modify them.

Record:

```text
assertions now passing
assertions superseded by stronger checks
assertions still failing
assertions no longer applicable
```

Every prior material gap must either pass directly or be replaced by a stronger
passing Repair 02 assertion.

Do not dismiss failures merely because output structure changed.

---

# 38. Dominium Immutability

Run all supported seam operations against a temporary Dominium repository and
the pinned local Dominium checkout where safe.

Before and after compare:

```text
HEAD
refs
index
config
tracked worktree
untracked inventory
ignored inventory
selected source bytes
status
```

No Dominium file, ref, branch, index, config, ignored cache, or worktree may
change.

Separate benign filesystem metadata changes from content/ref/index/config
changes.

---

# 39. No Runtime-Capability Expansion

Confirm Repair 02 introduced none of:

```text
Dominium command invocation
Host runtime
Host SDK
Workbench implementation
bridge runtime
service
database runtime
network-backed seam operation
provider/model call
worker execution
PatchTransaction apply
DevelopmentTransaction
PreviewSession
preview/apply/rollback
target-repository mutation
branch/worktree automation
GitHub mutation
release or promotion
```

A runtime dependency manifest is not a plugin runtime or service.

A portability subprocess is not worker dispatch.

No new CLI operation may grant execution authority.

---

# 40. Report Consistency

Cross-check:

```text
Repair 02 status.yaml
repair-report.json
remaining-gap-disposition.json
test-summary.json

current seam-bundle.json
source-snapshot.json
projection-index.json
validation.json
conformance-results.json
conformance-assertions.json
compatibility.json
demo-result.json
fixture-manifest.json
portability-result.json
runtime-dependency-manifest.json

interop seam bundle
bridge manifest
conformance expectations

task evidence
```

Verify agreement on:

```text
task ID
source revision
record count
fixture count
test count
registry counts
conformance count
passed count
operation counts
forbidden count
portability result
output hashes
warning count
non-capabilities
recommended next task
```

Any material contradiction fails the check.

---

# 41. New Regression Search

Look beyond the ten known gaps.

Specifically probe:

```text
schema allows wrong field types despite required keys
schema kind/spec cross-substitution
false-boundary field declared but not required
unbounded unknown authority field
registry summary digest circularity
registry selected-ID order ambiguity
fixture remove missing key silently succeeds
fixture negative array index
operation unique-count/raw-count confusion
coverage set true without guard
forbidden Git verb classified as read-only family
raw operation trace not auditable
dependency manifest generated from same hard-coded list it claims to prove
isolated process inherits original PYTHONPATH
two missing output files compare equal
Dominium absolute path omitted from path-leak scan
conformance assertion description does not match implementation
unsupported-operation assertion checks only next-task ID
no-write assertion trusts only a self-declared flag
network assertion trusts only status fields
```

A new material defect routes to Repair 03.

---

# 42. Material Failure Conditions

Return `REQUEST_CHANGES` for any material defect, including:

```text
registry source digest or Git object mismatch
registry summary counts or ID digests incorrect
undisclosed truncation
public schema accepts wrong required-field types
public schema allows cross-kind record substitution
required false-boundary status can be removed
authority-changing unknown field bypasses validation
any negative fixture fails replay
fixture replay permits unsafe or ambiguous operation
any required semantic fixture code is absent
conformance result lacks required fields
conformance assertion is semantically unrelated to its description
aggregate-only conformance can return PASS
operation counts do not reconcile
coverage is declared without enforceable guard
forbidden operation executes
forbidden Git verb classified incorrectly
runtime dependency manifest incomplete or incorrect
isolated run imports from original checkout
required output missing in both isolated roots
portable output contains an absolute local path
cross-process deterministic bytes differ
Dominium changes
a previously closed original finding reopens
report contradiction
missing required evidence
```

If material findings exist, recommend exactly:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03
```

Do not repair them in this task.

---

# 43. Warning Conditions

Warnings may remain for:

```text
offline-only seam
pinned Dominium revision behind remote
no Host runtime
no Workbench
no bridge runtime
no service
no transport
no providers or workers
no command invocation
no preview/apply/rollback
minimum Python 3.11 not executed locally
platforms not executed
bounded registry projection with complete provenance and disclosure
```

Warnings are acceptable only when claims remain narrow and truthful.

---

# 44. Required Queue Surfaces

Materialize:

```text
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/task.yaml
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/ExecPlan.md
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/prompt.md
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/status.yaml
.aide/queue/AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02/evidence/
```

Register the task in `.aide/queue/index.yaml`.

Update only:

```text
PLANS.md
IMPLEMENT.md
```

as required by queue law.

---

# 45. Required Reports

Write consolidated reports under:

```text
.aide/reports/dominium-readonly-seam-v0-repair-02-check/
```

Required:

```text
status.md
check-report.json
ten-gap-closure.json
ten-gap-closure.md
five-finding-closure.json
five-finding-closure.md
source-chain-review.md
registry-provenance-review.md
schema-contract-review.md
fixture-replay-review.md
conformance-shape-review.md
conformance-semantic-review.md
operation-ledger-review.md
runtime-dependency-review.md
portability-determinism-review.md
dominium-immutability-review.md
report-consistency-review.md
new-regression-review.md
warning-disposition.md
explicit-non-capabilities.md
next-task-prompt.md
```

`check-report.json` must contain each independent assertion with:

```text
id
category
description
outcome
severity
expected
observed
evidence_refs
source_gap_id where applicable
source_finding_id where applicable
```

---

# 46. Required Evidence

Record at minimum:

```text
live AIDE branch, HEAD, and worktree
full Repair 02 commit SHA
complete build/check/repair source chain
historical evidence immutability
Repair 02 evidence completeness
Repair 02 changed-file review
ten-gap closure
five-original-finding closure
registry byte/hash/Git-object recomputation
schema-validator results
wrong-type schema cases
all fixture replay results
five formerly failing fixture results
conformance shape results
conformance semantic injections
operation count reconciliation
operation family injection results
dependency manifest verification
independent import graph
sanitized isolated process results
required output completeness
cross-process hash comparison
absolute-path leak scan
Dominium before/after state
focused test results
broad AIDE validation
strict secret scan
unsupported operation probes
recommended next task
```

---

# 47. Validation Matrix

Run all applicable commands:

```bash
git status --short --branch
git diff --check
git diff --cached --check

git rev-parse 1e8889e
git show --no-patch --format=fuller 1e8889e

py -3 -m compileall \
  core/interop/dominium \
  core/protocol \
  .aide/scripts/tests

py -3 -m unittest discover \
  -s .aide/scripts/tests \
  -p "test_aide_dominium_readonly_seam*.py"

py -3 .aide/scripts/aide_lite.py dominium-seam status
py -3 .aide/scripts/aide_lite.py dominium-seam snapshot
py -3 .aide/scripts/aide_lite.py dominium-seam project
py -3 .aide/scripts/aide_lite.py dominium-seam validate
py -3 .aide/scripts/aide_lite.py dominium-seam diff
py -3 .aide/scripts/aide_lite.py dominium-seam demo

py -3 .aide/scripts/aide_lite.py task inspect \
  --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

py -3 .aide/scripts/aide_lite.py task evidence \
  --task-id AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

py -3 .aide/scripts/aide_lite.py task inspect \
  --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

py -3 .aide/scripts/aide_lite.py task evidence \
  --task-id AIDE-CHECK-DOMINIUM-READONLY-SEAM-V0-REPAIR-02

py -3 .aide/scripts/aide_lite.py validate
```

Also run:

```text
independent ten-gap harness
independent registry provenance checker
independent Draft 2020-12 schema validation
wrong-type and cross-kind schema matrix
independent 32-fixture replay
fixture replayer abuse matrix
conformance shape checker
conformance semantic injection matrix
aggregate-conformance fail-closed check
operation-ledger reconciliation
Git verb classifier matrix
operation-family injection matrix
serialized dependency-manifest verification
independent AST import closure
sanitized manifest-driven isolated runs
fresh-process and hash-seed determinism runs
required output set comparison
absolute-path leak scan
Dominium full-state before/after comparison
previous independent-check tool reruns
secret-like scan
commit-policy validation
```

Restore unrelated generated churn before completion.

---

# 48. Result Classification

Use the established result vocabulary.

Successful result:

```text
PASS_WITH_WARNINGS
material_finding_count: 0
```

Failure result:

```text
REQUEST_CHANGES
```

Do not accept partial closure.

---

# 49. Exit Criteria

Stop at `needs_review` only when:

* all ten Repair 02 gaps are independently closed;
* all five previously open original findings are independently closed;
* the thirteen already-closed findings remain closed;
* registry provenance independently verifies;
* the public schema constrains field presence, type, kind, and status boundaries;
* all 32 negative fixtures independently replay;
* all five formerly failing fixtures emit required semantic codes;
* fixture replay is strict and non-executable;
* all 23 conformance results are structurally and semantically valid;
* aggregate-only conformance cannot pass;
* operation counts and observation counts reconcile;
* every operation family has an actual guard and tested injection;
* forbidden Git operations are refused before execution;
* dependency manifest is complete and hash-valid;
* isolated execution uses only serialized manifest contents;
* sanitized fresh processes succeed;
* every required portable output exists;
* deterministic outputs are byte-equal;
* no absolute path leaks;
* Dominium remains unchanged;
* no capability boundary is broadened;
* reports and evidence are complete;
* exactly one next task is recommended.

If all conditions pass, recommend exactly:

```text
AIDE-ACCEPT-DOMINIUM-READONLY-SEAM-V0-01
```

Otherwise recommend exactly:

```text
AIDE-BUILD-DOMINIUM-READONLY-SEAM-V0-REPAIR-03
```

Generate the selected next-task prompt, but do not begin or execute it.

```

This check is the right final gate before acceptance: narrower than the prior checks, but stricter about whether the new evidence actually proves the claims it labels as passing.
```
