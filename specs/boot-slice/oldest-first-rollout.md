# Oldest-First Rollout

## Global Principle

AIDE follows an oldest-first rollout doctrine, but the doctrine is applied honestly:

- within each family, the oldest documented version ids are attempted first
- across families, the first rollout phase targets the oldest committed lane in each family
- companion fallback lanes may proceed when the primary native lane is blocked, but that does not erase the native oldest-first target

This avoids a fake linear order across partially unresolved archival timelines while preserving the oldest-first rule where the repository has real evidence.

## Actual Rollout Structure

### Phase 1: Family-Oldest Lanes

Start with the oldest committed lane in each family:

- `hosts/microsoft/visual-studio/com-addin`
- `hosts/microsoft/visual-studio-mac/monodevelop-addin`
- `hosts/apple/xcode/companion`
- `hosts/metrowerks/codewarrior/ide-sdk`

This phase proves the boot slice on the oldest family frontier before later breakpoints are allowed to dominate the program.

### Phase 1 Fallback: Family Fallback Lanes

If a phase-1 native or archival-native lane is blocked, companion fallback may proceed in the same family:

- `hosts/microsoft/visual-studio-mac/companion`
- `hosts/metrowerks/codewarrior/companion`

The fallback is a continuity rule, not a redefinition of the family's primary oldest lane.

### Phase 2: Next Breakpoints

After phase 1 is satisfied or explicitly blocked with records, move to the next researched breakpoint in the affected families:

- `hosts/microsoft/visual-studio/vsix-v1`
- `hosts/apple/xcode/xcodekit`

### Phase 3: Reference Native Lane

After the older Windows and Apple breakpoints are accounted for, move to the main native Windows reference lane:

- `hosts/microsoft/visual-studio/vsix-v2-vssdk`

### Phase 4: Modern Advance

Advance to the newest modern Windows lane only after earlier Windows breakpoints are represented:

- `hosts/microsoft/visual-studio/extensibility`

## Family-Specific Sequencing

### Microsoft Visual Studio

`vs97 -> vs6 -> vs2002 -> vs2003 -> vs2005 -> vs2008 -> vs2010 -> vs2012 -> vs2013 -> vs2015 -> vs2017 -> vs2019 -> vs2022 -> vs2026`

Mapped rollout lanes:

- `com-addin`
- `vsix-v1`
- `vsix-v2-vssdk`
- `extensibility`

### Microsoft Visual Studio For Mac

`vsmac2017 -> vsmac2019 -> vsmac2022`

Mapped rollout lanes:

- `monodevelop-addin`
- `companion` as fallback when the native archival path is blocked

### Apple Xcode

`xcode1 -> xcode2 -> xcode3 -> xcode4 -> xcode5 -> xcode6 -> xcode7 -> xcode8 -> xcode9 -> xcode10 -> xcode11 -> xcode12 -> xcode13 -> xcode14 -> xcode15 -> xcode16 -> xcode26`

Mapped rollout lanes:

- `companion` for `xcode1` through `xcode7`
- `xcodekit` for `xcode8` and later

### Metrowerks CodeWarrior

`cw3 -> cw5 -> cw6 -> cw7 -> cw8 -> cw9 -> cw10 -> cw11`

Mapped rollout lanes:

- `ide-sdk` as the primary lane, exact for classic families and conservative for later umbrella coverage
- `companion` as fallback when native proof is blocked or the later umbrella cannot honestly stay native

## Blocker Handling

Blocked lanes do not cancel oldest-first. They create a recorded stop condition:

1. record the blocker explicitly
2. keep the blocked lane in its original phase
3. continue with the family fallback lane if one exists
4. continue with the next unblocked lane in the same global phase

## Consumption Rule For Later Prompts

Later implementation prompts should select work in this order:

1. lowest incomplete rollout phase
2. oldest unresolved version id within that lane's sequence basis
3. family fallback only when the primary lane is explicitly blocked

This makes the rollout plan both oldest-first and operationally realistic.
