# Visual Studio On Windows

## Major-Version Table

| Record id | Display name | Host OS | Vendor lifecycle | Primary AIDE lane | Notes |
| --- | --- | --- | --- | --- | --- |
| `vs97` | Microsoft Visual Studio 97 | `windows` | Out of support | `com-addin` | Official 2026 servicing guidance lists Visual Studio 97 as out of support with baseline service pack 3 and June 2003 end-of-support month. Exact release date is unresolved in current-source coverage. |
| `vs6` | Microsoft Visual Studio 6.0 | `windows` | Out of support | `com-addin` | Official 2026 servicing guidance lists Visual Studio 6.0 as out of support with service pack 6 and September 2005 end-of-support month. Exact release date is unresolved in current-source coverage. |
| `vs2002` | Microsoft Visual Studio .NET 2002 | `windows` | Out of support | `com-addin` | Official 2026 servicing guidance lists Visual Studio .NET (2002) as out of support with service pack 1 and July 2009 end-of-support month. Exact release date is unresolved in current-source coverage. |
| `vs2003` | Microsoft Visual Studio .NET 2003 | `windows` | Out of support | `com-addin` | Lifecycle page gives exact support dates through 2013-10-08. This remains inside AIDE's legacy `com-addin` umbrella rather than a literal Microsoft lane name. |
| `vs2005` | Microsoft Visual Studio 2005 | `windows` | Out of support | `com-addin` | Lifecycle page gives exact support dates through 2016-04-12. This is still pre-VSIX for AIDE purposes. |
| `vs2008` | Microsoft Visual Studio 2008 | `windows` | Out of support | `com-addin` | Lifecycle page gives exact support dates through 2018-04-10. This is still pre-VSIX for AIDE purposes. |
| `vs2010` | Microsoft Visual Studio 2010 | `windows` | Out of support | `vsix-v1` | Microsoft documentation for SharePoint tools in Visual Studio 2010 explicitly references a `VSIX Project` template and VSIX output. |
| `vs2012` | Microsoft Visual Studio 2012 | `windows` | Out of support | `vsix-v2-vssdk` | Microsoft documents VSIX schema 2.0 as introduced in Visual Studio 2012. |
| `vs2013` | Microsoft Visual Studio 2013 | `windows` | Out of support | `vsix-v2-vssdk` | No new adapter-lane breakpoint was required by the sources reviewed for this prompt. |
| `vs2015` | Microsoft Visual Studio 2015 | `windows` | Out of support | `vsix-v2-vssdk` | Release notes state that add-in project templates and the Add-in Manager were removed in this release. |
| `vs2017` | Microsoft Visual Studio 2017 | `windows` | Supported through 2027-04-13 | `vsix-v2-vssdk` | Lifecycle page still shows support through 2027-04-13. |
| `vs2019` | Microsoft Visual Studio 2019 | `windows` | Supported through 2029-04-10 | `vsix-v2-vssdk` | Lifecycle page still shows support through 2029-04-10. |
| `vs2022` | Microsoft Visual Studio 2022 | `windows` | Supported through 2032-01-13 | `extensibility` | Microsoft states Visual Studio 2022 is the first 64-bit Visual Studio. Legacy VSSDK and newer VisualStudio.Extensibility both remain relevant. |
| `vs2026` | Microsoft Visual Studio 2026 | `windows` | Supported through 2027-11-09 | `extensibility` | Visual Studio 2026 follows the Modern Lifecycle Policy, annual release servicing, and the new extension compatibility model. |

## Fact

- Visual Studio 2026 follows the Modern Lifecycle Policy and adds annual-release servicing with LTSC handling. Source: https://learn.microsoft.com/en-us/visualstudio/releases/2026/servicing-vs
- Microsoft's current lifecycle pages provide exact start and end dates for Visual Studio .NET 2003, Visual Studio 2005, Visual Studio 2008, Visual Studio 2010, Visual Studio 2012, Visual Studio 2013, Visual Studio 2015, Visual Studio 2017, Visual Studio 2019, Visual Studio 2022, and Visual Studio 2026. Sources:
  - https://learn.microsoft.com/en-us/lifecycle/products/microsoft-visual-studio-net-2003?branch=live
  - https://learn.microsoft.com/en-us/lifecycle/products/microsoft-visual-studio-2005
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2008
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2010
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2012
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2013
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2015
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2017
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2019
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2022
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-2026
- Microsoft archived documentation shows that Visual Studio 2010 had a `VSIX Project` template and that building it produced a VSIX file. Source: https://learn.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/gg241221%28v%3Doffice.14%29
- Microsoft documents that VSIX schema 2.0 was introduced in Visual Studio 2012. Source: https://learn.microsoft.com/en-us/visualstudio/extensibility/vsix-extension-schema-2-0-reference?view=vs-2022
- Microsoft release notes state that Visual Studio 2015 removed add-in project templates and the Add-in Manager. Source: https://learn.microsoft.com/en-us/visualstudio/releases/2015/vs2015-rtm-vs
- Microsoft states that Visual Studio 2022 is the first 64-bit Visual Studio. Source: https://devblogs.microsoft.com/visualstudio/visual-studio-2022/
- Microsoft describes the new VisualStudio.Extensibility SDK as out-of-process, and Microsoft later documents standalone VSIX packaging, hot loading, project-system queries, debugger visualizers, and LSP support for that SDK. Sources:
  - https://devblogs.microsoft.com/visualstudio/the-future-of-visual-studio-extensibility-is-here/
  - https://devblogs.microsoft.com/visualstudio/visualstudio-extensibility-17-9/
- Microsoft states that Visual Studio 2022 VSIX-based extensions work in Visual Studio 2026 without modification, using the new compatibility model. Source: https://devblogs.microsoft.com/visualstudio/modernizing-visual-studio-extension-compatibility-effortless-migration-for-extension-developers-and-users/

## Inference

- `com-addin` is an AIDE umbrella for pre-VSIX Windows Visual Studio native extension surfaces. It is not a claim that every pre-2010 extensibility contract was literally a Microsoft COM add-in product category.
- `vsix-v1` is the cleanest conservative breakpoint for Visual Studio 2010-era VSIX packaging.
- `vsix-v2-vssdk` is the cleanest conservative breakpoint from Visual Studio 2012 through most of the Visual Studio 2022 era because Microsoft's sources explicitly tie VSIX schema 2.0 to Visual Studio 2012 and the 2026 compatibility guidance still assumes VSIX-based extensions are the installed extension family.
- `extensibility` is a late-2022-and-forward AIDE lane for the VisualStudio.Extensibility SDK and related modern contracts, not a claim that the older VSSDK became irrelevant.

## Unresolved

- Current official Microsoft sources do not provide the same exact release-date detail for Visual Studio 97, Visual Studio 6.0, and Visual Studio .NET 2002 that they provide for later releases. Those records remain deliberately partial.
- This prompt does not attempt a full pre-2010 taxonomy of DTE automation, packages, wizards, or other legacy Visual Studio extensibility surfaces. The `com-addin` lane remains an intentionally conservative umbrella until a later legacy-specific prompt refines it.

