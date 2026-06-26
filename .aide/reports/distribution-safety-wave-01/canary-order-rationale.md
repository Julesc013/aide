# Canary Order Rationale

The canary order is:

1. ScreenSave
2. Eureka
3. Dominium

ScreenSave should come first because it is the smaller and more deterministic target profile. It is best suited for validating dry-run ownership classification, install/update planning, and no-apply boundaries.

Eureka should come second because it stresses evidence and provenance complexity after the smaller profile has passed.

Dominium should come third because it has the broadest product, Workbench, and domain surface. It should not be used as the first real-profile proof.

All canary profile tasks in this wave are inventory, profile, ownership classification, and dry-run planning tasks unless a later reviewed task explicitly grants mutation authority.
