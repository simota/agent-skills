# Risk Assessment

Quantified risks per blueprint. Every risk gets probability × impact × mitigation. Qualitative-only entries are not allowed.

---

## 2026 Update — Risks added or escalated since 2024

### Policy / Deadline risks (high impact, time-bound)

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Xcode 26 + iOS 26 SDK not adopted by **2026-04-28** (no exceptions, no extensions) | 4 | 5 | 20 | Pin Xcode 26 + iOS 26 SDK as a Phase 0 / 1 dependency; CI on Xcode 26 by Q1 2026. **Deadline is past as of 2026-05 — all new uploads must comply** |
| Privacy Manifest missing or incomplete (3rd-party SDK has no manifest) | 4 | 4 | 16 | Audit all SDKs at SURVEY; reject those without manifests; track manifest completeness as a P0 gate |
| Apple 5-tier Age Rating questionnaire not filed by **2026-01-31** | 4 | 5 | 20 | **Already enforced — App Store Connect blocks new submissions and updates for unanswered apps**. Add to Phase 0 checklist; coordinate with App Store Connect ahead of time |
| App Store 5.1.2(i) AI disclosure UI missing for third-party AI usage | 4 | 5 | 20 | Design the consent UI flow at MVP; never ship a "stub" disclosure |
| Google Play targetSdk 35 not met (since 2025-08-31) | 2 | 5 | 10 | Targeting check pre-MVP; verify all libs support API 35 |
| Google Play targetSdk 36 missed (mandatory **2026-08-31**) | 4 | 5 | 20 | Plan migration window in Phase 1-2; Wear OS / TV / Auto exempt (stay on 35). Existing apps below API 35 already invisible to new users on modern OS |
| Google Play 16KB page size missed — extension hard cutoff **2026-05-31** | 4 | 5 | 20 | Audit NDK libs at SURVEY; reject SDKs without 16KB binaries; update Android Studio NDK; verify AGP packaging pipeline preserves alignment. **Deadline is this month** |
| Google Play Photo Picker not adopted (since 2025-05-28) | 3 | 4 | 12 | Default to Photo Picker; declare media permission only when essential |
| Google Play Data Safety form inaccurate (incl. ANDROID_ID classification) | 3 | 4 | 12 | Hand off to Cloak; align with Privacy Manifest for cross-platform consistency |
| Firebase Dynamic Links retired (2025) — link infra not replaced | 3 | 3 | 9 | Run AASA / assetlinks.json natively; choose MMP (Branch / AppsFlyer / Adjust) |
| EU AI Act Article 50 transparency labeling missing (enforcement **2026-08-02**) | 3 | 4 | 12 | Label AI interactions, mark synthetic content machine-readable, disclose deepfakes; align with App Store 5.1.2(i) and Play AI Content Policy |
| Japan APPI 2026 amendment ignored for JP-targeted apps (biometric / children's / AI-training data) | 3 | 4 | 12 | Cabinet-approved 2026-04-06/07; full effect by 2028. Plan transition with Cloak — biometric rules and parental consent for under-16 are new |

### Regulatory risks (cross-cutting)

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| EU Accessibility Act (in force 2025-06-28) violation | 3 | 5 | 15 | Conform to EN 301 549 / WCAG 2.1 AA; coordinate with Cloak / Polyglot |
| EU DSA Trader Status not declared (since 2025-02-17) | 2 | 5 | 10 | Declare trader status in App Store Connect even if not selling in EU |
| DMA fee model misconfigured for EU distribution | 2 | 4 | 8 | Confirm model (CTC 5%, no CTF after 2026-01-01); coordinate with Finance |
| Children-targeted app missing Declared Age Range API or new 5-tier rating | 3 | 5 | 15 | Verify against `regulatory-checklist-2026.md` Section A.8 |
| Fintech / Crypto submission lead time underestimated | 4 | 4 | 16 | Add weeks-to-months buffer; per-country license proof; KYC/AML docs |
| Loan app violation of US 2025-11 cap (36% APR / 60-day balloon) | 2 | 5 | 10 | Legal review at design; avoid balloon-loan UX |

### Architecture / SDK risks

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Liquid Glass non-adoption causing layout breakage on iOS 26 | 3 | 3 | 9 | Test against iOS 26 simulator at MVP; or document explicit fallback |
| Material 3 Expressive components missed in component plan | 3 | 2 | 6 | Replace deprecated `BottomAppBar`/`CircularProgressIndicator` with M3-Expressive variants |
| Edge-to-edge enforcement (API 36) — bottom UI overlapping system bars | 4 | 3 | 12 | `Modifier.windowInsetsPadding()` from day 1; verify with Modifier.systemBars |
| Predictive Back default ON (API 36) — `onBackPressed()` not dispatched | 3 | 3 | 9 | Migrate to `OnBackPressedDispatcher` / Compose `BackHandler` |
| Forced resizability (sw 600dp+ at API 36) — broken phone-only layouts on tablets/foldables | 3 | 3 | 9 | Adaptive layout testing on tablet / foldable / trifold |
| `@Observable` migration risk — `@StateObject` semantics differ on `@Observable` | 2 | 3 | 6 | Use `@State` only at top of view tree; document re-creation hazards |
| Swift 6 strict concurrency — Sendable / actor isolation errors blocking build | 3 | 3 | 9 | Adopt incrementally; complete-checking on key modules; Swift 6.2 Approachable Concurrency in Xcode 26 reduces friction |
| Compose Strong Skipping — instance-equality recomposition bugs | 3 | 3 | 9 | Use `kotlinx.collections.immutable` / `@Immutable`; profile recomposition |
| Privacy Sandbox SDK Runtime — RE-enabled ad SDK adds IPC latency | 2 | 3 | 6 | Audit ad SDK RE status; latency-sensitive paths use non-RE alternatives or accept the IPC tax |
| Apple Intelligence / Gemini Nano on-device AI not feasible on baseline devices | 2 | 3 | 6 | Feature-flag and gracefully degrade |

### Security / Auth risks

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Tokens / passkey stored in UserDefaults / SharedPreferences (insecure default port) | 4 | 5 | 20 | **Hard rule**: Keychain (iOS) / EncryptedSharedPreferences or Tink (Android). Never relax this |
| Sign in with Apple omitted alongside third-party social login (high reviewer-flag rate) | 3 | 4 | 12 | Add SIWA at design time; "privacy-equivalent" custom paths trigger review delays |
| Cookie session bridged to mobile via WebView (legacy recovery) | 2 | 4 | 8 | Default to native token auth; cookie sync only as last-resort recovery |
| Refresh-token race conditions during concurrent retry | 4 | 3 | 12 | In-flight refresh lock + queue; OkHttp `Authenticator` / URLSession async wrapper |
| Cert pinning misconfigured (backup pin missing) | 2 | 4 | 8 | Pin + backup pin; rotation plan via remote config |

### Process / delivery risks

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Big Bang web shutdown attempted — no Strangler Fig | 3 | 5 | 15 | Force 5-phase Strangler Fig with reversible cuts up to step 4; see `migration-roadmap.md` |
| KMP / RN / Flutter sneaks back mid-project after pure-native commitment | 2 | 3 | 6 | `cross-platform-decision-tree.md` decision is journaled; revisit only at named triggers |
| Two-platform divergence drift across iOS / Android features | 4 | 3 | 12 | Single product owner; per-screen parity review; parity-matrix verdict tracked through phases |
| Store rejection cycle longer than expected (regulated category) | 4 | 3 | 12 | Buffer Phase 2-3 timelines; pre-flight `regulatory-checklist-2026.md` |
| Mobile rollback slower than web (release pause) | 4 | 3 | 12 | Server-driven feature flags as primary mitigation; staged rollout from day 1 |

---

---

## Scoring

| Probability | Score | Meaning |
|-------------|-------|---------|
| Very low | 1 | Edge case, unlikely |
| Low | 2 | Possible but mitigated |
| Medium | 3 | Likely to surface during development |
| High | 4 | Will surface; expect it |
| Very high | 5 | Will block delivery without action |

| Impact | Score | Meaning |
|--------|-------|---------|
| Trivial | 1 | Workaround, no schedule slip |
| Minor | 2 | Minor schedule slip |
| Moderate | 3 | Phase slip 1-2 weeks |
| Major | 4 | Phase slip 1+ month, scope cut |
| Critical | 5 | Project rework or blocked launch |

**Risk score = Probability × Impact** (1-25). Anything ≥ 12 is a red risk and must surface in the blueprint executive summary.

---

## Common Web→Native Risks

### Architecture & scope

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Web routing translates poorly to native nav | 4 | 3 | 12 | MAP phase rigor; per-screen mapping table; user testing |
| Global Redux store ported as monolith | 3 | 3 | 9 | Decompose into per-feature ViewModels; document migration in MAP |
| Web SSR/RSC features lost on mobile | 4 | 2 | 8 | Adapt to client-rendered + API; flag in parity matrix |
| Multi-tab UX has no mobile equivalent | 3 | 2 | 6 | Drop or adapt; surface in parity matrix |
| Browser-only APIs used (BroadcastChannel, WebUSB, etc.) | varies | varies | — | Per-API decision in survey; parity-matrix verdict |

### Third-party & SDKs

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Third-party SDK has no native counterpart | 3 | 4 | 12 | Replace, drop, or build wrapper; flag in survey |
| Native SDK requires higher min-OS | 3 | 3 | 9 | Choose alternative or raise baseline |
| Vendor SDK violates store policy | 2 | 5 | 10 | Switch vendor; do not ship |
| SDK adds unacceptable bundle size | 3 | 2 | 6 | Lazy-load or replace |

### Auth & security

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| localStorage-stored token ported insecurely | 4 | 5 | 20 | **Hard rule: never port tokens to UserDefaults / SharedPreferences.** Keychain / EncryptedSharedPreferences mandatory |
| Session cookie reused on mobile | 3 | 4 | 12 | Replace with token flow; coordinate with backend |
| Refresh token race conditions | 4 | 3 | 12 | In-flight refresh lock; queue concurrent requests |
| Sign in with Apple missing | 4 | 5 | 20 | Required by App Store if any third-party login is offered; add in P1 |
| PKCE not implemented for OAuth | 3 | 4 | 12 | Mandatory for native OAuth; verify in PR |
| Biometric bypass exposes secret | 2 | 5 | 10 | Use system BiometricPrompt / LocalAuthentication APIs only |
| Cert pinning misconfigured | 2 | 4 | 8 | OkHttp `CertificatePinner` / URLSession `SecTrust` with backup pin and rotation plan |

### Data, offline, sync

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Online-only mindset ports to mobile | 4 | 3 | 12 | Mandatory offline-tier decision per domain |
| T2/T3 sync underestimated | 3 | 4 | 12 | Default to T1; only escalate when justified; design conflict policy |
| API too chatty for mobile | 3 | 3 | 9 | `Gateway` redesign; combine endpoints |
| Large payload slow on mobile | 3 | 3 | 9 | Pagination, server-side resize, gzip / brotli |
| Cache invalidation diverges between platforms | 3 | 3 | 9 | Document per-feature TTL and invalidation rules |
| Local DB migration on app upgrade fails | 3 | 4 | 12 | Versioned schema migrations; tested rollback path |

### Platform compliance

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Privacy manifest (iOS 17+) missing entries | 4 | 3 | 12 | Audit at P0; align with Cloak |
| Data safety form (Play) inaccurate | 4 | 3 | 12 | Audit at P0; align with Cloak |
| ATT (App Tracking Transparency) missed | 3 | 4 | 12 | Required if tracking; surface UX |
| IAP rules violated (external payment links) | 3 | 5 | 15 | Audit before submission; coordinate with Legal |
| Age rating wrong | 3 | 3 | 9 | Set correctly at submission |
| Restricted content (UGC, gambling, health) | 2 | 5 | 10 | Per-store policy review; legal review |
| Permission abuse (background location, etc.) | 3 | 4 | 12 | Justify each permission; remove unused |

### Performance

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Cold start > 2s | 3 | 3 | 9 | Defer non-essential init; lazy DI; startup profiler |
| Memory pressure on older devices | 3 | 3 | 9 | Profile on baseline device; cap caches |
| Image-heavy lists drop frames | 3 | 3 | 9 | Use Coil/Glide / SDImage with proper sizing |
| Animation jank | 2 | 2 | 4 | Profile + reduce-motion respect |

### Process & delivery

| Risk | Prob | Impact | Score | Mitigation |
|------|------|--------|-------|------------|
| Big-bang web shutdown | 3 | 5 | 15 | Phased shutdown with reversal until step 4 |
| Two-platform divergence drift | 4 | 3 | 12 | One product owner; per-screen parity review |
| Store rejection cycle | 4 | 2 | 8 | Pre-flight checklist; first submission expects 1 cycle |
| KMP / RN sneaks back in mid-project | 2 | 3 | 6 | Pure-native scope locked at blueprint; document |
| Non-mobile team mismaps web complexity | 3 | 3 | 9 | Survey discipline + parity matrix as agreement |

---

## Risk Matrix Output Skeleton

```markdown
# Risk Matrix: <App Name>

## Red (Score ≥ 12)
| ID | Risk | Prob | Impact | Score | Mitigation | Owner |
| R1 | localStorage tokens insecure | 4 | 5 | 20 | Keychain / EncryptedSharedPreferences | Native |
| R2 | Sign in with Apple missing | 4 | 5 | 20 | Add in P1 | Native + Launch |
| …  | …                                  | … | … | …  | …                                          | …          |

## Amber (Score 6-11)
| ID | Risk | Prob | Impact | Score | Mitigation | Owner |

## Green (Score ≤ 5)
| ID | Risk | Prob | Impact | Score | Mitigation | Owner |

## Top 5 mitigations to land in Phase 0
1. Define token storage policy and ship secure-storage abstraction
2. Confirm Sign in with Apple requirement and add to design system
3. Resolve any "no-native-SDK" third-party gaps before P1 scope freeze
4. Confirm offline-tier decision per data domain
5. Audit privacy manifest / Play data-safety alignment with Cloak
```

---

## When to Escalate

- Any Red risk that the user has not seen → surface in `## NEXUS_HANDOFF` and as `Pending Confirmations`.
- Any cluster of ≥ 5 Amber risks in one area (e.g., auth) → recommend a deep-dive (chain `Sentinel` for security, `Crypt` for tokens).
- Any risk that materially changes scope → update parity matrix and roadmap.

The risk matrix is a living document — updated at every blueprint revision.
