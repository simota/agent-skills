# API Review Checklist

## Design Review

```markdown
## API Design Review: [Endpoint Name]

### Naming & Structure
- [ ] URL follows REST conventions (nouns, plural)
- [ ] HTTP methods used correctly
- [ ] Consistent naming style (camelCase/snake_case)
- [ ] Nested resources properly structured
- [ ] Query parameters for filtering/sorting (not in body)

### Request
- [ ] Request body schema defined
- [ ] Required vs optional fields clear
- [ ] Field types appropriate
- [ ] Validation rules specified
- [ ] Examples provided

### Response
- [ ] Response schema defined
- [ ] All possible status codes documented
- [ ] Error responses consistent
- [ ] Pagination for list endpoints
- [ ] Timestamps in ISO 8601 format

### Security
- [ ] Authentication specified
- [ ] Authorization rules documented
- [ ] Sensitive data not in URL/logs
- [ ] Rate limiting defined
- [ ] Input validation prevents injection

### Documentation
- [ ] Summary and description present
- [ ] Request/response examples
- [ ] Error scenarios documented
- [ ] Edge cases covered
```

## Specification Validation

Before handoff to Builder, validate the specification:

```markdown
## API Specification Validation Checklist

### Schema Completeness
- [ ] すべてのリクエストボディにスキーマ定義がある
- [ ] すべてのレスポンスにスキーマ定義がある
- [ ] 必須フィールドが明示されている
- [ ] フィールドの型が適切（string/number/boolean/array/object）
- [ ] 制約（minLength, maxLength, minimum, maximum, pattern）が定義されている

### Example Coverage
- [ ] リクエストボディの例がある
- [ ] 成功レスポンスの例がある
- [ ] エラーレスポンスの例がある
- [ ] エッジケースの例がある（空配列、null値など）

### Error Definition
- [ ] すべての可能なステータスコードが列挙されている
- [ ] エラーコードが一覧されている
- [ ] エラーメッセージが実装と一致している

### Tool Validation
- [ ] OpenAPI Linter (spectral) でエラーなし
- [ ] スキーマがJSONとして有効
- [ ] $ref が正しく解決される
```
