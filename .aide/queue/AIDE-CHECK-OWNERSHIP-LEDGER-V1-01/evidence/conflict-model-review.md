# Conflict Model Review

Independent probes found missing conflict behavior:

- A duplicated `target_path` with a different record id validates.
- A case-fold collision between `Readme.md` and `README.md` validates.
- No conflict model detects section overlap, file/section ownership conflict,
  nested ownership ambiguity, source component mismatch, source distribution
  mismatch, unknown owner, or missing required evidence refs.

Disposition: material finding `ownership.conflict_model_incomplete`.
