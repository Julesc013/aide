# AIDE-BUILD-PROJECTGRAPH-CONTEXTPACK-SLICE-01

## Objective

Build a narrow ProjectGraph-driven ContextPack selection slice.

## Plan

1. Define which ProjectGraph facts may enter a ContextPack.
2. Include allowed roots, forbidden roots, likely paths, symbols, contracts,
   tests, doc claims, issues, warnings, and evidence requirements.
3. Preserve existing ContextPack authority and queue truth.
4. Validate and stop at `needs_review`.
