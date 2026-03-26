# AIDE Evaluations

`evals/` is the control plane for AIDE evaluation, verification, evidence capture, and result reporting.

This area records:

- evaluation models and taxonomies
- verification categories and playbooks
- grader or routine definitions
- run and report shapes
- evidence expectations that support matrix and support claims

This area is not the same as:

- future code-level `tests` trees, which may hold executable checks later
- `matrices/`, which track support and verification posture but do not define eval models or store run records

Early AIDE phases emphasize deterministic structural verification. Later phases can add stronger smoke, workflow, packaging, and feature evals without changing the basic control-plane shape defined here.
