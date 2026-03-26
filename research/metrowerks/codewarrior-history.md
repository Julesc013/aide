# CodeWarrior History

## Verified facts

- NXP's preserved CodeWarrior catalog still exposes multiple distinct product branches, including classic IDE families and later Eclipse-based families, instead of a single flat release ladder.
  - Source: https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/downloads:CW_DOWNLOADS
- Preserved NXP product pages verify classic IDE families at least through `v3.2`, `v5.2`, `v6.3`, `v7.2`, `v8.3`, and `v9.2`.
  - Sources:
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-68k-embedded-systems-classic-ide-v3-2:CW-68K-EMBEDDED
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-hcs12x-microcontrollers-classic-ide-v5-2:CW-HCS12X
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-for-microcontrollers-classic-ide-rs08-hcs08-coldfire-v1-v6-3:CW-MICROCONTROLLERS
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-coldfire-architectures-classic-ide-v7-2:CW-COLDFIRE
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-56800-e-digital-signal-controllers-classic-ide-v8-3:CW-56800E-DSC
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-mobilegt-classic-ide-v9-2:CW-MOBILEGT
- Preserved later NXP lines verify at least `10.x` and `11.x` families, and one current preserved `11.2` page explicitly says the tool is based on Eclipse.
  - Sources:
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-network-applications/codewarrior-development-suites-for-networked-applications:CW-DS-NETAPPS
    - https://www.nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-for-56800-digital-signal-controller-v11-2:CW-DSC

## Major-family table

| AIDE id | Verified family marker | Host-platform evidence | Architectural note |
| --- | --- | --- | --- |
| `cw3` | NXP preserves a `68K Embedded Systems (Classic IDE) v3.2` page. | The preserved page lists Windows 2000 and Windows XP/Vista 32-bit system requirements. | Earliest verified major family in the current source set. |
| `cw5` | NXP preserves `HCS12(X) Microcontrollers (Classic IDE) v5.2` and lists IDE version `5.9`. | The preserved page lists Windows 7, 8, 8.1, and 10 host platforms. | Strong classic-IDE evidence for the documented plug-in era. |
| `cw6` | NXP preserves `Microcontrollers ... v6.3`. | Source set confirms a preserved Windows-hosted classic product page. | Keeps the classic umbrella intact for 8/16/32-bit MCU work. |
| `cw7` | NXP preserves `ColdFire Architectures (Classic IDE) v7.2`. | Source set confirms a preserved Windows-hosted classic product page. | Still a classic IDE family. |
| `cw8` | NXP preserves `56800/E ... (Classic IDE) v8.3`. | The preserved page carries classic IDE material and attached SDK and COM manuals. | Important because the product page directly links extension-surface documents. |
| `cw9` | NXP preserves `mobileGT (Classic IDE) v9.2`. | The preserved page lists Windows 2000/XP and 64-bit Windows 7 installation guidance. | Last clearly verified classic family in this run. |
| `cw10` | NXP preserves `10.x` release materials in later network and MCU lines. | Current-source coverage verifies Windows hosts for MCU `11.1`; separate Linux-hosted classic ColdFire evidence exists outside the `10.x` line. | AIDE treats this as the start of the later umbrella that no longer maps cleanly to the classic SDK label. |
| `cw11` | NXP preserves `11.1` and `11.2` lines, and `11.2` explicitly states an Eclipse platform. | The `11.2` page lists Windows 10 32-bit and 64-bit host support. | Verified later-generation family with an Eclipse-based platform. |

## Inferences

- AIDE's committed `metrowerks.codewarrior` family spans at least two materially different eras:
  - classic IDE families with documented native SDK and COM automation
  - later Eclipse-based suites that still belong to the CodeWarrior product lineage but no longer match the classic SDK label exactly
- Because the repository currently has only `ide-sdk` and `companion` lanes for CodeWarrior, `ide-sdk` must be treated as exact for classic IDE families and as a conservative umbrella for later Eclipse-era families until a later prompt decides whether they deserve a separate lane.

## Unresolved or unverified

- The current source set does not establish a clean, official, fully continuous major-version ladder between the early classic Mac era and the preserved embedded `v3.2` page.
- The current source set does not establish formal lifecycle end dates for most CodeWarrior families in a way that cleanly maps to AIDE's `supported|out-of-support|retired|unverified` enum, so machine-readable lifecycle values remain conservative.
- Macintosh-hosted CodeWarrior history is historically important but not strong enough in the gathered official source set to normalize into machine-readable host reach yet.
