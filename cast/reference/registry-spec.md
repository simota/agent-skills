# Cast Registry Specification

Purpose: Define the registry structure, lifecycle transitions, and validation rules for `.agents/personas/registry.yaml`.

## Contents

1. Directory layout
2. Registry schema
3. Lifecycle states
4. Operations
5. Validation rules

## Directory Layout

```text
.agents/personas/
├── registry.yaml
├── {service-name}/
│   └── {persona-name}.md
└── _archive/
    └── {service-name}/
```

## Registry Schema

### Top-Level Fields

| Field | Meaning |
|---|---|
| `version` | Registry schema version |
| `services` | Service-level persona index |
| `updated` | Last registry update date |

### Service Entry Fields

| Field | Required | Meaning |
|---|---|---|
| `service` | Yes | Service identifier |
| `type` | Yes | `b2b`, `b2c`, `internal`, or mixed usage marker |
| `personas` | Yes | Persona entries |
| `coverage` | Yes | Coverage summary |

### Persona Entry Fields

| Field | Required | Meaning |
|---|---|---|
| `name` | Yes | Persona display name |
| `file` | Yes | Relative file path |
| `status` | Yes | `draft`, `active`, `evolved`, `archived` |
| `type` | Yes | `user` or `internal` |
| `category` | Yes | Persona family |
| `version` | Yes | `X.Y` |
| `confidence` | Yes | `0.0-1.0` |
| `updated` | Yes | ISO date |
| `echo_base_mapping` | No | Echo anchor |

### Coverage Fields

| Field | Meaning |
|---|---|
| `segments_covered` | Count of covered segments |
| `coverage_gaps` | Known uncovered or stale areas |
| `duplicates` | Known overlap or merge candidates |

## Lifecycle States

| Status | Meaning | Allowed next steps |
|---|---|---|
| `draft` | Created but insufficiently validated | validate, edit, delete |
| `active` | Validated and in use | evolve, distribute, audit, archive |
| `evolved` | Transitional state during accepted update | settle to `active` |
| `archived` | Preserved but not active | restore or keep archived |

## Operations

| Operation | Registry effect |
|---|---|
| `CONJURE` | Add persona entry |
| `FUSE` | Update existing persona metadata |
| `EVOLVE` | Increment version, update status and confidence |
| `AUDIT` | No structural change; produce findings |
| `DISTRIBUTE` | No structural change; may emit handoff artifacts |
| `Archive` | Move to `_archive/`, set `status: archived` |

### Archive Rules

When archiving:

1. Move the file to `_archive/{service-name}/`.
2. Set `status: archived`.
3. Update the stored file path.
4. Record archival reason and date.
5. Update coverage if no replacement exists.

## Validation Rules

- File path must exist.
- Persona names must be unique within a service.
- Status must be one of `draft`, `active`, `evolved`, `archived`.
- Confidence must be within `0.0-1.0`.
- Version must match `X.Y`.
- Dates must be ISO-formatted.
- Active personas should have an Echo mapping unless intentionally exempt.
- Coverage counts must be internally consistent.
