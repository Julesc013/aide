# Evidence Review

- PASS: `authority.fixture_backed_adapter_declared` - Source declares the underlying executor as a fixture-backed local callable.
- PASS: `authority.no_live_dominium_executor` - Source does not invoke a Dominium-owned executable or command implementation.
- PASS: `executor.clean_success_entered_once` - The success executor function was independently instrumented and entered once for a clean supported request.
- PASS: `result.typed_fixture_success` - Supported request returns a typed fixture-backed success result.
- PASS: `state.fixture_workspace_unchanged` - Before/after workspace digests are independently recomputed and unchanged.
- PASS: `refusal.unsupported_no_executor` - Unsupported capabilities return typed refusal and do not enter the success executor.
- PASS: `refusal.malformed_request_no_executor` - Malformed registered requests return typed refusal and do not enter the success executor.
- PASS: `result.hash_derived_from_fixture_input` - Success result includes hashes derived from fixture input bytes.
- PASS: `determinism.semantic_projection_equal` - Two clean runs produce identical semantic projection JSON.
- PASS: `determinism.output_hashes_equal` - Two clean runs produce identical deterministic output hashes and CLI streams.
- PASS: `leak_scan.no_absolute_paths_or_secrets` - Generated build reports and fixtures do not leak local absolute paths or secret-like values.
- PASS: `record.context_descriptor_valid` - ContextDescriptor identifies the registered capability.
- PASS: `record.context_pack_valid` - ContextPack identifies the registered capability.
- PASS: `record.workunit_valid` - WorkUnit records a single authorized invocation.
- PASS: `evidence.claims_match_behavior` - EvidencePacket claims match independently observed invocation behavior.
- PASS: `event.refs_resolve` - EventRecord causation, correlation, subject, and evidence refs resolve to generated records.
- PASS: `boundary.false_fields_complete` - Forbidden boundary fields remain boolean false in the invocation result.
- PASS: `authority.warning_is_precise` - Build status distinguishes fixture-backed adapter execution from live Dominium command execution.
