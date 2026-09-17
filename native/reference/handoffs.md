# Native Handoff Contracts

Read only the row for the selected recipient. Shared envelope, ownership and delivery semantics: `_common/HANDOFF.md`. Values must describe the actual Swift/SwiftUI or Kotlin/Compose project, installed toolchain and verified artifacts, not a fictitious app or a cached minimum version.

## Incoming

| Marker | Required domain payload |
|---|---|
| `PORT_TO_NATIVE_HANDOFF` | Consume the canonical schema in `../port/reference/handoffs.md`: blueprint, parity matrix, architecture map, screen specifications and platform defaults. Do not substitute a prototype summary. |
| `FORGE_TO_NATIVE_HANDOFF` | `prototype_url`, `target_platforms`, `framework`, `validated_patterns` (navigation/state/data), `prototype_quality` (L0–L3), `known_issues`, `handoff_notes`. A cross-platform prototype is evidence/input, not permission to implement that framework. |
| `VISION_TO_NATIVE_HANDOFF` | `design_direction`, `platform_considerations` (ios/android), `key_screens` (name/description), `interaction_patterns`, `references`. |
| `BUILDER_TO_NATIVE_HANDOFF` | `api_specification` (base_url/auth/endpoints with method/path/request_type/response_type), `shared_types` (path/description), `error_handling`, `notes`. Pass credential references only. |

## Outgoing

| Marker | Required domain payload |
|---|---|
| `NATIVE_TO_RADAR_HANDOFF` | `test_scope` (component or flow, type, installed framework, key_scenarios), `platform_specific_tests` (ios/android), `mock_data_location`. Radar owns unit/integration assertions; browser/mobile E2E execution routes to Voyager. |
| `NATIVE_TO_GEAR_HANDOFF` | `ci_cd_requirements` (build/test/deploy by platform), `environment_variables` (names and secret-store references, never values), `fastlane_lanes` only when the project uses Fastlane. Carry signing/provisioning requirements without credentials; do not prescribe Expo, EAS, Jest or OTA for pure-native delivery. |
| `NATIVE_TO_LAUNCH_HANDOFF` | `app_version`, `build_number`, `platforms` (ios: min_os/bundle_id/build_artifact/signing; android: min_sdk/package/build_artifact/signing), `store_compliance` (privacy/iap/content with evidence and unresolved items), `release_notes` by locale, `rollout_plan`, `feature_flags`, `rollback_plan`. Distinguish halt/flag-off/hotfix from an unsupported promise of instantly reverting a released store binary. |
| `NATIVE_TO_VITRINE_HANDOFF` | `components` (name/path/variants/interface schema), actual native preview/catalog configuration and `preview_notes`. `NATIVE_TO_SHOWCASE_HANDOFF` is the legacy name; route existing input to Vitrine, never revive a retired skill or generate React Native stories for a pure-native component. |

## Release Evidence

- Use `reference/store-compliance.md` for applicable policy checks, and `reference/release-rollout.md` for rollout/halt controls; their requirements are not duplicated here.
- Unknown or unverified compliance checks remain unknown/unverified. Never paste sample `OK`, age ratings, SDK deadlines, test metrics or build identifiers as observations.
- A handoff does not authorize deployment, external publication, signing changes, data export or additional spending. Preserve pending approvals and failed checks in the shared envelope.
