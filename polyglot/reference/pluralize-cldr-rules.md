# Pluralization and CLDR Rules Reference

Purpose: Use this file to implement locale-correct plural handling in Polyglot's `pluralize` subcommand. English has 2 plural categories; Arabic has 6; Polish has 4; Japanese has 1. Hardcoded `count === 1 ? 'item' : 'items'` breaks for most of the world. Always route plural selection through CLDR categories via ICU MessageFormat (MF1) or MessageFormat 2.0 (MF2), and validate every branch per target locale.

## Scope Boundary

- **Polyglot `pluralize`**: CLDR plural-rule implementation, ICU `plural` / `selectordinal` branch authoring, per-locale category coverage, plural-branch test design.
- **Prose (elsewhere)**: UX copy authoring in the source language, including singular/plural phrasing in English copy. Prose owns the source strings; `pluralize` owns how they vary across locales.
- **Artisan (elsewhere)**: framework-specific plural hooks (`useTranslation().t` call sites, `<Plural>` JSX components, vue-i18n `$tc`). `pluralize` defines the ICU payload; Artisan wires the call site.
- **Accord (elsewhere)**: spec-level L10n requirements ("must support Arabic 6 forms"). `pluralize` implements against those specs — it does not author them.

If the ask is "write an ICU plural branch / cover all CLDR categories for locale X" → `pluralize`. If it is "choose the right English wording for 1 item vs 0 items" → Prose. If it is "wire `t()` into a React hook" → Artisan.

## CLDR Plural Categories

CLDR defines up to six cardinal categories. Every locale uses a subset.

| Category | Meaning | English example | Notes |
|----------|---------|-----------------|-------|
| `zero` | zero quantity (locale-defined) | - | Arabic, Welsh, Latvian use this |
| `one` | singular | `1 item` | En/Ja/Zh define `one` differently |
| `two` | dual | - | Arabic, Welsh, Slovenian |
| `few` | paucal / small-count | - | Polish, Russian, Czech |
| `many` | many / fractional | - | Polish, Russian; also used for fractions in some locales |
| `other` | catch-all (required) | `2 items` | Every locale MUST have `other` |

Rules:
- `other` is **mandatory** in every ICU `plural` block — it is the fallback category.
- Never assume `count === 1 → one`: in French, `0` and `1` both match `one`; in Russian, `21` matches `one`.
- Always derive categories from CLDR data (via `Intl.PluralRules` or an ICU library), not from numeric comparisons.

## Locale Category Sets

| Locale | Cardinal categories | Forms |
|--------|---------------------|-------|
| Japanese (`ja`), Chinese (`zh`), Korean (`ko`), Thai (`th`), Vietnamese (`vi`), Indonesian (`id`) | `other` | 1 form |
| English (`en`), German (`de`), Spanish (`es`), Italian (`it`), Dutch (`nl`), Swedish (`sv`) | `one`, `other` | 2 forms |
| French (`fr`), Portuguese (`pt`) | `one`, `many`, `other` | 3 forms (incl. compact-decimal `many`) |
| Polish (`pl`) | `one`, `few`, `many`, `other` | 4 forms |
| Russian (`ru`), Ukrainian (`uk`), Czech (`cs`) | `one`, `few`, `many`, `other` | 4 forms |
| Welsh (`cy`) | `zero`, `one`, `two`, `few`, `many`, `other` | 6 forms |
| Arabic (`ar`) | `zero`, `one`, `two`, `few`, `many`, `other` | 6 forms |

Verify the exact set for any target locale against CLDR (<https://cldr.unicode.org/>). Category sets do shift between CLDR releases — pin your data version.

## ICU MessageFormat Patterns

### MF1 cardinal plural

```icu
{count, plural,
  =0 {No messages}
  one {# message}
  other {# messages}
}
```

### MF1 with exact match

```icu
{count, plural,
  =0 {Your inbox is empty}
  =1 {One unread message}
  one {# unread message}
  other {# unread messages}
}
```

`=0` / `=1` are **exact match** (literal number). `one` is the CLDR category (which for en matches count === 1 only, but for ru matches 1, 21, 31, ...). Use `=0` when the zero case has a distinct UX (empty state).

### Arabic 6-form example

```icu
{count, plural,
  zero  {لا توجد رسائل}
  one   {رسالة واحدة}
  two   {رسالتان}
  few   {# رسائل}
  many  {# رسالة}
  other {# رسالة}
}
```

### SelectOrdinal (ranking, position)

```icu
{position, selectordinal,
  one   {#st place}
  two   {#nd place}
  few   {#rd place}
  other {#th place}
}
```

Ordinal category sets differ from cardinal — English ordinal has 4 categories (`one`/`two`/`few`/`other`), Japanese has 1.

### MF2 (MessageFormat 2.0, CLDR 46.1, finalized March 2025)

```mf2
.input {$count :number}
.match $count
0       {{No items}}
one     {{{$count} item}}
other   {{{$count} items}}
```

MF2 uses `.match` selectors and supports custom functions. Recommended for new projects; MF1 remains the norm for existing codebases.

## Fallback Strategy

When a locale file is missing a plural category (e.g., translator shipped only `one` + `other` for Russian):

1. **CI gate (preferred)** — fail the build if any locale is missing a required category for its CLDR rule set.
2. **Runtime fallback (last resort)** — fall back to the `other` branch of the same locale. Never fall back to a different locale's plural rule.
3. **Never silently duplicate** `one` into `few`/`many` — that is the bug that ships "1 файл" for count=3 in Russian.

```ts
// runtime guard
const required = new Intl.PluralRules(locale).resolvedOptions().pluralCategories;
const covered = Object.keys(translation.plural);
const missing = required.filter(c => !covered.includes(c));
if (missing.length) {
  console.error(`Missing plural categories for ${locale}: ${missing.join(', ')}`);
}
```

## Testing Plural Branches

Every ICU `plural` block needs one test per category, plus boundary values.

| Locale | Test counts | Why |
|--------|-------------|-----|
| `en` | 0, 1, 2 | `other`, `one`, `other` |
| `ru` | 0, 1, 2, 5, 21, 101 | `many`, `one`, `few`, `many`, `one`, `one` |
| `ar` | 0, 1, 2, 3, 11, 100 | `zero`, `one`, `two`, `few`, `many`, `other` |
| `pl` | 0, 1, 2, 5, 22 | `many`, `one`, `few`, `many`, `few` |
| `ja` | 0, 1, 2, 1000 | all `other` |

```ts
describe.each([
  ['en', 0, '0 items'], ['en', 1, '1 item'], ['en', 2, '2 items'],
  ['ru', 1, '1 файл'], ['ru', 3, '3 файла'], ['ru', 5, '5 файлов'],
  ['ar', 0, 'لا توجد رسائل'], ['ar', 2, 'رسالتان'], ['ar', 11, '11 رسالة'],
])('plural %s / %i', (locale, n, expected) => {
  it('renders correct form', () => {
    expect(t('inbox.count', { count: n }, { locale })).toBe(expected);
  });
});
```

## Anti-Patterns

- Hardcoded ternary: `count === 1 ? 'item' : 'items'` — fails for every non-English locale and is a scope-creep gateway.
- String concatenation for count: `t('count') + ' ' + count + ' ' + t('items')` — word order is wrong in Arabic, Japanese, German.
- Missing `other` branch — ICU throws at runtime; there is no "default" fallback.
- Conflating `=0` (exact) with `zero` (CLDR) — `zero` is only meaningful in Arabic/Welsh/Latvian; use `=0` for English empty states.
- Copying English plural rules into every locale file — translator will ship "1 файлов" and "5 файл" in Russian.
- Testing only `count=1` and `count=2` — misses Russian `few` (counts 2-4), Arabic `two`/`few`, Polish `many`.
- Using `Intl.PluralRules.select()` without also loading matching ICU locale data — runtime says "few" but message file only has "one"/"other".
- Running AI/MT on a plural string as flat text (without ICU metadata) — MT loses the branch structure and ships a single form for all counts.

## Handoff

**To Prose:**
- English source strings that read awkwardly in the `zero` branch ("You have 0 messages" vs "Your inbox is empty") — Prose authors the better empty-state copy.
- Ambiguous count phrasing ("last 1 day" vs "yesterday") that should be reframed before translation.

**To Artisan:**
- Call-site shape: `t('key', { count })` or `<Plural value={count} />` per framework.
- Server/client boundary for RSC: plural evaluation happens where the ICU payload is rendered; Artisan decides client vs server.

**To Radar:**
- Per-locale plural-branch test matrix (counts above), including Arabic 6-form and Russian/Polish edge cases.
- Snapshot tests for pseudo-locale with `[!! 5 ïtëms !!]` verifying no hardcoded singular/plural survived extraction.

**To TMS (via `translate` subcommand):**
- ICU plural strings flagged as "do not flatten" for MT — require human translator coverage of all CLDR categories for the target locale.

**Escape hatches / follow-ups:**
- `#TODO(agent): add CLDR category coverage gate` when a locale ships without full category support.
- `#TODO(agent): migrate plural string to MF2` when MF1 nesting becomes unreadable.
