# Mandatory stable-profile obligations (working control)

This tracks the adopted `specs/control-plane/product/scope-and-profiles.md`
baseline. A source test is not whole-product release evidence.

| Journey | Code owner | Exact current check | Delivered evidence | Remaining blocker and next action |
|---|---|---|---|---|
| Obtain and run without checkout | Portable export and release builder | `test_export_import.py`; `release validate` | ZIP/tar extracted consumer at dev `3bdeb220` | Requalify final integrated bytes, then consumer acquisition from published asset. |
| Initialize new project | `import-pack` | `test_import_fixture_creates_templates_and_preserves_agents` | Fresh ZIP consumer APPLIED and doctor PASS | Establish full first-run project profile acceptance. |
| Adopt brownfield safely | `import-pack` and observation | `test_import_preserves_authored_agents_bytes_outside_portable_section` | Brownfield tar consumer preserved owner files | Expand supported brownfield recovery and qualification. |
| Customize and explain update | `import-pack` ownership/explanation | New tests in this WorkUnit | Pending final archive consumer | Implement and qualify matching/stale rationale, conflict, explicit feedback now. |
| Diagnose and repair | `repair` planners | Existing repair suite; no final apply test | Planner only | Implement admitted apply behavior and delivered recovery test. |
| Roll back | `rollback` planners | Existing rollback suite; no final apply test | Planner only | Implement admitted recovery apply behavior and delivered test. |
| Detach owned material | `uninstall` planner | Existing uninstall suite; no deletion test | Planner only | Implement owner-scoped removal apply and preservation test. |
| Continue offline | Lite local commands | `doctor`, `validate`, extracted consumer | Local pack consumer, no model/network calls | Qualify final environment and unavailable-capability behavior. |
| Stable publication and update | Release generator and publication route | `release validate`, deterministic replay | Local assets only | Exact main review, authorized publish, remote-byte and downloaded update proof. |

Native Windows privilege and separately admitted hosted behavior keep their
own gates. This matrix does not expand the baseline to every optional surface.
