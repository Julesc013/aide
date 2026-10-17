# Current-task view source outcome

The existing `task current` command now accepts `--task-id ID` and `--json`.
Both formats show the same bounded observation of the objective, recorded
outcome, owner, next action, remaining obligations and evidence availability.
Planning declarations cannot overwrite recorded status. Missing or conflicting
facts remain visible; present evidence does not imply verified acceptance.

Source c7ea89dc and fixture repair 0f6182d6 received independent source/effect
acceptance. The first job ran 51 methods, passing the 29 original tests but
reporting eight setup errors across five new methods. The repaired final job
passed all 22 affected methods plus three actual CLI smokes without skips.
The original failure remains in evidence. No product assertion was weakened.
Both jobs were collected, verified, quiesced and retired with reservations freed.

The live smoke correctly distinguishes completed DiskEd preparation from its
unfinished target adoption. No downstream repository was changed. No model
calls were made; complete model/controller effort is unknown. This establishes
the bounded source behavior, not a new package, release or host support claim.

See `evidence/first-attempt-result.json` and `evidence/final-result.json` for exact
subjects, tests, smoke identities, retained digests and resource observations.
