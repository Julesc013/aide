# Apple Open Questions

## Unresolved lineage items

- The official source set used in this prompt verifies Xcode 1 through Xcode 16 and Xcode 26, but it does not justify fabricating Xcode 17 through Xcode 25 as distinct major families.
- The exact first shipping breakpoint for the public XcodeKit and Xcode Source Editor extension surface is not pinned to one decisive Apple release-note page in the gathered source set.

## Unresolved extensibility items

- The public Apple sources gathered here do not establish a deeper general-purpose native Xcode plug-in contract beyond the source-editor surface that XcodeKit exposes.
- Pre-XcodeKit extensibility history for older Xcode families remains under-documented in the currently gathered official source set.

## AIDE abstraction notes

- The `companion` lane is an AIDE abstraction, not an Apple product label.
- For older Xcode families, `companion` currently means "fallback because no current public native lane is established in this prompt," not "Apple officially recommended this architecture."

## Deliberate deferrals

- Exact packaging and installation details for future Apple-native or companion artifacts are deferred to later packaging prompts.
- Environment acquisition, signing, notarization, and distribution rehearsal are deferred to later lab and packaging prompts.
