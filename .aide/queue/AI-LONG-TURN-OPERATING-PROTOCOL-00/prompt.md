# AI-LONG-TURN-OPERATING-PROTOCOL-00 Prompt Summary

Create a repo-local operating protocol for long-running AIDE and Codex queued
turns.

The protocol should cover:

- turn budgets
- commit cadence rules
- task-chain limits
- continuation rules
- manual and external stop conditions
- validation ladders
- queue handoff rules
- final report shape
- failure recovery

This WorkUnit is the docs-only split of a broader attached prompt. The broader
prompt included stale product and branch state and language about branch,
promotion, publication, and external evidence gates. Those parts are excluded
from implementation here and are represented only as stop conditions or report
fields.

Do not change runtime behavior, product gates, branch state, publication state,
target repositories, provider/model surfaces, Gateway surfaces, network state,
or external discovery evidence.
