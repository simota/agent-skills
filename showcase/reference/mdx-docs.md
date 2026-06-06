# MDX Documentation in Storybook Reference

Purpose: Hand-author rich component documentation in Storybook using MDX 3 + Storybook 10's Doc Blocks. MDX combines Markdown narrative with embedded JSX, letting authors mix prose, live story embeds, prop tables, and design tokens in a single file. Used when Autodocs' single-page generated output is insufficient — typically for design-system foundations, multi-page guides, and migration handbooks.

## Scope Boundary

- **showcase `mdx`**: hand-authored `.mdx` documentation pages with Doc Blocks (`<Meta>`, `<Story>`, `<Canvas>`, `<Controls>`, `<Source>`, `<ArgTypes>`). Multi-page narrative docs.
- **showcase `story` (default, elsewhere)**: CSF story authoring. MDX consumes those stories — does not replace them.
- **showcase `catalog` (elsewhere)**: hierarchy/organization decisions (Atoms/Molecules/Organisms). MDX is the surface; catalog is the structure.
- **showcase `interaction` (elsewhere)**: play-function tests. MDX can embed stories that contain play functions, but does not author them.
- **artisan (elsewhere)**: production component code. MDX documents components but never alters them.
- **forge (elsewhere)**: prototype-stage docs are inline READMEs at most; MDX investment comes after promotion.
- **voyager (elsewhere)**: E2E flow narratives belong in test reports, not component docs.
- **echo `walkthrough` (elsewhere)**: persona walkthrough output is its own artifact; reference from MDX, but do not duplicate.
- **quill (elsewhere)**: long-form prose docs outside Storybook (READMEs, contributor guides). Hand off when the audience expands beyond component consumers.

## Workflow

```
SCAN     →  audit existing Autodocs pages: which need narrative beyond auto-generated tables?
         →  flag candidates: design tokens, complex composition rules, migration guides

PLAN     →  decide Autodocs vs MDX per component (see trade-off table below)
         →  outline MDX page structure: Intro → Anatomy → Variants → Usage → Accessibility → API

AUTHOR   →  scaffold .mdx with <Meta of={Component} /> binding to CSF file
         →  embed stories via <Canvas of={Component.Variant} />; never re-define stories in MDX

VERIFY   →  preview in Storybook → check Doc Blocks render, links navigate, ToC is correct
         →  validate prop tables match component types; no stale Story references

HANDOFF  →  hand to Quill for prose review on >500-word pages; to Muse for token doc alignment
```

## Doc Blocks Reference (Storybook 10)

| Block | Purpose | Required prop |
|-------|---------|---------------|
| `<Meta>` | Bind MDX page to a CSF file | `of={meta}` |
| `<Title />` | Auto title from meta | — |
| `<Subtitle>` | One-line tagline under title | children |
| `<Description>` | Pulls JSDoc from component or meta | `of={Component}` (optional) |
| `<Primary>` | First story as hero canvas | — |
| `<Canvas>` | Embed a single story with code toggle | `of={StoryExport}` |
| `<Story>` | Embed without canvas chrome | `of={StoryExport}` |
| `<Controls>` | Interactive args panel | `of={StoryExport}` |
| `<ArgTypes>` | Static prop table | `of={Component}` or `of={StoryExport}` |
| `<Source>` | Render code block from a story | `of={StoryExport}` |
| `<Stories>` | List all sibling stories | `includePrimary={false}` |

## Autodocs vs Hand-Authored MDX Trade-off

| Concern | Autodocs (`tags: ['autodocs']`) | Hand-Authored MDX |
|---------|--------------------------------|--------------------|
| Setup cost | Zero — single tag | Per-page authoring |
| Maintenance | Auto-syncs with CSF | Manual updates required |
| Narrative depth | Single page, fixed layout | Unlimited; multi-section |
| Multi-page docs | Not supported | Supported |
| Custom JSX (diagrams, demos) | Not supported | First-class |
| Design-system foundations | Inadequate | Recommended |
| Best for | Atoms, simple molecules | Organisms, foundations, guides |

Rule of thumb: start with Autodocs for every component. Promote to MDX only when narrative, composition rules, or cross-component guidance is required.

## Code-Pattern Table

| Pattern | Use case | Snippet |
|---------|----------|---------|
| Page binding | Anchor MDX to CSF | `import * as ButtonStories from './Button.stories';` then `<Meta of={ButtonStories} />` |
| Hero example | Lead with primary story | `<Primary />` |
| Variant gallery | Show all variants | `<Stories includePrimary={false} />` |
| Inline live demo | Embed one story with controls | `<Canvas of={ButtonStories.Loading} /> <Controls of={ButtonStories.Loading} />` |
| Token reference | Document design tokens | Embed `<ColorPalette>`, `<Typeset>`, `<IconGallery>` from `@storybook/blocks` |
| Cross-page link | Navigate within docs | `[Forms guide](?path=/docs/foundations-forms--docs)` |
| Custom JSX | Composition diagrams | Import a React component and render inline |
| Multi-page docs | Foundations / guides hierarchy | Separate `Foundations.mdx`, `Spacing.mdx`, `Color.mdx` files with shared sidebar |

## Anti-Patterns

- Re-defining stories inline in MDX with `<Story name="...">` and JSX children — Storybook 7+ deprecates this; always author CSF first and embed via `of={...}`.
- Using MDX for every component — undermines Autodocs ROI; reserve MDX for components where narrative adds genuine value.
- Skipping `<Meta of={meta} />` — without it, ArgTypes/Controls cannot resolve, and the doc page detaches from the CSF source.
- Hand-writing prop tables in Markdown — diverges from component types over time; always use `<ArgTypes>` for type-driven tables.
- Embedding raw screenshots of stories — defeats live, interactive doc purpose. Use `<Canvas>` so consumers can interact and copy code.
- Mixing CSF and MDX in the same file — Storybook 8+ disallows it; keep `.stories.tsx` pure CSF and `.mdx` pure docs.
- Long single-page docs with no headings — Storybook auto-generates a ToC from `##`/`###`; without headings, navigation collapses.
- Forgetting to register MDX in `.storybook/main.ts` `stories` glob (`'../src/**/*.mdx'`) — page silently does not appear.
- Using MDX 1/2 syntax in MDX 3 — MDX 3 is stricter (no implicit `<p>` wrapping in some contexts, JSX comments only). Migration required when upgrading Storybook 7→8/10.

## Multi-Page Docs Structure

```
src/docs/
├── Introduction.mdx          (<Meta title="Foundations/Introduction" />)
├── DesignTokens.mdx
├── Spacing.mdx
├── Color.mdx
└── Migration.mdx
src/components/
├── Button/
│   ├── Button.stories.tsx
│   └── Button.mdx            (<Meta of={ButtonStories} />)
```

## Handoff

- **To Artisan**: missing JSDoc / prop descriptions surfaced while authoring `<ArgTypes>`. Component-side fix required.
- **To Muse**: token references in MDX foundations need authoritative source — request canonical token doc, render via `<ColorPalette>`/`<Typeset>`.
- **To Frame (Figma)**: design-system MDX pages should mirror Figma library structure; flag drift between Figma component names and MDX page titles.
- **To Quill**: prose review for foundations / migration guides exceeding ~500 words; ensure voice and terminology align with project glossary.
- **To Voyager**: usage examples in MDX that imply E2E flows (multi-page tutorials) should reference Voyager's E2E suite, not duplicate it.
