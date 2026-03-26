# AIDE Architecture

This directory contains the canonical architecture documents for AIDE's shared core and host-adapter contract system.

Files in this area define:

- the overall system shape
- the boundary between shared and host-specific logic
- the adapter contract and execution modes
- feature, settings, diagnostics, protocol, and capability-negotiation models
- architecture decisions that are intended to remain durable across later prompts

These documents guide the future `shared/` implementation tree. They should be updated when implementation forces a durable contract change, not when a temporary experiment occurs.
