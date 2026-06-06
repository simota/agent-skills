# Mobile Prototyping Reference

Purpose: Ship a demoable mobile prototype inside the ≤4h time-box. The prototype validates a single interaction or flow hypothesis — not the full app. Native capabilities are stubbed during STRIKE and swapped for real APIs only if the hypothesis survives.

## Scope Boundary

- **Forge `mobile`**: throwaway-first mobile PoC (Expo / RN / Flutter), native capabilities stubbed, simulator-only by default.
- **Native (elsewhere)**: production mobile build, store review prep, offline strategy, navigation architecture.

If the hypothesis asks "does this flow feel right?" → `mobile`. If it asks "does this scale under real network/battery/permissions?" → hand off to `Native`.

## Stack Selection

| Framework | Pick when | Skip when |
|-----------|-----------|-----------|
| Expo (SDK 52+) | React knowledge, fastest bootstrap, Expo Go preview | Need custom native modules early |
| React Native bare | Native module needed, custom build flavors | Single-session PoC — overkill |
| Flutter | Team already fluent in Dart, motion-heavy UI | Team unfamiliar with Dart (time-box blown on syntax) |
| Capacitor + React | Existing web app becoming mobile PoC | True native feel is the hypothesis |

Default: **Expo** — fastest time-to-demoable for single-slice PoC.

## Workflow

```
SCAFFOLD  →  declare hypothesis + target platform (iOS / Android / both)
          →  pick framework, run CLI scaffold (`npx create-expo-app`)
          →  list native capabilities (camera / push / location / biometric / file)
          →  decide: stub all, stub critical path only, or real API

STRIKE    →  build single screen or flow (navigation min: 1-3 screens)
          →  stub native capabilities with Promise-returning mocks
          →  use deterministic mock data (avoid network in STRIKE)
          →  happy path demoable in simulator / Expo Go

COOL      →  verify on both orientations if relevant
          →  check safe-area insets (notch / home indicator)
          →  note skipped: keyboard avoidance, offline, deep-link, push perms
          →  screenshot / screen-record for PRESENT

PRESENT   →  ADOPT / ITERATE / DISCARD
          →  if ADOPT: hand off to Native with stubs + hypothesis outcome
```

## Native Capability Stubs

Never wire real permissions during STRIKE. Ship mocks that return instantly.

```ts
// stubs/camera.ts
export async function takePhoto(): Promise<{ uri: string }> {
  await new Promise(r => setTimeout(r, 400)); // mimic shutter delay
  return { uri: 'https://picsum.photos/seed/photo/400/600' };
}

// stubs/location.ts
export async function getLocation(): Promise<{ lat: number; lng: number }> {
  return { lat: 35.6762, lng: 139.6503 }; // deterministic
}

// stubs/biometric.ts
export async function authenticate(): Promise<boolean> {
  await new Promise(r => setTimeout(r, 300));
  return true; // always succeed in PoC
}
```

Swap stubs → real APIs only at the ADOPT boundary, and hand off to Native.

## Platform Preview Strategy

| Preview | When | Cost |
|---------|------|------|
| Expo Go (physical phone) | Fastest demo loop, shareable via QR | Cannot test custom native modules |
| iOS Simulator | Layout + touch affordances | No camera, no real push, mac-only |
| Android Emulator | Layout + Material affordances | Slow cold start; prefer Expo Go |
| Real device build (EAS) | Native modules or store preview | ≥30 min build — rarely worth it in PoC |

Default: **Expo Go over QR code**. If the hypothesis is "does the native API work?", real-device build is justified — but that's an `mobile` escape hatch, usually → `Native`.

## Time-Box Anti-Patterns

- ❌ Bootstrap EAS build pipeline during PoC (adds 45+ min, adds zero hypothesis value).
- ❌ Wire real push notifications "just to show it works" — permission dialog breaks demo.
- ❌ Polish safe-area + keyboard avoidance + dark mode in one session.
- ❌ Add a navigation library when 2 screens and `useState` would suffice.
- ❌ Configure CodePush / OTA before knowing if the flow is kept.

## What Goes in the Handoff to Native

- Screenshot or screen-recording of demoable flow.
- List of stubbed native capabilities (camera / location / push / biometric / file).
- Mock data shapes used (so Native can build real types).
- Known skipped: offline, deep-link, permission denial paths, locale, keyboard, push token lifecycle.
- Hypothesis outcome: what was learned, what flow changed, what the next production bet is.
