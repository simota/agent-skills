# Feature Parity Matrix

The parity matrix is the central decision document of the blueprint. Every web feature gets a verdict: `Full | Adapted | Deferred | Dropped`. No silent omissions.

> **2026-05 grounding for verdicts:** iOS builds with Xcode 26 + iOS 26 SDK (mandatory since 2026-04-28); Liquid Glass applies by default to native UI; Android Material 3 Expressive rolled out via `material3:1.4.0` stable (2025-09) + `1.5.0-alpha` ongoing; Compose BOM 2026.05.00. Verdicts that depend on AI features must consider App Store 5.1.2(i), Google Play AI Content Policy, **and EU AI Act Article 50** (transparency labeling applicable from 2026-08-02).

---

## Verdict Definitions

| Verdict | Meaning | When to use |
|---------|---------|-------------|
| `Full` | Behaves identically on iOS, Android, and Web | Feature is platform-agnostic and survives translation cleanly |
| `Adapted` | Same user value, redesigned to fit platform conventions | Web pattern is non-native; adaptation preserves intent |
| `Deferred` | Skipped in MVP / Phase 1, planned for later phase | Feature is valuable but high cost or low MVP impact |
| `Dropped` | Will not exist on native | Web-only capability, regulatory mismatch, or product decision |

> **Rule:** No "TBD". Every row gets a verdict. If you cannot decide, raise it as a blocking question.

---

## Matrix Template

| # | Web feature | User value | Platform feasibility (iOS / Android) | iOS impl summary | Android impl summary | Verdict | Phase | Owner agent | Notes / risks |
|---|-------------|------------|--------------------------------------|------------------|----------------------|---------|-------|-------------|---------------|
| 1 | Home feed | Browse content | High / High | `HomeView` + `HomeViewModel`, paged | `HomeScreen` + `HomeViewModel`, Paging 3 | Full | P1 (MVP) | Native | — |
| 2 | Search with autocomplete | Find content | High / High | `SearchView`, debounced `Task` | `SearchScreen`, debounced Flow | Full | P1 | Native | — |
| 3 | Right-click context menu | Quick actions | None / None | Long-press → context menu | Long-press → dropdown menu | Adapted | P1 | Native | UX divergence; document in UX adaptation |
| 4 | Print to PDF | Save / share | Low / Low | Share sheet → save to Files (PDF generation server-side) | Share sheet → save to Downloads | Adapted | P2 | Native + Gateway | Generate PDF server-side, not client |
| 5 | Multi-window editing | Power users | Medium (iPad) / Medium (foldables) | iPad multi-scene support | Foldable / multi-window flag | Deferred | P3 | Native | Justifies Phase 3, not MVP |
| 6 | Browser extension companion | Power users | None / None | — | — | Dropped | — | — | Out of scope; document in risks |
| 7 | Push notifications (transactional) | Re-engagement | High / High | APNs + UNUserNotificationCenter | FCM + NotificationManager | Full | P1 | Native + Gateway | Server payload schema needs design |
| 8 | Email magic link login | Auth | Medium / Medium | Universal Link → auth coordinator | App Link → auth coordinator | Adapted | P1 | Native + Gateway | Token-in-link expires fast; design carefully |
| 9 | OAuth login (Google) | Auth | High / High | Sign in with Apple OR ASWebAuthenticationSession | Credential Manager + AppAuth | Adapted | P1 | Native | iOS must offer Sign in with Apple if any third-party OAuth is offered (App Store rule) |
| 10 | In-app purchase / subscription | Revenue | High (StoreKit 2) / High (Play Billing) | StoreKit 2 + server receipt validation | Play Billing Library + server validation | Adapted | P1-P2 | Native + Gateway | If web-paid users open mobile app, must honor subscription per platform rules |
| 11 | Cookie-based session | Auth | None (insecure) / None (insecure) | Replace with token in Keychain | Replace with token in EncryptedSharedPreferences | Adapted | P1 | Native + Gateway | **Never** port cookies to mobile; redesign |
| 12 | Drag-and-drop file upload | Convenience | Low / Low | Document picker | Document picker (SAF) | Adapted | P1 | Native | No DnD UX on phone; tablets get more |
| 13 | Cross-tab sync | Multi-tab UX | None / None | — | — | Dropped | — | — | Mobile is single-window; not applicable |
| 14 | URL as full state handle | Sharing | Medium / Medium | Universal Links + state-encoder | App Links + state-encoder | Adapted | P2 | Native + Gateway | Re-encode state for shareable links |
| 15 | Service-worker offline mode | Offline | Adapted (T1+) / Adapted (T1+) | URLCache + Core Data tier | OkHttp cache + Room tier | Adapted | P1 | Native + Schema | Offline tier per data domain |
| 16 | WebRTC video call | Communication | Medium (CallKit) / Medium (ConnectionService) | WebRTC iOS SDK + CallKit | WebRTC Android SDK + ConnectionService | Adapted | P3 | Native | Deferred unless core feature |
| 17 | Browser geolocation | Location | High (CoreLocation) / High (FusedLocationProvider) | CoreLocation, foreground default | FusedLocation, foreground default | Adapted | P1 | Native | Permission UX matters; pre-prompt rationale |
| 18 | Web Share API | Share | High / High | Activity controller (UIActivityViewController) | ShareSheet (Intent.ACTION_SEND) | Full | P1 | Native | — |
| 19 | Camera (getUserMedia) | Capture | High / High | AVCaptureSession or PhotosUI | CameraX | Adapted | P2 | Native | If photo-only, use system pickers |
| 20 | Print | Output | Low / Low | UIPrintInteractionController | PrintHelper | Adapted | P3 | Native | Niche on mobile |

---

## Scoring Rubric

For each web feature, evaluate three dimensions:

### 1. Platform feasibility (1-5 per platform)

| Score | Meaning |
|-------|---------|
| 5 | Direct native equivalent (e.g., share sheet, push notifications) |
| 4 | Native equivalent with minor adaptation (e.g., context menu via long-press) |
| 3 | Native pattern exists, requires re-design (e.g., multi-tab → multi-window iPad/foldable) |
| 2 | Approximate via workaround (e.g., print → server PDF + share) |
| 1 | No native counterpart; would have to be invented |

### 2. User value (1-5)

| Score | Meaning |
|-------|---------|
| 5 | Core value prop |
| 4 | Frequently used |
| 3 | Useful, not core |
| 2 | Edge case / power user |
| 1 | Vestigial |

### 3. Cost (1-5)

| Score | Meaning |
|-------|---------|
| 1 | < 1 person-day |
| 2 | 1-3 person-days |
| 3 | 1-2 weeks |
| 4 | 1 month |
| 5 | > 1 month or external dependency |

### Verdict guide

| Feasibility (min iOS/Android) | User value | Cost | Verdict |
|------------------------------|------------|------|---------|
| 5-4 | 5-3 | any | `Full` (5) or `Adapted` (4) |
| 3 | 5-3 | 1-3 | `Adapted` |
| 3 | 5-4 | 4-5 | `Deferred` (later phase) |
| 2 | 5-4 | any | `Adapted` (re-design) |
| 2 | 3-2 | any | `Deferred` |
| 1 | any | any | `Dropped` (or `Adapted` if invention is justified) |
| any | 1 | any | `Dropped` |

---

## Phase Allocation

| Phase | Scope | Verdict mix |
|-------|-------|-------------|
| `P1` (MVP) | Auth, core flow, primary value-prop screens, push, deep links, offline T1 | Mostly `Full` + `Adapted` |
| `P2` (Parity) | Secondary flows, advanced search, settings, shared content | Remaining `Full` + `Adapted` |
| `P3` (Enhancement) | Power-user features, multi-window, complex media, niche utilities | `Deferred` items |
| `—` | `Dropped` items | None |

---

## Anti-Patterns

| Anti-pattern | Why it's bad | Fix |
|--------------|--------------|-----|
| Marking everything `Full` | Hides UX divergence; sets up implementation surprise | Be honest. Most features are `Adapted` |
| Skipping `Dropped` rows | Stakeholders later say "but we had this on web" | List every dropped feature explicitly |
| `Adapted` without spec | Implementer has to redesign, often poorly | Adapted rows must include a one-line redesign description |
| 80% in P1 | MVP becomes the whole product | Cap P1 at ~40-50% of features; the rest distributes across P2/P3 |
| Ignoring platform rules | App Store / Play Store reject | Flag IAP, age rating, restricted content, required features (Sign in with Apple) at matrix time |

---

## Output

The matrix lives as a Markdown table in the blueprint. For large apps (>50 features) split by feature area (`Auth`, `Catalog`, `Cart`, `Account`, `Notifications`, `Settings`).

Summary line for the blueprint and `_STEP_COMPLETE`:

```
parity_summary: "Full=N Adapted=M Deferred=K Dropped=L (total=N+M+K+L)"
```

If `Dropped + Deferred > 30%`, flag in **risk matrix** and surface as a question — the user may want to reconsider scope.
