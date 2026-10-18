**Product:** `core/runtime/continuous_worker/requests.py` owns explicit-v2
cancellation; `dependency_mcp.py` exposes it through the existing observation tool.
`.aide/scripts/tests/test_continuous_worker_request_cancellation.py` adds focused
regressions and an actual CLI/MCP consumer. Original suites are byte-identical.

**Documentation:** `docs/reference/local-dependency-requests.md`, root planning,
implementation/documentation indexes and campaign/queue records describe qualified
scope and remaining boundaries. Task-local runners, exact maps, reviews and
results retain attempts and corrections. [REPORT.md](../REPORT.md) summarizes them.

**Generated:** only the development pack's `manifest.yaml` source commit changed;
all 867 payload/static members and eight release assets are unchanged. Six
changelog preview outputs cover the fixed reviewed range. Exact closure paths
and hashes are in [closure-source.json](closure-source.json); prior committed
paths are available in `git diff --name-only 8fe2d12..HEAD`.
