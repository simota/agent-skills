# Locale Detection and Negotiation Reference

Purpose: Use this file to design locale resolution in Polyglot's `locale` subcommand. Picking the right locale for a user is a negotiation between signals: `Accept-Language` header, IP geolocation, user-saved preference, URL path prefix, cookie, and framework default. The resolution order and fallback chain decide what the user sees first — and whether they keep their explicit choice across visits.

## Scope Boundary

- **Polyglot `locale`**: BCP 47 parsing, `Accept-Language` negotiation, fallback chain design, user-override persistence strategy, URL-routing patterns for locale (`/en`, `?lang=en`, `Accept-Language` header).
- **Prose (elsewhere)**: source-language copy. `locale` decides which translation file serves; Prose authors the copy inside the file.
- **Artisan (elsewhere)**: framework-specific locale hooks (Next.js middleware, vue-i18n `composer.locale`, React Server Component request locale). `locale` designs the resolution algorithm; Artisan wires it into the framework.
- **Accord (elsewhere)**: spec-level L10n requirements ("support 12 locales with fallback to English"). `locale` implements against those specs.

If the ask is "how do we detect or persist the user's locale?" → `locale`. If it is "what does the English copy say?" → Prose. If it is "where does Next.js middleware go?" → Artisan.

## BCP 47 Language Tag Structure

A BCP 47 tag has up to five subtags, ordered from broad to narrow:

```
zh - Hant - HK - x-custom
│    │      │    │
│    │      │    └─ Private-use (rarely used)
│    │      └────── Region (ISO 3166-1 or UN M.49)
│    └───────────── Script (ISO 15924, 4-letter, title case)
└────────────────── Language (ISO 639-1 / 639-3, 2-3 letter, lowercase)
```

| Example | Meaning |
|---------|---------|
| `en` | Language only — matches any English region |
| `en-US` | English, United States |
| `en-GB` | English, United Kingdom |
| `zh-Hans` | Chinese, Simplified script |
| `zh-Hant-HK` | Chinese, Traditional script, Hong Kong |
| `pt-BR` / `pt-PT` | Portuguese (Brazil) / (Portugal) — significant vocabulary differences |
| `sr-Latn` / `sr-Cyrl` | Serbian (Latin) / (Cyrillic) — same language, different scripts |

Rules:
- Language is lowercase; script is title case; region is uppercase. Case is informational — matchers should be case-insensitive.
- Never invent codes (`cn` is not Chinese — `zh` is; `jp` is not Japanese — `ja` is).
- Skip subtags that add no value: emit `en-US` only if you actually differentiate en-US from en-GB; otherwise emit `en`.

## Fallback Chain

A locale request is resolved by walking from narrowest to broadest tag, then to the system default.

```
zh-Hant-HK  →  zh-Hant  →  zh  →  en  (default)
pt-BR       →  pt       →  en (default)       (never falls back to pt-PT)
fr-CA       →  fr       →  en (default)       (never to fr-FR unless explicitly mapped)
```

Rules:
- **Script boundary is hard**: `zh-Hant-HK` must NEVER fall back to `zh-Hans`. Traditional and Simplified Chinese readers cannot read each other's script fluently.
- **Region boundary is soft**: `pt-BR` → `pt` → `en` is fine when there is only one `pt` file; but if the product ships distinct `pt-BR` and `pt-PT`, never silently substitute across regions.
- **Always terminate at the app's default** (usually `en` or the project's source language). Never fall back to an empty string — render the default with a flag, not nothing.

### Implementation

```ts
function buildChain(tag: string, defaultLocale = 'en'): string[] {
  const parts = tag.split('-');
  const chain: string[] = [];
  for (let i = parts.length; i > 0; i--) {
    chain.push(parts.slice(0, i).join('-'));
  }
  if (!chain.includes(defaultLocale)) chain.push(defaultLocale);
  return chain;
}

buildChain('zh-Hant-HK'); // → ['zh-Hant-HK', 'zh-Hant', 'zh', 'en']
buildChain('pt-BR');      // → ['pt-BR', 'pt', 'en']
```

## Accept-Language Negotiation

Browsers send ordered, weighted preferences. Parse, sort by `q`, match against supported set using fallback chain, and return the app's default on no match.

```
Accept-Language: fr-CH, fr;q=0.9, en;q=0.8, de;q=0.7, *;q=0.5
```

```ts
function negotiate(header: string, supported: string[], fallback = 'en'): string {
  const requested = header.split(',').map(p => {
    const [tag, qPart] = p.trim().split(';');
    const q = qPart ? parseFloat(qPart.split('=')[1]) : 1.0;
    return { tag: tag.toLowerCase(), q };
  }).sort((a, b) => b.q - a.q);
  const supportedLower = supported.map(s => s.toLowerCase());
  for (const { tag } of requested) {
    for (const candidate of buildChain(tag, fallback)) {
      const idx = supportedLower.indexOf(candidate.toLowerCase());
      if (idx >= 0) return supported[idx];
    }
  }
  return fallback;
}
```

Use `Intl.Locale` (ES2020+) for canonicalization: `new Intl.Locale('zh-hant-hk').toString()` → `zh-Hant-HK`.

## Resolution Priority

When a user hits a page, resolve locale in this order:

| Priority | Source | Why |
|----------|--------|-----|
| 1 | URL path / query (`/fr/about`, `?lang=fr`) | Shareable links, crawlers, explicit |
| 2 | User preference (authenticated user's saved locale) | Explicit choice persists across devices |
| 3 | Cookie (e.g., `NEXT_LOCALE=fr`) | Explicit guest choice on this device |
| 4 | `Accept-Language` header | Browser signal |
| 5 | IP geolocation | Last resort, never override explicit signals |
| 6 | App default | Fallback |

Rules:
- **Explicit beats inferred**. If the user selects `ja` in a picker, never overwrite it with `en-US` from `Accept-Language` on the next request.
- **Geolocation is a hint, not a verdict**. A Spanish tourist in Tokyo wants `es`, not `ja`, just because the IP is in Japan.
- **URL locale wins over cookie**. Shared link `/de/pricing` must render German even if the cookie says `en`.

## User Override Persistence

When the user picks a locale from a picker:

1. Write it to a **cookie** (`NEXT_LOCALE`, `i18next`, etc.) with ≥ 1 year expiry, `SameSite=Lax`.
2. For authenticated users, write to the user record (`users.locale_preference`).
3. Redirect to the new locale URL (`/en/...` → `/de/...`) — do not just swap content under the same URL; it breaks shareability and crawlers.
4. On subsequent requests, the cookie/user record takes precedence over `Accept-Language`.

```ts
// on locale picker change
await fetch('/api/locale', { method: 'POST', body: JSON.stringify({ locale: 'de' }) });
document.cookie = `NEXT_LOCALE=de; Max-Age=31536000; Path=/; SameSite=Lax`;
window.location.href = `/de${window.location.pathname.replace(/^\/[a-z-]+/, '')}`;
```

## Geolocation-Inferred Defaults

For first-time anonymous visitors:

| Signal combination | Chosen locale |
|--------------------|---------------|
| No `Accept-Language` + IP in Japan | `ja` (weak inference) |
| `Accept-Language: en` + IP in Japan | `en` (explicit wins) |
| `Accept-Language: ja, en` + IP anywhere | `ja` |

Always expose a visible locale picker so the inference is correctable. Never use geolocation as the *only* signal.

## Anti-Patterns

- `Accept-Language: en-US` matched only against `en-US` (exact) — falls through to default. Always walk the chain (`en-US` → `en`).
- `zh` silently mapped to `zh-Hans` without checking `Hant-HK` / `Hant-TW` — Hong Kong/Taiwan users get Mainland-simplified script.
- `toLocaleDateString('en-US')` hardcoded in rendering — all Intl API calls must read resolved locale, not a literal.
- Overwriting user's saved locale with `Accept-Language` on every request — user selects `fr`, next visit shows `en` because browser locale is `en`.
- Using `navigator.language` as authoritative — it is a hint, same priority as `Accept-Language`.
- Caching a page keyed only by URL (not by resolved locale) — CDN serves French to an English visitor on the same path.
- Geolocating by IP without disclosing it in the privacy policy — in some jurisdictions this triggers consent requirements.
- Missing `Vary: Accept-Language` header — intermediate caches serve wrong locale.
- Locale picker that hides inactive locales — users who landed in a non-preferred locale can't escape.
- Building a fallback chain that crosses scripts (`zh-Hant` → `zh-Hans`) — hard failure for readers who cannot read the other script.

## Handoff

**To Artisan:**
- Framework integration points: Next.js `middleware.ts`, Vue Router guards, React Server Component `headers()` access.
- Client vs server locale source of truth — prefer server-resolved locale passed as prop to client components (RSC pattern).

**To Prose:**
- Locale-specific copy variations when region matters (e.g., `pt-BR` vs `pt-PT` "Fill in" vs "Fill out").

**To Accord:**
- Spec clarifications on supported locale list, fallback defaults, and whether distinct regional variants are required.

**To `translate` subcommand:**
- The supported-locale list and default-locale anchor so the TMS target-language set matches app routing.

**To Radar:**
- Locale negotiation tests: `Accept-Language` variants, cookie override, geolocation-override paths, malformed tags, empty header.

**Escape hatches / follow-ups:**
- `#TODO(agent): add Vary: Accept-Language header` when the response is cached.
- `#TODO(agent): expose locale picker on every page` when inference is the only signal.
- `#TODO(agent): canonicalize BCP 47 tags` when matching is case-sensitive and misses cases.
