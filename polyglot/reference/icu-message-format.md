# ICU Message Format & Translation Key Conventions

Patterns for ICU MessageFormat syntax and translation file organization.

## 2026 Format Landscape: ICU MF1 Stays the Default

| Format | Status (2026-05) | Recommended for |
|--------|-------------------|------------------|
| **ICU MessageFormat 1** | Stable, default | Every new project in 2026; covered by every TMS (Lokalise / Crowdin / Phrase / Locize / Tolgee) and every major library (i18next, FormatJS / react-intl, next-intl, vue-i18n, LinguiJS) |
| **MessageFormat 2** | Stable spec since 2025; refinements in CLDR 47 (Oct 2025) and CLDR 48 | Greenfield projects with MF2-aware tooling, or libraries piloting MF2 (e.g., experimental i18next adapter) — **do not migrate** an MF1 codebase to MF2 yet, the TMS / SDK ecosystem has not caught up |
| **CLDR 47** | Current shipping release; powers `Intl.PluralRules`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat` in modern runtimes | Pull in via tzdata-style OS package + JDK / browser ICU refresh |

Practical posture for 2026:

- **Default to ICU MessageFormat 1** for new code. Every TMS and every mainstream framework still consumes MF1; switching to MF2 today means manually patching the round-trip pipeline at every TMS boundary.
- **Watch MessageFormat 2** as a 12-24 month migration target. Locize and a handful of next-intl experiments support it; broad TMS support (Crowdin / Lokalise / Phrase) is still pending — Crowdin's monthly 2026 release notes contained zero MF2 mentions through the first half of 2026.
- **Refresh CLDR / ICU** on the same cadence as tzdata. CLDR 47 changes plural categories for several minority languages and rounding behaviour for several currencies; long-lived containers running on CLDR 45 or older will silently disagree with newer browsers on the same input.

---

## ICU Message Format

### Basic Plural

```json
// en.json
{
  "items_count": "{count, plural, =0 {No items} one {# item} other {# items}}"
}

// ja.json
{
  "items_count": "{count, plural, other {#個のアイテム}}"
}
```

```typescript
t('items_count', { count: 0 });  // → "No items"
t('items_count', { count: 1 });  // → "1 item"
t('items_count', { count: 5 });  // → "5 items"
```

### Select (Gender/Type)

```json
{
  "greeting": "{gender, select, male {He} female {She} other {They}} liked your post.",
  "notification_type": "{type, select, comment {commented on} like {liked} share {shared} other {interacted with}} your post"
}
```

```typescript
t('greeting', { gender: 'female' });           // → "She liked your post."
t('notification_type', { type: 'comment' });    // → "commented on your post"
```

### SelectOrdinal

```json
{
  "ranking": "You came in {place, selectordinal, one {#st} two {#nd} few {#rd} other {#th}} place!"
}
```

```typescript
t('ranking', { place: 1 });  // → "You came in 1st place!"
t('ranking', { place: 3 });  // → "You came in 3rd place!"
```

### Nested Messages

```json
{
  "notification": "{count, plural, =0 {No new notifications} one {{name} sent you a message} other {{name} and # others sent you messages}}"
}
```

### Date and Number in Messages

```json
{
  "last_login": "Last login: {date, date, medium}",
  "account_balance": "Your balance is {amount, number, currency}"
}
```

### Complex Example

```json
{
  "order_summary": "{itemCount, plural, =0 {Your cart is empty.} one {You have # item ({price, number, currency}) ready for checkout.} other {You have # items (total: {price, number, currency}) ready for checkout.}}"
}
```

---

## Translation Key Naming Conventions

### Flat vs Nested Structure

```json
// BAD: Flat (hard to maintain)
{
  "homeHeroTitle": "Welcome",
  "homeHeroDescription": "Description",
  "authLoginTitle": "Login"
}

// GOOD: Nested (organized by feature/page)
{
  "home": {
    "hero": {
      "title": "Welcome",
      "description": "Description"
    }
  },
  "auth": {
    "login": {
      "title": "Login",
      "button": "Sign In"
    }
  }
}
```

### Namespace Design

```
locales/
├── en/
│   ├── common.json      # Shared across app (buttons, labels)
│   ├── auth.json         # Login, signup, password reset
│   ├── dashboard.json    # Dashboard-specific
│   ├── settings.json     # Settings page
│   ├── errors.json       # Error messages
│   └── validation.json   # Form validation messages
├── ja/
│   ├── common.json
│   ├── auth.json
│   └── ...
```

### Common Namespace Examples

**common.json** — Shared UI elements:
```json
{
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "submit": "Submit",
    "back": "Back",
    "next": "Next",
    "close": "Close"
  },
  "status": {
    "loading": "Loading...",
    "saving": "Saving...",
    "success": "Success!",
    "error": "An error occurred"
  },
  "pagination": {
    "previous": "Previous",
    "next": "Next",
    "page": "Page {{current}} of {{total}}"
  }
}
```

**errors.json** — Error messages with context:
```json
{
  "network": {
    "offline": "You appear to be offline. Please check your connection.",
    "timeout": "Request timed out. Please try again.",
    "server": "Server error. Please try again later."
  },
  "auth": {
    "invalid_credentials": "Invalid email or password.",
    "session_expired": "Your session has expired. Please log in again."
  },
  "validation": {
    "required": "This field is required.",
    "email_invalid": "Please enter a valid email address.",
    "password_weak": "Password must be at least 8 characters."
  }
}
```

### Key Naming Patterns

| Pattern | Example | Use Case |
|---------|---------|----------|
| `feature.element.action` | `auth.login.submit` | Button actions |
| `feature.element.state` | `order.status.pending` | Status text |
| `feature.message.type` | `cart.error.empty` | Error/success messages |
| `feature.label.field` | `profile.label.email` | Form labels |
| `feature.placeholder.field` | `search.placeholder.query` | Input placeholders |
| `feature.title.page` | `settings.title.page` | Page titles |

### Context-Aware Keys

```json
{
  "user_profile": {
    "page_title": "User Profile",
    "form": {
      "submit": "Update Profile"
    }
  }
}
```

### Translator Comments

```json
{
  "greeting": "Hello, {{name}}!",
  "_greeting_comment": "Appears at the top of the dashboard. 'name' is the user's first name.",

  "items_count": "{count, plural, one {# item} other {# items}}",
  "_items_count_comment": "Shopping cart item count. Keep it short for mobile.",

  "delete_confirm": "Are you sure you want to delete \"{{itemName}}\"?",
  "_delete_confirm_comment": "Confirmation dialog. itemName can be long (up to 50 chars)."
}
```

## TypeScript Type-Safe Translation Keys

### next-intl v4 (Recommended for Next.js)

```typescript
// global.d.ts
import en from './messages/en.json';

declare module 'next-intl' {
  interface AppConfig {
    Messages: typeof en;
    Locale: 'en' | 'ja' | 'zh' | 'ko';
  }
}

// Usage — type errors on invalid keys
const t = useTranslations('HomePage');
t('title');          // OK
t('nonExistent');    // TS Error
```

### i18next TypeScript Extension

```typescript
// i18next.d.ts
import 'i18next';
import type common from '../locales/en/common.json';
import type auth from '../locales/en/auth.json';

declare module 'i18next' {
  interface CustomTypeOptions {
    defaultNS: 'common';
    resources: {
      common: typeof common;
      auth: typeof auth;
    };
  }
}
```

### Dot-Notation Key Type Utility

```typescript
type DotKeys<T, Prefix extends string = ''> = T extends object
  ? {
      [K in keyof T]: K extends string
        ? T[K] extends object
          ? DotKeys<T[K], `${Prefix}${K}.`>
          : `${Prefix}${K}`
        : never;
    }[keyof T]
  : never;

import type en from '../locales/en.json';
type TranslationKey = DotKeys<typeof en>;
// → "home.hero.title" | "home.hero.description" | "auth.login.title" | ...
```

## AI Translation Workflow Integration

### GitHub Actions Auto-Translation

```yaml
# .github/workflows/i18n-translate.yml
name: Auto Translate i18n
on:
  push:
    branches: [main]
    paths:
      - 'messages/en.json'

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: i18n-actions/ai-i18n@v1
        with:
          provider: anthropic
          source-locale: en
          target-locales: ja,zh,ko
          source-file: messages/en.json
          format: json
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - uses: peter-evans/create-pull-request@v6
        with:
          title: 'i18n: auto-translate updated strings'
          body: 'LLM auto-translation. Merge after human review.'
          branch: i18n/auto-translate
```

### Best Practices

- LLM translation is effective for UI copy (buttons, error messages) at minimal cost
- Include translation context in prompts (`_comment` field helps)
- Recommended workflow: machine translate → human review → update translation memory
- Use lingo.dev CLI for CI/CD integration: `lingo push` / `lingo pull`
