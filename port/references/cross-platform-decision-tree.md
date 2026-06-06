# Cross-Platform Decision Tree (2026)

Choose the right path **once** at SURVEY. After committing, drop the alternatives. This file exists to make the choice deliberate, not to keep cross-platform options alive forever.

Port's primary remit is **pure-native iOS + Android**. KMP-shared-logic is allowed as a **hybrid** option when the survey justifies it. Compose Multiplatform / RN / Flutter are documented here for completeness; if any of them is the right answer, route to `Native` instead.

---

## 1. The Five Paths

| Path | UI | Logic | Maturity (2026-05) |
|------|----|----|------|
| **Pure-Native** | SwiftUI (Swift 6.3, Xcode 26) + Compose (Material 3 / Material 3 Expressive) | Per-platform Swift / Kotlin 2.4+ | Mature |
| **KMP shared logic + Native UI** | SwiftUI + Compose | Kotlin Multiplatform (Kotlin 2.2.20+; K2 default; Swift export under active dev) shared business logic | Mature (Stable since Nov 2023) |
| **Compose Multiplatform** | Compose for both iOS & Android | Kotlin Multiplatform | iOS Stable since 2025-05 (CMP 1.8); **CMP 1.11.0 (2026-05) — concurrent rendering on a dedicated render thread is default**; Web/Wasm still beta |
| **React Native (New Arch)** | RN | TypeScript / React 19.1 | Mature. **Legacy Architecture frozen in 0.80 (2025-06); option to disable New Arch removed in 0.82; Legacy code fully removed in 0.83 + Expo SDK 55 (2026)** |
| **Flutter (Impeller)** | Flutter | Dart 3.7+ | Mature. **Impeller default on iOS + Android (since 3.29, 2025-02); API 28- falls back to Skia from 3.29.3 / 3.32. "Great Thread Merge" enables sync FFI** |
| **Capacitor 7 / Tauri 2 (web-shell)** | WebView (Capacitor 7) / WebView+native (Tauri 2) | TS / Rust+TS | Capacitor 7 GA (2025-04, Android 15 / iOS 18, SPM-only); Tauri 2 mobile stable (2025-01) |

> Compose Multiplatform 1.8 brought iOS to Stable in 2025-05; **CMP 1.11.0 (2026-05) makes off-thread render the default**. Production users include Netflix, McDonald's, Cash App, Shopify, Forbes, Zürcher Kantonalbank. KMP adoption rose 7% (2024) → 18% (2025). Source: JetBrains release notes and KMP production surveys.

---

## 2. Decision Tree

```
[Start]
  ↓
Q1: Does the project explicitly require pure-native iOS + Android UI?
  ├─ YES → Q2
  └─ NO  → Q5

Q2: Is shared business logic (≥60% pure logic, e.g., validation, parsing,
    pricing, sync engine) a major portion of the codebase?
  ├─ YES → Q3
  └─ NO  → ★ Pure-Native (no KMP)

Q3: Does the team have Kotlin fluency on both iOS and Android sides
    (or can pair iOS engineers with KMP-aware Android engineers)?
  ├─ YES → Q4
  └─ NO  → ★ Pure-Native (defer KMP for later refactor)

Q4: Is the shared logic portable (no UIKit/SwiftUI/AppKit deps,
    no Compose deps)?
  ├─ YES → ★ Hybrid: KMP-shared-logic + Pure-Native UI
  └─ NO  → ★ Pure-Native (refactor to extract pure logic first)

Q5: Is the UI almost identical on both platforms and a single team
    will own both?
  ├─ YES → Q6
  └─ NO  → ★ Pure-Native (route back to Q2 path)

Q6: Does the team have Kotlin (and Compose) experience?
  ├─ YES → ★ Compose Multiplatform (1.8+ iOS Stable)
  └─ NO  → Q7

Q7: Does the team have strong React/TypeScript experience?
  ├─ YES → ★ React Native (New Architecture)
  └─ NO  → ★ Flutter (broad Dart expertise easier to hire than RN-specific)
```

End markers (★) are the recommended path.

If the user has explicitly asked for pure-native, **always finish at ★ Pure-Native or ★ Hybrid**. Q5+ branches are documented for reference only.

---

## 3. Scoring Matrix

Score each project on 1–5 against the table; sum the recommended path.

| Criterion | Pure-Native | KMP+Native UI | Compose MP | RN | Flutter |
|-----------|-------------|---------------|-----------|----|---------|
| Performance ceiling | ◎ 5 | ○ 4 | ○ 4 | △ 3 (improved 2025) | ○ 4 |
| OS-specific feature access (Live Activities, App Intents, Glance, Apple Intelligence, Gemini Nano) | ◎ 5 | ○ 4 | △ 3 | △ 3 | △ 3 |
| Platform-specific UX divergence | ◎ 5 | ◎ 5 | × 1 | × 1 | × 1 |
| Code sharing potential | △ 2 | ◎ 5 | ◎ 5 | ◎ 5 | ◎ 5 |
| Apple HIG / Material 3 Expressive native feel | ◎ 5 | ◎ 5 | ○ 4 | ○ 3 | △ 3 |
| Build / CI complexity | ○ 4 | △ 3 | △ 3 | ○ 4 | ○ 4 |
| Hire-ability (2026) | ◎ 5 | ○ 4 | △ 3 | ◎ 5 | ○ 4 |
| Day-1 AI on-device APIs | ◎ 5 | ○ 4 | △ 3 | △ 3 | △ 3 |
| Existing React/TS asset reuse | × 1 | × 1 | × 1 | ◎ 5 | × 1 |
| Existing Kotlin asset reuse | × 1 | ◎ 5 | ◎ 5 | × 1 | × 1 |
| Time-to-MVP for two platforms | △ 2 | ○ 4 | ◎ 5 | ◎ 5 | ◎ 5 |
| Bundle size | ◎ 5 | ○ 4 | △ 3 (+9 MB) | △ 3 | △ 3 |

Use this only for tie-breakers; the decision tree is the primary guide.

---

## 4. Pure-Native is the Right Answer When

- The product's value depends on **OS-specific surfaces**: Live Activities + Dynamic Island, App Intents + Apple Intelligence, Apple Watch / CarPlay companion, Widgets / Glance, Apple Vision Pro, Gemini Nano on-device AI.
- **Performance is critical** (60fps interactive lists, real-time canvas, gaming-adjacent).
- The team prefers **maximum platform feel** and is willing to maintain two implementations.
- The product is regulated and cross-platform abstractions add audit complexity.

## 5. Hybrid (KMP shared + Native UI) is the Right Answer When

- ≥60% of business logic is **platform-independent** (validation, sync engine, pricing, parsing, networking).
- Team has **Kotlin fluency** or willingness to onboard.
- Native UI freedom is still required (HIG / Material 3 Expressive native experiences).
- Team accepts the build-system complexity (Gradle on iOS via XCFramework / SPM bridge).

## 6. Pure-Native is the WRONG Answer When

- Startup MVP needs both platforms in **weeks**, not months.
- Web team has substantial React/TS investment and the UI is intentionally identical on both.
- Single small team (≤3 engineers) cannot sustain two codebases long-term.
- The product is a content-display app with minimal OS integration.

In these cases, recommend `Native` agent with cross-platform recipe.

---

## 7. Lessons from 2018-2025

- **Airbnb** (2018) sunset RN and returned to pure-native — initialization, async first-render, debug experience, type safety (pre-TS), and code-share illusion (web↔mobile rarely shared) drove the decision. The technical lessons are still valid in 2026 but the "type safety" complaint no longer holds (TypeScript is mature).
- **Discord** (2024-2025) chose to stay on RN and improved cold start by ~50% with Margelo's help. Hot spots (video decode, complex animation, keyboard) were dropped to native modules. Counter-example to Airbnb: **framework choice ≠ verdict**.
- **Linear** built a local-first sync engine that delivers near-native feel even in a web app. Lesson: when "feels native" is the goal, the **sync engine** matters more than the framework.
- **Notion / Figma / Excalidraw** use CRDTs (Yjs / Automerge / Loro) for collaborative editing and ship the same engine across web and mobile. Lesson: invest in **portable engines** before locking in a UI choice.

---

## 8. Decision Output Skeleton

```markdown
# Cross-Platform Path Decision: <App Name>

## Choice
Path: ★ [Pure-Native | Hybrid (KMP+Native UI) | Compose Multiplatform | React Native | Flutter]

## Rationale
- Q1 result: …
- Q2 result: …
- Q3 result: …
- Q4 result: …
(Q5+ if applicable)

## Scoring (top 3 paths)
| Criterion | Chosen | Runner-up | Third |
| …         | …       | …         | …     |

## Why we did NOT choose
- [Path]: [reason]

## Risks acknowledged
- [Risk 1: e.g., team needs Kotlin training]
- [Risk 2: e.g., bundle size +9MB]

## Re-evaluation trigger
- Decide if/when this should be revisited (e.g., team size doubles, KMP iOS UI matures further, performance regression)

## Handoff
- If pure-native or hybrid → continue to Port `blueprint`
- If RN / Flutter / Compose Multiplatform → route to Native; Port stops
```

This decision is journaled in `.agents/port.md` along with the date and the scoring snapshot. Future Port invocations on the same project should respect the decision unless explicitly revisited.

---

## 9. Sources (2026-05 snapshot)

- JetBrains Blog — "Compose Multiplatform 1.8.0 — iOS Stable & Production Ready" (2025-05)
- JetBrains Blog — "Compose Multiplatform 1.11.0 Is Now Available" (2026-05)
- JetBrains KMP Roadmap and "Compatibility and versions" docs (kotlinlang.org/docs/multiplatform/compose-compatibility-and-versioning.html)
- kmpship.app — "Is Kotlin Multiplatform production-ready in 2026?"
- Airbnb Engineering — "Sunsetting React Native" (2018) and follow-up retrospectives
- Discord Blog / Margelo — "Native iOS performance with React Native" (2024-2025)
- React Native release notes 0.79 (2025-04), 0.80 (2025-06 — Legacy Architecture frozen), 0.82 (2025-11/12 — New Arch disable-option removed), 0.83 (2026 — Legacy code removed)
- reactwg/react-native-new-architecture — "Freezing the Legacy Architecture" (Discussion #290)
- Expo Changelog — SDK 53 (2025-04, RN 0.79, New Arch default) / SDK 54 (2025-09, RN 0.81 + precompiled iOS XCFrameworks)
- Flutter release notes 3.29 (2025-02, Impeller default on Android), 3.29.3 / 3.32 (Skia fallback for API 28-), 3.32 (web stateful hot reload experimental)
- Ionic Blog — "Capacitor 7 has hit GA!" (2025-04)
- Tauri Blog — "Tauri 2.0 Release Candidate" / Tauri 2 stable (2025-01)
- Android Developers Blog — Compose / Material 3 1.4 (2025-09-24) / Material 3 Expressive rollout (2025-09) / Compose BOM 2026.05 (Compose 1.11.1)
