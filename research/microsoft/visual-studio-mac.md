# Visual Studio For Mac

## Major-Version Table

| Record id | Display name | Host OS | Vendor lifecycle | Primary AIDE lane | Notes |
| --- | --- | --- | --- | --- | --- |
| `vsmac2017` | Microsoft Visual Studio 2017 for Mac | `macos` | Out of support | `monodevelop-addin` | Lifecycle page gives exact dates through 2019-03-08. Microsoft's 2016 introduction article describes Visual Studio for Mac as an evolution of Xamarin Studio and as based on MonoDevelop. |
| `vsmac2019` | Microsoft Visual Studio 2019 for Mac | `macos` | Out of support | `monodevelop-addin` | Lifecycle page gives exact dates through 2022-05-23. The reviewed Microsoft extensibility material still points to the MonoDevelop-derived extension model. |
| `vsmac2022` | Microsoft Visual Studio 2022 for Mac | `macos` | Retired | `monodevelop-addin` | Lifecycle page shows the product family retiring on 2024-08-31, and Microsoft's retirement announcement confirms that cutoff and the product's archival-only future. |

## Fact

- Microsoft introduced Visual Studio for Mac in 2016 as an evolution of Xamarin Studio and states that it is based on the open source MonoDevelop IDE. Source: https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/connect/visual-studio-development-%E2%80%93-introducing-visual-studio-for-mac
- The lifecycle page for Visual Studio for Mac provides the overall family retirement date and the exact release dates for the 2017, 2019, and 2022 product lines. Source: https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-for-mac
- Microsoft documents an extension workflow for Visual Studio for Mac through the Extension Manager and references Add-in Maker for building extensions. Source: https://learn.microsoft.com/en-us/archive/msdn-magazine/2017/december/visual-studio-customizing-visual-studio-for-mac
- Microsoft announced that Visual Studio for Mac would be retired on 2024-08-31, receive no new framework, runtime, or language support after the announcement, and remain available only as a legacy installation after support ends. Source: https://devblogs.microsoft.com/visualstudio/visual-studio-for-mac-retirement-announcement/

## Inference

- `monodevelop-addin` is the correct conservative AIDE lane name for Visual Studio for Mac native extensibility because Microsoft's own material ties the product to Xamarin Studio and MonoDevelop, and the reviewed customization article still describes add-in-oriented extension tooling.
- `companion` is an AIDE fallback lane for adjacent or archival workflows around a retired host family. It is not a literal Microsoft product label.

## Unresolved

- This prompt does not reconstruct every add-in API breakpoint or package format across Visual Studio for Mac 2017, 2019, and 2022. Later archival prompts may need to catalog those differences more explicitly.
- Microsoft retirement guidance points users toward VS Code and Windows-hosted Visual Studio, but it does not define an AIDE-style archival companion pattern. That lane therefore stays explicit about being an AIDE abstraction.

