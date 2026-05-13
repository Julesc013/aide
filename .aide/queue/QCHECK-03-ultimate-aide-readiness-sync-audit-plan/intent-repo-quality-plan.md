# Intent Compiler, Repo Intelligence, and Quality Plan

## Q36 Intent Compiler And Prompt Normalization v0

Purpose: compile raw user prompts into bounded WorkUnits before execution.

Required inputs:

- raw prompt text;
- repo identity;
- queue index;
- current task packet;
- branch role;
- dirty state;
- target repo policy;
- allowed and forbidden paths;
- existing WorkUnit/task evidence;
- validation commands.

Required outputs:

- normalized intent;
- task class;
- risk class;
- one-shot/two-shot/split recommendation;
- dependency check;
- branch preflight;
- context packet request;
- evidence requirements;
- no-op or resume decision;
- blocked reason when unsafe.

Acceptance:

- Repeated prompts no-op or resume from repo state.
- Broad prompts split into bounded WorkUnits.
- Wrong repo prompts block or redirect.
- Target mutations require target repo context.
- Generated WorkUnit packets are compact and evidence-backed.

## Q37 Repo Intelligence Index v0

Required indexes:

- file inventory;
- root inventory;
- ownership map;
- dependency map;
- test map;
- doc-link map;
- source-of-truth map;
- generated/manual map;
- command map;
- target tool map.

Acceptance:

- Deterministic JSON and Markdown outputs.
- No product behavior changes.
- No source content dumps.
- Target tools are classified, not replaced.

## Q38 File Quality Ledger v0

Required signals:

- stale path refs;
- orphan files;
- unowned files;
- duplicate policy records;
- docs consistency issues;
- missing tests;
- generated artifact drift;
- large-file prompt risk;
- low-reuse/high-duplication areas;
- boundary-risk roots.

Acceptance:

- Ledger is advisory.
- No automatic refactor.
- No deletion.
- Findings are evidence-backed and path-specific.
