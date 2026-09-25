# AIDE-STABLE-LITE-TASK-TRUTH-01

Fix the proven empty-target `task status` truth defect from the independently
reviewed Windows Lite consumer. Accept only an explicit packet task identity
or a leading PHASE/GOAL identity; ignore incidental task IDs in guidance.
When the target queue is empty, report no selected WorkUnit rather than an
AIDE source phase. Keep the existing empty-queue command exit convention.
Write a red regression first, run affected tests, obtain independent exact
source review, then hand the accepted source to a separate current-generator
artifact projection and installed-byte qualification WorkUnit.
