<!-- Rename this file to {{SIGNAL_LOG}} when rendering the kit. -->
# {{SIGNAL_NOUN}} Log (append-only)

The audit trail of every {{SIGNAL_NOUN}} and what became of it. **Append new entries; preserve their original date, source, layer, and raw {{SIGNAL_NOUN}}.** Fill or update Analysis, Proposed {{RULE_NOUN}}, Status, Reviewed by, Decision date, Promoted to, and Reject reason as the entry progresses through the loop. Record later decision changes as appended notes so prior review history remains visible. Each entry follows `_templates/signal-entry.md`.

> Status flow: `new` → `analyzed` → (`promoted` | `rejected`). A `promoted` entry links to the {{RULE_NOUN}} slug it produced.
> IDs combine `{{SIGNAL_PREFIX}}`, the capture date as eight digits, and a mnemonic (example: `{{SIGNAL_PREFIX}}-20260115-input-validation`); check uniqueness and add a source/session suffix on collision.
> Promotion threshold: {{PROMOTION_THRESHOLD}}.
> Archive: move resolved prior-year entries to a `<this-file-basename>-<YEAR>.md` sibling when this file grows large.

---

<!-- New {{SIGNAL_NOUN_PLURAL}} are appended below by CAPTURE with status: new. -->
