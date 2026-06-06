# Official Standards Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Gauge が CLASSIFY / RECOMMEND フェーズで参照する公式基準リファレンス。

---

## 1. 公式4段階チェックリスト

### Phase 1: Before You Start

| # | Check | Detail |
|---|-------|--------|
| 1 | Use case identification | 2-3 concrete use cases defined |
| 2 | Tool inventory | Built-in or MCP tools identified |
| 3 | Guide review | Official guide and example skills reviewed |
| 4 | Folder structure plan | Directory layout planned |

### Phase 2: During Development

| # | Check | Detail |
|---|-------|--------|
| 5 | Folder naming | kebab-case |
| 6 | SKILL.md existence | Exact spelling `SKILL.md` (case-sensitive) |
| 7 | YAML delimiters | `---` present at start and end |
| 8 | name field | kebab-case, no spaces, no capitals, matches folder |
| 9 | description field | Includes WHAT + WHEN |
| 10 | No XML tags | No `<` `>` anywhere in file |
| 11 | Clear instructions | Actionable, not vague |
| 12 | Error handling | Recovery steps included |
| 13 | Examples | At least one usage example |
| 14 | References linked | `reference/` files properly referenced |

### Phase 3: Before Upload

| # | Check | Detail |
|---|-------|--------|
| 15 | Trigger test — obvious | Triggers on direct requests |
| 16 | Trigger test — paraphrased | Triggers on rephrased requests |
| 17 | Negative trigger test | Does NOT trigger on unrelated topics |
| 18 | Functional tests | Core workflow completes successfully |
| 19 | Tool integration | MCP/built-in tools work (if applicable) |

### Phase 4: After Upload

| # | Check | Detail |
|---|-------|--------|
| 20 | Real conversation test | Works in actual usage |
| 21 | Under/over-trigger monitor | Trigger behavior observed |
| 22 | User feedback collection | Feedback loop established |
| 23 | Iteration cycle | Description and instructions updated based on feedback |

---

## 2. 公式 Frontmatter 検証仕様

### Required Fields

| Field | Format | Constraint | Validation Rule |
|-------|--------|-----------|----------------|
| `name` | `kebab-case` | No spaces, no capitals, no underscores | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `description` | Free text | ≤ 1024 chars, no XML tags (`<` `>`) | Must include WHAT + WHEN (trigger phrases) |

### Security Restrictions

| Rule | Reason |
|------|--------|
| No XML angle brackets in frontmatter | Frontmatter appears in system prompt; prevents injection |
| No `"claude"` / `"anthropic"` in name | Reserved prefixes |
| Safe YAML parsing only | No code execution in YAML |

### Optional Fields

| Field | Format | Constraint |
|-------|--------|-----------|
| `license` | SPDX identifier | e.g. `MIT`, `Apache-2.0` |
| `allowed-tools` | Space-separated tool list | e.g. `"Bash(python:*) WebFetch"` |
| `compatibility` | Free text | 1-500 characters |
| `metadata` | YAML mapping | Any key-value pairs (`author`, `version`, `mcp-server`, `category`, `tags`, etc.) |

### YAML Formatting Rules

```yaml
# CORRECT — delimiters present
---
name: my-skill
description: Does things
---

# WRONG — missing delimiters
name: my-skill
description: Does things

# WRONG — unclosed quotes
---
name: my-skill
description: "Does things
---
```

### File Naming Rules

| Element | Rule | Example |
|---------|------|---------|
| SKILL.md | Exact case-sensitive name | `SKILL.md` ✅, `skill.md` ❌, `SKILL.MD` ❌ |
| Skill folder | kebab-case | `notion-project-setup` ✅, `Notion Project Setup` ❌ |
| No README.md | Inside skill folder | Documentation in `SKILL.md` or `reference/` only |

> **Note**: エコシステムの `normalization-checklist.md` は16項目の内部基準を使用するが、この公式チェックリストはAnthropic公式の品質基準。両方を満たすことが理想。

---

## 3. トラブルシューティング 6カテゴリ

### Category 1: Upload Failure

| Error | Cause | Solution |
|-------|-------|----------|
| `"Could not find SKILL.md"` | ファイル名が正確でない | `ls -la` で確認、`SKILL.md` にリネーム |
| `"Invalid frontmatter"` | YAML フォーマットエラー | `---` デリミタ確認、引用符閉じ確認 |
| `"Invalid skill name"` | name にスペースまたは大文字 | kebab-case に修正 |

### Category 2: Skill Doesn't Trigger (Undertriggering)

**Symptom**: Skill never loads automatically

**Diagnosis**:
- Description が generic すぎる（"Helps with projects"）
- トリガーフレーズが不足
- 関連ファイルタイプの言及がない

**Solution**: Description を改善 — 具体的なキーワード・技術用語を追加

**Debug method**: `"When would you use the [skill name] skill?"` と Claude に問う

### Category 3: Skill Triggers Too Often (Overtriggering)

**Symptom**: Skill loads for unrelated queries

**Solutions**:
1. Negative triggers 追加: `"Do NOT use for simple data exploration"`
2. スコープ明確化: `"specifically for online payment workflows, not for general financial queries"`
3. Description をより具体的に

### Category 4: Instructions Not Followed (Execution Issues)

**Symptom**: Skill loads but Claude doesn't follow instructions

**Common Causes & Solutions**:

| Cause | Solution |
|-------|----------|
| Instructions too verbose | Concise bullet points, detailed docs to `reference/` |
| Critical instructions buried | Put key rules at top, use `## Important` / `## Critical` |
| Ambiguous language | `"CRITICAL: Before calling create_project, verify: ..."` |
| Model laziness | Add `"Take your time to do this thoroughly"` (user prompt に追加がより効果的) |

**Advanced**: Deterministic validation にはスクリプトを bundling する

### Category 5: MCP Connection Issues

**Symptom**: Skill loads but MCP calls fail

**Checklist**:
1. MCP server connected (Settings > Extensions)
2. Authentication valid (API keys, OAuth tokens, permissions/scopes)
3. MCP independent test: `"Use [Service] MCP to fetch my projects"` — failure = MCP issue, not skill
4. Tool names correct (case-sensitive)

### Category 6: Large Context Issues

**Symptom**: Slow responses or degraded quality

**Causes**: Skill content too large, too many skills enabled, no progressive disclosure

**Solutions**:
1. SKILL.md を 5,000 words 以下に最適化
2. 詳細を `reference/` へ移動
3. 20-50以上のスキルが同時有効なら選択的に有効化
4. Skill packs で関連機能をグループ化

---

## 4. 品質シグナル

### Quantitative Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Trigger rate | **90%+** on relevant queries | Run 10-20 test queries, track automatic loading vs explicit invocation |
| Workflow efficiency | Complete in X tool calls | Compare same task with/without skill, count tool calls and tokens |
| API reliability | **0 failed API calls** per workflow | Monitor MCP server logs, track retry rates and error codes |

### Qualitative Metrics

| Metric | Assessment Method |
|--------|------------------|
| No next-step prompting needed | During testing, note how often redirect/clarification is needed. Ask beta users. |
| Workflow completes without correction | Run same request 3-5 times, compare structural consistency and quality |
| Consistent cross-session results | Can a new user accomplish the task on first try with minimal guidance? |

---

## 5. 配布要件

### Distribution Surfaces

| Surface | Method |
|---------|--------|
| **Claude.ai** | Settings > Capabilities > Skills > Upload (zip) |
| **Claude Code** | Place in skills directory |
| **API** | `/v1/skills` endpoint, `container.skills` parameter |
| **Organization** | Admin workspace-wide deployment (centralized management, automatic updates) |

### Positioning Best Practices

| Do | Don't |
|----|-------|
| Focus on **outcomes** | Focus on technical implementation |
| Highlight MCP + Skills story | Describe folder structure |
| Provide installation guide | Assume users know the process |

### GitHub Distribution

1. Public repo with clear README (repo-level, NOT inside skill folder)
2. Link from MCP documentation
3. Include quick-start guide with screenshots
