# CodeWarrior Extension Technology Map

## Lane: `ide-sdk`

- Verified fact: preserved CodeWarrior classic documentation exposes an IDE SDK plug-in API and COM automation.
  - Sources:
    - https://www.nxp.com/docs/en/reference-manual/SDKAPIRM.pdf
    - https://www.nxp.com/docs/en/reference-manual/COMAPIRM.pdf
    - https://www.nxp.com/docs/en/user-guide/IDE_5.6_Automation_Guide.pdf
- AIDE meaning: the native CodeWarrior lane for in-host integration where acceptable documentation shows a real IDE extension or automation surface.
- Exactness:
  - Exact for classic IDE families documented by the preserved SDK and automation manuals.
  - Conservative abstraction for later Eclipse-based CodeWarrior lines, because the repository has no separate CodeWarrior-Eclipse lane yet.

## Lane: `companion`

- Verified fact: the current source set does not establish one clean native contract that spans all preserved CodeWarrior eras.
- AIDE meaning: an out-of-process fallback for archival workflows, unsupported host variants, or later CodeWarrior lines whose native contract is still unresolved.
- Exactness:
  - Not a vendor product label.
  - Pure AIDE architectural abstraction.

## Why AIDE keeps this mapping for now

- It preserves the committed host-family scaffold from earlier prompts.
- It keeps classic IDE SDK work attached to a documented native surface.
- It avoids fabricating a dedicated later-era lane before the Eclipse-era contract has been normalized from primary sources.

## Future refinement points

- Decide whether later Eclipse-based CodeWarrior lines deserve a distinct adapter technology rather than remaining under the current `ide-sdk` umbrella.
- Determine whether classic COM automation and classic plug-in APIs should remain one AIDE lane or split later for finer historical accuracy.
