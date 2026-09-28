# Turn-boundary subtotal repair

- Base: `dev@ef938eef1b78218cadb6a5cc97702abe6e8d47e2`, tree `25ce3e5846c9e390ee1e190e924fde63b7c8e10f`.
- Scope: portable `job usage` importer, one regression and this WorkUnit.
- Red: configured D-managed job `bdfa68a448f14f17a2280cdb3290609b` ran `python -m unittest discover -s .aide/scripts/tests -p test_efficiency_wait.py -v`; 18 cases, one expected assertion failure (`None != 6`), 17 passed. Receipt SHA-256 `33248a9d3ef120dd695e1dd88ddd59b9e59ebf2bdddfe8108a93373a4c661a1f`.
- Green: same command and runner, job `6da5799b571b4b7dae42b76c8bc6620b`; 18/18 passed. Receipt SHA-256 `d87a0c223fbebdb924ba32054418cf6d45974b49cd04af957592d1affe0290e6`.
- Both receipts report quiescent exit, retired scratch and released reservation. Green peak observed memory: 295,247,872 bytes; scratch: 3,329 bytes.
- The repair excludes a boundary-ambiguous record from known subtotals. It retains valid distinct-session known usage, the same-session overlap guard, partial status and unknown full totals.
- No model request was made by this observer. No live model usage, independent source verdict, current-byte release qualification or publication is claimed.
