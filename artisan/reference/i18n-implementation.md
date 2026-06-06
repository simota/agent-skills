# Internationalization Implementation Reference

Purpose: Wire i18n into a production frontend file at the component level — `t()` extraction, ICU MessageFormat for plurals/selects, `Intl` APIs for locale-aware formatting, and RTL-safe layout. This recipe is scoped to a single component or page, not to repo-wide pipelines.

## Scope Boundary

- **Artisan `i18n`**: component-level implementation. Extract strings to `t()`, use ICU for plurals/selects, wire `Intl.DateTimeFormat`/`NumberFormat`, switch physical to logical CSS properties, handle locale-aware input.
- **Polyglot (elsewhere)**: full i18n/l10n specialist work. Extraction tooling (i18next-parser, FormatJS CLI), translation catalog architecture, locale pipeline, translator workflow, pseudo-localization, translation memory, repo-wide key governance.

If the ask is "internationalize this `<PricingCard>` so it renders correctly in fr-FR and ar-SA" → `i18n`. If the ask is "set up our whole app for 12 locales with a translator handoff process" → `Polyglot`. Cross-link: Artisan's component output becomes the input Polyglot scales out.

## Workflow

```
ANALYZE  →  enumerate user-visible strings, dates, numbers, currencies, units
         →  identify plurals, gender/selects, relative time ("3 days ago")
         →  identify layout assumptions that break in RTL (padding-left, text-align: left, arrows)
         →  confirm locale source (URL segment / cookie / user pref / Accept-Language)

DESIGN   →  pick i18n library already in repo (react-intl / i18next / next-intl / vue-i18n)
         →  map each dynamic string to an ICU pattern (plural / select / number / date)
         →  decide Intl formatter instance scope (memoize per locale to avoid re-construction)
         →  decide RTL strategy: logical CSS properties + dir="rtl" on <html>

IMPLEMENT →  replace hardcoded strings with t('key', { vars })
         →  replace toLocaleDateString shorthands with Intl.DateTimeFormat(locale, opts)
         →  replace `margin-left` with `margin-inline-start`, `left:` with `inset-inline-start:`
         →  mirror directional icons (chevrons/arrows) when dir === 'rtl'

VERIFY   →  render in at least one LTR non-English locale + one RTL locale (ar or he)
         →  check pluralization in a language with >2 plural forms (ru, pl, ar)
         →  check date/number/currency formatting matches locale expectations
         →  check truncation/overflow with German (longer words) and Japanese (no spaces)
```

## Patterns

```tsx
// ICU plural + select (react-intl / FormatJS)
<FormattedMessage
  id="cart.items"
  defaultMessage="{count, plural, =0 {No items} one {# item} other {# items}}"
  values={{ count }}
/>

// Intl formatters — memoize per locale
const currency = useMemo(
  () => new Intl.NumberFormat(locale, { style: 'currency', currency: 'JPY' }),
  [locale],
);
<span>{currency.format(price)}</span>

// Relative time
const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
rtf.format(-3, 'day'); // "3 days ago" / "il y a 3 jours" / "منذ 3 أيام"

// Logical CSS properties for RTL-safe layout
.card {
  padding-inline: 1rem;        /* not padding-left/right */
  margin-inline-start: 0.5rem; /* not margin-left */
  text-align: start;           /* not left */
  border-inline-start: 2px solid; /* not border-left */
}

// Directional icon mirror
<ChevronIcon className={dir === 'rtl' ? 'scale-x-[-1]' : ''} aria-hidden />
```

## Anti-patterns

- String concatenation for sentences: `t('greeting') + ' ' + name + '!'` — breaks word order in many languages. Use `t('greeting', { name })` with a placeholder inside the message.
- `new Intl.DateTimeFormat(...)` inside render without memoization — 100–1000 formatters per render hurts INP.
- Hardcoding `toLocaleDateString()` with no locale arg — silently falls back to runtime default, producing inconsistent output per user.
- `if (count === 1) return '1 item'; else return count + ' items';` — hardcoded English plural rule. Use ICU `plural`.
- Physical CSS (`left`, `right`, `margin-left`) in layout code — doubles the work for RTL. Use logical properties.
- Embedding translator-facing instructions inside the UI string — should live in message-catalog metadata/description.
- Relying on `dir="auto"` for mixed-direction input without understanding Unicode Bidi isolation — emits the wrong glyphs for embedded numbers/URLs.

## Locale-Switching Wiring

- URL-based (`/en/...`, `/ja/...`) is the most SEO-friendly and cache-friendly; store the selection in a cookie for the next visit.
- When locale changes, re-initialize `Intl.*` formatters and update `<html lang>` + `<html dir>` on the same tick to avoid FOUC.
- Persist user-selected locale independent of browser `Accept-Language` — never silently override an explicit choice on next visit.

## Handoff

- To `Polyglot` when the component pattern needs to scale to a full extraction pipeline, catalog architecture, or translator workflow.
- To `Prose` for source-string copy review before handoff to translators (voice/tone consistency in the base locale).
- To `Radar` for snapshot tests across locales and RTL rendering.
- To `Vitrine` for per-locale stories that lock the rendering contract.
