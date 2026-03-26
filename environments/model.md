# Environment Model

## Purpose

This document defines the stable concepts used to track AIDE environment work.

## Environment family

An environment family is a reusable environment pattern.

Examples:

- a virtualization recipe for a Windows host and guest combination
- an emulation pattern for a historical platform
- a physical-hardware setup class

Families describe structure. They do not claim that a specific runnable instance already exists.

## Environment instance

An environment instance is a concrete tracked setup or attempted setup.

An instance may reference:

- one environment family
- one host OS family
- one guest OS family where applicable
- one IDE family and exact IDE version id where known
- media, toolchain, and snapshot records
- current bring-up or bootability state

## Install media

Install media is the tracked source material needed to construct or recover an environment.

Examples include:

- installer images
- optical-disc images
- locally held archives
- user-supplied packages

Media records track provenance and storage expectations. They do not imply redistribution rights.

## Toolchain

A toolchain record tracks environment-adjacent compilers, SDKs, runtimes, debuggers, or related support material required for bring-up or validation.

Toolchains are tracked separately because one environment may need several of them and the same toolchain may be reused across multiple environments.

## Snapshot

A snapshot is a checkpoint or recoverable image associated with an environment instance.

Snapshots may represent:

- VM checkpoints
- emulator save states
- disk images
- archival captures

Snapshot records track existence and storage expectations without assuming the binary image lives in Git.

## Bootability state

Bootability state records how far a concrete environment has progressed.

The stable vocabulary for this repository is defined in `environments/catalogs/bootability-status.yaml`.

## Blocker

A blocker is an explicit impediment to acquisition, installation, boot, validation, or preservation.

Blockers may attach to:

- an environment family
- a concrete environment instance
- install media
- a toolchain
- a playbook step

## Archival record

An archival record captures historically useful environment evidence even when a runnable setup does not currently exist.

Archival records are important because old-IDE support is partly an environment-preservation problem, not only a software-integration problem.

## Relationship summary

- families define reusable environment patterns
- instances reference families and concrete status
- media and toolchains support instances
- snapshots preserve instance state
- blockers explain why an instance is stalled
- archival records preserve evidence when a runnable path is not yet available
