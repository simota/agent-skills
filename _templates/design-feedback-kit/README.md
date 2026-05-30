# Design Feedback Learning Kit

A per-project mechanism that turns **UI/UX feedback** into durable **design principles**, then enforces those principles on all future design work — for both **frontend (web)** and **native apps (iOS / Android)**.

- **Source of truth:** Markdown + assets, version-controlled in the project repo (this kit, installed as `design/`).
- **Learning mode:** semi-automated — agents *propose* principles; a human *approves* before they become binding.
- **Platform model:** a platform-agnostic **core** layer plus per-platform layers (`frontend`, `ios`, `android`) that only hold deltas.

> The principles files are the contract. Mockups are evidence. The feedback log is the audit trail of *why* each principle exists.

---

## The Loop

```
   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │ CAPTURE  │ → │ ANALYZE  │ → │  REVIEW  │ → │ PROMOTE  │ → │ ENFORCE  │
   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
   feedback-log    Voice/Echo      human         principles/    every UI
   (status:new)    extract draft   approve/edit  <scope>.md     task reads
                   (status:        /reject       (status:       principles/
                    proposed)                     accepted)      first
```

| Step | What happens | Owner | Skill(s) |
|------|--------------|-------|----------|
| **1. CAPTURE** | Any UI/UX feedback (interview, review, support ticket, analytics signal, usability test) is appended to `feedback-log.md` with `status: new`. | anyone | — (manual) or `voice` for bulk import |
| **2. ANALYZE** | Cluster feedback into themes, judge emotional friction. Draft a principle **only when a theme clears the promotion threshold** (≥2 independent items, or 1 high-severity). Marks feedback `status: analyzed`, writes drafts as `status: proposed`. | agent | `voice` (sentiment/themes), `echo` (cognitive walkthrough), `palette` (usability lens) |
| **3. REVIEW** | Human reviews each proposed principle: **Accept / Edit / Reject**. Resolves conflicts with existing principles. **Mandatory human gate — never auto-approved, even under AUTORUN.** | **human** | presented via `AskUserQuestion` |
| **4. PROMOTE** | Accepted principle merged into the right layer (`core` / `frontend` / `ios` / `android`) with a slug ID, and indexed in `INDEX.md`. Source feedback marked `status: promoted`. Quantitative parts encoded as design tokens. | agent | `muse` (tokens), `vision` (direction), `lore` (curation/dedup) |
| **5. ENFORCE** | Every subsequent UI task scans `INDEX.md` + reads `principles/` *before* designing/coding. **Mandatory PR gate** checks adherence and blocks violations; gaps become new feedback (loop closes). | agent | `vision`, `artisan`, `flow`, `prose`, `echo`, `palette`, `canon` (compliance), `guardian` (PR gate) |

---

## Directory Layout (installed as `design/` in the target project)

```
design/
├── README.md                 # this file — the mechanism
├── AGENT_GUIDE.md            # how agents run each loop step + enforcement rules
├── CLAUDE.snippet.md         # paste into the project's CLAUDE.md to wire enforcement
├── feedback-log.md           # append-only intake + learning history (audit trail)
├── principles/
│   ├── INDEX.md              # by-tag / by-scope index — scan this before designing
│   ├── core.md               # platform-agnostic principles (source of truth)
│   ├── frontend.md           # web-only deltas
│   ├── ios.md                # iOS / HIG deltas
│   └── android.md            # Android / Material deltas
├── mockups/
│   └── README.md             # naming + storage convention; principle-linked
└── _templates/
    ├── principle-entry.md    # schema for one principle
    └── feedback-entry.md     # schema for one feedback item
```

---

## Install into a project

1. Copy this directory into the target repo as `design/`:
   ```bash
   cp -R _templates/design-feedback-kit <project>/design
   ```
2. Paste `design/CLAUDE.snippet.md` into the project's `CLAUDE.md` (or `AGENTS.md`) so every agent loads the principles before UI work.
3. Seed `principles/core.md` with any existing conventions (or leave the examples and let the loop populate it).
4. Run the loop whenever feedback arrives — see `AGENT_GUIDE.md`.

---

## Design rules for the kit itself

- **One principle = one file entry**, never a vague paragraph. Each carries a slug ID, a testable statement, rationale, tags, source feedback, and Do/Don't examples.
- **IDs are kebab-case slugs** (`P-CORE-control-feedback`, `FB-20260115-double-save`), not running numbers — so concurrent appends by different people never collide, and the ID reads as its own index entry.
- **Core holds only what is true on every platform.** If a rule needs `if iOS` / `if web`, it belongs in a platform layer as a delta — do not duplicate.
- **Human approval is mandatory** before a draft becomes `accepted`, in every execution mode. A single complaint is a signal, not a law — respect the promotion threshold.
- **No two accepted principles may directly conflict.** At REVIEW, a conflicting draft is resolved by supersede, scope-narrow, or reject (see `AGENT_GUIDE.md`).
- **Every principle traces to evidence.** No principle without at least one `feedback-log.md` source ID (exception: seeded baseline principles, marked `source: baseline`).
- **Deprecate, don't delete.** Superseded principles move to the file's `## Archive (deprecated)` section with `Superseded by:`, preserving the rationale trail while keeping the active list (what ENFORCE reads) lean.
- **Re-review cadence.** Quarterly, scan principles whose `Last reviewed` is >90 days old: confirm still-valid, update, or deprecate. Prevents stale rules from being enforced forever. Archive prior-year `feedback-log` entries in the same pass.
