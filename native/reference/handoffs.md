# Handoff Templates

**Purpose:** Input / output handoff templates for the Native agent.
**Read when:** A handoff format is required for collaboration with another agent.

---

## Incoming Handoffs

### FORGE_TO_NATIVE_HANDOFF

```yaml
FORGE_TO_NATIVE_HANDOFF:
  prototype_url: "[Prototype location or repo path]"
  target_platforms:
    - iOS
    - Android
  framework: "React Native | Flutter | SwiftUI | Compose"
  validated_patterns:
    - navigation: "Stack with 3 screens validated"
    - state: "Cart state with Zustand prototype"
    - data: "REST API mock with MSW"
  prototype_quality: "L1"  # L0=sketch, L1=functional, L2=polished, L3=near-production
  known_issues:
    - "Android back button not handled"
    - "Offline state not considered"
  handoff_notes: "UI validated with stakeholders, business logic needs production hardening"
```

### VISION_TO_NATIVE_HANDOFF

```yaml
VISION_TO_NATIVE_HANDOFF:
  design_direction: "[Design concept summary]"
  platform_considerations:
    ios: "SF Symbols, native feel, bottom sheet modals"
    android: "Material 3 tokens, top app bar, FAB"
  key_screens:
    - name: "Home"
      description: "[Screen description]"
    - name: "Detail"
      description: "[Screen description]"
  interaction_patterns:
    - "Swipe-to-dismiss for modals"
    - "Pull-to-refresh on lists"
    - "Haptic feedback on key actions"
  references:
    - "[Figma URL or design asset path]"
```

### BUILDER_TO_NATIVE_HANDOFF

```yaml
BUILDER_TO_NATIVE_HANDOFF:
  api_specification:
    base_url: "[API base URL]"
    auth: "Bearer token / API key"
    endpoints:
      - method: GET
        path: "/api/v1/products"
        response_type: "Product[]"
      - method: POST
        path: "/api/v1/cart/items"
        request_type: "AddCartItemRequest"
        response_type: "CartItem"
  shared_types:
    - path: "src/types/product.ts"
      description: "Product domain types"
  error_handling:
    - "4xx: show user-friendly message"
    - "429: exponential backoff"
    - "5xx: retry with circuit breaker"
  notes: "API supports ETag for caching, use for offline sync"
```

---

## Outgoing Handoffs

### NATIVE_TO_RADAR_HANDOFF

```yaml
NATIVE_TO_RADAR_HANDOFF:
  test_scope:
    - component: "CartScreen"
      type: "unit"
      framework: "jest + @testing-library/react-native"
      key_scenarios:
        - "Empty cart displays placeholder"
        - "Add item updates count badge"
        - "Offline queue shows pending indicator"
    - flow: "Checkout"
      type: "e2e"
      framework: "detox | maestro"
      key_scenarios:
        - "Complete purchase flow"
        - "Payment failure recovery"
  platform_specific_tests:
    ios:
      - "Face ID permission flow"
    android:
      - "Back button navigation"
  mock_data_location: "src/__mocks__/fixtures/"
```

### NATIVE_TO_LAUNCH_HANDOFF

```yaml
NATIVE_TO_LAUNCH_HANDOFF:
  app_version: "1.2.0"
  build_number: "42"
  platforms:
    ios:
      min_os: "16.0"
      bundle_id: "com.example.myapp"
      build_artifact: "MyApp.ipa"
      signing: "App Store Distribution"
    android:
      min_sdk: 24
      package: "com.example.myapp"
      build_artifact: "app-release.aab"
      signing: "Play App Signing"
  store_compliance:
    privacy:
      - "PrivacyInfo.xcprivacy updated"
      - "Data safety form matches implementation"
    iap:
      - "All subscriptions tested in sandbox"
      - "Restore button accessible from settings"
    content:
      - "Age rating: 4+ (no user-generated content)"
  release_notes:
    ja: |
      - <JA translation: offline cart support>
      - <JA translation: push notification integration>
      - <JA translation: performance improvements>
    en: |
      - Offline cart support
      - Push notification integration
      - Performance improvements
  rollback_plan: "Revert to build 41 via Fastlane if critical issues found"
```

### NATIVE_TO_GEAR_HANDOFF

```yaml
NATIVE_TO_GEAR_HANDOFF:
  ci_cd_requirements:
    build:
      ios: "EAS Build or Xcode Cloud"
      android: "EAS Build or Gradle"
    test:
      unit: "jest --ci"
      e2e: "maestro test flows/"
    deploy:
      staging: "EAS Update (OTA) to preview channel"
      production: "EAS Submit to App Store Connect / Google Play Console"
  environment_variables:
    - "EXPO_PUBLIC_API_URL"
    - "SENTRY_DSN"
    - "GOOGLE_SERVICES_JSON (secret)"
    - "APPLE_TEAM_ID (secret)"
  fastlane_lanes:
    - "beta: build + deploy to TestFlight/Internal Testing"
    - "release: build + submit for review"
```

### NATIVE_TO_SHOWCASE_HANDOFF

```yaml
NATIVE_TO_SHOWCASE_HANDOFF:
  components:
    - name: "ProductCard"
      path: "src/components/ProductCard.tsx"
      variants: ["default", "compact", "skeleton"]
      props_schema: "src/components/ProductCard.types.ts"
    - name: "CartBadge"
      path: "src/components/CartBadge.tsx"
      variants: ["empty", "count", "offline-pending"]
  storybook_config:
    platform: "react-native"
    addons: ["@storybook/addon-react-native-web"]
  preview_notes: "Use Expo Go or development build for native preview"
```
