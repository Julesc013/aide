# Initial exact-base integration plan

User authority: current explicit implementation, testing, documentation, synchronization, commits and normal merges through FacMan 0.1 Beta1. This admits the Q30 future branch operation; it does not rewrite Q30 historical restrictions.

Observed 2026-09-06 under BLACKGLASS-WIN1\Jules / GitHub Julesc013:
- AIDE local main: 7d8bf19d878fd9ad29859a6cba4b7de64ad80ecc.
- AIDE origin/main: c39f47ea3cdb2f8359722906f3f486f3c8af19b7.
- The three remote commits change README.md only; local README.md is unchanged.
- All local edits are the reviewed continuous-worker pilot, its tests/evidence/docs, the new programme admission, and generated AIDE helper/intake/context reports. No unrelated changes are staged or discarded.
- Pilot source manifest 9340793dac9777ae137fbc1c060b2d9c10383cfc761e15258f3f578f51b0cdee, 51 passing tests and independent assurance remain historical evidence for that exact source, not live activation proof.

Planned sequential operations:
1. Verify exact local/remote refs and unchanged README.md; fast-forward local main to observed origin/main while preserving the classified local edits. Git must refuse any collision.
2. Create local dev from that exact current origin/main and task/aide-continuous-worker-pilot-01 from dev. No reset, stash, worktree, deletion or history rewrite.
3. Repair portable export validation in this bounded change set, inspect every generated file, run required validation, and commit the reviewed source plus honest incomplete activation status using AIDE structured format.
4. Push the new dev base and task branch without force only after local validation; create a reviewed task-to-dev PR. Use normal required checks and independent assurance before merge, then reviewed dev-to-main promotion. Source commit never certifies a live worker.

The generic helper's dirty_tree_requires_classification is resolved by this inventory and the non-overlapping README-only upstream delta. Missing dev is resolved only by the explicit branch operation above under current user authority. No protected push of unreviewed source is authorized. Creating the previously absent dev at exact canonical main is bootstrap, not integration of new source.
