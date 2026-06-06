# Platform Permissions Guide

**Purpose:** Permission management patterns and best practices for pure-native iOS / Android.
**Read when:** Implementing camera, location, notification, or other permission requests.

---

## iOS Permissions

### Info.plist Usage Description Keys

| Permission | Key | Example Description |
|------------|-----|---------------------|
| Camera | NSCameraUsageDescription | Used to take product photos. |
| Photo Library | NSPhotoLibraryUsageDescription | Used to choose a profile picture. |
| Location (in use) | NSLocationWhenInUseUsageDescription | Used to find nearby stores. |
| Location (always) | NSLocationAlwaysUsageDescription | Used to track delivery progress. |
| Notifications | (runtime request) | Requested at runtime via UNUserNotificationCenter |
| Contacts | NSContactsUsageDescription | Used by the friend invite feature. |
| Microphone | NSMicrophoneUsageDescription | Used to record voice messages. |
| Face ID | NSFaceIDUsageDescription | Used for secure sign-in. |
| Tracking | NSUserTrackingUsageDescription | Used to personalize ads. |

### iOS Permission Flow (Swift / SwiftUI)

```swift
import AVFoundation

@MainActor
final class CameraPermissionCoordinator {
    enum Result { case granted, denied, blocked }

    func requestCamera() async -> Result {
        // 1. Check current status
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            return .granted
        case .denied, .restricted:
            // 4. Guide to Settings (blocked path)
            return .blocked
        case .notDetermined:
            // 2. Soft pre-prompt (custom UI)
            guard await showPrePromptUI() else { return .denied }
            // 3. System prompt
            let granted = await AVCaptureDevice.requestAccess(for: .video)
            return granted ? .granted : .denied
        @unknown default:
            return .denied
        }
    }

    private func showPrePromptUI() async -> Bool {
        // Render a custom modal explaining why camera access is needed
        // Return true if the user taps Continue
        true
    }
}
```

---

## Android Permissions

### AndroidManifest.xml Declarations

```xml
<!-- Normal permissions (auto-granted) -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.VIBRATE" />

<!-- Dangerous permissions (runtime request required) -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.READ_CONTACTS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />

<!-- Android 13+ notification permission -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

<!-- Android 14+ photo/video picker -->
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_MEDIA_VIDEO" />
```

### Android Runtime Permission (Jetpack Compose)

```kotlin
@Composable
fun CameraFeature() {
    val cameraPermissionState = rememberPermissionState(Manifest.permission.CAMERA)

    when {
        cameraPermissionState.status.isGranted -> {
            CameraPreview()
        }
        cameraPermissionState.status.shouldShowRationale -> {
            // Pre-prompt with rationale
            RationaleDialog(
                title = "Camera access",
                message = "We use the camera to take product photos.",
                onConfirm = { cameraPermissionState.launchPermissionRequest() },
                onDismiss = { /* Show degraded UI */ },
            )
        }
        else -> {
            // First request or permanently denied
            PermissionRequestButton(
                text = "Enable camera",
                onClick = { cameraPermissionState.launchPermissionRequest() },
            )
        }
    }
}
```

---

## Pre-Prompt Best Practices

### Do

- Request immediately before the user uses the feature (do not bulk-request at app launch).
- Explain *why* concretely ("to take product photos", not "to improve the app").
- Provide a graceful fallback when the user declines.
- Provide a deep link to Settings when the permission is blocked.

### Don't

- Request all permissions in a batch at app launch.
- Use vague reasons ("to improve the app experience").
- Re-prompt repeatedly after denial.
- Show errors without explaining that the feature requires the permission.

### Pre-Prompt UI Pattern

```
┌────────────────────────────────┐
│  Camera access                 │
│                                │
│  We use the camera to take     │
│  product photos.               │
│                                │
│  [Not now]   [Continue]        │
└────────────────────────────────┘
        ↓ tap Continue
┌────────────────────────────────┐
│  "MyApp" Would Like to         │
│  Access the Camera             │
│                                │
│  [Don't Allow]   [OK]          │  ← system dialog
└────────────────────────────────┘
```

---

## Permission Audit Checklist

| Check | iOS | Android |
|-------|-----|---------|
| Declare only required permissions | Info.plist review | Manifest review |
| Usage Description is concrete | Required | N/A (rationale in code) |
| Pre-prompt UI implemented | Recommended | shouldShowRationale |
| Graceful degradation on denial | Required | Required |
| Settings entry on blocked / permanently denied | Required | Required |
| Android 13+ notification permission | N/A | POST_NOTIFICATIONS |
