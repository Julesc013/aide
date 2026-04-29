# Q02 Remaining Risks And Deferrals

## Review Risks

- Q00 remains `needs_review`.
- Q01 remains `needs_review`.
- Q02 proceeded because the current human prompt explicitly authorized implementation despite those prior review gates.
- Q02 is `needs_review` and must not be treated as accepted until reviewed.

## Deferred Queue Work

- Q03 profile contract v0 is not implemented.
- Q04 Harness v0 is not implemented.
- Q05 generated artifacts v0 is not implemented.
- Q06 compatibility baseline is not implemented.
- Q07 Dominium Bridge baseline is not implemented.
- Q08 self-hosting automation is not implemented.

## Structural Deferrals

- Existing `shared/**` code was not migrated into `core/**`.
- Existing host proof lanes were not moved into `hosts/extensions/**`.
- Existing `scripts/**` were not moved into `hosts/cli/**` or `core/harness/**`.
- Existing control-plane areas were mapped conceptually, not physically moved.

## Product Deferrals

- Runtime, Service, Commander, Mobile, IDE extension implementation, provider adapters, app surfaces, generated artifacts, packaging automation, release publishing, and autonomous service logic remain out of scope.
