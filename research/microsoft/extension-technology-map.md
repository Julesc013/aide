# Microsoft Extension-Technology Map

## Purpose

This document explains why AIDE uses the existing Microsoft lane names in `hosts/microsoft/**` and where those names are exact mappings versus conservative architectural umbrellas.

## Mapping Table

| AIDE lane | Intended meaning | Mapping quality | Evidence |
| --- | --- | --- | --- |
| `com-addin` | Pre-VSIX legacy-native Windows Visual Studio extensibility umbrella. | Conservative AIDE abstraction. | Current Microsoft lifecycle material still distinguishes the older releases, but the prompt scope does not fully reconstruct every pre-2010 contract family. |
| `vsix-v1` | Visual Studio 2010-era VSIX packaging lane. | Close architectural mapping. | Microsoft archived documentation for Visual Studio 2010 explicitly references a `VSIX Project` template and VSIX output. Source: https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/gg241221%28v%3Doffice.14%29 |
| `vsix-v2-vssdk` | Visual Studio 2012-and-later VSIX 2.0 plus VSSDK lane. | Close architectural mapping. | Microsoft documents VSIX schema 2.0 as introduced in Visual Studio 2012. Source: https://learn.microsoft.com/en-us/visualstudio/extensibility/vsix-extension-schema-2-0-reference?view=vs-2022 |
| `extensibility` | Modern VisualStudio.Extensibility lane for current Windows Visual Studio contracts. | Exact product-family mapping at the SDK level, not a whole-host replacement claim. | Microsoft's VisualStudio.Extensibility material describes a new SDK, modern APIs, and out-of-process execution. Sources: https://devblogs.microsoft.com/visualstudio/the-future-of-visual-studio-extensibility-is-here/ and https://devblogs.microsoft.com/visualstudio/visualstudio-extensibility-17-9/ |
| `monodevelop-addin` | Native Visual Studio for Mac extension lane derived from Xamarin Studio and MonoDevelop add-in behavior. | Conservative but well-supported mapping. | Microsoft's archived Visual Studio for Mac material ties the product directly to Xamarin Studio and MonoDevelop and documents add-in-oriented extension tooling. Sources: https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/connect/visual-studio-development-%E2%80%93-introducing-visual-studio-for-mac and https://learn.microsoft.com/en-us/archive/msdn-magazine/2017/december/visual-studio-customizing-visual-studio-for-mac |
| `companion` | Out-of-process AIDE fallback lane for constrained, retired, or deferred Microsoft host families. | Explicit AIDE abstraction, not a Microsoft label. | Microsoft retirement guidance for Visual Studio for Mac points to alternatives outside a native in-host extension path, which justifies keeping an adjacent AIDE lane without calling it official Microsoft extensibility. Source: https://devblogs.microsoft.com/visualstudio/visual-studio-for-mac-retirement-announcement/ |

## Fact

- Microsoft's sources support a real breakpoint between pre-VSIX Visual Studio, VSIX in Visual Studio 2010, VSIX schema 2.0 in Visual Studio 2012, and newer VisualStudio.Extensibility work in the Visual Studio 2022 era.
- Microsoft's Visual Studio 2026 extension-compatibility guidance is still centered on VSIX-based extensions and their compatibility with 2022-built extensions. Source: https://devblogs.microsoft.com/visualstudio/modernizing-visual-studio-extension-compatibility-effortless-migration-for-extension-developers-and-users/

## Inference

- AIDE keeps both `vsix-v2-vssdk` and `extensibility` because Microsoft's current material supports coexistence rather than a clean one-step replacement.
- AIDE keeps `com-addin` rather than renaming it in this prompt because the existing repository doctrine prefers version-neutral compatibility lanes and later legacy prompts can split the pre-VSIX family only if the research payoff justifies it.

## Future Refinement

- A later Microsoft-legacy prompt may split the `com-addin` umbrella if official source coverage is strong enough to justify narrower lanes.
- A later modern-Visual-Studio prompt may need to refine how `vsix-v2-vssdk` and `extensibility` coexist across Visual Studio 2022 and 2026 once AIDE starts implementation work.

