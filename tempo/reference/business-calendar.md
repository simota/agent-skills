# Business Calendar — Holidays, Banking Days, Fiscal Years, Business Hours

Reference for business-calendar logic. Read when implementing holiday-aware scheduling, banking-day arithmetic, or business-hour gating.

---

## Japan Public Holidays (祝日)

### Source of truth

- **内閣府 (Cabinet Office)**: https://www.cao.go.jp/chosei/shukujitsu/
- CSV download: `syukujitsu.csv` (encoding: Shift_JIS historically; UTF-8 also available).
- Announced typically 1-2 years in advance; special holidays (e.g., imperial events) can be announced with shorter notice.
- **Hot-reload is mandatory** — do NOT compile-time bake holiday data into binaries; mid-year announcements (e.g., 2019 Emperor enthronement, 2020 Olympics shifts) have broken hardcoded calendars.

### Fixed-date holidays (2026 reference)

| Holiday | 和名 | Date |
|---------|------|------|
| 元日 | New Year's Day | Jan 1 |
| 建国記念の日 | National Foundation Day | Feb 11 |
| 天皇誕生日 | Emperor's Birthday | Feb 23 |
| 昭和の日 | Showa Day | Apr 29 |
| 憲法記念日 | Constitution Day | May 3 |
| みどりの日 | Greenery Day | May 4 |
| こどもの日 | Children's Day | May 5 |
| 山の日 | Mountain Day | Aug 11 |
| 文化の日 | Culture Day | Nov 3 |
| 勤労感謝の日 | Labor Thanksgiving Day | Nov 23 |

### Happy Monday system (ハッピーマンデー制度)

Since 2000-2003, four holidays moved from fixed dates to "Nth Monday of month":

| Holiday | 和名 | Rule |
|---------|------|------|
| 成人の日 | Coming of Age Day | 2nd Monday of January |
| 海の日 | Marine Day | 3rd Monday of July |
| 敬老の日 | Respect for the Aged Day | 3rd Monday of September |
| スポーツの日 | Sports Day | 2nd Monday of October |

Calculation example (2026):
- 2nd Monday of January 2026 = Jan 12 (Sun Jan 4 → Mon Jan 5 is 1st; Mon Jan 12 is 2nd).

### Equinox-based holidays

| Holiday | 和名 | Rule |
|---------|------|------|
| 春分の日 | Vernal Equinox Day | Mar 20 or 21 (announced by 国立天文台 previous Feb) |
| 秋分の日 | Autumnal Equinox Day | Sep 22 or 23 (announced by 国立天文台 previous Feb) |

Do NOT compute from ephemeris — always use the official announcement. Approximation formula (for pre-computation only): `int(20.8431 + 0.242194 * (year - 1980) - int((year - 1980) / 4))` for spring, `int(23.2488 + 0.242194 * (year - 1980) - int((year - 1980) / 4))` for autumn. Verify against 内閣府.

### 振替休日 (Substitute Holiday) Rule

**Rule (since 2007 revision):** If a 祝日 falls on a Sunday, the **next non-holiday weekday** becomes a holiday.

Examples:
- Sunday, May 3, 2026 (Constitution Day) → Monday, May 4 is already a holiday (Greenery Day) → Tuesday, May 5 is already a holiday (Children's Day) → **Wednesday, May 6 is 振替休日**.
- If Sunday falls between holidays, walk forward until a non-holiday weekday is found.

Pre-2007 rule was simpler (only the Monday), so historical calendars differ.

### 国民の休日 (Sandwich Holiday) Rule

**Rule:** A non-祝日 weekday that is **sandwiched by two 祝日s on both sides** becomes a holiday.

Classic example: May 4 (before it was made Greenery Day) was sandwiched between May 3 (Constitution Day) and May 5 (Children's Day) → 国民の休日.

Post-2007, the May 4 gap was closed by making Greenery Day May 4. Sandwich holidays now occur in rare configurations (e.g., September "Silver Week" years when 敬老の日 + 秋分の日 align).

### Library implementations

| Library | Language | Notes |
|---------|----------|-------|
| `@holiday-jp/holiday_jp` | JS/TS (npm) | Official-looking; covers 振替休日 + 国民の休日 |
| `japanese-holidays` | JS (npm) | Alternative; verify against 内閣府 data |
| `jpholiday` | Python (PyPI) | Well-maintained; Holiday class per date |
| `holiday_jp` | Ruby (gem) | Rails-friendly |
| `holidays-jp` | Go | `go-pkg-holidays` |

All should be paired with a periodic update job — libraries ship snapshots; 内閣府 updates are the truth.

### Dynamic loading pattern

```typescript
// Load holidays at startup from CSV (fetched/cached from 内閣府)
async function loadHolidays(year: number): Promise<Map<string, string>> {
  const csv = await fetchWithCache(
    `https://www.cao.go.jp/chosei/shukujitsu/syukujitsu.csv`,
    { maxAge: 24 * 60 * 60 }
  );
  return parseHolidayCSV(csv);
}

// Refresh on a monthly schedule (via Tempo-designed cron)
```

---

## Banking Days (銀行営業日)

### Definition

Days banks process transactions. Excludes:
- **土日 (Saturday, Sunday)** — since 1989, all major banks close Saturdays.
- **祝日** — all public holidays.
- **12/31, 1/2, 1/3** — 年末年始 (banking calendar closure), regulated by **銀行法施行令 第5条** (Banking Act Enforcement Order Art. 5).

Note: **1/1 is 元日 (祝日)**, already excluded. 1/2 and 1/3 are NOT 祝日 but are bank holidays.

### Full-bank-holiday dates (2026 example)

| Date | Type |
|------|------|
| Jan 1 (Thu) | 元日 |
| Jan 2 (Fri) | 年末年始 |
| Jan 3 (Sat) | 年末年始 + weekend |
| Dec 31 (Thu) | 年末年始 |

### Business-day arithmetic

Common operations:
- `isBankingDay(date)`: not weekend, not 祝日, not year-end banking holiday.
- `nextBankingDay(date)`: walk forward, skipping non-banking days.
- `addBankingDays(date, N)`: walk forward N banking days (for settlement date calculation).
- `previousBankingDay(date)`: walk backward.
- `bankingDaysBetween(from, to)`: inclusive/exclusive rules must be documented.

### T+N settlement patterns (reference)

- T+1 (FX): typically spot trades.
- T+2 (equity): JP equity market standard since 2019-07-16 (previously T+3).
- T+3 / T+5: varies by instrument.

---

## Fiscal Year (会計年度)

### Japan corporate

- **Default**: Apr 1 – Mar 31 (most public companies, government, education).
- **Also common**: Jan 1 – Dec 31 (matches calendar year, used by foreign subsidiaries, some tech firms).
- Choice is documented in articles of incorporation; hardcoding assumes Apr-Mar.

### Government / education

- Apr 1 – Mar 31 (固定).
- Fiscal year label: "令和8年度" = Apr 1, 2026 – Mar 31, 2027.

### Quarter boundaries (Apr-Mar fiscal year)

| Quarter | Dates |
|---------|-------|
| Q1 (第1四半期) | Apr 1 – Jun 30 |
| Q2 (第2四半期) | Jul 1 – Sep 30 |
| Q3 (第3四半期) | Oct 1 – Dec 31 |
| Q4 (第4四半期) | Jan 1 – Mar 31 |

### Month-end close

- **月末締め (end-of-month closing)**: many Japanese accounting workflows close on the last calendar day of the month.
- **20日締め**: some companies close on the 20th (e.g., payroll cycle).
- **15日締め月末払い**: cutoff on the 15th, payment at month-end.

Scheduling "on the last banking day of the month": walk back from the last calendar day, skipping non-banking days.

---

## Business Hours (営業時間)

### Typical JP definitions

- **一般企業**: 09:00-17:00 or 09:00-18:00 JST, Mon-Fri, excluding 祝日.
- **銀行窓口**: 09:00-15:00 JST, Mon-Fri, excluding 祝日 and 12/31, 1/2, 1/3.
- **コンビニ**: 24/7 (irrelevant for scheduling).

### Business-hours gate

```typescript
function isBusinessHour(instant: Instant): boolean {
  const zdt = instant.toZonedDateTimeISO('Asia/Tokyo');
  const dow = zdt.dayOfWeek;    // 1=Mon..7=Sun
  if (dow === 6 || dow === 7) return false;
  if (isJPHoliday(zdt.toPlainDate())) return false;
  const hour = zdt.hour;
  const min = zdt.minute;
  return (hour > 9 || (hour === 9 && min >= 0)) && (hour < 17);
}
```

### Async business-hours pattern

Business-hour-gated scheduling (e.g., "send reminder during JP business hours only"):
1. At scheduled fire time, check business-hour gate.
2. If outside: enqueue to a "deferred" queue with a target time = next business-hour start.
3. At target time, re-check (DST, holiday additions, etc.) before executing.

---

## Cross-Country Calendars

Multi-region products need per-region calendars.

### Islamic world

- **Ramadan**: lunar month; shifts ~10 days earlier each solar year. Affects business hours (shortened in many Muslim-majority countries), commerce patterns.
- **Eid al-Fitr, Eid al-Adha**: lunar; dates announced locally (moon sighting varies).
- **Friday**: weekend day in Saudi Arabia, Iran, Afghanistan, and others (though Saudi moved weekend to Fri-Sat in 2013).

### Chinese New Year (春節)

- Lunar; typically late Jan - mid Feb.
- Major business shutdown in China, Taiwan, Hong Kong, Singapore, Malaysia, Vietnam (Tết).
- **7-day official holiday** in mainland China, plus adjusted working Saturdays ("借調" — makeup workdays).

### US holidays

- Federal: New Year's, MLK Day (3rd Mon Jan), Presidents' Day (3rd Mon Feb), Memorial Day (last Mon May), Juneteenth (Jun 19), Independence Day (Jul 4), Labor Day (1st Mon Sep), Columbus Day (2nd Mon Oct), Veterans Day (Nov 11), Thanksgiving (4th Thu Nov), Christmas (Dec 25).
- **Thanksgiving + Black Friday**: commerce spike starts here; scheduling-sensitive.

### EU

- Country-specific; no pan-EU holiday set. Major ones: Christmas, New Year's, Easter (movable — computus algorithm).
- **Easter**: first Sunday after the first ecclesiastical full moon after March 21. Pre-compute via library (e.g., `dateutil.easter` in Python).

### Prayer times (observability — not scheduling but relevant for UX)

- 5 daily prayers in Islam: Fajr (pre-dawn), Dhuhr (noon), Asr (afternoon), Maghrib (sunset), Isha (night).
- Times vary by geography and date; use libraries like `adhan` (JS/Python/Swift).

### Library recommendations

| Region | Library |
|--------|---------|
| Japan | `@holiday-jp/holiday_jp`, `jpholiday` |
| US | `holidays` (Python), `@date-fns/holidays` |
| EU (country-specific) | `holidays` (Python, 50+ countries) |
| Cross-country | `workalendar` (Python, extensive) |
| Islamic / Hijri | `hijri-date` (npm), `hijri-converter` (Python) |
| Chinese lunar | `lunar-javascript` (npm), `lunardate` (Python) |

---

## iCal / ICS Feed Integration

### Pattern

Publish company-specific calendars (e.g., "Acme banking holidays 2026") as `.ics` feeds so downstream services can subscribe.

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Acme//Banking Holidays//EN
BEGIN:VEVENT
UID:2026-0101@acme.example
SUMMARY:元日
DTSTART;VALUE=DATE:20260101
DTEND;VALUE=DATE:20260102
END:VEVENT
END:VCALENDAR
```

Parse with libraries:
- JS: `ical.js`, `node-ical`.
- Python: `icalendar`, `ics`.
- Go: `github.com/arran4/golang-ical`.

Subscribe with HTTP `ETag` / `If-Modified-Since` to avoid unnecessary fetches.

---

## Hot-Reload of Calendar Data

Calendar data MUST be dynamic, not baked:

1. Store holidays in a DB table or external KV (`calendar:jp:2026` → JSON).
2. Fetch from 内閣府 CSV (or similar source per region) on a **monthly** Tempo-designed cron.
3. Cache in-process with TTL (1h-24h).
4. On fetch failure: keep serving stale cache; alert if cache age > 7 days.
5. Unit test: synthetic holiday injection to verify gate logic.

---

## Checklist: business-calendar implementation

- [ ] Holidays loaded from DYNAMIC source (CSV, API, DB), not hardcoded.
- [ ] 振替休日 and 国民の休日 rules implemented (JP only).
- [ ] Banking days exclude 12/31, 1/2, 1/3 in addition to 祝日 and weekends.
- [ ] Fiscal year boundary documented (Apr-Mar vs Jan-Dec).
- [ ] Business-hours gate accepts an IANA TZ parameter.
- [ ] Deferred-queue pattern implemented for business-hour-only tasks.
- [ ] Monthly calendar refresh scheduled (Tempo cron spec).
- [ ] Stale-cache alert wired up.
- [ ] Tests cover Happy Monday dates (vary by year).
- [ ] Tests cover equinox edge cases (20 vs 21, 22 vs 23).
- [ ] Multi-region product: per-region calendar resolution (user location / tenant config).
