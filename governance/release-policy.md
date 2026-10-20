### Release policy

**Current product state:** Lite 1.1.0 is published, acquired and consumer-verified; 1.0.0 remains preserved. Lite 1.2.0 exact archive/profile qualification is independently accepted and integrated at `3fec7ac3`; its separately admitted [publication WorkUnit](../.aide/queue/AIDE-LITE-1-2-PUBLICATION-01/ExecPlan.md) owns tag, publication and acquired-byte acceptance. Legacy native ports and future products remain staged. The [changelog](../CHANGELOG.md) and [current campaign](../.aide/queue/AIDE-CONVERGENCE-AND-DELIVERY-01/CURRENT.md) distinguish these states.

**Before every new tag**

1. Reconcile the README, relevant docs, root TODO, PLANS, ROADMAP and CHANGELOG with the exact intended release. Preserve historical records and classify remaining work accurately.
2. Confirm the public contract, version, qualified profile, predecessor/migration obligations, source and artifact identities, applicable checks and independent review. Resolve contradictory current claims before tagging.
3. Review concise release notes and human download labels. Use one physical line per paragraph or bullet in public Markdown; preserve structural breaks, code and explicitly required vintage-format exports. Let the renderer wrap prose.
4. Integrate the reviewed checkpoint through the project’s authorized Git workflow. Reobserve source/tree, refs, assets, permissions and the exact tag effect immediately before mutation.
5. Publish immutable assets, verify remote tag/release/asset identities, download the deliverables and complete applicable consumer acceptance. Refresh the current docs/checklist with observed outcomes.

These are the default AIDE-managed release requirements, including adopting projects. Project-owned document mappings and stronger rules take precedence; identify an absent or inapplicable surface explicitly rather than invent completed work. The filesystem queue owns work and acceptance; TODO is a compact navigation/checklist surface, PLANS holds detailed execution intent, and ROADMAP preserves direction. A report or preview never authorizes publication.

**Versions and names**

| Identity | Default |
| --- | --- |
| Product version | SemVer for an independently released deliverable and its declared public contract. |
| Lite tag / title | `aide-lite-v1.1.0` / **AIDE Lite 1.1.0**. |
| Prerelease | `aide-lite-v1.2.0-rc.1` / **AIDE Lite 1.2.0 RC 1**, when actually qualified and admitted. |
| Bundled components and archive formats | Share the product release version. |
| Independent extensions/runtimes | Separate versions only when independently packaged, released and governed by their own compatibility contract. |
| Whole repository source | Exact Git commit/tree; no separate numerical version for every internal module. |
| Schemas, protocols and profiles | Their own compatibility identities, recorded in the release manifest. |

Use patch versions for compatible fixes, minor versions for compatible additions and major versions for incompatible public-contract changes with reviewed migration/refusal and recovery. A commit type or breaking marker does not itself authorize a version bump. Source directories retain compatibility-technology names rather than release/version ranges.

**Release presentation and provenance**

- Keep the GitHub title short: product and version. Start the body with a useful summary, then a few H3/H4 sections, grouped change bullets, downloads, upgrade guidance and material limitations. Do not repeat the release title in the body.
- Give every downloadable deliverable a clear display label and a stable, machine-friendly filename. Identify platform/architecture only when it distinguishes real payloads. A label change must preserve asset identity and content.
- Record tag object/target/tree, payload source/tree, exact hashes and qualification separately. A frozen package may retain an earlier payload source when the reviewed tag identifies a later qualification/publication checkpoint; make the distinction explicit. GitHub’s automatic source archives are repository snapshots, not the portable install package.
- Published package bytes and existing tags are immutable. Presentation-only metadata corrections require a scoped review, preserved preimages and readback; they must not replace assets, rename files, retag or imply fresh product qualification.
- Support claims bind exact profiles, command/capability sets and evidence. Acceptance for one environment or route does not qualify another host, backend, model, platform, whole-session containment or whole-outcome efficiency. A declaration or candidate support tier is not activation; refused behavior and unqualified behavior remain distinct.
- Keep Q47/Q48 local bundles and drafts marked preview-only. Signing, notarization, protection changes and publication effects need their own actual authority and evidence.

**History:** the bootstrap sequence—inventory, matrices, scaffolding, harness, shared core, adapters, environments, evaluations and packaging—remains planning history. Current releases proceed through the qualified capability and contract gates above.
