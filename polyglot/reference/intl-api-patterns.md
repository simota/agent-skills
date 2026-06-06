# Intl API Patterns

Native JavaScript `Intl` API patterns for locale-aware formatting. These work in all modern browsers and Node.js without any library.

> **2026 `Intl` baseline.** The platform now ships these as Baseline Widely Available: `Intl.Segmenter` (grapheme / word / sentence segmentation — replaces `lodash.words` / manual regex), `Intl.DurationFormat`, `Intl.DisplayNames` (locale names, language names, region names, scripts, currencies), and the full set of `Intl.PluralRules` / `Intl.NumberFormat` updates from **CLDR 47** (Oct 2025). Browsers and Node 22+ bundle a current CLDR, but long-lived Docker containers may ship with an older ICU — refresh the base image on the same cadence as `tzdata`. See `polyglot/reference/library-setup.md` for runtime-pinning guidance.

---

## Date Formatting (Intl.DateTimeFormat)

```typescript
const date = new Date('2024-01-15T10:30:00');

// Short date
new Intl.DateTimeFormat('ja-JP').format(date);
// → "2024/1/15"

new Intl.DateTimeFormat('en-US').format(date);
// → "1/15/2024"

// Long date with options
new Intl.DateTimeFormat('ja-JP', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
  weekday: 'long',
}).format(date);
// → "2024年1月15日月曜日"

// Time
new Intl.DateTimeFormat('ja-JP', {
  hour: '2-digit',
  minute: '2-digit',
  hour12: false,
}).format(date);
// → "10:30"

// Date and time (dateStyle/timeStyle shorthand)
new Intl.DateTimeFormat('ja-JP', {
  dateStyle: 'full',
  timeStyle: 'short',
}).format(date);
// → "2024年1月15日月曜日 10:30"

// Reusable formatter (better performance — create once, use many)
const dateFormatter = new Intl.DateTimeFormat('ja-JP', {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
});
dateFormatter.format(date); // Use repeatedly
```

---

## Number Formatting (Intl.NumberFormat)

```typescript
const num = 1234567.89;

// Basic number
new Intl.NumberFormat('ja-JP').format(num);
// → "1,234,567.89"

new Intl.NumberFormat('de-DE').format(num);
// → "1.234.567,89"

// Currency
new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY',
}).format(num);
// → "￥1,234,568"

new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
}).format(num);
// → "$1,234,567.89"

// Compact notation
new Intl.NumberFormat('en-US', {
  notation: 'compact',
  compactDisplay: 'short',
}).format(num);
// → "1.2M"

new Intl.NumberFormat('ja-JP', {
  notation: 'compact',
  compactDisplay: 'short',
}).format(num);
// → "123万"

// Percent
new Intl.NumberFormat('ja-JP', {
  style: 'percent',
  minimumFractionDigits: 1,
}).format(0.1234);
// → "12.3%"

// Units
new Intl.NumberFormat('ja-JP', {
  style: 'unit',
  unit: 'kilometer',
  unitDisplay: 'short',
}).format(100);
// → "100 km"
```

---

## Relative Time (Intl.RelativeTimeFormat)

```typescript
const rtf = new Intl.RelativeTimeFormat('ja-JP', {
  numeric: 'auto', // "yesterday" vs "1 day ago"
});

rtf.format(-1, 'day');     // → "昨日"
rtf.format(-2, 'day');     // → "2日前"
rtf.format(1, 'day');      // → "明日"
rtf.format(-1, 'hour');    // → "1時間前"
rtf.format(-30, 'minute'); // → "30分前"
rtf.format(-1, 'month');   // → "先月"
rtf.format(-1, 'year');    // → "去年"

// Always numeric
const rtfNumeric = new Intl.RelativeTimeFormat('ja-JP', {
  numeric: 'always',
});
rtfNumeric.format(-1, 'day'); // → "1日前"
```

### Helper: Auto-Select Unit

```typescript
function getRelativeTime(date: Date, locale: string = 'ja-JP'): string {
  const now = new Date();
  const diffMs = date.getTime() - now.getTime();
  const diffSecs = Math.round(diffMs / 1000);
  const diffMins = Math.round(diffSecs / 60);
  const diffHours = Math.round(diffMins / 60);
  const diffDays = Math.round(diffHours / 24);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });

  if (Math.abs(diffSecs) < 60) return rtf.format(diffSecs, 'second');
  if (Math.abs(diffMins) < 60) return rtf.format(diffMins, 'minute');
  if (Math.abs(diffHours) < 24) return rtf.format(diffHours, 'hour');
  if (Math.abs(diffDays) < 30) return rtf.format(diffDays, 'day');
  if (Math.abs(diffDays) < 365) return rtf.format(Math.round(diffDays / 30), 'month');
  return rtf.format(Math.round(diffDays / 365), 'year');
}
```

---

## List Formatting (Intl.ListFormat)

```typescript
const items = ['Apple', 'Banana', 'Cherry'];

// Conjunction (and)
new Intl.ListFormat('en-US', { type: 'conjunction' }).format(items);
// → "Apple, Banana, and Cherry"

new Intl.ListFormat('ja-JP', { type: 'conjunction' }).format(items);
// → "Apple、Banana、Cherry"

// Disjunction (or)
new Intl.ListFormat('en-US', { type: 'disjunction' }).format(items);
// → "Apple, Banana, or Cherry"

// Unit (no conjunction)
new Intl.ListFormat('en-US', { type: 'unit', style: 'narrow' }).format(items);
// → "Apple Banana Cherry"
```

---

## Plural Rules (Intl.PluralRules)

```typescript
// Determine plural category
const pr = new Intl.PluralRules('en-US');
pr.select(0);  // → "other"
pr.select(1);  // → "one"
pr.select(2);  // → "other"

const prJa = new Intl.PluralRules('ja-JP');
prJa.select(1);  // → "other" (Japanese has no singular/plural distinction)

// Ordinal (1st, 2nd, 3rd...)
const prOrdinal = new Intl.PluralRules('en-US', { type: 'ordinal' });
prOrdinal.select(1);  // → "one"   (1st)
prOrdinal.select(2);  // → "two"   (2nd)
prOrdinal.select(3);  // → "few"   (3rd)
prOrdinal.select(4);  // → "other" (4th)

// Helper for ordinal suffix
function getOrdinalSuffix(n: number, locale: string = 'en-US'): string {
  const pr = new Intl.PluralRules(locale, { type: 'ordinal' });
  const suffixes: Record<string, string> = {
    one: 'st', two: 'nd', few: 'rd', other: 'th',
  };
  return `${n}${suffixes[pr.select(n)]}`;
}
```

---

## Display Names (Intl.DisplayNames)

```typescript
// Language names
const langNames = new Intl.DisplayNames('ja-JP', { type: 'language' });
langNames.of('en');  // → "英語"
langNames.of('ja');  // → "日本語"
langNames.of('zh');  // → "中国語"

// Region names
const regionNames = new Intl.DisplayNames('ja-JP', { type: 'region' });
regionNames.of('US');  // → "アメリカ合衆国"
regionNames.of('JP');  // → "日本"

// Currency names
const currencyNames = new Intl.DisplayNames('ja-JP', { type: 'currency' });
currencyNames.of('USD');  // → "米ドル"
currencyNames.of('JPY');  // → "日本円"
```

---

## Performance Tips

1. **Reuse formatters** — `new Intl.*Format()` is expensive; create once, call `.format()` many times
2. **Cache by locale** — Store formatters in a Map keyed by locale string
3. **Avoid in render loops** — Create formatters outside of React render or use `useMemo`

```typescript
// Good: cached formatter
const formatterCache = new Map<string, Intl.DateTimeFormat>();

function getDateFormatter(locale: string): Intl.DateTimeFormat {
  if (!formatterCache.has(locale)) {
    formatterCache.set(locale, new Intl.DateTimeFormat(locale, {
      year: 'numeric', month: 'short', day: 'numeric',
    }));
  }
  return formatterCache.get(locale)!;
}
```

## Duration Formatting (Intl.DurationFormat)

Intl.DurationFormat became Baseline Newly Available in March 2025 (Chrome 129+, Firefox 136+).

### Basic Usage

```typescript
const duration = { hours: 1, minutes: 46, seconds: 40 };

// Long style
new Intl.DurationFormat('ja-JP', { style: 'long' }).format(duration);
// → "1時間46分40秒"

new Intl.DurationFormat('en-US', { style: 'long' }).format(duration);
// → "1 hour, 46 minutes, and 40 seconds"

// Digital style (timer display)
new Intl.DurationFormat('en-US', { style: 'digital' }).format(duration);
// → "1:46:40"

// Short style
new Intl.DurationFormat('ja-JP', { style: 'short' }).format(duration);
// → "1 時間 46 分 40 秒"
```

### Helper with Fallback

```typescript
function formatDuration(
  duration: Intl.DurationFormatInput,
  locale: string,
  style: 'long' | 'short' | 'narrow' | 'digital' = 'short'
): string {
  if ('DurationFormat' in Intl) {
    return new Intl.DurationFormat(locale, { style }).format(duration);
  }
  const { hours = 0, minutes = 0, seconds = 0 } = duration;
  return `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
```

## Text Segmentation (Intl.Segmenter)

Intl.Segmenter provides locale-aware text segmentation for word, sentence, and grapheme boundaries.

### Word Segmentation

```typescript
const segmenter = new Intl.Segmenter('ja-JP', { granularity: 'word' });
const text = 'こんにちは世界、今日はいい天気ですね。';

const words = [...segmenter.segment(text)]
  .filter((s) => s.isWordLike)
  .map((s) => s.segment);
// → ["こんにちは", "世界", "今日", "いい", "天気", "です", "ね"]
```

### Grapheme-Safe Truncation

```typescript
function truncateByGrapheme(text: string, maxLength: number, locale: string): string {
  const segmenter = new Intl.Segmenter(locale, { granularity: 'grapheme' });
  const graphemes = [...segmenter.segment(text)];
  if (graphemes.length <= maxLength) return text;
  return graphemes.slice(0, maxLength).map((s) => s.segment).join('') + '…';
}

truncateByGrapheme('👨‍👩‍👧‍👦 family', 3, 'en-US');
// → "👨‍👩‍👧‍👦 f…" (correctly counts family emoji as 1 grapheme)
```
