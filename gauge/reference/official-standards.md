# Official Standards Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

Official standards reference used by Gauge in the CLASSIFY / RECOMMEND phases.

---

## 1. Official 4-Phase Checklist

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

## 2. Official Frontmatter Validation Spec

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

> **Note**: The ecosystem's `normalization-checklist.md` uses a 16-item internal standard, while this official checklist is Anthropic's official quality standard. Meeting both is ideal.

---

## 3. Troubleshooting — 6 Categories

### Category 1: Upload Failure

| Error | Cause | Solution |
|-------|-------|----------|
| `"Could not find SKILL.md"` | Filename is not exact | Verify with `ls -la`, rename to `SKILL.md` |
| `"Invalid frontmatter"` | YAML format error | Check `---` delimiters, check for unclosed quotes |
| `"Invalid skill name"` | Spaces or capitals in name | Fix to kebab-case |

### Category 2: Skill Doesn't Trigger (Undertriggering)

**Symptom**: Skill never loads automatically

**Diagnosis**:
- Description is too generic ("Helps with projects")
- Missing trigger phrases
- No mention of relevant file types

**Solution**: Improve the description — add specific keywords and technical terms

**Debug method**: Ask Claude `"When would you use the [skill name] skill?"`

### Category 3: Skill Triggers Too Often (Overtriggering)

**Symptom**: Skill loads for unrelated queries

**Solutions**:
1. Add negative triggers: `"Do NOT use for simple data exploration"`
2. Clarify scope: `"specifically for online payment workflows, not for general financial queries"`
3. Make the description more specific

### Category 4: Instructions Not Followed (Execution Issues)

**Symptom**: Skill loads but Claude doesn't follow instructions

**Diagnose the layer before rewording.** "It was ignored" is a symptom, not a cause, and the
reflex fix — adding emphasis — is the one intervention that reliably makes things worse. Work down
this list in order and stop at the first layer that explains the behavior:

| # | Layer | Check |
|---|-------|-------|
| 1 | **Loading** | Did the file actually enter context? Wrong cwd, unmatched filename, empty file, truncation, or a post-compaction reload that never happened. Verify before anything else. |
| 2 | **Scope** | It loaded, but does it apply to this task? Test the negative case too — a scoped rule leaking into unrelated work is the same defect inverted. |
| 3 | **Ambiguity** | Can the line be read two ways? Rewrite as Condition + Directive + Verification + Boundary: not "run relevant tests" but "on `src/api/**` changes run `make test-api`; add `make test-contract` for public schema changes." |
| 4 | **Conflict** | List *every* source touching this action — root, package, local, managed, task prompt, hook/CI — before editing any one of them. |
| 5 | **Context overload** | The rule is clear but buried. Remove duplicates, scope the loading, move procedures to `reference/`. |
| 6 | **Capability** | Does the session have the tool the rule assumes? If not, the rule needs a stated fallback, not stronger wording. |
| 7 | **Enforceability** | A constraint that must hold even under pressure belongs in a hook or permission rule — see `_common/MECHANISM_SELECTION.md`. |
| 8 | **Variability** | Adherence is never 100%. Do not conclude from one run; reproduce before rewriting. |

> **Do not add emphasis as a first move.** More `IMPORTANT` / `CRITICAL` markers inflate priority
> across the whole file: when everything is critical, nothing is, and the markers stop carrying
> signal. Anthropic measured a **3% intelligence drop** from this class of pressure wording, and it
> does not surface in task-level evals — `_common/OPUS_5_AUTHORING.md`. Reserve emphasis for the
> few constraints that genuinely outrank the rest, after layers 1-4 are ruled out.

**Then** apply the ordinary fixes: concise bullets with detail moved to `reference/`, key rules
placed early, and a bundled script wherever the check can be made deterministic.

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
1. Optimize SKILL.md to under 5,000 words
2. Move details to `reference/`
3. If 20-50+ skills are enabled simultaneously, enable selectively
4. Group related features with Skill packs

---

## 4. Quality Signals

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

## 5. Distribution Requirements

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
