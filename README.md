# Atlas-Ai

Atlas v1.0 is a frozen, repository-oriented, deterministic architecture implementation scaffold.

## Architecture Status

- Architecture: Frozen
- Implementation: Started
- Version: 1.0.0

## Current Implementation Scope

This repository contains the initial implementation scaffold for all 22 frozen Atlas repositories, shared core primitives, a deterministic Event Bus, and architecture compliance tests.

## Frozen Rules

- One repository owns one domain.
- Repositories communicate through public interfaces or Event Bus.
- Runtime, Security, Audit, Configuration, and Logging are infrastructure concerns.
- Objects exchanged across boundaries are immutable.
- Determinism is mandatory.

## Hybrid Repository Layout

Atlas-Ai now exposes each frozen repository at the repository root for architecture visibility while keeping executable Python implementations under the `atlas/` package for deterministic imports. See `LAYOUT.md` for the mapping.
