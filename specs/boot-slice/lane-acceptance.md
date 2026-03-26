# Lane Acceptance

The following table defines the minimum accepted proof for every committed lane in the first boot slice.

| Lane | Minimum acceptance target | Expected support mode | Expected execution mode bias | Editor or file interaction | Evidence that counts as success | Common blockers |
| --- | --- | --- | --- | --- | --- | --- |
| `hosts/microsoft/visual-studio/com-addin` | `L1` report-first proof; `L2` marker optional | `legacy-native` | `cli-bridge` | optional | invokable entry point, boot-slice report, capability report, explicit editor-marker status | legacy Windows environment, pre-VSIX umbrella ambiguity, stable editor hook not yet chosen |
| `hosts/microsoft/visual-studio/vsix-v1` | `L1` report-first proof; `L2` marker optional | `legacy-native` | `cli-bridge` | optional | invokable VSIX entry point, boot-slice report, capability report, optional edit preview | Visual Studio 2010 environment, legacy VSIX packaging and shell bring-up |
| `hosts/microsoft/visual-studio/vsix-v2-vssdk` | `L2` reference-native proof | `native` | `embedded` | required | invokable command, boot-slice report, capability report, deterministic marker edit or preview in active text | VSSDK command wiring, shell package bring-up, editor-context plumbing |
| `hosts/microsoft/visual-studio/extensibility` | `L1` report-first proof; `L2` marker optional after the first out-of-process path is stable | `native` | `local-service` | optional | invokable modern entry point, boot-slice report, capability report, explicit unavailable or deferred reasons when richer editor proof is not ready | out-of-process contract setup, service lifecycle, coexistence with older Visual Studio assumptions |
| `hosts/microsoft/visual-studio-mac/monodevelop-addin` | `L1` archival-native proof; `L2` marker optional | `legacy-native` | `cli-bridge` | optional | invokable add-in or archival-native entry point, boot-slice report, capability report, archival note | retired host family, reproducible macOS environment, add-in packaging detail gaps |
| `hosts/microsoft/visual-studio-mac/companion` | `L1` companion fallback proof | `companion` | `cli-bridge` | replaced by fallback proof | companion entry point, boot-slice report, capability report, explicit reason native lane is blocked or deferred | archival environment access, companion orchestration shape, retired-host limitations |
| `hosts/apple/xcode/xcodekit` | `L2` editor-native proof | `native` | `embedded` | required | invokable source-editor command, boot-slice report, capability report, deterministic `AIDE_BOOT:` marker edit or preview on active text | containing-app and extension packaging, narrow source-editor-only context |
| `hosts/apple/xcode/companion` | `L1` companion fallback proof | `companion` | `cli-bridge` | replaced by fallback proof | companion entry point, boot-slice report, capability report, explicit reason older or broader Xcode workflows stay outside the native lane | older Xcode environment reconstruction, coexistence with broader workflows, companion orchestration shape |
| `hosts/metrowerks/codewarrior/ide-sdk` | `L1` archival-native proof; `L2` marker optional | `legacy-native` | `cli-bridge` | optional | invokable SDK or automation entry point, boot-slice report, capability report, archival note, optional active-document marker preview | classic environment access, SDK versus COM split, later Eclipse-era umbrella ambiguity |
| `hosts/metrowerks/codewarrior/companion` | `L1` companion fallback proof | `companion` | `cli-bridge` | replaced by fallback proof | companion entry point, boot-slice report, capability report, explicit reason native path is blocked or unresolved | environment reconstruction, local artifact flow, unresolved later-era contract boundaries |

## Reading Rule

- `required` means lane completion needs the `boot.slice.editor-marker` proof.
- `optional` means lane completion can stop at `boot.slice.invoke` while still recording the `L2` path honestly for later promotion.
- `replaced by fallback proof` means the lane completes the slice through deterministic report output and explicit unavailable-reason reporting instead of a native text edit.
