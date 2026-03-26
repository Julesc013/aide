# Shared Local Service

`shared/local-service/` is the future home for the shared broker or daemon surface used by `local-service` execution.

This area should own local service lifecycle, request dispatch, and health boundaries without absorbing host-specific UI or packaging logic.
