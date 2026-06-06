# Error Response & Pagination Patterns

> **Scope**: Error response format/catalog and pagination patterns (offset/cursor). For rate-limit algorithms, headers, and 429 semantics, see `rate-limit-patterns.md` (the canonical source).

## Error Response Design

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid data",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email must be a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Password must be at least 8 characters"
      }
    ],
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "documentation": "https://api.example.com/docs/errors#VALIDATION_ERROR"
  }
}
```

### Error Code Catalog

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Request validation failed |
| `INVALID_JSON` | 400 | Request body is not valid JSON |
| `MISSING_FIELD` | 400 | Required field not provided |
| `INVALID_FORMAT` | 400 | Field format is invalid |
| `UNAUTHORIZED` | 401 | Authentication required |
| `INVALID_TOKEN` | 401 | Token is invalid or expired |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource does not exist |
| `METHOD_NOT_ALLOWED` | 405 | HTTP method not supported |
| `CONFLICT` | 409 | Resource state conflict |
| `RATE_LIMITED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

## Pagination Patterns

### Offset-based Pagination

```json
// Request
GET /api/v1/users?limit=10&offset=20

// Response
{
  "data": [...],
  "meta": {
    "total": 150,
    "limit": 10,
    "offset": 20,
    "hasMore": true
  },
  "links": {
    "self": "/api/v1/users?limit=10&offset=20",
    "first": "/api/v1/users?limit=10&offset=0",
    "prev": "/api/v1/users?limit=10&offset=10",
    "next": "/api/v1/users?limit=10&offset=30",
    "last": "/api/v1/users?limit=10&offset=140"
  }
}
```

### Cursor-based Pagination (Recommended for large datasets)

```json
// Request
GET /api/v1/users?limit=10&cursor=eyJpZCI6MTIzfQ==

// Response
{
  "data": [...],
  "meta": {
    "limit": 10,
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTMzfQ==",
    "prevCursor": "eyJpZCI6MTEzfQ=="
  },
  "links": {
    "self": "/api/v1/users?limit=10&cursor=eyJpZCI6MTIzfQ==",
    "next": "/api/v1/users?limit=10&cursor=eyJpZCI6MTMzfQ==",
    "prev": "/api/v1/users?limit=10&cursor=eyJpZCI6MTEzfQ=="
  }
}
```

### Comparison

| Aspect | Offset | Cursor |
|--------|--------|--------|
| Random access | Yes | No |
| Consistent with changes | No | Yes |
| Performance on large sets | Poor | Good |
| Simple implementation | Yes | More complex |
| Use case | Small datasets, UI pages | Large datasets, feeds |

### Pagination Selection Criteria

```
予想レコード数は？
├─ <1,000件 → Offset (シンプルで十分)
├─ 1,000〜10,000件 → 用途次第
│   ├─ ランダムアクセス必要 → Offset
│   └─ 一貫性重視 → Cursor
└─ >10,000件 → Cursor (パフォーマンス優先)

リアルタイム更新があるか？
├─ はい（フィード、通知等） → Cursor
└─ いいえ → Offset でも可

ページ番号UIが必要か？
├─ はい（「3ページ目」表示） → Offset
└─ いいえ（無限スクロール等） → Cursor
```

**選択時の確認事項:**
- [ ] 既存APIの方式と整合性があるか
- [ ] クライアント実装の複雑さは許容範囲か
- [ ] 将来のデータ増加を考慮しているか
