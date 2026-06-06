# Common Infographic Output Spec

> Shared payload spec for any agent to emit a visual-summary handoff. No new agent. No middle layer.

## Purpose

Any agent that produces analytical results MAY append an `Infographic_Payload` to its output. The payload is a self-contained, schema-validated description of an infographic that a downstream image-generation agent (typically Sketch) can render directly into a one-glance visual.

This spec exists so visualization stays opt-in per agent, the vocabulary stays closed and consistent across the ecosystem, and no orchestration overhead is added.

## Five Principles

1. **No data, no visual** — emit no payload when `data_points` is empty.
2. **One visual element = one data point** — every visible element maps to a `data_points` entry with `evidence`.
3. **Closed vocabulary** — `layout`, `style_pack`, and `icon_hint` use only the values catalogued below. New values require Architect approval.
4. **Upstream PII scrub** — the source agent owns redaction; downstream consumers re-scan but cannot recover lost context.
5. **Image generation is delegated** — payload producers never call image APIs. Receivers (Sketch, etc.) execute.

## Schema

```yaml
Infographic_Payload:
  intent: status | summary | dashboard | comparison | timeline
  layout: hero-stat | card-grid | dashboard | timeline | matrix
  style_pack: corporate-clean | editorial-magazine | data-viz-bold | minimalist-iso | warning-alert
  title: <≤ 40 chars>
  subtitle: <≤ 80 chars, optional>
  data_points:
    - label: <short>
      value: <number | short text>
      unit: <%, count, ms, USD, ...>
      tone: neutral | positive | warning | critical
      icon_hint: <from icon catalog>
      evidence: <path:line | metric URL | report ref>
  aspect_ratio: "16:9" | "1:1" | "2:3"
  pii_redacted: true | false
  notes: <optional, e.g. "exec audience: simplify jargon">
```

Validation rules:
- `intent`, `layout`, `style_pack`, `title`, `data_points`, `aspect_ratio`, `pii_redacted` are required
- `data_points` length must match the chosen layout's range (see Layout Catalog)
- Reject the payload silently if any rule fails — never emit a half-valid block

## Layout Catalog (5)

| Layout | Use | Composition | Data Points |
|--------|-----|-------------|-------------|
| `hero-stat` | Single dominant metric | One large numeral + label + 3-4 supporting KPIs | 1 primary + 3-4 supporting |
| `card-grid` | Parallel comparison | 3-9 cards, each: icon + value + label | 3-9 |
| `dashboard` | Multi-dimensional snapshot | Charts + gauges + trend lines + KPI tiles | 5-12 |
| `timeline` | Sequence of events over time | Horizontal axis + markers + labels + emphasis | 5-15 |
| `matrix` | 2-axis classification | 4 quadrants or heatmap grid | 6-30 |

## Style Pack Catalog (5)

| Pack | Tone | Palette | Use |
|------|------|---------|-----|
| `corporate-clean` | Flat, restrained, business-doc | Navy / gray / single accent | Exec reports, audits |
| `editorial-magazine` | Magazine, strong typography, generous whitespace | Multi-color, ink texture | Internal comms, onboarding |
| `data-viz-bold` | Chart-led, high contrast | Bright contrasts (blue/orange/green) | Dashboards, KPIs |
| `minimalist-iso` | Isometric / line art | Mono + one accent | Architecture, system overview |
| `warning-alert` | Strong urgency colors | Red / yellow / black | Incidents, vulnerabilities |

## Icon Catalog

Closed vocabulary (~50). Use the exact tokens below as `icon_hint`:

| Group | Tokens |
|-------|--------|
| Status | `check-circle` `x-circle` `alert-triangle` `info-circle` `question-mark` |
| Security | `shield` `shield-broken` `lock-closed` `lock-open` `key` `fingerprint` |
| Trend | `chart-up` `chart-down` `chart-line` `chart-bar` `chart-pie` |
| Time | `clock` `calendar` `hourglass` `timer` `refresh` |
| Quality | `thumbs-up` `thumbs-down` `star` `flag` `ribbon` |
| Code | `branch` `commit` `pull-request` `merge` `code-block` |
| System | `server` `database` `cloud` `container` `network` |
| People | `user` `users` `user-group` `profile` `persona` |
| Comms | `message` `bell` `mail` `phone` `broadcast` |
| Money | `coin` `currency` `wallet` `receipt` `scale` |

Unknown icon → use the closest catalog entry; never invent tokens.

## Payload → Sketch Prompt Template

Receivers (typically Sketch) construct prompts as follows:

```
[Style]: <style_pack visual language keywords>
[Layout]: <layout name>, <N> elements
[Title]: <title>
[Subtitle]: <subtitle if any>
[Elements]:
  - <data_point.label>: <value> <unit> (<tone> color, <icon_hint>)
  - ...
[Composition]: <aspect_ratio>, infographic, single panel, no characters
[Negative]: photograph, anime, gore, sexualization, watermark, signature,
            multiple titles, illegible text, fictional logos
```

The negative prompt is fixed across the ecosystem to keep outputs as data-summary infographics rather than illustrative scenes.

## Integration Patterns (3)

Each adopting skill picks one or more, fully opt-in.

### P-1 — Append to Output Requirements (recommended default)
Add one bullet to the skill's Output Requirements section:
```markdown
- Optionally emit `Infographic_Payload` per `_common/INFOGRAPHIC.md`
  (recommended: layout=<X>, style_pack=<Y>) when a visual summary adds value.
```

### P-2 — Dedicated Recipe (visualize-only mode)
Add a recipe row:
```markdown
| Visualize | `visualize` | | Emit Infographic_Payload only, skip prose | `_common/INFOGRAPHIC.md` |
```
Use when reports are large and the user often wants the visual alone.

### P-3 — Embedded in AUTORUN `_STEP_COMPLETE`
Add an optional field under the existing `Output:` block:
```yaml
_STEP_COMPLETE:
  Agent: <name>
  ...
  Output: ...
  Infographic_Payload:    # optional
    intent: ...
    layout: ...
    ...
```
Use for chains where Nexus auto-renders visuals downstream.

## Adoption Notes

- **Do not modify `description:`** — keep trigger keys stable. Adoption is signaled in the body of SKILL.md, not the frontmatter.
- **Minimum viable adoption** — one P-1 bullet in Output Requirements.
- **Never break existing Output structure** — payload is additive, never replaces prose results.
- **Silent skip** — if `data_points` is empty, PII not scrubbed, or vocabulary out of catalog, omit the payload rather than emit a partial one.
- **Per-agent recommendations** — skills SHOULD recommend a default `layout` × `style_pack` pair in their P-1 bullet so the user gets a coherent visual on the first try.

## Recommended Defaults (current adopters)

| Agent | Default layout | Default style_pack | Notes |
|-------|----------------|--------------------|-------|
| Sentinel | `card-grid` | `warning-alert` | CVE / secret / auth scorecards |
| Pulse | `dashboard` | `data-viz-bold` | KPI overview |
| Atlas | `matrix` | `minimalist-iso` | Service × risk matrix |
| Trail | `timeline` | `editorial-magazine` | Commits / regressions / releases |
| Voice | `hero-stat` | `corporate-clean` | NPS / sentiment headline |
| Beacon | `dashboard` | `data-viz-bold` | SLO / error budget / latency |
| Ledger | `card-grid` | `corporate-clean` | Top-N service costs |
| Compete | `matrix` | `editorial-magazine` | Competitor × feature matrix |
| Helm | `timeline` | `corporate-clean` | Strategic roadmap |
| Harvest | `dashboard` | `corporate-clean` | PR throughput, review time |
| Schema | `matrix` | `minimalist-iso` | Entity-relationship overview |
| Voyager | `dashboard` | `data-viz-bold` | E2E run summary |
| Vista | `dashboard` | `data-viz-bold` | Test-quality snapshot |
| Field | `card-grid` | `editorial-magazine` | Persona / insight cards |
| Oath | `card-grid` | `warning-alert` | Control-status scorecard |
| Triage | `timeline` | `warning-alert` | Incident timeline |
| Experiment | `hero-stat` | `data-viz-bold` | Uplift / verdict summary |
| Echo | `card-grid` | `editorial-magazine` | Friction / emotion summary |

Hex (character anthropomorphization) and Realm (pixel-art ecosystem) intentionally use their own pipelines and do not emit `Infographic_Payload`.

## Versioning

This spec is v1. Schema changes require Architect approval. Adopters reference `_common/INFOGRAPHIC.md` without pinning a version; backward-compatible additions are expected.
