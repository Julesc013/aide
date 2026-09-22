# Admission Review Request

## Gate

`.aide/policies/review-gates.yaml` requires explicit human review for changes
to `.aide/queue/**`.

## Proposed Effect

Add `AIDE-CONVERGENCE-AND-DELIVERY-01` as a review-gated umbrella programme and
index it. The programme coordinates future child WorkUnits but authorizes no
implementation, branch mutation, main promotion, release, publication, secret
access, machine configuration change, or target-repository mutation.

## Candidate

- Base HEAD: `2a44f17eb7232757133df549ac6fc519d535e71b`
- Owner intent hash: `1de3e5eff2b91fe5908d362f51f8513cdd73a5d87c97b1244425bccf0261fbad`
- Private action-pack hash: `13c4975eefbbe8c4e088f83f3cbf405cb5ca99a95c4e8678568163e03286b2c9`
- Recovery status hash: `739962744b5e3a98d2c6c2acecd0d8ae355f8db4a4419a3ecfd13481b6f4a87b`
- Task SHA-256: `e351d952e212f433ec8971de25e6d5c94788f08703d1169426047a47c2534e06`
- Status SHA-256: `c1a7f164caaa4f654505eb7291f40d01ea97cbfdae07e98d0a8cb340ae634349`
- ExecPlan SHA-256: `08a62941a06ba288675d18d60eefef4c7557be42c6719bda5de7e33f22e486b0`
- Prompt SHA-256: `add48abe57a3a40a16acf0c0fb6ea0e4bde572d12bd1bd5accbbc92646fb0878`
- Queue index SHA-256: `aebb81236d03b83f2c6f9267ec9853c36222998fbc3409dd4cb9a1b31885a98f`

## Remaining Risk

- Multiple Codex processes exist; future writers must recheck ownership and state.
- One stale detached worktree registration is unavailable and must not be pruned.
- Existing dirty task evidence remains unclassified at the individual-path level.
- The private source material has identity proof but no semantic adoption.

## Rollback

Before acceptance, remove only this candidate's new queue directory and exact
index entry, then restore the previous four latest-intake artifacts from the
private recovery snapshot. No such rollback is performed automatically.

## Exact Decision Requested

Approve or reject admission of this programme packet at its recorded candidate
identity. Approval permits preparation and execution of separately bounded child
WorkUnits; it does not approve any future main merge, tag, asset upload, or
publication candidate.
