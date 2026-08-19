# Interview-Format Article

## Purpose

Reshape raw Q&A material — interview transcripts, podcast episodes, AMA threads, lightning talks, customer conversations — into a polished interview-format article that preserves the interviewee's voice while removing filler and re-sequencing for narrative arc.

## Scope Boundary

- IN scope: transcript triage, question re-writing, answer trimming, voice preservation, narrative re-sequencing, pull-quote extraction, reader-facing intro and outro.
- OUT of scope: live interviewing technique (delegate to `field`), podcast production (different domain), video editing (delegate to `director`), short blurb / quote-card design (delegate to `prose` or `ink`).

## Core Concepts

### Interview Article ≠ Transcript

Raw transcripts are a tax on the reader: filler words, asides, lost threads, and chronological order. Published interviews **respect the spoken voice** but **re-organize for the page**.

| Raw Transcript | Published Interview |
|----------------|---------------------|
| Chronological | Narrative-ordered |
| All filler retained | Filler trimmed |
| Topics interleaved | Topics consolidated |
| Q1 → A1 → Q2 → A2 strict | Reordered around themes |
| ~10,000 words for 60 min | 1,500–4,000 words polished |
| Speaker filler ("um", "you know") | Removed unless characteristic |

### Three Interview Article Forms

| Form | When | Length |
|------|------|--------|
| Q&A direct | Engineer interviews, expert deep-dives — "Q:" / "A:" format with minimal narration | 1,500–3,000 words |
| Narrative-with-quotes | Profile pieces — author voice frames the interviewee's quotes | 2,000–4,000 words |
| Roundtable | 3+ participants on one topic — questions become section headers, answers attributed | 3,000–6,000 words |

### Voice Preservation Rules

The interviewee must read the published version and feel "yes, that's me, just sharper". Rules:

1. Never write words the interviewee didn't say in spirit. Paraphrasing is allowed; fabrication is not.
2. Keep characteristic syntax — sentence fragments, technical jargon, regional expressions — even when they violate "good writing".
3. Trim filler ("um", "you know", "kind of") unless the speaker uses them as a deliberate cadence.
4. Reorder sentences within an answer for clarity, but don't fuse two unrelated answers into one.
5. Send a draft to the interviewee for fact-check + voice-check before publish. Allow 3–5 line edits, not full rewrites.

### Question Re-Writing

Spoken questions are often messy. Rewrite for the page:

| Spoken | Written |
|--------|---------|
| "So, like, I wanted to ask you, um, you know, about, like, the migration, like, what was the hardest part?" | "What was the hardest part of the migration?" |
| "Cool, cool, so, before we wrap up, just one more, what would you tell someone starting out today?" | "What would you tell someone starting out today?" |

Keep the question short, specific, and free of compound clauses. A good written question fits one breath.

### Answer Trimming

A 60-minute interview often produces 8,000–12,000 words. The article needs ~2,000–3,000. Cut by:

1. Remove verbal filler globally.
2. Drop tangents that don't serve the article's through-line.
3. Compress redundant restatements ("So basically, like I said earlier …").
4. For each answer, keep the surprising / specific / actionable parts; cut the obvious.
5. Consolidate two adjacent answers if they share a topic.

The author's job is to **respect the reader's time** while **honoring the interviewee's contribution**.

### Re-Sequencing

Chronological order rarely produces the best article. Common re-orderings:

| Strategy | When |
|----------|------|
| Best-first | Lead with the most surprising or quote-worthy answer; build context after |
| Theme-clustered | Group by topic across the interview (career → tech → philosophy) |
| Tension-arc | Open with conflict / problem, build to resolution / lesson |
| Reverse-chronological | For "lessons learned" pieces, end-state first |

Never re-sequence in a way that distorts meaning. If the interviewee said "X, but only after Y", don't isolate X without Y.

### Pull-Quotes

Extract 3–5 pull-quotes (one sentence, 80–160 chars) and surface them in the article:

- Format: oversized type, separated from body, attributed.
- Choice criteria: surprising, repeatable, on-brand for the interviewee, complete on its own.
- Avoid choosing quotes that are unflattering when isolated — context matters.

### Author Intro and Outro

Every interview article needs an author frame:

| Section | Content |
|---------|---------|
| Intro (100–200 words) | Who is this person? Why are we talking to them? What did the conversation cover? Why should the reader care? |
| Setup (1–2 lines per major topic) | Brief author narration between sections |
| Outro (50–100 words) | Where to find the interviewee (links, with consent), what's coming next, optional CTA |

The intro is where the reader decides to keep reading. Treat it as seriously as a hook (see `hook-design.md`).

### Consent and Attribution

| Item | Default |
|------|---------|
| Real name | Confirm explicitly; pseudonym only on request |
| Affiliation / company | Confirm; some interviewees can name employer, others cannot |
| Photo | Always opt-in, with credit |
| Contact links | Twitter / X / personal site / GitHub — opt-in per link |
| Off-the-record | Mark clearly during interview; never include even in paraphrased form |
| Sensitive content | Pre-publish review; allow withdrawal of any specific quote |

Get written consent for: real-name use, photo use, sensitive opinion attribution, employer mention. Tone: respectful and clear.

### Footnotes for Technical Claims

Interviewees often state facts that need verification. The article should:

- Include footnotes / inline links for any concrete claim (numbers, project history, public events).
- Use a "[Editor's note: …]" insertion for clarifications, never silent edits.
- Mark uncertain claims with `[citation needed]` until verified.

## Workflow

1. **Receive raw material** — transcript (Whisper / Otter / Rev), notes, recording.
2. **First-pass triage** — identify the 5–8 most interesting moments, the through-line theme, and the unusable sections.
3. **Choose form** — Q&A direct / narrative-with-quotes / roundtable.
4. **Re-sequence** — best-first / theme-clustered / tension-arc / reverse-chrono.
5. **Trim answers** — remove filler, consolidate redundancy, cut tangents.
6. **Rewrite questions** — short, specific, spoken-clutter removed.
7. **Extract pull-quotes** — 3–5 candidates.
8. **Write intro and outro** — frame the conversation for the reader.
9. **Fact-check** — verify dates, numbers, project history; add footnotes / links.
10. **Send draft for interviewee review** — allow 3–5 line edits; protect against full rewrites.
11. **Publish with consent confirmations** in place.
12. **Distribute** — pull-quotes become atomic assets (see `content-repurposing.md`).

## Output Template

```yaml
interview_article:
  interviewee:
    name: "Real name (with consent)"
    role: "current role and affiliation (with consent)"
    links:
      - { type: x, url: "...", consent: yes }
      - { type: github, url: "...", consent: yes }
      - { type: site, url: "...", consent: no }  # not included
  form: q_and_a_direct
  through_line: "Why our most reliable service had no tests, and what we learned."
  re_sequence_strategy: best_first
  raw_word_count: 11_400
  published_word_count: 2_350
  intro_words: 180
  outro_words: 70
  sections:
    - id: S1
      heading: "The day production didn't break"
      questions:
        - q: "When did you first realize the no-test approach was actually working?"
          a_excerpt: "..."
          a_word_count: 280
    - id: S2
      heading: "..."
  pull_quotes:
    - text: "Tests are a constraint we add for our own benefit, not the system's."
      length_chars: 64
      placement: between_S1_and_S2
  fact_checks:
    - claim: "We ran without unit tests for 4 years"
      status: verified
      source: internal_postmortem_link
  consent:
    real_name: yes
    employer_mention: yes
    photo: no
    pre_publish_review_completed: yes
    interviewee_edits_applied: 3
```

## Anti-Patterns

- Publishing the raw transcript verbatim — disrespects the reader's time and the interviewee's actual ideas.
- Heavy paraphrasing that loses voice — the published interview reads like the author talking, not the interviewee.
- Cutting tangents that contained the most surprising moment because they were "off-topic".
- Re-sequencing that changes meaning ("X, but only after Y" → "X").
- Publishing without pre-publish review — interviewees lose trust permanently.
- Pulling out-of-context quotes for shock value.
- Using the interviewee's identity (name, employer) without explicit consent.
- Skipping fact-checks on numerical claims because "they said it confidently".
- No author intro — the reader has no entry point to the conversation.
- Q&A format with bloated multi-clause questions — kills readability.
- "Lightly edited for clarity" footer when edits were heavy — be honest about the level of editing.

## Deliverable Contract

An interview article is complete when:

- Through-line theme is articulated.
- Form is chosen (Q&A direct / narrative-with-quotes / roundtable).
- Raw word count and published word count documented.
- Intro and outro present and within word budgets.
- Pull-quotes extracted (3–5).
- Fact-checks logged for all numerical / historical claims.
- Pre-publish review completed and edits applied.
- Consent confirmed for real name, employer, photo, and contact links.
- Atomic-asset hand-off plan (see `content-repurposing.md`) drafted.

## References

- Errol Morris, *A Wilderness of Error* — methodology for interview-driven longform.
- Claudia Dreifus, *Talk: Conversations with the World's Most Interesting Writers* — Q&A interview craft.
- John Brockman, Edge.org interviews — structural conventions for expert-Q&A.
- The Paris Review *Art of Fiction* / *Art of Non-Fiction* series — gold standard for narrative-with-quotes.
- Niemen Storyboard — annotated journalism interview articles.
- Sarah Koenig, *Serial* — sequencing interview material as narrative arc.
- AP Stylebook, *Quotations* chapter — voice preservation and consent norms.
- IRE (Investigative Reporters & Editors) — fact-checking and source-protection guidelines.
- Reuters *Handbook of Journalism* — pre-publish review and accuracy standards.
