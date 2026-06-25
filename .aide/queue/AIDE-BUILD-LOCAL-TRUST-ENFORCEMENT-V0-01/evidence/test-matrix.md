# Test Matrix

Focused tests cover:

- allowed evaluation persistence
- local Service event persistence
- one-use grant consumption
- idempotent replay without a second event
- concurrent final-use refusal after grant consumption
- full accepted trust refusal-code matrix
- fixture restart persistence
- false process/network/worker/provider boundaries
- AIDE Lite `local-trust fixture` command

Regression tests cover the accepted trust contract and accepted local Service
foundation.
