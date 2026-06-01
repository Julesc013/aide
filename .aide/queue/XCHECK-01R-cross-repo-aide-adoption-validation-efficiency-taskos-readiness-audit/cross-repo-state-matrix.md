# Cross-Repo State Matrix

| Repo | Path | Branch | Commit | Dirty | Checkpoint Status | Current Readiness |
|---|---|---|---|---|---|---|
| AIDE | `C:\Projects\AIDE\aide` | `main` | `dab004e322cac8aec41e7d41787c8482a97f4ae9` | generated audit/status changes only after start | Q36-Q48/QCHECK/QFIX `needs_review` | source usable, test-tier work must run first |
| Dominium | `C:\Projects\Dominium\dominium` | `main` | `311c86158587f3fc906b823bc3326259c1859dfc` | clean | DCHECK `needs_review`; later target work present | AIDE-operable with target warnings; product boot blocked by RepoX evidence |
| Eureka | `C:\Projects\Eureka\eureka` | `main` | `e582028b1db977e28ba6ddc0ed284ca6ccf48234` | clean | ECHECK `needs_review`; later local-loop work present | fixture/local product loop advanced; live/production deferred; `dev` ahead of `main` |

No target repository writes were performed.
