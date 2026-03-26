# Microsoft Platform Reach

## Host Reach

| Family | Verified host OS families | Reach posture | Notes |
| --- | --- | --- | --- |
| `microsoft.visual-studio` | `windows` | `native` | The Windows Visual Studio family is modeled only as a Windows-hosted IDE family in this prompt. |
| `microsoft.visual-studio-mac` | `macos` | `native` for `monodevelop-addin`, `companion` for the fallback lane | Visual Studio for Mac is a macOS-hosted IDE family and is now retired. |

## Fact

- Visual Studio on Windows remains a Windows-hosted IDE family throughout the versions cataloged here. The lifecycle and servicing documents reviewed for this prompt do not establish any non-Windows host OS for the main IDE line.
- Visual Studio for Mac is a macOS-hosted IDE family. Microsoft's introduction article, lifecycle page, and retirement announcement all treat it as a Mac IDE. Sources:
  - https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/connect/visual-studio-development-%E2%80%93-introducing-visual-studio-for-mac
  - https://learn.microsoft.com/en-us/lifecycle/products/visual-studio-for-mac
  - https://devblogs.microsoft.com/visualstudio/visual-studio-for-mac-retirement-announcement/
- Visual Studio for Mac supported building for multiple downstream platforms, but the prompt's matrix schema is host- and lane-oriented, not a full application-target catalog. Source: https://learn.microsoft.com/en-us/archive/msdn-magazine/2016/connect/visual-studio-development-%E2%80%93-introducing-visual-studio-for-mac

## Inference

- No change is required to `inventory/os-families.yaml` for this prompt because the existing `windows` and `macos` ids are sufficient for the Microsoft host reach that is actually modeled in the current matrices.
- Downstream application-target modeling for Xamarin, MAUI, Android, iOS, or cloud deployment belongs in later platform or workload prompts rather than this Microsoft host-atlas prompt.

## Unresolved

- This prompt does not build a deployment-target matrix for Visual Studio or Visual Studio for Mac workloads. Only host reach that affects AIDE adapter architecture is recorded here.
- Cross-OS `companion` reach for retired Visual Studio for Mac workflows remains deferred until AIDE defines a concrete companion protocol and artifact model.

