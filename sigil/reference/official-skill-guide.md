# Official Skill Guide Reference

> Source: "The Complete Guide to Building Skills for Claude" (Anthropic, 2025)

The official spec reference that Sigil consults during the CRAFT / VERIFY phases.

---

## 1. Progressive Disclosure: The 3-Level Architecture

Skills adopt three levels of context management:

| Level | What | When loaded | Token impact |
|-------|------|-------------|-------------|
| **1st — YAML frontmatter** | name + description | Always (system prompt) | Minimal |
| **2nd — SKILL.md body** | Full instructions | When Claude judges the skill relevant | Medium |
| **3rd — Linked files** | `reference/`, `scripts/`, `assets/` | On-demand, as Claude navigates | Variable |

**Design principle**: Keep SKILL.md focused on core instructions, and move detailed documentation to `reference/`, linking to it. SKILL.md is recommended to stay under 5,000 words.

---

## 2. YAML Frontmatter Full Specification

### Required Fields

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### `name` Rules

- kebab-case only (`my-cool-skill`)
- No spaces, no capitals, no underscores
- Must match the folder name
- Must not include `"claude"` / `"anthropic"` (reserved)

### `description` Rules

- **Required structure**: `[What it does]` + `[When to use it]` + `[Key capabilities]`
- **Limit**: 1024 characters (official)
- XML tags (`<` `>`) are forbidden (security constraint: frontmatter is expanded into the system prompt)
- Include concrete trigger phrases
- Mention relevant file types if applicable

> **Note**: The ecosystem-internal [`skill-templates.md`](skill-templates.md#frontmatter-rules) restricts `description` to "one Japanese sentence," but the official spec's limit is 1024 characters. The ecosystem restriction is an additional guardrail for context efficiency and routing decisions, and does not exceed the official spec.

### Optional Fields

| Field | Constraint | Purpose |
|-------|-----------|---------|
| `license` | e.g. `MIT`, `Apache-2.0` | Open-source distribution |
| `allowed-tools` | e.g. `"Bash(python:*) WebFetch"` | Tool access restriction |
| `compatibility` | 1-500 characters | Environment requirements |
| `metadata` | Any YAML key-value | `author`, `version`, `mcp-server`, `category`, `tags` etc. |

### Security Restrictions

- XML angle brackets (`<` `>`) — must not appear in frontmatter
- `"claude"` / `"anthropic"` must not be used in `name` (reserved prefix)
- Code execution in YAML is not allowed (safe YAML parsing)

---

## 3. Description Writing Rules

### Good Examples

```yaml
# Specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Clear value proposition
description: End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".
```

### Bad Examples

```yaml
# Too vague — won't trigger reliably
description: Helps with projects.

# Missing triggers — Claude can't judge when to load
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

### Debugging Approach

> Ask Claude: "When would you use the [skill name] skill?" — Claude will quote the description back. Adjust based on what's missing.

---

## 4. Instruction Structure Best Practices

### Recommended Structure

```markdown
---
name: your-skill
description: [...]
---
# Your Skill Name

## Instructions

### Step 1: [First Major Step]
Clear explanation of what happens.
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
Expected output: [describe what success looks like]
```

### Examples
Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link

### Troubleshooting
Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

### Best Practices

| Practice | Detail |
|----------|--------|
| **Be Specific** | `Run python scripts/validate.py --input {filename}` > `Validate the data` |
| **Progressive Disclosure** | Core instructions in SKILL.md, detailed docs in `reference/` |
| **Error Handling** | Include MCP connection failure recovery steps |
| **Reference Bundled Resources** | `Before writing queries, consult reference/api-patterns.md` |
| **Critical Instructions First** | Put key rules at the top; use `## Important` / `## Critical` headers |
| **Concise Over Verbose** | Bullet points and numbered lists over prose |

### Advanced: Deterministic Validation

> For critical validations, consider bundling a script that performs checks programmatically rather than relying on language instructions. Code is deterministic; language interpretation isn't.

---

## 5. File Structure Requirements

```
your-skill-name/
├── SKILL.md              # Required — main skill file
├── scripts/              # Optional — executable code
│   ├── process_data.py
│   └── validate.sh
├── reference/           # Optional — documentation
│   ├── api-guide.md
│   └── examples/
└── assets/               # Optional — templates, fonts, icons
    └── report-template.md
```

**Critical Rules**:
- The filename must be exactly `SKILL.md` (case-sensitive). `SKILL.MD` and `skill.md` are not allowed.
- The folder name must be kebab-case: `notion-project-setup`
- Do not include a `README.md` inside the skill folder (documentation belongs in `SKILL.md` or `reference/`)
- Prepare a GitHub repo-level README separately (for distribution)

---

## 6. The MCP + Skills Relationship (Kitchen Analogy)

| Aspect | MCP (Connectivity) | Skills (Knowledge) |
|--------|--------------------|--------------------|
| Role | Professional kitchen (tools, ingredients, equipment) | Recipes (step-by-step instructions) |
| Function | Connects Claude to services (Notion, Asana, Linear, etc.) | Teaches Claude how to use services effectively |
| Provides | Real-time data access and tool invocation | Workflows and best practices |
| Answers | **What** Claude can do | **How** Claude should do it |

### Without Skills (MCP only)

- Users connect MCP but don't know what to do next
- Support tickets asking "how do I do X with your integration"
- Each conversation starts from scratch
- Inconsistent results

### With Skills + MCP

- Pre-built workflows activate automatically
- Consistent, reliable tool usage
- Best practices embedded in every interaction
- Lower learning curve

---

## 7. Composability & Portability

- **Composability**: Claude can load multiple skills simultaneously. Skills should work well alongside others, not assume exclusive capability.
- **Portability**: Skills work identically across Claude.ai, Claude Code, and API. Create once, works across all surfaces (provided environment supports dependencies).

---

## 8. Testing Methodology (3 Levels × 3 Areas)

### 3 Testing Levels

| Level | Method | Setup |
|-------|--------|-------|
| **Manual** | Run queries directly in Claude.ai | No setup, fast iteration |
| **Scripted** | Automate test cases in Claude Code | Repeatable validation |
| **Programmatic** | Run an evaluation suite via the Skills API | Systematic, defined test sets |

### 3 Testing Areas

#### Area 1: Triggering Tests

- ✅ Triggers on obvious tasks
- ✅ Triggers on paraphrased requests
- ❌ Doesn't trigger on unrelated topics

```
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
```

#### Area 2: Functional Tests

- Valid outputs generated
- API calls succeed
- Error handling works
- Edge cases covered

#### Area 3: Performance Comparison

Baseline (without skill) vs With skill comparison:
- Back-and-forth messages count
- Failed API calls
- Token consumption

---

## 9. Iteration Signals

### Undertriggering Signals

- Skill doesn't load when it should
- Users manually enabling it
- Support questions about when to use it
- **Solution**: Add more detail and nuance to description — include keywords, especially technical terms

### Overtriggering Signals

- Skill loads for irrelevant queries
- Users disabling it
- Confusion about purpose
- **Solution**: Add negative triggers, be more specific. Clarify scope.

```yaml
# Negative trigger example
description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. Do NOT use for simple data exploration (use data-viz skill instead).
```

### Execution Issues

- Inconsistent results
- API call failures
- User corrections needed
- **Solution**: Improve instructions, add error handling. Put critical instructions first. Use scripts for deterministic validation.

---

## 10. Official Quick Checklist

### Before You Start

- [ ] 2-3 concrete use cases identified
- [ ] Tools identified (built-in or MCP)
- [ ] Reviewed guide and example skills
- [ ] Planned folder structure

### During Development

- [ ] Folder named in kebab-case
- [ ] `SKILL.md` file exists (exact spelling)
- [ ] YAML frontmatter has `---` delimiters
- [ ] `name` field: kebab-case, no spaces, no capitals
- [ ] `description` includes WHAT and WHEN
- [ ] No XML tags (`<` `>`) anywhere
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked

### Before Upload

- [ ] Tested triggering on obvious tasks
- [ ] Tested triggering on paraphrased requests
- [ ] Verified doesn't trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Tool integration works (if applicable)

### After Upload

- [ ] Test in real conversations
- [ ] Monitor for under/over-triggering
- [ ] Collect user feedback
- [ ] Iterate on description and instructions
