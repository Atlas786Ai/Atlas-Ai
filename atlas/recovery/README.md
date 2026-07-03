# RecoveryRepository

Purpose: frozen Atlas v1.0 implementation of `RecoveryRepository`.

Responsibilities are limited to the repository domain defined in the Atlas Codex Implementation Guide.

## Public Interfaces

- `recover()`
- `rollback()`
- `restore_snapshot()`
- `restart_workflow()`
- `validate_recovery()`
- `archive_recovery()`
- `get_recovery()`

## Architecture

This repository follows the canonical Atlas repository template: configuration, constants, interfaces, models, schemas, services, validators, serializers, mappers, events, exceptions, metrics, health, version, tests, and docs.

## Owner

Atlas Governance

## Version

1.0.0
