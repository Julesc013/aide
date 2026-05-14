# Repair Model Report

## Summary

Q44 adds AIDE's generic Repair / Doctor Model v0. It observes AIDE install
health, diagnoses repair needs, classifies them, creates a candidate repair
plan, renders a dry-run summary, and produces an advisory doctor report.

## Policies

- `.aide/policies/repair.yaml`
- `.aide/policies/repair-classes.yaml`
- `.aide/policies/repair-safety.yaml`
- `.aide/policies/repair-detection.yaml`
- `.aide/policies/repair-verification.yaml`
- `.aide/policies/doctor.yaml`

## Schemas

- `.aide/repair/repair-observation.schema.json`
- `.aide/repair/repair-diagnosis.schema.json`
- `.aide/repair/repair-plan.schema.json`
- `.aide/repair/repair-operation.schema.json`
- `.aide/repair/repair-dry-run.schema.json`
- `.aide/repair/repair-report.schema.json`
- `.aide/repair/repair-classification.schema.json`
- `.aide/repair/doctor-report.schema.json`
- `.aide/repair/repair-verification.schema.json`

## Commands

- `repair observe`
- `repair diagnose`
- `repair plan`
- `repair dry-run`
- `repair validate`
- `repair status`
- `repair explain ISSUE_OR_PATH`
- `repair classes`
- `repair doctor`

## Generated Artifacts

- `.aide/repair/latest-repair-observation.json`
- `.aide/repair/latest-repair-observation.md`
- `.aide/repair/latest-repair-diagnosis.json`
- `.aide/repair/latest-repair-diagnosis.md`
- `.aide/repair/latest-repair-plan.json`
- `.aide/repair/latest-repair-plan.md`
- `.aide/repair/latest-repair-dry-run.json`
- `.aide/repair/latest-repair-dry-run.md`
- `.aide/repair/latest-doctor-repair-report.json`
- `.aide/repair/latest-doctor-repair-report.md`
- `.aide/repair/latest-repair-verification-plan.md`

## No-Apply Guarantee

- `no_apply: true` is present on the generated observation, diagnosis, plan, dry-run, and doctor report.
- Every generated repair operation has `apply_allowed: false`.
- Every generated repair operation has `overwrite_allowed: false`.
- Every generated repair operation has `delete_allowed: false`.
- Q44 implements no repair apply command and performs no target mutation.
