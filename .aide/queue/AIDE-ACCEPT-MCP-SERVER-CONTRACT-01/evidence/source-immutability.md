# Source Immutability

Observed source-chain hashes before acceptance writes included:

- `.aide/reports/mcp-server-contract/contract.json`: `sha256:3c0a158ae7a6eee0875bc7b6079cf184e40cfbb8cb61fa00d41710fc242cf66a`.
- `.aide/reports/mcp-server-contract/fixture-index.json`: `sha256:27973aa9c6ca8308efdc576126f11690672d21169d6eabc3f8e615637dac305f`.
- `.aide/reports/mcp-server-contract-check/check-report.json`: `sha256:d25088895080eec7806e771c4861679a50868cf3223f98da556ed6d98e4ce6c8`.
- `.aide/reports/mcp-server-contract-repair/repair-report.json`: `sha256:c83497b7bd8c957b9b4e42324e753550f6650bd72d083016aec655742f579f88`.
- `.aide/reports/mcp-server-contract-repair-check/check-report.json`: `sha256:f282aa0479dca854cd4ad95b709da56cbdec576b309f7083f8fd39574c13441f`.

The acceptance changes are isolated to the allowed acceptance paths plus queue/planning logs.
