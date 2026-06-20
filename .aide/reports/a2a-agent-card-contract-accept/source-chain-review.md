# Source Chain Review

The live source chain is complete:

| Task | Result | Commit | Acceptance use |
| --- | --- | --- | --- |
| `AIDE-ACCEPT-MCP-SERVER-CONTRACT-01` | `ACCEPTED_WITH_WARNINGS` | `57eac272976208ac27f3b723d546de3859fefdcb` | MCP predecessor |
| `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-01` | `PASS_WITH_WARNINGS` | `a9082beb3b1323328f81e693d2bdb05464502dd4` | build baseline |
| `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-01` | `FAILED_VALIDATION` | `c5de2c769e34269552fced9a105ec5b340eb6704` | preserved failed check |
| `AIDE-BUILD-A2A-AGENT-CARD-CONTRACT-REPAIR-01` | `PASS_WITH_WARNINGS` | `b9a35ff1e99d8a2d2f56c14303bdda3c8fe7a579` | bounded repair |
| `AIDE-CHECK-A2A-AGENT-CARD-CONTRACT-REPAIR-01` | `PASS_WITH_WARNINGS` | `cac752bb2bf3da3598659b9e1bae92b1d832a138` | independent repair check |

The repair check recommends `AIDE-ACCEPT-A2A-AGENT-CARD-CONTRACT-01`.
