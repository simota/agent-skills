# Breaking Change Detection

## Detection Checklist

```markdown
## API Change Impact Analysis

**Endpoint:** [METHOD /path]
**Change Type:** [Add/Modify/Remove]

### Field Changes
| Field | Before | After | Breaking? |
|-------|--------|-------|-----------|
| [field] | [type] | [type] | [Yes/No] |

### Request Changes
- [ ] Required field added → BREAKING
- [ ] Field type changed → BREAKING
- [ ] Field removed → BREAKING (if clients send it)
- [ ] Validation stricter → BREAKING
- [ ] Optional field added → Safe

### Response Changes
- [ ] Field removed → BREAKING
- [ ] Field type changed → BREAKING
- [ ] Field renamed → BREAKING
- [ ] New field added → Safe
- [ ] Null handling changed → Potentially breaking

### Behavioral Changes
- [ ] Error codes changed → Potentially breaking
- [ ] Pagination changed → BREAKING
- [ ] Rate limits changed → Potentially breaking
- [ ] Authentication changed → BREAKING

### Impact Assessment
**Affected Clients:** [List known consumers]
**Migration Effort:** [Low/Medium/High]
**Recommended Action:** [Version bump / Deprecate / Safe to deploy]
```

## Compatibility Matrix

```
Before → After         Breaking?   Action Required
─────────────────────────────────────────────────
string → number        YES         New version
number → string        YES         New version
required → optional    NO          Safe
optional → required    YES         New version
field exists → removed YES         New version
null → non-null        YES         New version
non-null → nullable    NO          Safe (usually)
array → object         YES         New version
add enum value         NO*         Safe (lenient clients)
remove enum value      YES         New version
```
