# AIDE Core

## Purpose

AIDE Core is the durable, host-agnostic substance of AIDE. It owns the semantics that AIDE Hosts and AIDE Bridges consume, validate, or expose.

Q02 creates this skeleton only. It does not move the bootstrap-era `shared/**` implementation, change imports, or claim the reboot Core is implemented.

## Internal Bands

- Contract: profiles, schemas, commands, policies, tasks, eval declarations, component maps, and environment declarations.
- Harness: import, compile, validate, doctor, bakeoff, migrate, drift-check, fixture, and evidence machinery.
- Runtime: future broker, scheduler, router, context service, patch engine, approvals, workers, transport, and state/cache substrate.
- Compatibility: schema versions, migrations, replay corpora, shims, upgrade gates, deprecation rules, and support posture.
- Control: eval inventories, environment records, matrices, packaging metadata, benchmarks, cost/latency envelopes, and queue policy links.
- SDK: future stable consumption surfaces for hosts, services, protocol bindings, generated artifacts, capability descriptors, and replay or approval schemas.

## First Stack

The first shipped reboot stack remains Contract + Harness + Compatibility + Dominium Bridge. This directory records the target shape; it does not implement that stack.

## Bootstrap-Era Boundary

Existing `shared/**`, `specs/**`, `evals/**`, `inventory/**`, `matrices/**`, `environments/**`, `packaging/**`, and host proof records remain in their current locations until a later reviewed queue item authorizes a safe migration.
