# Ordinary host boundary — 2026-10-04

The actual installed Codex 0.145.0 app-server resolved the command-local named profile, root deny, minimal/source read, elevated Windows sandbox and disabled optional app/plugin/browser/hooks/multi-agent routes. No model or thread was started. User model, effort, provider and account defaults were not rewritten. Strict config validation encountered an existing `preferred_auth_method` field unsupported by this executable; no global field was removed. Ordinary non-strict loading resolved the tested security fields correctly.

Same harmless exact fixture and policy, three routes:

| Route | Excluded read | Excluded write handle | Allowed write |
| --- | --- | --- | --- |
| Direct codex sandbox -P | allowed (FAIL) | denied | prior accepted worker proof |
| Normal app-server command/exec | denied | denied | succeeds |
| Native app-server filesystem API | allowed (FAIL) | write succeeds (FAIL) | succeeds |

The new source-bound probe reproduces the retained direct-route read gap without accessing the original config or real secrets. Route-specific observations establish that the tested entry points enforce different properties. They do not diagnose the internal host implementation cause or claim every editor implementation has this behavior.

`outer-launch.toml` prepares the smallest command-local scope for this documentation/qualification task. Source/toolchain and existing storage are readable; exact task and root evidence records writable; Git, policy and control records excluded from worker modification. It grants no write access to the shared storage pool: that requires a specific existing runner-owned lease rather than a pool-wide grant. `outer-launch.py` renders supported CLI overrides and disables declared MCP servers without installing global config or starting another controller/model. It refuses legacy sandbox-setting composition. No speculative cache flags or model selection.

**Exact remaining host action:** the active client must replace its supplied disabled/unrestricted filesystem permission profile with an enforced scope covering source `D:/Projects/AIDE/aide` and the exact runner-owned output lease, applying to both shell and file/editor tools. Omit independently unrestricted plugin/browser/connector routes for this qualification. Then run this same harmless probe and one real task through that actual client path. These tools expose no operation to change the active client permission profile or restart it. A command profile alone is insufficient; its native filesystem API tests failed. Do not launch a broad unattended campaign with the current disabled profile.

Current outer shell and apply_patch remain Full Access. Remote connectors, integrations, other sessions and client-owned logs/state have independent boundaries. Disk admission remains monitored/cooperative, not a hard quota. The ordinary scoped real-task acceptance remains **unqualified**, with this external setup requirement retained; the previous 64-test worker qualification remains valid and unchanged.

All probe-created files were exact harmless owned fixtures and retired; owned app-server processes exited. A teardown CRLF expectation failure was reconciled and retained in outer-host-probe-recovery.json before repeating the changed probe. No machine-wide ACL/account/quota changes, secret reads, model turns or full suites. Report resource coverage honestly: the small retained probe record and source helper are counted; client state/log growth was not measured and no whole-campaign total is claimed.

Official scope: https://learn.chatgpt.com/docs/permissions and https://learn.chatgpt.com/docs/app-server . Permission profiles govern local commands; other host/tool surfaces require separate controls.
