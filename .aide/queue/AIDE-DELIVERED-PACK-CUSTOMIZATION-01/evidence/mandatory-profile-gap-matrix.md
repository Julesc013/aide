# Mandatory stable-profile obligations (working control)

This tracks the adopted `specs/control-plane/product/scope-and-profiles.md`
baseline against the current local 1.0.0 ZIP (SHA-256 `27948415…`) on
2026-09-29. A source test or local consumer is not published-release evidence.

| Journey | Code owner | Exact current check | Delivered evidence | Remaining blocker and next action |
|---|---|---|---|---|
| Obtain and run without checkout | Portable export and release builder | Current ZIP/TAR six-consumer matrix in `AIDE-STABLE-LITE-RELEASE-EFFECT-01/evidence/current-runner-consumer-summary.json` | Six serial local consumers passed and retired scratch | Download and test the published asset after release. |
| Initialize new project | `import-pack` | Current ZIP `consumer_canary_runner.py` retained job `1fc7bdf5` | Fresh receipt digest `bfbe4185…`; no feedback created by default | Final downloaded-byte first-run check. |
| Adopt brownfield safely | `import-pack` and observation | Same current ZIP consumer job | Brownfield receipt digest `3f889770…`; earlier authored-file preservation tests | Final downloaded-byte brownfield check and declared support boundaries. |
| Customize and explain update | `import-pack` ownership/explanation | Current ZIP `consumer_canary_runner.py` job `1fc7bdf5`, plus source ancestry | Direct edit gave `PRESERVATION_REQUIRED`; V2 preview/apply refused conflict without changing bytes or receipt, resolved update applied; V3 conflict/resolution also passed. The oracle rejects invented rationale. | Downloaded-byte repeat and real published-successor update remain. |
| Diagnose and repair | Delivered `repair` apply | Current ZIP `lifecycle_canary_runner.py` retained job `f21eaf88`, output SHA-256 `3486ee10…` | `PASS`; owned-file repair applied and restart returned `RECOVERED` | Final downloaded-byte recovery and supported-environment check. |
| Roll back | Delivered rollback apply | Same current ZIP lifecycle job | `PASS`; rollback returned `ROLLED_BACK` using a synthetic successor | Qualify the real published predecessor/successor path where promised. |
| Detach owned material | Delivered removal apply | Same current ZIP lifecycle job | `PASS`; fresh and brownfield `DETACHED`, changed ownership `PARTIAL_REMOVAL` | Final downloaded-byte ownership/preservation check. |
| Continue offline | Lite local commands | Current ZIP `context_offline_canary.py` consumer and local Python socket guard | Local commands passed; no model request in the host-context canary | OS-level offline behavior remains unproven for child processes. |
| Stable publication and update | Release generator and publication route | Current ZIP SHA-256 `27948415…`; independent local technical acceptance and zero-change replay | Local asset and six-consumer qualification; remote `dev@005c8036` | Live-host efficiency and final effect acceptance, ten owner-only historical dispositions, main/tag/publication, remote-byte and downloaded update proof. |

The current ZIP lifecycle job `f21eaf88b56043f09fde3d83bb85e01a` is
retained under the approved D job root. Its receipt SHA-256 is
`222afd022ad4fce186a51936d8109d7aa64e9f627f6ec1a74edd25bec0ee7ee9`;
its `output/summary.json` SHA-256 is
`3486ee100782a3fb39b2f251d70f77dfccb83716ab46bd75a3fa1c67a283dfeb`.
The summary binds the current ZIP hash, reports `PASS`, and marks its
synthetic successor as unpublished. This corrects the older planner-only rows;
it does not claim a published upgrade/rollback path.

The current ZIP customization consumer summary SHA-256 is
`307036fc99e5acca5a56f3d9fc5a990da20e12d2bb38e8ea936ad326c54313f0`.
Its bound local oracle checks the direct-edit bytes and receipt before and
after refused V2 apply, then the resolved V2/V3 paths. The successor packs
are synthetic fixtures, not published release versions.

Native Windows privilege and separately admitted hosted behavior keep their
own gates. This matrix does not expand the baseline to every optional surface.
