# CodeWarrior Platform Reach

## Verified facts

- Preserved classic product pages verify multiple Windows-hosted CodeWarrior families.
  - Sources:
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-68k-embedded-systems-classic-ide-v3-2:CW-68K-EMBEDDED
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-hcs12x-microcontrollers-classic-ide-v5-2:CW-HCS12X
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-mobilegt-classic-ide-v9-2:CW-MOBILEGT
- Preserved ColdFire Linux pages verify Linux-hosted CodeWarrior editions and mixed Windows/Linux host reach in at least one product line.
  - Source: https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-coldfire-architectures-linux-editions-classic-ide-v2-5:CW-COLDFIRE-LINUX
- Preserved manuals explicitly mention Solaris and Linux users in the classic documentation set.
  - Source: https://www.nxp.com/docs/en/user-guide/IDE_5.6_Users_Guide.pdf
- Preserved product pages emphasize processor, board, and embedded-target coverage much more than general-purpose target operating systems.
  - Sources: the product pages listed in `sources.md`

## AIDE interpretation

- Host reach that is strong enough for machine-readable posture now:
  - `windows`
  - `linux`
  - `unix`
- High-level target reach that is strong enough for machine-readable posture now:
  - `other`

`other` is used conservatively because the preserved CodeWarrior materials are primarily organized around processor and board families, not a normalized host-style OS matrix that maps cleanly onto AIDE's current `os-families` catalog.

## Unresolved or deferred

- Classic Macintosh host reach is not normalized into machine-readable posture in this prompt because the source set gathered in this run is weaker than the Windows/Linux/Unix evidence.
- The current prompt does not split CodeWarrior target reach by RTOS, board package, or processor family; that would require a different inventory model than `os-families`.
