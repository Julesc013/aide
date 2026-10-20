### Packaging and release shape

AIDE Lite 1.1 has a published portable package for its exact local Windows CLI profile. Newer development lifecycle evidence covers four exact modern environments; a multi-profile 1.2 package still requires its own qualified archives and public contract. Other host, native-extension and service shapes remain declarations or planned capabilities until their own evidence exists. [Release policy](../governance/release-policy.md) governs versions, pre-tag documentation, publication and acquired-byte acceptance.

**Deliverables**

- ZIP and TAR.GZ archives may carry the same portable payload; use one product version and verify both exact identities.
- New multi-profile metadata describes exact environments, capabilities and supported/refused/unqualified command sets over that shared payload. Preserve historical v1 Windows identities and predecessor behavior; [profile declarations](../docs/reference/lite-release-profiles.md) grant no execution or publication effects.
- Manifests and checksum files accompany the downloadable packages. Retain stable machine filenames and meaningful human display labels.
- A release title identifies product/version once. The body presents grouped changes, upgrade instructions, downloads and relevant limitations with logical paragraphs and compact lists.
- Packaging matrices and catalogs describe maintenance/support posture; they do not establish shipment, signing or parity.
- Historical and archival lanes may use different packaging or fixed-width transport profiles. Apply those requirements to explicit outputs rather than hard-wrapping canonical public Markdown.

**Ownership and preservation:** project customization, task history, evidence and unknown ownership remain protected by the applicable lifecycle contracts. New pack contents or metadata do not silently widen support. Preserve frozen/public artifacts and their provenance; new bytes require a new qualified subject.

The original bootstrap packaging placeholders remain history. Actual release records must identify what was built, qualified, published and acquired.
