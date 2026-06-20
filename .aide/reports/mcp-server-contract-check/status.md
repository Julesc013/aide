# MCP Server Contract Check Status

Result: `FAILED_VALIDATION`

Checked task: `AIDE-BUILD-MCP-SERVER-CONTRACT-01`

Checked commit: `c8a143f76af585ae3a0cc3004fb5278c57f264e0`

Material findings: `2`

The build chain and evidence are present, but the independent check found
material MCP fixture-alignment defects. The contract must not proceed to
acceptance until a bounded repair and independent repair check pass.

Recommended next task: `AIDE-BUILD-MCP-SERVER-CONTRACT-REPAIR-01`
