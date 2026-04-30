# Dominium Policies

## Purpose

This directory contains strict Dominium Bridge policy overlays.

The overlays are stricter than baseline AIDE policy. They do not weaken `.aide/policies/**` or `.aide/queue/policy.yaml`, and they do not authorize bypassing AIDE review gates.

## Records

- `review-gates.yaml`: bridge review gates for adoption, pinning, generated targets, and policy changes.
- `proof-gates.yaml`: Dominium-local proof evidence expectations.
- `generated-artifacts.yaml`: generated target rules for future Dominium outputs.
