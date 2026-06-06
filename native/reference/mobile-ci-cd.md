# Mobile CI/CD

**Purpose:** Mobile CI/CD pipeline design using Fastlane / Xcode Cloud / GitHub Actions for pure-native iOS Swift / Android Kotlin.
**Read when:** Configuring build automation, test execution, or store deployment.

---

## CI/CD Platform Comparison

| Feature | EAS Build | Fastlane | Xcode Cloud | GitHub Actions |
|---------|-----------|----------|-------------|----------------|
| iOS build | ✅ Cloud | ✅ Local/CI | ✅ Cloud | ✅ macOS runner |
| Android build | ✅ Cloud | ✅ Local/CI | ❌ | ✅ Any runner |
| Signing mgmt | ✅ Automatic | ✅ Match | ✅ Automatic | Manual |
| Cost | Expo plan | Free (OSS) | Free (Apple) | Runner cost |
| Best for | Expo projects | Any RN/native | Swift/SwiftUI | Custom pipelines |

---

## EAS Build (Expo)

### eas.json Configuration

```json
{
  "cli": { "version": ">= 12.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "ios": { "resourceClass": "m-medium" }
    },
    "production": {
      "autoIncrement": true,
      "ios": { "resourceClass": "m-medium" }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "ascAppId": "1234567890",
        "appleTeamId": "XXXXXXXXXX"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

### Build & Submit Commands

```bash
# Development build (with dev client)
eas build --profile development --platform all

# Preview build (internal distribution)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Submit to stores
eas submit --platform ios --profile production
eas submit --platform android --profile production
```

---

## Fastlane

### iOS Fastfile

```ruby
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    setup_ci if ENV['CI']
    match(type: "appstore", readonly: true)
    increment_build_number(xcodeproj: "MyApp.xcodeproj")
    build_app(
      scheme: "MyApp",
      export_method: "app-store",
      clean: true
    )
    upload_to_testflight(skip_waiting_for_build_processing: true)
    slack(message: "New iOS beta uploaded to TestFlight")
  end

  desc "Deploy to App Store"
  lane :release do
    setup_ci if ENV['CI']
    match(type: "appstore", readonly: true)
    build_app(scheme: "MyApp", export_method: "app-store")
    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      force: true
    )
  end
end
```

### Android Fastfile

```ruby
default_platform(:android)

platform :android do
  desc "Deploy to Google Play Internal Testing"
  lane :beta do
    gradle(task: "clean bundleRelease")
    upload_to_play_store(
      track: "internal",
      aab: "app/build/outputs/bundle/release/app-release.aab"
    )
    slack(message: "New Android beta uploaded to Play Console")
  end

  desc "Promote to Production"
  lane :release do
    upload_to_play_store(
      track: "production",
      track_promote_to: "production",
      rollout: "0.1"  # 10% staged rollout
    )
  end
end
```

---

## GitHub Actions Workflow

```yaml
name: Mobile CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test -- --ci --coverage

  build-ios:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --profile preview --platform ios --non-interactive

  build-android:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --profile preview --platform android --non-interactive
```

---

## Signing Management

### iOS Code Signing

| Method | Description | Best For |
|--------|-------------|----------|
| EAS automatic | Expo manages certificates | Expo projects |
| Fastlane Match | Git-based certificate sharing | Team projects |
| Xcode automatic | Xcode manages profiles | Solo/small team |
| Manual | Developer portal management | Enterprise |

### Android Signing

| Method | Description | Best For |
|--------|-------------|----------|
| Play App Signing | Google manages release key | All new apps |
| EAS credentials | Expo manages keystore | Expo projects |
| Manual keystore | Self-managed .jks/.keystore | Legacy apps |

---

## Environment Configuration

```bash
# .env.development
EXPO_PUBLIC_API_URL=http://localhost:3000
EXPO_PUBLIC_SENTRY_DSN=

# .env.staging
EXPO_PUBLIC_API_URL=https://staging-api.example.com
EXPO_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/123

# .env.production
EXPO_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/456
```
