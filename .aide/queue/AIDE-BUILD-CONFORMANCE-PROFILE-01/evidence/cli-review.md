# CLI Review

Added `conformance-profile` commands:

- `conformance-profile status`
- `conformance-profile project`
- `conformance-profile validate`

The CLI prints explicit boundary lines for:

- profile-only status;
- no result generation;
- no execution;
- no admission;
- no trust promotion;
- no adapter/runtime/PatchTransaction/ContextPack behavior;
- no branch, target, GitHub, Gateway, network, or provider/model mutation.

No execution, run, admit, result, repair, mutate, or apply subcommands were added.
