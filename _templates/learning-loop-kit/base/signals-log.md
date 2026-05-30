<!-- Rename this file to {{SIGNAL_LOG}} when rendering the kit. -->
# {{SIGNAL_NOUN}} Log (append-only)

The audit trail of every {{SIGNAL_NOUN}} and what became of it. **Never edit history; only append and update `status`/`promoted-to`.** Each entry follows `_templates/signal-entry.md`.

> Status flow: `new` → `analyzed` → (`promoted` | `rejected`). A `promoted` entry links to the {{RULE_NOUN}} slug it produced.
> ID format: `{{SIGNAL_PREFIX}}-YYYYMMDD-<slug>` (date + mnemonic — collision-free).
> Promotion threshold: {{PROMOTION_THRESHOLD}}.
> Archive: move resolved prior-year entries to a `<this-file-basename>-<YEAR>.md` sibling when this file grows large.

---

<!-- New {{SIGNAL_NOUN_PLURAL}} are appended below by CAPTURE with status: new. -->
