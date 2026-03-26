# AIDE Capability Levels

## Purpose

This document defines the capability levels used by AIDE to describe verified integration depth for a host lane.

## Capability Levels

- `L0`: loads and identifies host and version.
- `L1`: registers a command or entry point.
- `L2`: provides editor or file interaction.
- `L3`: provides project or workspace awareness.
- `L4`: provides deep IDE integration.

## Interpretation Rules

- Capability levels describe verified depth, not aspiration.
- A lane claiming `L3` is expected to satisfy the lower levels needed to reach that state unless explicitly documented otherwise.
- Capability levels do not imply identical user experience across hosts.
- Capability levels should be paired with support tier, state, and mode for honest reporting.

## Capability Ceilings

- Capability ceilings differ by host family and extension technology.
- Some hosts will only ever support a companion or archival lane and may never reach `L4`.
- A lower ceiling is not a defect if it is the highest honest result for that host contract.

## Usage Rule

- Use capability levels when describing the current verified ceiling of a lane.
- Do not use them as a substitute for exact feature-by-feature evaluation evidence.
