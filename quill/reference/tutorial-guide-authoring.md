# Tutorial / How-To Guide Authoring Reference

Purpose: Produce learning-oriented documentation that lets a reader complete a real task on their machine from zero. A tutorial teaches by guided practice; a how-to guide solves a specific problem for someone who already knows the basics. Getting the Diátaxis quadrant right is the first authoring decision.

## Scope Boundary

- **Quill `tutorial`**: code-adjacent, repo-owned learning material — tutorials, how-to guides, runnable code snippets living next to the API they document.
- **Scribe (elsewhere)**: formal specifications (PRD / SRS / HLD / LLD). A tutorial is not a spec; it is practice.
- **Atlas (elsewhere)**: ADRs and architecture analysis. A tutorial may link to an ADR for *why*, but does not author it.
- **Zine (elsewhere)**: external tech-blog articles for note / Zenn / Qiita / dev.to. Zine tells a story; `tutorial` teaches a task.
- **Prose (elsewhere)**: in-product microcopy and UX writing. Tutorials target developers; microcopy targets end users.

If the reader needs to learn the product by doing → tutorial. If they already know it and need to solve one problem → how-to. If they need the list of every option → reference (stays in JSDoc / API docs). If they need conceptual background → explanation (often the job of the README or an Atlas ADR).

## Diátaxis Quadrant Selection

| Quadrant | Purpose | Reader state | Correct voice |
|----------|---------|--------------|---------------|
| Tutorial | Learn by guided practice | New to the tool, no goal of their own yet | "Now we add…" — teacher leads |
| How-to Guide | Accomplish a specific goal | Has a goal, knows the basics | "To do X, run…" — problem/solution |
| Reference | Look up exact info | Knows what they need, wants canonical definition | Neutral, dense, complete |
| Explanation | Understand concepts / design | Curious about why | Discursive, context-rich |

Before writing, pick one quadrant. A document trying to be two quadrants at once fails both. If a tutorial keeps sprouting reference tables, split the reference out and link.

## Progressive Disclosure

A learning doc reveals complexity only when the reader is ready for it. Three layers:

1. **Minimum viable path**: the shortest sequence of commands / code that produces a visible result. No error handling, no configuration options, no alternatives.
2. **First useful variation**: the one branch most readers take next. Introduced only after Layer 1 works.
3. **Escape hatches**: links to reference / explanation for readers who need more. Never inline.

Anti-pattern: opening a tutorial with an architecture diagram. The reader has not yet earned the context to understand it.

## Tutorial Workflow

```
FRAME     →  declare audience (Node dev? Python dev? beginner? senior?)
          →  declare outcome ("by the end, you will have…")
          →  state prerequisites (OS, versions, accounts, prior knowledge)
          →  state non-outcomes ("this tutorial does NOT cover production auth")

WRITE     →  Layer 1 happy path end-to-end
          →  every code block is self-contained and copy-pasteable
          →  every command has expected output shown underneath
          →  every step ends in a checkpoint the reader can verify

VERIFY    →  do the tutorial yourself on a clean machine or container
          →  fix every "it works on my box" assumption (paths, env, versions)
          →  time it — a 45-minute tutorial marketed as "15 minutes" loses trust

HANDOFF   →  link to how-to guides for variations
          →  link to reference for exhaustive options
          →  link to ADR / explanation for "why this way"
```

## Prerequisite Stating

State prerequisites in a banner the reader cannot skip. Split into required vs recommended so beginners do not bounce.

```markdown
## Before you start

**Required**
- Node.js 22.x (LTS) — `node --version` to check
- A GitHub account
- 15 minutes

**Recommended**
- Familiarity with `git` basics
- A code editor (VS Code, WebStorm, Neovim — any)

**Not needed**
- Docker, AWS, or a production server — we run everything locally
```

Telling the reader what is *not* needed is as valuable as telling them what is — it defuses anxiety for beginners.

## Executable Code-Snippet Design

Every tutorial snippet must pass four tests:

1. **Copy-pasteable**: no ellipses, no `// ...`, no "imagine the rest of the file". The reader pastes and it runs.
2. **Context-anchored**: either the snippet is the entire file (with filename in the heading) or shows unambiguous insertion point.
3. **Deterministic**: no `Math.random()`, no `new Date()` without pinning, no network calls that can flake. Seed or mock.
4. **Expected output shown**: every runnable snippet is immediately followed by what the reader should see.

```markdown
### Step 3. Run the script

```bash
node hello.js
```

You should see:

```
Hello, Diátaxis!
Records processed: 3
```

If you see `MODULE_NOT_FOUND`, re-check Step 1 — you probably skipped `npm install`.
```

The "if you see X, check Y" line is cheap insurance against the silent bounce.

## Validation Checkpoint Pattern

Long tutorials lose readers quietly. Checkpoint every 3–5 steps with a verification the reader performs. A good checkpoint is:

- **Observable**: "you see `✓ 12 passed`", not "it should work now".
- **Cheap**: single command or URL open, not a multi-step procedure.
- **Recoverable**: linked to a troubleshooting block for the two most common failures.

```markdown
### ✅ Checkpoint

Run `npm test` — you should see `2 passing`.

<details>
<summary>Didn't work?</summary>

- `Cannot find module './lib'` → make sure you saved `lib.js` in Step 2.
- `SyntaxError: Unexpected token` → check that your Node version is 22.x (`node --version`).
</details>
```

## Screenshot vs Text Trade-offs

| Use screenshot when | Use text when |
|---------------------|---------------|
| GUI state cannot be expressed in text (dashboards, IDE UI) | CLI output, code, config — text is searchable and translatable |
| Visual layout is the lesson (drag targets, menu paths) | Command sequence or file content |
| A single annotated image replaces 10 lines of prose | The reader copy-pastes the output |

Rules for screenshots:

- Annotate with numbered call-outs, not free-text scribbles.
- Pin the tool version in the caption ("VS Code 1.96") — screenshots rot faster than text.
- Crop tight — full-window screenshots waste reader bandwidth and leak irrelevant UI.
- Keep the source file (Figma, Excalidraw) in `docs/_screenshots-src/` so a rebuild is cheap.

Never use a screenshot for terminal output a reader must copy.

## Anti-Patterns

- ❌ Mixing Diátaxis quadrants in one document — tutorials that sprout reference tables, how-tos that become explanations.
- ❌ Starting with "Introduction" and three pages of concepts before the first command.
- ❌ `// ... (rest of file omitted)` in a tutorial snippet — the reader cannot run it.
- ❌ No expected output after a runnable command — the reader does not know if it worked.
- ❌ Skipping prerequisites ("you probably have Node installed") — the beginner you lose is the reader you most needed.
- ❌ Screenshots of terminal output — unsearchable, untranslatable, and they rot.
- ❌ Long tutorials with no checkpoints — quiet bounce rate, no feedback signal.
- ❌ Claiming "15 minutes" when you have not timed it on a clean machine.
- ❌ Covering production concerns (auth, scaling, deploy) in a "getting started" tutorial — split into a separate how-to.

## Handoff / Next Steps

**From Quill (`tutorial`) → Quill (`readme`):**
- Link the new tutorial from the README "Learn" section; keep the README short and route to the tutorial.

**From Quill (`tutorial`) → Reel / Director:**
- If the tutorial would benefit from a terminal GIF or video walkthrough, hand off to Reel (CLI demo) or Director (feature demo) with the exact command sequence and the timing budget.

**From Quill (`tutorial`) → Prose:**
- If the tutorial surfaces in-product UI text that is confusing new users, hand off to Prose for microcopy revision — do not patch user-facing strings inside the tutorial.

**From Quill (`tutorial`) → Gear:**
- Wire the tutorial's runnable snippets into CI via "Docs as Tests" (Doc Detective or similar) so the tutorial cannot silently rot. A tutorial that last worked on v2.1 and still claims to support v4 is the highest-signal form of documentation rot.

**From Quill (`tutorial`) → Lore:**
- Once the tutorial has been validated by real users, record what worked (checkpoint placement, prerequisite framing) as a reusable pattern for future tutorials.
