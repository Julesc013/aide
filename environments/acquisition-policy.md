# Acquisition Policy

## Purpose

This document defines AIDE's operational policy for recording install sources, media provenance, redistribution posture, and local storage expectations.

It supports repository discipline. It is not legal advice.

## Core rule

AIDE does not assume that proprietary installers, images, or toolchains belong in Git.

The repository should track metadata about acquisition and provenance without redistributing assets that are proprietary, locally held, or otherwise unsuitable for source control.

## Expected recordkeeping

When media or toolchains are tracked, future prompts should record:

- source class
- redistribution posture
- provenance evidence status
- checksum status where feasible
- local storage expectation
- license-note status
- concise notes about unresolved acquisition or licensing questions

## Source classes

Typical source classes include:

- official-download
- official-archive
- owned-physical-media
- user-supplied
- third-party-archive
- unknown

These are operational categories only. They do not themselves grant redistribution rights.

## Redistribution posture

Each tracked item should record whether it is:

- redistributable
- local-only
- unknown

`local-only` is the conservative default for proprietary or unresolved material.

## Provenance and checksum posture

Environment work should prefer explicit provenance records and checksums when those can be captured honestly.

Examples of useful provenance evidence include:

- recorded download URL or archive source
- physical-media label notes
- user-supplied source attestation
- recorded checksum or hash note

If provenance is incomplete, record that explicitly rather than inventing certainty.

## Storage expectation

The repository tracks metadata and references. Actual install media, snapshots, and heavyweight images may remain:

- outside Git in local storage
- on removable media
- in archival storage referenced by metadata only

## Operational boundary

This policy supports repository behavior, evidence capture, and conservative handling of historical assets.

It does not provide legal advice or determine license rights on its own.
