# Shared-Core Boot-Slice Smoke Run

## Scope

P10 shared-core bootstrap runtime only.

This run does not claim any host-adapter success. It verifies the executable shared core, its deterministic fixtures, and the host-agnostic CLI bridge.

## Commands Run

- `py -3 -m unittest discover -s shared/tests -t .`
- `py -3 -m shared.cli --request fixtures\boot-slice\success-request.json --pretty`

## Passed

- Shared-core request dispatch matched the committed success, deferred, malformed-request, and capability-report fixtures.
- The CLI bridge consumed a deterministic JSON request fixture and emitted deterministic JSON output.
- Structured capability reporting, unavailable or deferred reporting, and diagnostic payloads were present in the runtime responses.

## Deferred

- Host-lane invocation evidence remains deferred because no `hosts/**` adapter implementation exists in P10.
- Local-service daemon behavior remains deferred; only the transport-agnostic request model and CLI bridge are implemented here.
- Broader feature coverage beyond the first boot slice remains deferred.

## Evidence References

- `shared/tests/test_boot_slice_runtime.py`
- `shared/tests/test_boot_slice_cli.py`
- `fixtures/boot-slice/success-request.json`
- `fixtures/boot-slice/success-response.json`
- `fixtures/boot-slice/unavailable-request.json`
- `fixtures/boot-slice/unavailable-response.json`
- `fixtures/boot-slice/invalid-request.json`
- `fixtures/boot-slice/invalid-response.json`
- `fixtures/boot-slice/capability-request.json`
- `fixtures/boot-slice/capability-response.json`
