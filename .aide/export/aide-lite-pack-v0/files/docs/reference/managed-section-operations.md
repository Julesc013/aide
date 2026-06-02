# Managed Section Operations

Managed-section transaction records describe edits bounded by explicit begin and end markers. A valid managed-section operation records the target path, section id, marker strings, preimage hash, predicted postimage hash, staged replacement, rollback record, and safety gates.

AIDE-APPLY-00 can plan and verify managed-section records in fixtures only. It does not write managed sections to active repository files and does not remove managed sections.

Future managed-section patching must preserve manual content outside markers, reject missing or duplicated markers unless explicitly reviewed, record preimages before postimages, and create rollback records before any reviewed apply step.
