# Handoff Payload Schemas

**Purpose:** Full input/output handoff payloads for Berth's partners.
**Read when:** Receiving from or sending to Native, Launch, Cloak, Snap, Prose, or Gear.

---

## Incoming

### `NATIVE_TO_BERTH_HANDOFF`
```yaml
NATIVE_TO_BERTH_HANDOFF:
  platforms: ["iOS", "Android"]
  build_artifacts: ["[IPA path]", "[AAB path]"]
  app_version: "[semver]"
  bundle_ids: { ios: "[id]", android: "[applicationId]" }
  entitlements: ["[push, app groups, associated domains, …]"]
  privacy_manifest_present: true | false
  declared_permissions: ["[permission strings]"]
  third_party_sdks: ["[sdk + collected data]"]
  parity_notes: "[iOS/Android feature divergences]"
```

### `LAUNCH_TO_BERTH_HANDOFF`
```yaml
LAUNCH_TO_BERTH_HANDOFF:
  app_version: "[semver]"
  platforms: ["iOS", "Android"]
  release_scope: "[what changed]"
  target_markets: ["[storefronts]"]
  monetization: "free | iap | subscription | paid | external_purchase"
  needs: "store-readiness verdict + submission timeline"
```

### `CLOAK_TO_BERTH_HANDOFF`
```yaml
CLOAK_TO_BERTH_HANDOFF:
  data_inventory:
    - type: "[e.g., precise location]"
      collected: true | false
      shared: true | false
      linked_to_identity: true | false
      used_for_tracking: true | false
      purpose: "[app functionality | analytics | ads | …]"
  consent_mechanism: "[how consent is obtained]"
```

---

## Outgoing

### `BERTH_TO_LAUNCH_HANDOFF`
```yaml
BERTH_TO_LAUNCH_HANDOFF:
  store_readiness: "GO | CONDITIONAL | NO_GO"
  blockers:
    ios: ["[blocker + guideline section]"]
    android: ["[blocker + policy reference]"]
  privacy_declarations:
    ios_app_privacy: "complete | incomplete"
    ios_privacy_manifest: "complete | incomplete | n/a"
    android_data_safety: "complete | incomplete"
  submission_timeline:
    ios: "[track sequence + submit date]"
    android: "[track sequence + submit date]"
    review_lead_time: "iOS ~24-48h, up to ~72h cross-store; fixed gate (verify current norms)"
  compliance_deadlines: ["[target API / SDK / 16KB / account-deletion]"]
  policy_as_of: "[date/version verified]"
  next_owner: "Launch (rollout staging, Go/No-Go, rollback)"
```

### `BERTH_TO_SNAP_HANDOFF`
```yaml
BERTH_TO_SNAP_HANDOFF:
  request: "screenshots + previews"
  ios_specs: ["[required device sizes per current App Store Connect]"]
  android_specs: ["[phone/tablet screenshot + feature graphic dims]"]
  locales: ["[locale list]"]
  notes: "status-bar-clean; reflect real UI (avoid 2.3 metadata rejection)"
```

### `BERTH_TO_PROSE_HANDOFF`
```yaml
BERTH_TO_PROSE_HANDOFF:
  request: "store listing copy + What's New"
  fields: ["title", "subtitle/short-desc", "description", "keywords", "whats_new"]
  locales: ["[locale list]"]
  constraints: "[char limits per store/field]; accurate to actual functionality"
```

### `BERTH_TO_GEAR_HANDOFF`
```yaml
BERTH_TO_GEAR_HANDOFF:
  request: "upload automation"
  ios: "fastlane deliver / Transporter; testflight track"
  android: "fastlane supply / bundletool; target track"
  metadata_source: "[path or console]"
  notes: "Berth has validated compliance; Gear automates upload only"
```

---

## Handoff Rules

- Validate every incoming payload on receipt. If `privacy_manifest_present: false` (iOS) or Data safety is incomplete (Android), **reject back to Native** before proceeding — these block all tracks.
- Berth never executes uploads or sets rollout percentages. Compliance verdict + submission plan in; rollout orchestration handed to `Launch`; upload mechanics handed to `Gear`.
- Always include `policy_as_of` so downstream agents know the freshness of the compliance verdict.
