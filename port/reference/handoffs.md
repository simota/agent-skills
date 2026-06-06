# Handoff Templates

Port is a design agent. Implementation flows downstream. These templates are the contracts Port emits to implementer agents.

Each handoff includes:
- A YAML block with required fields.
- The minimum content the receiving agent needs to start work.
- A one-line "what success looks like" for the receiver.

---

## Inbound

### `USER_TO_PORT_REQUEST`

```yaml
USER_TO_PORT_REQUEST:
  goal: "Port the web app at <repo or URL> to native iOS and Android"
  source_web_stack: "[detected at SURVEY]"
  target_platforms: ["iOS Swift", "Android Kotlin"]
  parity_goal: "MVP | Full | Enhanced"
  constraints:
    min_ios: "[default 16]"
    min_android: "[default API 28]"
    offline: "[T0 default | T1 | T2 | T3]"
    regulatory: "[GDPR | HIPAA | PCI-DSS | none]"
    budget: "[time / team / external]"
    web_shutdown: "[yes | no | undecided]"
  context:
    user_role: "[PM | Tech lead | Founder | Other]"
    existing_native: "[none | partial RN/Flutter | partial native | full native to be replaced]"
```

### `ATLAS_TO_PORT_HANDOFF` (input)

```yaml
ATLAS_TO_PORT_HANDOFF:
  application_architecture:
    style: "[SPA | SSR | RSC | Islands | Hybrid]"
    layering: "[layered | hex | clean | other]"
    god_classes: ["[list]"]
    circular_deps: ["[list]"]
  module_boundaries:
    - name: "[feature]"
      coupling: "[low | medium | high]"
  external_systems:
    - name: "[system]"
      protocol: "[REST | GraphQL | WS]"
      criticality: "[high | medium | low]"
```

### `LENS_TO_PORT_HANDOFF` (input)

```yaml
LENS_TO_PORT_HANDOFF:
  codebase_summary:
    routes: [count]
    components: [count]
    stores: [count]
    api_endpoints: [count]
  feature_inventory:
    - name: "[feature]"
      entry: "[file path]"
      depends_on: ["[modules]"]
      external_sdks: ["[list]"]
  storage_usage:
    localStorage: ["[keys]"]
    indexeddb: ["[stores]"]
    cookies: ["[names]"]
  auth_flow_summary: "[textual]"
```

### `FOSSIL_TO_PORT_HANDOFF` (input)

```yaml
FOSSIL_TO_PORT_HANDOFF:
  business_rules:
    - id: "[BR-001]"
      description: "[rule]"
      location: "[file:line]"
      portability: "[pure logic | UI-coupled | server-coupled]"
  legacy_patterns:
    - pattern: "[name]"
      reason_to_preserve: "[why]"
      reason_to_drop: "[why not]"
```

### `RESEARCHER_TO_PORT_HANDOFF` (input)

```yaml
RESEARCHER_TO_PORT_HANDOFF:
  personas: ["[name + summary]"]
  mobile_usage_patterns:
    - pattern: "[on-the-go | tablet-paired | offline-frequent]"
      frequency: "[%]"
  jobs_to_be_done: ["[JTBD]"]
  pain_points_with_web: ["[list]"]
```

### `VISION_TO_PORT_HANDOFF` (input)

```yaml
VISION_TO_PORT_HANDOFF:
  design_direction:
    visual_language: "[description]"
    motion_principles: ["[list]"]
    accessibility_targets: ["WCAG AA | AAA"]
  ios_specific: "[HIG considerations]"
  android_specific: "[Material 3 considerations]"
  design_tokens_ref: "[Muse handoff link]"
```

### `FRAME_TO_PORT_HANDOFF` (input)

```yaml
FRAME_TO_PORT_HANDOFF:
  figma_files: ["[file URL]"]
  components_extracted: [count]
  tokens_extracted: [count]
  code_connect_status: "[ready | partial | none]"
  per_screen_specs:
    - screen: "[name]"
      figma_node: "[node id]"
```

---

## Outbound

### `PORT_TO_NATIVE_HANDOFF`

```yaml
PORT_TO_NATIVE_HANDOFF:
  scope: "[per-screen impl spec | full app build-out]"
  target_platforms: ["iOS", "Android"]
  blueprint_ref: "[path to blueprint.md]"
  parity_matrix_ref: "[path]"
  architecture_map_ref: "[path]"
  per_screen_specs:
    - screen_name: "[Home]"
      web_route: "/"
      ios_view: "HomeView"
      ios_viewmodel: "HomeViewModel"
      ios_navigation: "[Tab root]"
      android_screen: "HomeScreen"
      android_viewmodel: "HomeViewModel"
      android_navigation: "[startDestination]"
      data_dependencies: ["[Repository names]"]
      offline_tier: "T1"
      a11y_notes: "[VoiceOver / TalkBack labels per element]"
      ux_divergence: "[any deliberate iOS vs Android difference]"
  defaults:
    ios:
      language: "Swift 6"
      ui: "SwiftUI"
      arch: "MVVM-C"
      min_os: "iOS 16"
      di: "[swift-dependencies | Factory | manual]"
    android:
      language: "Kotlin 2.4+"
      ui: "Jetpack Compose"
      arch: "MVVM (or MVI per screen)"
      min_os: "API 28"
      di: "Hilt"
  performance_budget:
    cold_start_max: "2.5s"
    crash_free_min: "99.85%"
    interaction_p95: "100ms"
  next_action: "Implement per-screen specs in Phase 1 order"
```

### `PORT_TO_SCAFFOLD_HANDOFF`

```yaml
PORT_TO_SCAFFOLD_HANDOFF:
  scope: "iOS and Android project skeleton"
  ios_skeleton:
    workspace: "Xcode workspace + SPM packages"
    targets: ["App", "AppTests", "AppUITests", "[WidgetExtension if any]"]
    packages: ["AppCore", "DesignSystem", "[Features...]"]
    capabilities: ["Sign in with Apple", "Push", "Associated Domains", "Keychain Sharing", "Background Fetch"]
    config: ["Info.plist usage strings", "PrivacyInfo.xcprivacy"]
  android_skeleton:
    project: "Gradle multi-module"
    modules: [":app", ":core:network", ":core:auth", ":core:database", ":core:designsystem", ":core:common", "[:feature:*]"]
    permissions: ["[list with rationale]"]
    config: ["AndroidManifest.xml", "ProGuard / R8 rules"]
  shared:
    ci_provider: "[GitHub Actions | Xcode Cloud + GitHub Actions]"
    secrets: ["[external services to provision]"]
    feature_flags_provider: "[name]"
    crash_reporting: "[Firebase Crashlytics | Sentry]"
    analytics: "[provider]"
  next_action: "Provision projects; ship Phase 0 skeleton with 'hello world authenticated' build"
```

### `PORT_TO_GATEWAY_HANDOFF`

```yaml
PORT_TO_GATEWAY_HANDOFF:
  scope: "Mobile-friendly API contract redesign"
  current_api:
    style: "[REST | GraphQL | mixed]"
    base_url: "[url]"
    auth: "[cookie | bearer | OAuth | OIDC]"
  mobile_requirements:
    - require: "Token-based auth (Authorization: Bearer)"
      reason: "Mobile cannot rely on cookies"
    - require: "Cursor or offset pagination on list endpoints"
      reason: "Mobile screens scroll-paginate; offset > 1000 is a smell"
    - require: "Server-side image variants and signed CDN URLs"
      reason: "Bandwidth + memory budget on mobile"
    - require: "ETag / Last-Modified on cacheable resources"
      reason: "Conditional fetches for offline tier"
    - require: "Retry-After header on 429 / 503"
      reason: "Mobile retry/backoff with jitter"
    - require: "Privacy of payload (no HTML bodies, no CSS classes)"
      reason: "Mobile renders native"
  endpoints_to_redesign:
    - path: "/feed"
      issues: ["No pagination", "Returns HTML"]
      proposal: "Add cursor pagination + JSON-only payload + image variants"
  push_api:
    needs: "Server endpoint to register/unregister APNs/FCM tokens per user/device"
    schema: "[token, platform, device_id, app_version, locale]"
  realtime_api:
    needs: "[WebSocket | SSE | none]"
  next_action: "Owner: Gateway. Produce OpenAPI spec for mobile-friendly endpoints, version v2"
```

### `PORT_TO_SCHEMA_HANDOFF`

```yaml
PORT_TO_SCHEMA_HANDOFF:
  scope: "Local database schema for iOS and Android"
  ios_target: "Core Data | SwiftData"
  android_target: "Room"
  domains:
    - name: "User"
      entities: ["UserProfile", "UserPreference"]
      offline_tier: "T1"
    - name: "Content"
      entities: ["Article", "Tag", "Comment"]
      offline_tier: "T1"
    - name: "Drafts"
      entities: ["Draft", "PendingWrite"]
      offline_tier: "T2"
  migrations:
    versioned: "yes"
    rollback: "supported"
  encryption:
    at_rest: "[NSFileProtection (iOS) | SQLCipher if regulated]"
  next_action: "Owner: Schema. Produce ER diagram and migration plan per domain"
```

### `PORT_TO_BUILDER_HANDOFF`

```yaml
PORT_TO_BUILDER_HANDOFF:
  scope: "Shared business logic candidates"
  approach: "Pure-native (no KMP) | KMP-shared business logic if approved"
  pure_logic_modules:
    - name: "[validation rules]"
      web_location: "[file]"
      target_iOS: "Swift module"
      target_android: "Kotlin module"
      shared_kmp: "[no | yes if KMP path approved]"
  business_rules_to_mirror_exactly:
    - id: "[BR-001]"
      description: "[rule]"
      acceptance_test: "[input → expected output]"
  next_action: "Owner: Builder. Implement and unit-test parity rules on both platforms"
```

### `PORT_TO_POLYGLOT_HANDOFF`

```yaml
PORT_TO_POLYGLOT_HANDOFF:
  scope: "Mobile i18n/l10n strategy"
  locales: ["[ja-JP, en-US, ...]"]
  rtl_support: "[yes | no]"
  ios_format: "String Catalog (.xcstrings) preferred; Localizable.strings fallback"
  android_format: "strings.xml per values-<locale>"
  pluralization: "ICU MessageFormat for both"
  date_currency_number: "Use platform formatters (DateFormatter / NumberFormatter; java.time / NumberFormat)"
  rtl_layouts: "[required screens]"
  ime_considerations: "[Japanese: input method handling; Korean / Chinese / etc.]"
  next_action: "Owner: Polyglot. Audit hardcoded strings and produce extraction plan per platform"
```

### `PORT_TO_VOYAGER_HANDOFF`

```yaml
PORT_TO_VOYAGER_HANDOFF:
  scope: "Mobile E2E test specification"
  framework_ios: "[XCUITest | Maestro]"
  framework_android: "[Espresso | Maestro | UI Automator]"
  critical_flows:
    - name: "Auth happy path"
      steps: ["Open app", "Tap login", "Enter credentials", "Verify home"]
    - name: "Push deep link to detail"
      steps: ["Receive push", "Tap notification", "Verify detail screen"]
    - name: "Offline read"
      steps: ["Disconnect network", "Open feed", "Verify cached items render"]
  performance_assertions:
    cold_start_p95: "2.5s"
  device_matrix:
    ios: ["iPhone 13", "iPhone 15 Pro Max"]
    android: ["Pixel 6", "Galaxy A54"]
  next_action: "Owner: Voyager. Implement and integrate to CI"
```

### `PORT_TO_LAUNCH_HANDOFF`

```yaml
PORT_TO_LAUNCH_HANDOFF:
  scope: "Phased rollout and store submission plan"
  phases: [P0, P1, P2, P3]
  per_phase_exit_gates:
    P1:
      - "Crash-free ≥ 99.5%"
      - "Cold start ≤ 2.5s"
      - "Auth + push + deep links verified"
  store_submissions:
    ios:
      track: "TestFlight Internal → External → App Review → Phased Release"
    android:
      track: "Internal → Closed → Open → Production Staged Rollout"
  rollback_strategy:
    primary: "Server-driven feature flags with kill switches"
    secondary: "Halt staged rollout; ship hotfix"
  web_shutdown:
    enabled: "[yes | no]"
    gates: "[install %, parity verification, NPS, support readiness]"
  next_action: "Owner: Launch. Coordinate first beta build and submission timing"
```

---

## Handoff Bundle (multi-target output)

When `_STEP_COMPLETE` lists multiple handoffs (typical for blueprint completion), assemble them into a `handoff-bundle.json` referencing each target. See `_templates/handoff-bundle.template.json` for the canonical structure.

---

## Receive-Side Validation (sanity checks)

Before sending any handoff, verify:

- [ ] `parity_matrix_ref` exists and is non-empty.
- [ ] `architecture_map_ref` exists and covers all P1 screens.
- [ ] `data_dependencies` per screen reference real Repositories defined in MAP.
- [ ] Auth flow has both iOS and Android entries.
- [ ] Push schema is included if push is in scope.
- [ ] Offline tier is set per data domain.
- [ ] Min-OS versions are set on both platforms.
- [ ] Risk matrix's Red entries each have a phase-pinned mitigation.

If any check fails, the blueprint is incomplete — return to `BLUEPRINT` before handing off.
