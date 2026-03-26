# CodeWarrior IDE SDK

## Verified facts

- The preserved CodeWarrior IDE SDK API Reference states that the CodeWarrior IDE exposes a plug-in API and that the IDE itself uses plug-ins for most of its services.
  - Source: https://www.nxp.com/docs/en/reference-manual/SDKAPIRM.pdf
- The preserved CodeWarrior COM API Reference shows that COM object interfaces were part of the documented classic IDE surface.
  - Source: https://www.nxp.com/docs/en/reference-manual/COMAPIRM.pdf
- The preserved CodeWarrior IDE Automation Guide documents Windows automation tasks including project and target management, building, compiling, linking, debugging, version-control access, menu-command invocation, and active-document access.
  - Source: https://www.nxp.com/docs/en/user-guide/IDE_5.6_Automation_Guide.pdf
- The preserved `56800/E ... (Classic IDE) v8.3` product page still lists the SDK API and COM API references under product documentation.
  - Source: https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-56800-e-digital-signal-controllers-classic-ide-v8-3:CW-56800E-DSC

## Implications for AIDE

- Fact: there was a documented native in-host extension and automation surface in the classic CodeWarrior line.
- Fact: the documented surface covered more than a command hook. The preserved manuals explicitly include project, build, debug, document, and automation topics.
- Inference: the classic `ide-sdk` lane has a credible target ceiling above `L1`, because the preserved manuals show project-aware and IDE-aware integration points.
- Inference: `L3` is a conservative target capability for the classic lane. The source set supports project/workspace awareness, but this prompt does not prove a stable deep-UI ceiling comparable to modern Windows Visual Studio VSSDK work.

## Limits and gaps

- Fact: the preserved classic SDK and COM manuals are tied to the classic IDE era. They do not, by themselves, prove that later `10.x` and `11.x` Eclipse-based CodeWarrior suites exposed the same native contracts.
- Inference: AIDE should keep using the `ide-sdk` lane for the committed CodeWarrior family now, but it should document that later Eclipse-based CodeWarrior releases are only an umbrella fit.
- Unresolved: the current source set does not yet isolate a clean Eclipse-era CodeWarrior extension contract strong enough to justify a new adapter-technology lane in this prompt.
