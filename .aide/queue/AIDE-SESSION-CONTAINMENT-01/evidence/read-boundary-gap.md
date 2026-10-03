# Retained installed-host read gap

Attempt `71fa58409e0d491d97b0f78c4a99c0f4` added an explicit :root deny and
exact configuration-file deny to the command-local profile. The installed
Codex 0.145.0 still allowed the configuration read. It denied a write-capable
handle to that same file, and the original configuration hash was unchanged.
Both failed-profile attempts retain their exact logs, effective profiles and
resource receipts. No source/runtime repair or newer-host qualification is
implied. Current default Codex resolves to that same installed 0.145.0 binary.

The whole-profile acceptance remains failed. The independent next operation
is a repository-only validation using the observed write/process boundary;
it has no private inputs, network or model request. This limited operation
does not depend on read concealment of its configuration. Its result must
report PARTIAL when the workload passes but the requested read profile fails.
This is not acceptance of full session containment or permission to use this
route with secrets.

The qualification entry now derives a narrower temporary execution selection
from the existing local configuration, preserving roots and volume identities.
It limits scratch to 32 MiB, retained output to 64 KiB and runtime to 900 seconds
without increasing any configured limit. Original log/memory/process limits
remain. Under the existing estate lock, it measures the shared retained root
and reserves retained-output + log + 1 MiB metadata headroom before child
execution. For this qualification entry only, the existing 256 MiB retained
allowance is used as an aggregate ceiling. This is an application admission
bound on cooperating work, not a filesystem quota or a production-wide
retention policy. Unmediated writers and other control roots remain uncovered.

The normal real task is the existing `aide_lite.py validate`, preceded by four
unchanged resource regression cases and a tiny exact-capacity boundary check.
The original validation criteria and complete output remain in the existing
runner's retained logs; the controller receives only the compact result.
