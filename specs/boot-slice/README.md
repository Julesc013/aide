# Boot Slice Specs

`specs/boot-slice/` defines the first implementation slice that later prompts must target before broader feature expansion.

The boot slice exists so AIDE can prove one shared-core contract across many host lanes without overcommitting to deep or uniform parity too early.

These documents are specification inputs for later implementation prompts. They define the first target, its rollout order, its degraded or blocked handling, and the machine-readable manifests that planning and verification work should consume.
