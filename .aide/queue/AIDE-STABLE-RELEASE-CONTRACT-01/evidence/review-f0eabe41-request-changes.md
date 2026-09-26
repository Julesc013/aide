# Stable interface contract review — f0eabe41

## Verdict

**REQUEST_CHANGES** — two new contract statements exceed the unchanged implementation's boundaries. Correct those descriptions or explicitly identify them as future qualification requirements before accepting this exact policy/doc candidate. No change to shipping state or source implementation is authorized by this review.

## Exact subject and scope

- Commit: `f0eabe41265d9ff9a4388ccef4ef5c31c3e49854`
- Tree: `2a6b1d9608851d1ab5e0fcd3a2503c2ceb7af6bc`
- Parent: `119529d076fdce289cacbb1737e8abf2582fe6fd`
- Subject: `fix(contract): retain customization and partial recovery interfaces`
- Existing checkout reused read-only: `D:\Projects\AIDE\aide-stable-lite-partial-import-recovery`
- Reviewed frozen release-versioning policy, product/reference doc delta, relevant existing import/customization/feedback/recovery functions, parser-only evidence, and follow-up scope/gates. Production Lite, core and generated artifact paths are unchanged by this commit.
- No new checkout, fixture, probe, agent, full suite, source edit or Git ref edit. The only reviewer-created file is this external report; no owned temporary fixture or live process remains.

## Findings

### 1. Feedback output exclusion names all packs, but only the incoming pack is checked

**Blocking policy/doc consistency finding.** New `.aide/policies/release-versioning.yaml` `customization_contract.feedback_rule` says the new local output is outside both the target and "packs". The new product-scope paragraph repeats that plural boundary. Existing `command_import_pack` (Lite line 43151) passes only `pack_root` and `target_root` into `write_import_feedback` (line 41245). The latter excludes descendants of those two roots, not `predecessor_pack`. This matters for the newly enumerated predecessor/resolution feedback forms.

Concrete static reproducer, not executed: with separate valid `new-pack`, `old-pack` and `target` roots and a complete predecessor dry-run plan, use:

```text
py -3 -I -B <new-pack>/files/.aide/scripts/aide_lite.py --repo-root <target> import-pack --pack <new-pack> --from-pack <old-pack> --target <target> --mode safe --dry-run --explain --feedback-out <old-pack>/feedback.json
```

For a new `feedback.json` in the existing predecessor root, the feedback helper's new-file check succeeds and its incoming-pack/target exclusion predicates do not match. It then opens that predecessor-local path with `"x"`. No later predecessor-root check exists. This is a source branch proof, not a claimed lifecycle test.

Requested correction: state the current exclusion precisely as target plus **incoming** pack, or explicitly record all-supplied-pack exclusion as an unimplemented final qualification requirement with no current-behavior claim. If the owner requires refusal for every supplied pack, keep that as a separate source qualification repair; this doc-only patch cannot claim it already holds. The preexisting detailed feedback documentation and parser help say "pack and target" singular and agree with the implementation.

### 2. Legacy/all-pending recovery refusal wording exceeds the partial-classification checks

**Blocking policy/doc consistency finding.** New `partial_recovery_contract` broadly says recovery requires exact original inputs for the saved pending import and that legacy intents without a full saved plan remain retained refusals. The full-snapshot and supplied digest/pack/predecessor/mode/controls/resolution checks are indeed present in `recover_partial_import` (line 42133), and it refuses a legacy **partial** intent lacking a snapshot. However `_apply_import_pack_unlocked` (line 42484) routes only classification `partial` to that function. Its unchanged `completed` branch reconciles stored receipt publication and retires the intent without requiring `plan_snapshot` or matching the supplied expected digest/mode/pack to the original intent. Its `no_effect` branch also has separate retirement behavior. `load_portable_import_intent` and `classify_portable_import_recovery` do not require a snapshot for those classifications.

Concrete static reproducer, not executed: take a valid legacy intent with no `plan_snapshot`, whose recorded operations all currently match their postimages and whose backups are absent. The classifier returns `completed`. On Windows, call safe `import-pack --recover-partial --expect-plan <different-valid-64-hex-digest>` with a separately valid pack and that target. After checksums/shape classification, the completed branch uses `pending["next_receipt"]` and retires the intent; the supplied digest and missing snapshot are not checked there. It can return `RECOVERED`, rather than the broadly documented retained refusal. This is existing completed-state reconciliation, not new payload replay.

Requested correction: limit the new exact-input/full-snapshot/refusal promise expressly to **continuing payload writes for a partial import**, and describe legacy **partial** intents as retained refusals. Preserve the separate existing completed/no-effect reconciliation behavior without broadening this review into a source recovery audit. Alternatively, declare a stronger all-pending policy as unimplemented qualification work rather than documenting it as existing behavior.

## Confirmed correct portions

- All 28 final candidate command forms appear exactly in the frozen parser receipt; required `<task>` and `<evidence-path>` placeholders are now present. Added explanation/local-feedback/recovery forms preserve explicit predecessor and resolution inputs.
- Existing metadata IDs are exactly `aide.project-customizations.v1` and `aide.project-customizations.v2`, at `.aide/customizations.json`. Incoming payload collision checks reserve that path, including case/trailing-dot aliases. No metadata is automatically supplied by a pack.
- `load_project_customizations` validates explanatory entries; `explain_import_result` only shows a rationale when its observed digest matches the plan preimage and currently observed bytes. Otherwise rationale remains unknown. Rationale does not grant ownership or mutation authority.
- Strict v2 controls validate supported/nonduplicate feature IDs and preserve prior disabled intent: missing controls, malformed v2, or downgrade to non-v2 with prior disabled features refuses silent reenablement. The currently implemented optional feature is only `local_state_examples`, scoped to `.aide.local.example/`; this does not make core files optional.
- Feedback requires explicit `--feedback-out` plus dry run and a complete plan, uses exclusive new-file creation, and writes a local manual-share packet. The reviewed command/helper contains no network/provider/model transmission. Separate sharing authorization remains intact.
- Partial-classification continuation is Windows-only, requires explicit apply mode and expected digest, validates the saved full plan/receipt, pack identities, mode, controls, exact resolution bytes/target set and preimage/postimage state. The new candidate is not evidence of delivered archive qualification.
- Final-manifest pinning for supported forms/options, metadata IDs and feature IDs is explicit. Version remains unselected; first qualified `1.0.0` is conditional on a fresh history check and frozen manifest. Activation requires frozen profile/source/tree/predecessors/assets/evidence and independent release ACCEPT. No promotion/publication/activation authority is introduced.
- Follow-up records preserve the previous accepted/integrated contract as historical work and keep this follow-up pending. Parent coverage/routing points to current work without implying permanent bulk placement or archive qualification.

## Verification commands and provenance

Reviewer verification performed:

1. `git show -s --format="%H %T %P%n%s" f0eabe41265d9ff9a4388ccef4ef5c31c3e49854` — identity/subject match above.
2. `git diff --check 119529d076fdce289cacbb1737e8abf2582fe6fd f0eabe41265d9ff9a4388ccef4ef5c31c3e49854` — PASS.
3. Exact Git delta and targeted existing function reads — source traces support the two findings above.
4. Compared frozen `candidate_public_cli` list with frozen `candidate-cli-check.json` rows — all 28 match, all recorded PASS, handlers invoked 0.
5. Independently verified frozen Lite and policy SHA-256 against the parser receipt, and all five code/policy/doc/checker bindings in `customization-contract-validation.json` against frozen Git blobs — PASS.
6. `git diff --name-only <parent> <candidate> -- .aide/scripts/aide_lite.py core .aide/export .aide/release` — empty; production/core/artifact bytes unchanged.

The parser check used the actual unchanged parser but did not invoke handlers or create fixtures. Its receipt correctly records precommit HEAD/base `119529d076fdce289cacbb1737e8abf2582fe6fd`; its policy and code hashes match this frozen candidate's exact bytes. It is not a clean candidate-HEAD lifecycle run. The earlier 25-form PASS and earlier two-placeholder-failure result have distinct policy hashes and remain separate, rather than being relabeled as 28 cases.

## Limitations and next review subject

No lifecycle handler, filesystem fixture, bulk test, artifact generator, archive or consumer was run by this reviewer. The source branch reproductions above were not executed. Syntax success is not runtime boundary qualification. Permanent storage placement and full delivered-artifact/Windows archive evidence remain open.

A narrowly scoped policy/doc correction addressing the two findings can be reviewed as a superseding delta while retaining this report unchanged. No broader scheduler, recovery or product audit is requested.
