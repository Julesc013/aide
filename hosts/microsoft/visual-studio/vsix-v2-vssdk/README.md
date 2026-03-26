# Visual Studio VSIX v2 VSSDK Lane

This directory is the `vsix-v2-vssdk` compatibility-technology lane for `microsoft.visual-studio`. It covers the Visual Studio 2012-and-later VSIX 2.0 plus VSSDK family that remains the main native extension baseline across supported Windows releases.

P11 adds an explicit blocked native boot-slice record for this lane:

- `boot_slice_request.json` records the intended `embedded` `L2` editor-marker request
- `blocked-proof.md` records why a real native VSSDK proof is not yet honest in the current environment

This lane still lacks a verified native command load, editor-context capture, and shell-hosted marker preview. The blocked record is intentional and preserves the lane as the Windows native reference target rather than silently collapsing it into newer or shallower proofs.
