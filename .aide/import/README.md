# AIDE Lite Import Templates

This directory contains target-neutral templates used by Q21 export/import
tooling. They are not AIDE's own project memory or queue history.

Use these templates when importing the portable AIDE Lite Pack into another
repository. Target repositories must generate their own snapshot, context map,
task packet, evidence packet, token reports, and project memory after import.

Do not copy source `.aide/queue/`, generated context, reports, `.aide.local/`,
raw prompts, raw responses, or provider credentials into target repos.
