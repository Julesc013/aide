# Implementation Summary

This task adds a thin Eureka adapter that binds one existing Eureka read-only
JSON command to the proposed generic registered-process provider.

The adapter provides:

- repository identity and revision preflight;
- clean checkout enforcement;
- exact argv construction;
- sanitized process environment;
- one-process launch accounting;
- Eureka JSON decoding;
- typed result/refusal mapping;
- before/after state comparison;
- scrubbed reports and deterministic projections.

It does not alter the generic provider.
