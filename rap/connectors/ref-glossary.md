# ref-glossary

Term definitions for Baton connector development.

---

## Core Terms

| Term | Definition |
|------|------------|
| **Baton** | The connector framework: Go SDK + individual connectors |
| **baton-sdk** | Go library that handles sync orchestration and pagination |
| **Connector** | Go binary that syncs access data from a system |
| **c1z** | Compressed sync output file (gzip SQLite) |
| **Meta-connector** | Configuration-driven connector (baton-http, baton-sql) |

## Access Model

| Term | Definition |
|------|------------|
| **Resource** | Entity in target system: user, group, role, app |
| **Resource Type** | Classification with traits (e.g., "user" with TRAIT_USER) |
| **Trait** | Resource classification: TRAIT_USER, TRAIT_GROUP, TRAIT_ROLE, TRAIT_APP |
| **Entitlement** | Permission that can be granted (e.g., "admin" on a group) |
| **Grant** | Assignment of entitlement to principal |
| **Principal** | Entity receiving grants (typically users) |

## SDK Concepts

| Term | Definition |
|------|------------|
| **ResourceSyncer** | Interface: ResourceType, List, Entitlements, Grants methods |
| **pagination.Token** | SDK type for page cursors |
| **pagination.Bag** | SDK type for nested pagination state |
| **uhttp** | SDK HTTP client with retries and rate limiting |
| **RawId** | Annotation carrying external system's identifier |

## Sync Lifecycle

| Term | Definition |
|------|------------|
| **Sync** | Reading access data from a system |
| **Uplift** | ConductorOne process transforming raw records to domain objects |
| **ID Correlation** | Matching resources across syncs using RawId |

## Provisioning

| Term | Definition |
|------|------------|
| **Provision** | Writing access changes (grant, revoke, create, delete) |
| **Grant** (operation) | Add entitlement to principal |
| **Revoke** | Remove entitlement from principal |
| **CreateAccount** | JIT provisioning - create user in target system |
| **DeleteResource** | Remove resource from target system |

## Run Modes

| Term | Definition |
|------|------------|
| **One-shot** | Run once, produce c1z file, exit |
| **Daemon** | Long-running, polls ConductorOne for tasks |
| **Hosted** | Run by ConductorOne infrastructure |

## Meta-Connector Terms

| Term | Definition |
|------|------------|
| **CEL** | Common Expression Language for data transformation |
| **items_path** | JSONPath to array in API response |
| **primary_key** | Column used for cursor pagination |
| **skip_if** | CEL condition to filter grants |
