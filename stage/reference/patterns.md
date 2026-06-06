# Stage Design Patterns

## Tooling Versions (verified 2026-05)

| Tool | Version | Released | Notes |
|------|---------|----------|-------|
| Marp CLI | 4.4.0 | 2025-05-06 | Node.js v26 support; Linux AArch64 (ARM64) standalone binary added. Built on Marpit 3.2.1 + Marp Core 4.3.0. API marked stable since 4.3.0. (https://github.com/marp-team/marp-cli/releases) |
| reveal.js | 6.0.1 | 2026-04-11 (after 6.0.0 on 2026-03-11) | Official React wrapper `@revealjs/react`; Vite 8 build pipeline; TS 6 types bundled; new `controls: 'speaker'` option; alt tag enforcement for images/videos. (https://github.com/hakimel/reveal.js/releases) |
| Slidev | 52.15.2 | 2025-05-10 | New versioning scheme: v0.50 (2024-12) → v51 (2025-01) → v52.x. Monaco editor enabled by default since 0.48; auto-registers Shiki languages to Monaco; v52.15 adds named animation presets, Bluesky embed, laser pointer, Mermaid renderer plugin, resizable presenter borders. (https://github.com/slidevjs/slidev/releases) |

When pinning in CI, prefer the major+minor (`@marp-team/marp-cli@4.4`, `reveal.js@6.0`, `@slidev/cli@52.15`) so security patches still flow.

## AI Slide Generation Landscape (2026-05)

When the user requests AI-generated decks rather than Markdown-based code, route or hand off as below.

| Tool | 2026 capabilities | Best for |
|------|------------------|----------|
| Gamma (https://gamma.app/) | "AI Agent" introduced in 2026 update for iterative refinement; Gamma Imagine (2026-03-17) generates charts/infographics; Nested Cards; subtle animations | Startups, marketing, link-shared decks |
| Beautiful.ai | Slide-by-slide structured templates with AI design suggestions; PPTX export | Corporate decks needing PowerPoint parity |
| Microsoft Copilot in PowerPoint | Builds decks from Word docs/outlines; image generation via DALL·E 3; narrative reorganization | Enterprise M365 environments |
| Google Slides + Gemini | Sidebar Gemini for layouts, diagrams, theme-matched new slides via prompt; Imagen-powered image gen | Google Workspace teams |

Stage itself outputs runnable Markdown (Marp/reveal/Slidev). For Gamma/Beautiful.ai/Copilot/Gemini decks, provide the narrative arc + content brief and direct the user to paste into the AI tool.

## Marp Syntax

```markdown
---
marp: true
theme: default
paginate: true
header: "Title"
footer: "Author | Date"
---

# Slide Title

Content here

---

# Next Slide

- Bullet 1
- Bullet 2

<!-- Speaker notes go here -->
```

### Marp Directives

| Directive | Purpose | Example |
|-----------|---------|---------|
| `<!-- _class: lead -->` | Title/lead slide style | Opening slides |
| `<!-- _class: invert -->` | Dark background | Emphasis slides |
| `<!-- _backgroundColor: #hex -->` | Custom background | Branded slides |
| `<!-- _color: #hex -->` | Text color | Contrast adjustment |
| `<!-- _paginate: false -->` | Hide page number | Title/closing slides |

## reveal.js Syntax

```html
<section>
  <h1>Slide Title</h1>
  <p>Content</p>
  <aside class="notes">Speaker notes</aside>
</section>

<section>
  <section>Vertical slide 1</section>
  <section>Vertical slide 2</section>
</section>
```

## Slidev Syntax

```markdown
---
theme: seriph
title: Presentation Title
---

# Slide 1

Content

---
transition: slide-left
---

# Slide 2

<v-click>Appears on click</v-click>

<!--
Speaker notes here
-->
```

## Narrative Arc Patterns

### Problem-Solution Arc

```
Slide 1: Hook (surprising stat or question)
Slide 2-3: Problem definition (pain points)
Slide 4: Impact/cost of the problem
Slide 5: Solution introduction
Slide 6-8: Solution demo/walkthrough
Slide 9: Results/proof
Slide 10: CTA
```

### AIDA Arc

```
Attention: Provocative opening (1 slide)
Interest: Why this matters (2-3 slides)
Desire: How it works, benefits (3-5 slides)
Action: What to do next (1-2 slides)
```

### Tutorial Arc

```
Goal: What you'll learn (1 slide)
Prerequisites: What you need (1 slide)
Steps: Step-by-step walkthrough (5-15 slides)
Summary: Key takeaways (1 slide)
Resources: Links and next steps (1 slide)
```

## Theme Design Patterns

### Minimal Dark

```yaml
theme:
  background: "#1a1a2e"
  text: "#eaeaea"
  accent: "#e94560"
  code_bg: "#16213e"
  font: "Inter, sans-serif"
  code_font: "JetBrains Mono, monospace"
```

### Corporate Light

```yaml
theme:
  background: "#ffffff"
  text: "#333333"
  accent: "#0066cc"
  code_bg: "#f5f5f5"
  font: "Noto Sans JP, sans-serif"
  code_font: "Source Code Pro, monospace"
```

## Code Slide Patterns

### Highlighted Code Block

```markdown
# Implementation

​```typescript {3-5|7-9}
function processOrder(order: Order) {
  // Step 1: Validate
  const validated = validate(order);
  if (!validated) throw new ValidationError();

  // Step 2: Process
  const result = await process(validated);
  return result;
}
​```
```

### Split Layout (Code + Explanation)

```markdown
# Architecture

::left::
​```typescript
const app = new Hono()
app.use(authMiddleware)
app.route('/api', apiRouter)
​```

::right::
1. Initialize framework
2. Apply auth middleware
3. Mount API routes
```

## Diagram Embedding (Mermaid v11+)

Mermaid v11.13.0 (2026-04, https://mermaid.ai/blog/posts/mermaid-v11-13-0-two-new-diagram-types-and-our-most-polished-release-yet) added new diagram types for slides:

| Diagram Type | Status | Best For |
|-------------|--------|---------|
| Flowchart | Stable | Architecture, decision trees |
| Sequence | Stable | API flows, request/response |
| ER | Stable | Data model slides |
| Gantt | Stable | Project timeline slides |
| Venn | NEW (v11.13) | Concept overlap, audience segmentation |
| Ishikawa | NEW (v11.13) | Root-cause analysis talks |
| Treemap | Beta (v11.8+) | Hierarchical data visualization |
| Wardley Map | Stable (v11+) | Strategy/vision keynotes |

**Slidev:** Use fenced code blocks tagged `mermaid`; Slidev auto-renders via the Mermaid renderer plugin (available since v52.15, https://github.com/slidevjs/slidev/releases).
**Marp:** Use `<!-- mermaid ... -->` HTML comment passthrough or inline SVG; direct fenced-code rendering is not built-in — pre-render diagrams to SVG/PNG for reliable output.
**reveal.js:** Include Mermaid.js CDN or npm package and initialize in `Reveal.initialize()`; use `<div class="mermaid">` tags in slides.

## Slide Count Guidelines

| Duration | Total slides | Content slides | Transition slides |
|----------|-------------|----------------|-------------------|
| 5 min LT | 8-12 | 6-8 | 2-4 |
| 15 min | 15-25 | 12-18 | 3-7 |
| 30 min | 30-45 | 25-35 | 5-10 |
| 45 min keynote | 45-70 | 35-50 | 10-20 |
