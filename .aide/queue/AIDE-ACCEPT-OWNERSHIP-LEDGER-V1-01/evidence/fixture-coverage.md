# Fixture Coverage

Fixture coverage is accepted with warnings after the Repair 01 check verified:

- valid fixtures for all eleven ownership classes;
- valid managed-section manual-outside preservation;
- valid optional extension round trip;
- invalid path, case, duplicate, evidence, source, digest, symlink, reparse,
  unknown-required-feature, and required-extension cases;
- invalid managed-section identity, marker, overlap, nested ambiguity, and
  file-section conflict cases;
- Q43 supported map, manual-review map, and unmapped-class refusal cases.

Fixture coverage is sufficient for accepting `ownership_ledger_v1` as
classification and preservation metadata. It is not install/update/apply proof.
