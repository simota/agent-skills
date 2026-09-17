# Framework Binding and Export Checks

Load only the selected framework row. `SKILL.md` owns narrative choices, slide-count/timing defaults and output routing; use `reference/narrative-arc-design.md` for a narrative-only task and `reference/slide-visual-design.md` for visual-system decisions.

| Framework | Syntax boundary | Verify against installed version |
|---|---|---|
| Marp | Markdown with `marp: true` frontmatter and `---` slide separators; per-slide `_class` / `_paginate` directives are comments, not speaker notes. Ordinary non-directive HTML comments hold notes. | CLI/engine/theme compatibility, preview command, browser dependency for PDF/PPTX/image conversion, selected export's notes/editability behavior |
| reveal.js | HTML `<section>` slides; nested sections create vertical stacks. Notes use `<aside class="notes">`; the notes plugin must be enabled. | Local web server and plugin initialization, speaker view, export/plugin compatibility, self-contained asset paths |
| Slidev | Markdown headmatter vs per-slide frontmatter; `---` separates slides. Notes must be the comment block **at the end of the slide**. | Installed layouts/theme components, code highlighting/animation syntax, presenter and export behavior |

Do not mix Slidev layout/code-highlight syntax into Marp or reveal.js. Do not treat a generic theme-token YAML sample as a renderer configuration. Use the project's installed/locked toolchain; record unavailable features instead of adding an unverified CLI option or forcing a major-version upgrade.

## Diagrams, Preview and Export

For diagrams, use the selected renderer's supported integration; otherwise pre-render to SVG/PNG and embed the artifact. Marp does not gain a Mermaid renderer merely from a copied HTML comment. Verify the actual diagram/plugin version rather than a cached list of “new” diagram types. Canvas supplies diagram content through `reference/handoffs.md` when delegated.

Deliver the single preview command, declared dependencies and all local assets. Preview representative title/content/code/diagram slides and every required output format. Check clipping, fonts/glyphs, notes, reading order and export fidelity; a successful process exit is not proof of accessible or editable output. Test the requested accessibility conformance on the actual exported artifact, not on an assumed conversion route.

For a requested non-Markdown authoring product, deliver the narrative/content handoff and state the output boundary; do not claim an unavailable integration generated the deck. No product/price/version catalog is maintained here.

## Canonical Checks

- Marp CLI: https://github.com/marp-team/marp-cli#readme — invocation, installed-version prerequisites and export options.
- Marpit: https://marpit.marp.app/directives and https://marpit.marp.app/usage — directives versus notes.
- reveal.js: https://revealjs.com/speaker-view/ — notes plugin, local-server requirement and export visibility.
- Slidev: https://sli.dev/guide/syntax.html — headmatter, note placement and renderer-specific syntax.

Checked 2026-09-17; recheck when the installed renderer/export path changes. Offline, use installed documentation and a real preview; report unsupported/unverified features explicitly.
