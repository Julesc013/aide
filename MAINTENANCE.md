# AIDE Maintenance

## Purpose

Maintenance in AIDE keeps the repository coherent as research, implementation, verification, and environment work evolve at different speeds. The goal is to preserve accuracy, not to create process for its own sake.

## Recurring Maintenance Domains

### Root Docs

- keep `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `MAINTENANCE.md`, `PLANS.md`, `IMPLEMENT.md`, and `DOCUMENTATION.md` aligned with actual repository state
- remove stale bootstrap or placeholder language when phases advance

### Governance Alignment

- confirm that new docs or implementation work still follow `governance/` law
- avoid silently redefining naming, support, capability, or release policy

### Inventory And Matrix Synchronization

- keep ids stable across `inventory/`, manifests, and matrices
- ensure support, capability, feature, test, packaging, and platform posture still reflect actual evidence
- keep committed families distinct from candidate families

### Research Corpus Hygiene

- keep source-backed research separate from implementation state
- keep unresolved items explicit when research gaps remain
- avoid duplicating research prose into manifests or matrices

### Environment And Lab Hygiene

- keep environment catalogs factual and explicit about bootability, blockers, and provenance
- keep labs as the place for partial or blocked work until it is ready for promotion

### Eval And Report Hygiene

- add run records and audit reports when implementation or verification actually occurs
- keep eval catalogs and test posture aligned with what was really checked

### Packaging And Release-Shape Hygiene

- keep packaging posture honest while the repo remains pre-product
- avoid implying releasable artifacts before manifests, evidence, and review are in place

### Backlog And Candidate-Family Hygiene

- keep `inventory/legacy-ide-families.yaml` conservative
- update candidate guidance only when research or implementation changes justify it
- do not promote new committed host families without corresponding research, inventory, matrix, and documentation work

## How Future Work Should Update These Domains

- update root docs when phase status or repo shape materially changes
- update matrices and eval records with the same diff that changes host-lane proof posture
- update environment or lab records when acquisition, bring-up, or blocker reality changes
- update research docs when a new source-backed fact changes how a lane should be understood
- update maintenance assets when recurring review work becomes clearer or more automatable

## Honesty Rules

When a lane or system is blocked, degraded, deferred, or unverified:

- say so explicitly
- keep the blocker or deferral reason attached to the relevant matrix, manifest, report, or run record
- do not replace a blocked native path with polished prose that implies it is solved

## Manual Now Versus Automation Later

Manual now:

- most cross-document review
- matrix and manifest consistency review
- host-lane state interpretation
- backlog and candidate promotion judgment
- final audit of blocked or deferred posture

Good candidates for later automation:

- path and file existence checks
- basic id cross-reference checks
- stale placeholder detection
- matrix field-shape validation
- report presence checks after implementation waves

Human-reviewed even if partially automated later:

- roadmap changes
- candidate-family promotion decisions
- support-tier or capability posture interpretation
- blocker and deferral judgment
