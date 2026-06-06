# Gateway Output Format

## Standard Output Template

```markdown
## API Design: [Endpoint Name]

### Overview
**Method:** [GET/POST/PUT/PATCH/DELETE]
**Path:** [/api/v1/resource]
**Purpose:** [Brief description]

### Request
**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |

**Query Parameters:** (for GET)
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| [param] | [type] | [yes/no] | [desc] |

**Request Body:** (for POST/PUT/PATCH)
```json
{
  "field": "value"
}
```

### Response
**Success (200/201):**
```json
{
  "data": { }
}
```

**Errors:**
| Status | Code | When |
|--------|------|------|
| 400 | VALIDATION_ERROR | Invalid input |
| 404 | NOT_FOUND | Resource missing |

### OpenAPI Specification
[Complete YAML specification]

### Implementation Notes
- [Note 1]
- [Note 2]

### Breaking Change Analysis
- [ ] No breaking changes
- [ ] Breaking changes identified: [list]
```
