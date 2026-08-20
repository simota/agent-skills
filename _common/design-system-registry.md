# Design System Registry (Common Protocol)

> **Tier:** `domain` — activates when the task's subject matches. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

**Purpose**: Persist per-project design systems (colors, typography, components, brand rules) so design-related skills can resume context across chains and sessions. Inspired by Claude Design by Anthropic Labs (2026-04-17): "During onboarding, Claude builds a design system for your team by reading your codebase and design files."

**Scope**: This protocol is used by `atelier`, `muse`, `frame`, `ink`, `palette`, and `artisan`. Other skills may read but should not write.

---

## Storage

### Location

Registry files live under `.agents/design-system/` in the project root:

```
.agents/
└── design-system/
    ├── default.json           # Default system (applied unless overridden)
    ├── marketing-2026.json    # Marketing campaign variant
    ├── dashboard-dark.json    # Product surface variant
    └── INDEX.md               # Human-readable index of known systems
```

Multiple systems per project are explicitly supported — mirrors Claude Design's "maintain multiple systems" capability.

### File Format

JSON with the following top-level keys. All keys optional except `name`, `version`, and `scope`.

```json
{
  "name": "marketing-2026",
  "version": "1.3.0",
  "scope": "project",
  "source": {
    "extracted_from": ["tailwind.config.ts", "figma://file/abc123", "app/globals.css"],
    "extracted_by": "frame+muse",
    "extracted_at": "2026-04-18T10:30:00Z"
  },
  "color": {
    "primary": { "50": "#f0f9ff", "500": "#0ea5e9", "900": "#0c4a6e" },
    "neutral": { "0": "#ffffff", "950": "#0a0a0a" },
    "semantic": {
      "success": "#10b981",
      "warning": "#f59e0b",
      "danger":  "#ef4444"
    }
  },
  "typography": {
    "families": {
      "sans": "Inter, system-ui, sans-serif",
      "serif": "Fraunces, Georgia, serif",
      "mono": "JetBrains Mono, Menlo, monospace"
    },
    "scale": {
      "xs": "0.75rem",
      "sm": "0.875rem",
      "base": "1rem",
      "lg": "1.125rem",
      "xl": "1.25rem"
    },
    "weights": { "regular": 400, "medium": 500, "bold": 700 }
  },
  "spacing": {
    "base_unit": "4px",
    "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96]
  },
  "radius": {
    "sm": "4px",
    "md": "8px",
    "lg": "16px",
    "pill": "9999px"
  },
  "shadow": {
    "sm": "0 1px 2px rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px rgb(0 0 0 / 0.10)"
  },
  "motion": {
    "durations": { "fast": "150ms", "base": "250ms", "slow": "400ms" },
    "easings": { "standard": "cubic-bezier(0.4, 0, 0.2, 1)" }
  },
  "components": {
    "Button": {
      "variants": ["primary", "secondary", "ghost"],
      "sizes": ["sm", "md", "lg"],
      "source": "components/ui/button.tsx"
    },
    "Card": { "source": "components/ui/card.tsx" }
  },
  "brand": {
    "voice": "Calm, technical, non-marketing",
    "do": ["Use specifics over adjectives", "Lowercase headlines"],
    "dont": ["Pastel palettes", '"Delightful" / "powerful" in copy'],
    "logo": {
      "primary": "assets/logo.svg",
      "monochrome_only": true
    }
  },
  "a11y": {
    "contrast_target": "WCAG 2.2 AA",
    "min_touch_target": "44px",
    "motion_preference": "respects prefers-reduced-motion"
  },
  "platform": ["web", "mobile-web"],
  "notes": "Derived from Tailwind config + Figma tokens file. Last synced with Figma 2026-04-17."
}
```

### INDEX.md (Human-readable index)

```markdown
# Design Systems Registry

| Name | Version | Scope | Updated | Source |
|------|---------|-------|---------|--------|
| default | 1.0.0 | project | 2026-04-15 | tailwind.config.ts |
| marketing-2026 | 1.3.0 | campaign | 2026-04-18 | figma + tailwind |
| dashboard-dark | 0.9.0 | product | 2026-04-17 | globals.css + handcrafted |
```

---

## Lifecycle

### Onboarding (first use on a project)

When any registered skill (atelier/muse/frame/ink/palette/artisan) is invoked on a project without `.agents/design-system/default.json`:

1. Detect source files: `tailwind.config.*`, `theme.ts`, `tokens.json`, `*.css` with CSS variables, Figma file IDs in README/package.json
2. If Figma access is available, use `frame` to extract via MCP
3. Derive tokens (colors/typography/spacing/radius/shadow/motion)
4. Scan for component barrels (`components/ui/*`, `src/components/*`) to populate `components.{Name}.source`
5. Write `default.json` + initial `INDEX.md`
6. Emit onboarding summary via `_STEP_COMPLETE` including a link to the new registry

### Read (typical case)

```
1. Read .agents/design-system/INDEX.md
2. If user specifies a variant (e.g., "use marketing tokens"), load that JSON
3. Else load default.json
4. Pass to downstream agents via DESIGN_INTENT_HANDOFF.Registry_Ref
```

### Write (updates)

Updates require explicit intent. Skills MUST NOT silently mutate registry files.

| Update type | Who | Approval needed |
|-------------|-----|-----------------|
| New token added (e.g., new color) | muse/frame | Auto, bump minor version |
| Existing token changed | muse/frame | User confirmation, bump major version |
| New component registered | artisan/forge | Auto, bump minor version |
| Brand voice / do-don't edited | atelier/vision | User confirmation |
| New variant file created | atelier | Auto (creates new file, doesn't mutate default) |
| System deleted | user | Hard confirmation only |

All writes append an entry to `INDEX.md`.

### Sync (keep registry fresh)

When source files drift from registry:
1. `frame` or `muse` detect drift on next invocation (hash comparison)
2. Emit `REGISTRY_DRIFT` warning in handoff
3. Suggest re-extraction to user; never auto-apply

---

## Access Rules

| Skill | Read | Write new | Write update | Delete |
|-------|------|-----------|--------------|--------|
| atelier | ✓ | ✓ | ✓ (with user confirm) | ✗ |
| muse | ✓ | ✓ | ✓ (tokens only, bump version) | ✗ |
| frame | ✓ | ✓ | ✓ (Figma-sourced fields) | ✗ |
| ink | ✓ | ✗ | ✓ (assets.icons only) | ✗ |
| palette | ✓ | ✗ | ✓ (a11y fields) | ✗ |
| artisan | ✓ | ✗ | ✓ (components source paths) | ✗ |
| forge | ✓ | ✗ | ✗ | ✗ |
| Other skills | ✓ | ✗ | ✗ | ✗ |

Non-design skills may read for context (e.g., `prose` checking brand voice) but must not write.

---

## Handoff Integration

When handing off, pass `Registry_Ref` in `DESIGN_INTENT_HANDOFF`:

```yaml
DESIGN_INTENT_HANDOFF:
  Intent: "..."
  Tokens: "registry:marketing-2026"   # shorthand → resolves to .agents/design-system/marketing-2026.json
  Registry_Ref: ".agents/design-system/marketing-2026.json"
  ...
```

Downstream agents MUST resolve `Registry_Ref` before starting work. If the file does not exist, escalate (do not proceed with hallucinated tokens).

---

## Anti-patterns

1. **Free-form tokens in handoffs** — always reference the registry; don't paste hex values inline unless the registry is truly empty
2. **Duplicating registries across skills** — single source of truth; one project, one `.agents/design-system/` directory
3. **Mutating `default.json` without version bump** — every change MUST bump `version` and log in `INDEX.md`
4. **Skipping onboarding** — if no registry exists on first design task, run onboarding rather than fabricating tokens
5. **Re-extracting on every invocation** — use hash/mtime checks; only re-extract when source drifted

---

## Secret and PII Guard

Registry files live alongside project source and may be committed. Treat them as public-by-default:

- **Never persist** API keys, Figma personal access tokens, customer PII, email addresses, or internal-only URLs containing auth.
- `source.extracted_from` MUST be file paths, bare Figma file IDs, or public URLs — never URLs with `?token=`, `Authorization:` headers, or query strings carrying credentials.
- `brand.logo.*` points to asset paths in the repo; never to authenticated CDN URLs.
- `notes` is human-readable prose — no stack traces, no error messages containing tokens, no debug dumps.
- If a registry write would otherwise violate these rules, skills MUST redact the sensitive fragment (e.g., `figma://file/ABC123` instead of `https://figma.com/file/ABC123?access_token=xxx`) or refuse the write.
- Project-level `.gitignore` is the responsibility of the repo owner, but `.agents/design-system/` SHOULD be committed so that design context persists across collaborators; this makes the secret guard non-optional.

Skills that detect a secret-looking value (high-entropy string, JWT-shaped token, `sk_` / `pk_` prefixes) during extraction MUST abort the write and surface a `REGISTRY_SECRET_DETECTED` warning in `_STEP_COMPLETE`.
