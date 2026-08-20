# Handoff Templates

**Purpose:** Input / output handoff templates for the Native agent (macOS scope).
**Read when:** A handoff format is required for collaboration with another agent.

---

## Incoming Handoffs

### FORGE_TO_NATIVE_MACOS_HANDOFF

```yaml
FORGE_TO_NATIVE_MACOS_HANDOFF:
  prototype_path: "[Prototype location or repo path]"
  framework: "SwiftUI"
  validated_patterns:
    - navigation: "3-pane NavigationSplitView validated"
    - state: "@Observable ViewModel prototype"
    - data: "Local JSON fixture, no persistence yet"
  prototype_quality: "L1"  # L0=builder, L1=functional, L2=polished, L3=near-production
  known_issues:
    - "No document persistence"
    - "No sandbox entitlements configured"
  handoff_notes: "UI validated with stakeholders, needs sandbox + document model + distribution plan"
```

### VISION_TO_NATIVE_MACOS_HANDOFF

```yaml
VISION_TO_NATIVE_MACOS_HANDOFF:
  design_direction: "[Design concept summary]"
  macos_considerations:
    chrome: "Liquid Glass sidebar + toolbar (Tahoe 26), standard title bar"
    window_strategy: "Single primary window, MenuBarExtra companion"
  key_screens:
    - name: "Main window"
      description: "[Screen description]"
    - name: "Preferences"
      description: "[Settings scene layout]"
  interaction_patterns:
    - "Drag-to-reorder in sidebar"
    - "Inspector reveals on selection"
    - "Keyboard-first navigation (⌘1-9 for sidebar sections)"
  references:
    - "[Figma URL or design asset path]"
```

### BUILDER_TO_NATIVE_MACOS_HANDOFF

```yaml
BUILDER_TO_NATIVE_MACOS_HANDOFF:
  api_specification:
    base_url: "[API base URL]"
    auth: "Bearer token / API key"
    endpoints:
      - method: GET
        path: "/api/v1/projects"
        response_type: "Project[]"
      - method: POST
        path: "/api/v1/projects"
        request_type: "CreateProjectRequest"
        response_type: "Project"
  shared_types:
    - path: "Sources/Shared/Models/Project.swift"
      description: "Project domain type (Codable)"
  error_handling:
    - "4xx: show user-facing alert"
    - "429: exponential backoff"
    - "5xx: retry with circuit breaker"
  notes: "API supports ETag for caching; consider for offline document sync"
```

---

## Outgoing Handoffs

### NATIVE_MACOS_TO_RADAR_HANDOFF

```yaml
NATIVE_MACOS_TO_RADAR_HANDOFF:
  test_scope:
    - component: "ProjectSidebarView"
      type: "unit"
      framework: "XCTest / Swift Testing"
      key_scenarios:
        - "Empty state shows placeholder"
        - "Selection updates inspector"
        - "Drag-to-reorder persists order"
    - flow: "Document open/save/autosave"
      type: "ui"
      framework: "XCUITest"
      key_scenarios:
        - "Open via File > Open and via Recent Documents"
        - "Autosave-in-place does not prompt Save dialog"
        - "Quit with unsaved changes prompts correctly"
  macos_specific_tests:
    - "Window restoration after relaunch"
    - "Sandbox: file access via security-scoped bookmark survives relaunch"
    - "MenuBarExtra opens/closes without leaking status item"
  mock_data_location: "Tests/Fixtures/"
```

### NATIVE_MACOS_TO_LAUNCH_HANDOFF

```yaml
NATIVE_MACOS_TO_LAUNCH_HANDOFF:
  app_version: "1.0.0"
  build_number: "12"
  distribution_channel: "developer_id"  # app_store | developer_id | both
  bundle_id: "com.example.myapp"
  min_os: "macOS 15.0 (Sequoia)"
  liquid_glass_baseline: "macOS 26 (Tahoe) — graceful fallback below"
  build_artifact: "MyApp.dmg"
  signing:
    identity: "Developer ID Application: Example Inc"
    hardened_runtime: true
  notarization:
    status: "notarized"  # pending | notarized | rejected | n/a (app_store)
    stapled: true
  sandbox_entitlements:
    - "com.apple.security.app-sandbox"
    - "com.apple.security.files.user-selected.read-write"
    - "com.apple.security.network.client"
  sparkle:
    appcast_url: "https://example.com/appcast.xml"
    signing: "EdDSA"
  release_notes:
    ja: |
      - <JA translation: document autosave support>
      - <JA translation: sidebar reordering>
    en: |
      - Document autosave support
      - Sidebar reordering
  rollback_plan: "Halt Sparkle appcast update, revert to build 11 artifact"
```

### NATIVE_MACOS_TO_GEAR_HANDOFF

```yaml
NATIVE_MACOS_TO_GEAR_HANDOFF:
  ci_cd_requirements:
    build: "Xcode Cloud or `xcodebuild archive`"
    sign: "codesign --deep --options runtime --entitlements MyApp.entitlements"
    notarize: "xcrun notarytool submit MyApp.zip --keychain-profile <profile> --wait"
    staple: "xcrun stapler staple MyApp.app"
    package: "create-dmg or pkgbuild, depending on distribution channel"
  environment_variables:
    - "APPLE_TEAM_ID (secret)"
    - "NOTARIZATION_KEYCHAIN_PROFILE (secret)"
    - "SPARKLE_ED25519_PRIVATE_KEY (secret, Developer ID only)"
  fastlane_lanes:
    - "beta: build + notarize + upload to TestFlight (App Store channel)"
    - "release_direct: build + notarize + staple + publish DMG + update appcast (Developer ID channel)"
```

### NATIVE_MACOS_TO_HONE_HANDOFF

```yaml
NATIVE_MACOS_TO_HONE_HANDOFF:
  app_bundle_id: "com.example.myapp"
  automation_surface:
    apple_events: "AppleScript dictionary exported via .sdef"
    scriptable_objects:
      - name: "document"
        properties: ["name", "path", "modified"]
      - name: "project"
        properties: ["title", "itemCount"]
    services_provided:
      - "Add Selection to MyApp"
  sdef_path: "MyApp/MyApp.sdef"
  notes: "Dictionary covers document CRUD and selection; Builder `automate` owns end-user automation scripts against this surface"
```

### NATIVE_MACOS_TO_CLOAK_HANDOFF

```yaml
NATIVE_MACOS_TO_CLOAK_HANDOFF:
  sandbox_entitlements:
    - entitlement: "com.apple.security.files.user-selected.read-write"
      justification: "User opens/saves documents via NSOpenPanel/NSSavePanel"
    - entitlement: "com.apple.security.network.client"
      justification: "Sync with backend API"
  data_collected: "Document content stored locally; no analytics SDK"
  security_scoped_bookmarks: "Used for Recent Documents list, refreshed on each access"
  review_request: "Confirm entitlement scope is least-privilege before Developer ID submission"
```

### NATIVE_MACOS_TO_CRYPT_HANDOFF

```yaml
NATIVE_MACOS_TO_CRYPT_HANDOFF:
  keychain_usage:
    - item: "API auth token"
      access_control: "kSecAttrAccessibleWhenUnlockedThisDeviceOnly"
  xpc_helper:
    present: false  # true if a privileged helper tool is part of this build
    smappservice_registration: "n/a"
  review_request: "Confirm token storage and (if present) XPC trust boundary before release"
```
