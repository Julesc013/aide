# Apple Extension Technology Map

Primary sources: [XcodeKit](https://developer.apple.com/documentation/xcodekit), [Creating a Source Editor Extension](https://developer.apple.com/documentation/XcodeKit/creating-a-source-editor-extension), [App Extensions Increase Your Impact](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/), [Creating an App Extension](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionCreation.html), [Xcode support matrix](https://developer.apple.com/support/xcode).

## Lane map

| AIDE lane | What it represents | Mapping quality | Notes |
| --- | --- | --- | --- |
| `xcodekit` | Apple's documented Xcode Source Editor extension surface through XcodeKit. | Exact enough for current AIDE planning. | Native, editor-centric, menu-invoked, containing-app based. |
| `companion` | Out-of-process fallback for older Xcode families or broader workflows that exceed the public XcodeKit surface. | Deliberate AIDE abstraction. | Not an Apple product label and not a claim of native parity. |

## Facts

- `xcodekit` is grounded in Apple's public API and extension-point documentation.
- Apple documents the Xcode Source Editor extension point as a scoped macOS app extension, not as a whole-IDE plug-in platform.

## Inferences

- `companion` is the honest place to put work that needs project-aware, service-oriented, or cross-process behavior that Apple does not expose through the public XcodeKit surface.
- For older Xcode families, `companion` is also the conservative umbrella because the source set used here does not establish a current public native lane equivalent to XcodeKit.

## Later refinement likely needed

- Pre-XcodeKit native extension history for older Xcode families may deserve a more exact archival map if later official Apple sources justify it.
- Packaging and installation details for a future AIDE companion should be refined in later packaging and environment prompts, not here.
