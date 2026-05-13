# Q31 Target Sync Readiness

## Q32 Eureka Sync

Q32 should run in the Eureka repository and import from the canonical Q31
`aide-lite-pack-v0` pack. It should:

- verify the source pack checksum, provenance, and boundary status;
- run safe import dry-run and write/import only portable governance files;
- preserve Eureka manual `AGENTS.md` content and Eureka-specific memory;
- ensure no AIDE queue history, generated branch state, generated context,
  reports, `.aide.local/`, secrets, raw prompts, or raw responses are copied;
- regenerate Eureka-local `doctor`, `validate`, `snapshot`, `index`, `context`,
  `pack`, commit, task, and Git policy/plan reports;
- record token and quality evidence in Eureka-local queue evidence.

## Q33 Dominium Sync

Q33 should repeat the same source-pack sync logic in Dominium after Q32 evidence
is available. Dominium-specific memory, branch posture, and project validation
must remain target-local.

## Ready Inputs

- Canonical pack path: `.aide/export/aide-lite-pack-v0`
- Pack status: PASS
- Q31 fixture import governance commands: PASS
- Q32 task packet: `.aide/context/latest-task-packet.md`
- Q32 task packet estimate: 3692 chars, approximately 923 tokens

## Cautions

- Do not manually copy target-local Eureka or Dominium fixes back into AIDE
  unless an AIDE queue item canonicalizes them.
- Do not use AIDE-generated branch detection or helper plans as target truth.
- Hook installation in targets remains opt-in.
- Branch protection, CI, release automation, provider/model calls, and live
  branch mutation remain future phases.
