# concepts-ids

RawId annotation, external_id, and how ConductorOne matches resources across syncs.

---

## Why ID Correlation Matters

ConductorOne needs to know if a resource in this sync is the same resource from a previous sync. This enables:
- Tracking changes over time
- Correlating resources across connectors
- Supporting pre-sync reservation patterns

## The RawId Annotation

When building a resource, include the external system's ID:

```go
resource, _ := resourceBuilder.NewGroupResource(
    group.Name,
    groupResourceType,
    group.Id,  // Used internally by SDK
    []resource.GroupTraitOption{},
)
// Add external ID for correlation
resource.WithAnnotation(&v2.RawId{Id: group.Id})
```

## ID Flow Through the System

| Stage | Term | Purpose |
|-------|------|---------|
| Connector output | `RawId` annotation | External system's stable identifier |
| Sync storage | `external_id` | Same value on ConnectorResource records |
| Domain objects | `source_connector_ids` | Map of connector_id to external_id |
| Domain objects | `raw_baton_id` | Canonical external ID after merge |

Flow: `RawId` (connector) -> `external_id` (sync) -> `source_connector_ids` (domain)

## What Value to Use

Use the external system's native, stable identifier:

| System | Use |
|--------|-----|
| Okta | `app.Id` |
| AWS | ARN |
| GCP | Project ID |
| GitHub | Repository ID (numeric) |
| Database | Primary key |

**Properties of good IDs:**
- Stable (doesn't change when resource is renamed)
- Unique within the system
- Native to the external system

## Common Mistakes

**Using display names:** Names change. `engineering-team` might become `platform-team`.

**Using composite keys:** If you construct `org/repo`, changes to either part break correlation.

**Omitting RawId:** Without it, ConductorOne can't correlate resources across syncs.

## Pre-sync Reservation

The `match_baton_id` field (in Terraform/API) allows creating ConductorOne objects before the connector discovers them. When the connector syncs, resources are matched by this ID.
