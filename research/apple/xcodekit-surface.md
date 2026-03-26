# XcodeKit Surface

Primary sources: [XcodeKit](https://developer.apple.com/documentation/xcodekit), [Creating a Source Editor Extension](https://developer.apple.com/documentation/XcodeKit/creating-a-source-editor-extension), [App Extensions Increase Your Impact](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/), [Creating an App Extension](https://developer.apple.com/library/archive/documentation/General/Conceptual/ExtensibilityPG/ExtensionCreation.html).

## Facts

- Apple documents `XcodeKit` as the public API family for Xcode source editor extensions.
- Apple treats `Xcode Source Editor` as a macOS app-extension point in the App Extension Programming Guide.
- Apple documents source editor extensions as commands chosen from Xcode's Editor menu.
- Apple documents `XCSourceTextBuffer` as the editable text-buffer context exposed to the extension.
- Apple documents app extensions as binaries delivered inside a containing app, not as standalone native plug-ins.
- Apple documents additional delivery constraints for app extensions, including containing-app requirements and Gatekeeper behavior outside the Mac App Store.

## Important architectural limits

- The public Apple surface is editor-centric. It is designed for command invocation against the current source buffer, not as a general-purpose replacement for the entire Xcode application model.
- The containing-app requirement matters for AIDE packaging and installation planning even before any implementation exists.
- Apple requires extensions to remain lightweight and narrowly scoped, which is a meaningful constraint for any future in-host AIDE workflow.

## Inferences

- The documented XcodeKit surface comfortably supports `L1` and `L2` planning in AIDE terms: command entry plus editor/file interaction.
- The same public source set does not justify claiming `L3` or `L4` natively through XcodeKit. Apple does not document a deep public project-model, debugger, or global-IDE automation contract here.
- This is why AIDE keeps `xcodekit` as the narrow native lane and retains `companion` for broader workflows.

## Unresolved

- The exact first Xcode major family that shipped this surface is not pinned to a single official release-note page in the source set used here.
- Deeper current-Xcode extensibility options, if any, require a later prompt and should not be inferred from XcodeKit alone.
