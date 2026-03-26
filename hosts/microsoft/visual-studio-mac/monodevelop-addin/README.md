# Visual Studio For Mac MonoDevelop Add-in Lane

This directory is the `monodevelop-addin` compatibility-technology lane for `microsoft.visual-studio-mac`. It reflects the product's Xamarin Studio and MonoDevelop-derived native extension model.

P11 adds an explicit blocked archival-native boot-slice record for this lane:

- `boot_slice_request.json` records the intended `cli-bridge` archival-native request
- `blocked-proof.md` records why a real native add-in proof is not yet honest in the current environment

This lane remains blocked by the retired host family, missing reproducible macOS environment, and incomplete packaging detail reconstruction. The blocked record preserves the native archival target while the companion lane carries the runnable fallback proof.
