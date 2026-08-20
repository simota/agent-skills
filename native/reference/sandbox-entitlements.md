# App Sandbox — Entitlements, Powerbox, Bookmarks, TCC

Production reference for scoping App Sandbox entitlements on macOS, resolving file access through Powerbox, managing security-scoped bookmarks across launches, and navigating TCC-protected resources. Companion to `reference/distribution.md` (hardened runtime is a *separate* system — see § 6) and `reference/xpc-helpers.md` (app groups feed shared-container IPC).

> Scope: App Sandbox (`com.apple.security.*` sandbox keys) and TCC (Info.plist usage-description strings + user-approved system settings). Signing/notarization mechanics live in `reference/macos-xcrun-cli.md`; the ship decision matrix lives in `reference/distribution.md`.

---

## 1. Enabling the Sandbox

- Xcode target → **Signing & Capabilities** → **App Sandbox** capability, or hand-edit `*.entitlements`:

```xml
<key>com.apple.security.app-sandbox</key>
<true/>
```

- `com.apple.security.app-sandbox` is mandatory for Mac App Store distribution; optional (but recommended) for Developer ID direct distribution.
- Every entitlement below is inert unless `app-sandbox` is `true`.

---

## 2. File-Access Entitlement Catalog

| Entitlement | Grants | Least-privilege guidance |
|---|---|---|
| `com.apple.security.files.user-selected.read-only` | Read files/folders the user picked via `NSOpenPanel`/drag-drop (Powerbox-mediated) | Default choice for "import/open a file" flows — never request broader access just to open one file |
| `com.apple.security.files.user-selected.read-write` | Read+write user-picked files/folders | Only when the app writes back to the *same* user-picked location (editors, not viewers) |
| `com.apple.security.files.user-selected.executable` | Execute a user-selected file (e.g. running a user-chosen script/binary) | Rare — pair with code-signing checks on the target before exec |
| `com.apple.security.files.downloads.read-only` / `.read-write` | Access `~/Downloads` without a picker prompt each time | Only if the app's core purpose is downloads management; otherwise use a picker |
| `com.apple.security.files.bookmarks.app-scope` | Resolve app-scoped security-scoped bookmarks (bookmark valid only for the app that created it) | Default bookmark scope for most apps (see § 4) |
| `com.apple.security.files.bookmarks.document-scope` | Resolve document-scoped bookmarks, shareable across apps/processes via the document itself | Document-based apps that hand bookmarks to XPC helpers or export them in a doc format |
| `com.apple.security.assets.pictures.read-only` / `.read-write` | `~/Pictures` without per-file picker | Photo/image-management apps whose *entire purpose* is browsing this library |
| `com.apple.security.assets.music.read-only` / `.read-write` | `~/Music` | Music-library apps only |
| `com.apple.security.assets.movies.read-only` / `.read-write` | `~/Movies` | Video-library apps only |

**Rule of thumb**: prefer `files.user-selected.*` + a persisted security-scoped bookmark over any `assets.*`/`files.downloads.*` blanket grant — the blanket grants exist for library-management apps (Photos-like, Music-like), not general-purpose apps that merely read a file from those folders occasionally.

---

## 3. Network, Device, and Personal-Information Entitlements

| Entitlement | Grants | Least-privilege guidance |
|---|---|---|
| `com.apple.security.network.client` | Outbound network connections | Required for any HTTP client / WebSocket / URLSession usage |
| `com.apple.security.network.server` | Inbound listening sockets | Only for apps that run a local server (sync daemons, local API); omit otherwise |
| `com.apple.security.device.camera` | Camera capture APIs | Pair with `NSCameraUsageDescription` (§ 6) — entitlement alone does not suppress the TCC prompt |
| `com.apple.security.device.microphone` | Microphone capture APIs | Pair with `NSMicrophoneUsageDescription` |
| `com.apple.security.device.usb` | Direct USB device communication (IOKit) | Hardware-integration apps only (MIDI controllers, peripherals) |
| `com.apple.security.device.bluetooth` | CoreBluetooth central/peripheral roles | Only if the app talks to BLE accessories directly |
| `com.apple.security.device.audio-video-bridging` | AVB networking devices | Pro-audio/video-over-IP apps `(unverified — narrow professional use case, confirm need against current entitlement docs before shipping)` |
| `com.apple.security.print` | `NSPrintOperation` / print panel | Needed even though printing feels like a "normal" OS feature — sandboxed apps must declare it |
| `com.apple.security.scripting-targets` | Scoped AppleScript/Apple Events access to specific *other* apps (dictionary + access level per target) | Prefer this scoped form over the blanket entitlement below when scripting a known set of apps |
| `com.apple.security.automation.apple-events` | Send Apple Events broadly (paired with per-target `NSAppleEventsUsageDescription` prompts at runtime) | Only for automation-hub apps; route "Native builds a scriptable app" vs "app scripts other apps" through the Native↔Hone boundary — this entitlement is for the latter direction |
| `com.apple.security.personal-information.addressbook` | Contacts framework access | Pair with `NSContactsUsageDescription` |
| `com.apple.security.personal-information.calendars` | EventKit calendar access | Pair with `NSCalendarsFullAccessUsageDescription` / `NSCalendarsWriteOnlyAccessUsageDescription` (macOS 14+ split, § 6) |
| `com.apple.security.personal-information.location` | Core Location | Pair with `NSLocationUsageDescription` (macOS uses the unified key, not the iOS when-in-use/always split) |
| `com.apple.security.personal-information.photos-library` | Photos library access via the Photos framework (distinct from `assets.pictures.*`, which is raw filesystem access to `~/Pictures`) | Use this over `assets.pictures.*` when integrating with the Photos app's managed library rather than a flat folder |

---

## 4. Temporary Exception Entitlements

Escape hatches for capabilities the standard catalog does not cover. **App Review scrutinizes every one of these** — justify in App Store Connect notes, and treat as a signal the app may need architectural rework (e.g. an XPC helper outside the sandbox) rather than a permanent fixture.

| Entitlement | Grants | Notes |
|---|---|---|
| `com.apple.security.temporary-exception.files.absolute-path.read-only` / `.read-write` | Access to a specific absolute path outside the sandbox container, declared as an array of path strings | Each string must start with `/`; directories must end with `/`. Prefer security-scoped bookmarks first |
| `com.apple.security.temporary-exception.mach-lookup.global-name` | Look up specific global Mach services by name (array of service names) | Common for talking to system daemons or Endpoint Security-adjacent XPC; App Store review is hostile to this — Developer ID distribution is the realistic path |
| `com.apple.security.temporary-exception.shared-preference.read-write` | Read/write another app's preferences domain via `CFPreferences`/`defaults` (array of bundle IDs) | Debug/power-user tooling; avoid in shipping consumer apps |

If a temporary-exception entitlement is doing permanent load-bearing work, that is itself the signal to reconsider architecture — most legitimate uses resolve to a proper XPC service (`reference/xpc-helpers.md`) or a narrower standard entitlement.

---

## 5. Powerbox and Open/Save Panel Behavior

- Under App Sandbox, `NSOpenPanel`/`NSSavePanel` are rendered by **Powerbox** (a separate, non-sandboxed system process), not by the app itself — this is why sandboxed apps can show file pickers rooted anywhere on disk despite the sandbox otherwise blocking that path.
- A user's selection in the panel is what *grants* the sandbox extension for that path — the grant does not exist before the user picks, and does not persist past the extension's lifetime unless captured as a security-scoped bookmark (§ 6).
- Drag-and-drop of a Finder item into the app grants the same kind of transient sandbox extension as a Powerbox selection — capture it the same way if persistence is needed.
- Panels configured with `directoryURL` pointing outside any entitled location still work because Powerbox — not the app process — resolves and renders the directory listing.

---

## 6. Security-Scoped Bookmarks — Full Lifecycle

Bookmarks are the mechanism for persisting Powerbox-granted file access across app relaunches without re-prompting the user every time.

### 6.1 Create (at time of Powerbox grant)

```swift
func makeBookmark(for url: URL) throws -> Data {
    try url.bookmarkData(
        options: .withSecurityScope,
        includingResourceValuesForKeys: nil,
        relativeTo: nil
    )
}
```

- Use `.withSecurityScope` (not the vanilla, non-scoped bookmark option) — the vanilla form does not carry sandbox-extension rights.
- Persist `Data` in UserDefaults, a plist, or a document's own file format (for document-scoped bookmarks).

### 6.2 Persist

Store the bookmark `Data` keyed by a stable identifier (e.g. document ID, or the resolved path as a cache key). Do **not** store the raw `URL.path` string as your only record — paths can move; bookmarks track the file through renames/moves within the same volume.

### 6.3 Resolve + Start Access (on every relaunch, before touching the file)

```swift
func resolveAndAccess(_ bookmark: Data) throws -> URL? {
    var isStale = false
    let url = try URL(
        resolvingBookmarkData: bookmark,
        options: .withSecurityScope,
        relativeTo: nil,
        bookmarkDataIsStale: &isStale
    )
    guard url.startAccessingSecurityScopedResource() else {
        return nil  // extension failed to start — treat as access denied, re-prompt via picker
    }
    if isStale {
        // Refresh: re-create the bookmark from `url` and persist it, but the current
        // access grant from startAccessingSecurityScopedResource() above is still valid.
    }
    return url
}
```

### 6.4 Stop Access

```swift
defer { url.stopAccessingSecurityScopedResource() }
```

- **The access-count pitfall**: `startAccessingSecurityScopedResource()`/`stopAccessingSecurityScopedResource()` calls are reference-counted per URL instance, not globally per path. Calling `start` twice on two separate `URL` instances resolved from the same bookmark, then `stop` once, leaves one grant open — but calling `stop` without a matching `start` on the *same instance* is a silent no-op, not an error. Always pair `start`/`stop` 1:1 on the exact `URL` value in scope, and prefer a `defer` immediately after a successful `start` so the pairing cannot be skipped by an early return.
- Do not call `start`/`stop` around every file operation in a tight loop — resolve once, hold the access for the duration of the logical operation (e.g. the whole document session), then stop.

### 6.5 Staleness Handling

- `bookmarkDataIsStale` becomes `true` when the underlying file moved/renamed since the bookmark was created but the system could still relocate it (rename-tracking succeeded, the recorded path is now out of date).
- On `isStale == true`: re-create the bookmark from the resolved `url` and overwrite the persisted `Data` — the resolve+access call that produced the stale flag still succeeded, so this is a background refresh, not a failure path.
- Resolution failure (thrown error, not just `isStale`) means the file was deleted, is on unmounted external/network media, or the bookmark is fundamentally invalid — fall back to re-prompting via `NSOpenPanel`.

---

## 7. App Group Containers + Shared UserDefaults

- Entitlement: `com.apple.security.application-groups` (array of group identifiers, e.g. `group.com.example.myapp`).
- Grants a shared container directory (`FileManager.default.containerURL(forSecurityApplicationGroupIdentifier:)`) reachable by every sandboxed process (main app, XPC services, extensions) in the same group — the standard channel for sharing files or a SQLite store between an app and its helper.
- Shared preferences: `UserDefaults(suiteName: "group.com.example.myapp")` reads/writes a preferences domain scoped to the group rather than the individual bundle ID — use this instead of `com.apple.security.temporary-exception.shared-preference.read-write` when both processes are yours.
- App groups are the standard IPC substrate feeding XPC services and `SMAppService` helpers — see `reference/xpc-helpers.md` § app-group-backed communication.

---

## 8. TCC-Protected Resources and Purpose Strings

TCC (Transparency, Consent, and Control) prompts are a layer *on top of* sandbox entitlements — an entitlement grants the sandbox extension category; the Info.plist usage-description string is what triggers and populates the user-facing consent dialog. Both are required together for camera/microphone/contacts/calendar/location.

| Resource | Info.plist key | Notes |
|---|---|---|
| Camera | `NSCameraUsageDescription` | |
| Microphone | `NSMicrophoneUsageDescription` | |
| Contacts | `NSContactsUsageDescription` | |
| Calendars (full) | `NSCalendarsFullAccessUsageDescription` | macOS 14+ split; replaces the pre-14 `NSCalendarsUsageDescription` for full read/write |
| Calendars (write-only) | `NSCalendarsWriteOnlyAccessUsageDescription` | macOS 14+ — for apps that only create events, not read the calendar |
| Reminders (full) | `NSRemindersFullAccessUsageDescription` | Same macOS 14+ split pattern as Calendars |
| Location | `NSLocationUsageDescription` | Mac uses the single unified key, unlike iOS's when-in-use/always split |
| Photos library (read) | `NSPhotoLibraryUsageDescription` | Pairs with `personal-information.photos-library` entitlement |
| Photos library (add-only) | `NSPhotoLibraryAddUsageDescription` | |
| Apple Events (per target) | `NSAppleEventsUsageDescription` | Prompted per target app the first time a script sends it an event |
| Speech recognition | `NSSpeechRecognitionUsageDescription` | |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` | |
| System administration | `NSSystemAdministrationUsageDescription` | Rare — privileged-tool-adjacent flows |
| Desktop folder (non-sandboxed) | `NSDesktopFolderUsageDescription` | Only relevant for TCC on *non-sandboxed* apps reading `~/Desktop` directly |
| Documents folder (non-sandboxed) | `NSDocumentsFolderUsageDescription` | Same caveat as above |
| Downloads folder (non-sandboxed) | `NSDownloadsFolderUsageDescription` | Same caveat as above |
| Network volumes | `NSNetworkVolumesUsageDescription` | |
| Removable volumes | `NSRemovableVolumesUsageDescription` | |

### 8.1 Mac-Specific TCC Categories with NO Programmatic Prompt

These cannot be requested via an Info.plist key or an API call that raises a system dialog. The app can only detect status and *direct the user* to System Settings → Privacy & Security to grant manually:

| Category | Detection API | Notes |
|---|---|---|
| Full Disk Access | No direct check API; probe by attempting a known-protected read (e.g. `~/Library/Mail`) and catching the failure | Deep-link: `x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles` |
| Accessibility | `AXIsProcessTrusted()` / `AXIsProcessTrustedWithOptions([kAXTrustedCheckOptionPrompt: true])` | The `WithOptions` prompt variant *does* open System Settings (not an in-app consent dialog) — still requires manual user action there |
| Screen Recording | `CGPreflightScreenCaptureAccess()` (check) / `CGRequestScreenCaptureAccess()` (opens System Settings, does not itself grant) | Newly-added apps require a **relaunch** after the user grants — first launch after grant still sees `false` |
| Input Monitoring | `IOHIDCheckAccess(kIOHIDRequestTypeListenEvent)` | Global keyboard/mouse event taps |

Design implication: any feature depending on these four must ship a clear in-app explanation *before* deep-linking to System Settings — there is no way to fold the ask into a native consent sheet.

---

## 9. Hardened Runtime vs. App Sandbox — Distinct Systems

These are two independent Apple security systems that both live in the same `.entitlements` file and get confused constantly:

| | App Sandbox | Hardened Runtime |
|---|---|---|
| Purpose | Confines the app's *filesystem/device/IPC reach* — what resources it can touch | Confines the app's *process/memory integrity* — what code can run inside it |
| Entitlement prefix | `com.apple.security.<category>` (e.g. `files.user-selected.read-only`) | `com.apple.security.cs.<capability>` and `com.apple.security.get-task-allow` |
| Enable flag | `com.apple.security.app-sandbox = true` | Set via `codesign --options runtime` (build setting: Hardened Runtime capability) — no single boolean entitlement key |
| Mandatory for | Mac App Store | Notarization (any Developer ID distribution) |
| Can both be on? | Yes — most shipping apps run sandboxed *and* hardened | Yes — this is the common case |
| Can Hardened Runtime be on without Sandbox? | N/A (independent) | Yes — Developer ID apps are commonly hardened but not sandboxed |
| Full catalog | This file | `reference/distribution.md` § 3 (hardened runtime entitlements + `codesign` flow) |

A `com.apple.security.cs.*` key with `app-sandbox` absent or `false` is completely valid and common for Developer ID-only apps that skip the sandbox but still need notarization's hardened-runtime prerequisite.

---

## 10. Sandbox-Incompatible Features

| Feature | Why it breaks under Sandbox | Workaround |
|---|---|---|
| Arbitrary path filesystem access (e.g. scanning `/Users/*/Library`) | No entitlement grants unrestricted filesystem walk | Scope to what the user explicitly picks; for legitimate system-wide tools, ship Developer ID *without* sandbox instead |
| Global keyboard/mouse hooks (`CGEventTap` system-wide) | Input Monitoring is a TCC gate, not a sandbox-grantable entitlement, and sandboxed apps additionally cannot install truly global taps in most configurations | Ship as Developer ID, unsandboxed, with Input Monitoring TCC approval |
| Shell-out to arbitrary system binaries (`Process()` launching non-bundled tools) | Sandbox blocks exec of unentitled external paths in the general case | Bundle the tool inside the app, or use `files.user-selected.executable` for a user-picked binary |
| Loading unsigned/third-party plug-ins | Sandbox + hardened runtime library validation both resist this by default | `com.apple.security.cs.disable-library-validation` (hardened runtime, not sandbox) — see `reference/distribution.md` |
| Direct `/dev` or low-level IOKit access outside declared device categories | Sandbox restricts IOKit user-client connections to declared categories (camera/USB/Bluetooth) | Move the driver-adjacent logic into a System Extension / DriverKit component (out of Native's macOS scope — pointer only) |
| Modifying another app's preferences/files directly | Sandbox container isolation | App Groups (§ 7) if both are yours; `temporary-exception.shared-preference.read-write` (§ 4) only as a stopgap |
| Full-volume backup/sync tools (Time Machine-style) | Needs Full Disk Access, which is TCC-gated with no sandbox entitlement equivalent | Developer ID unsandboxed + Full Disk Access TCC grant + clear onboarding UX (§ 8.1) |

---

## Sources

- [App Sandbox | Apple Developer Documentation](https://developer.apple.com/documentation/security/app-sandbox) (accessed 2026-07)
- [Security entitlements | Apple Developer Documentation](https://developer.apple.com/documentation/bundleresources/security-entitlements) (accessed 2026-07)
- [Enabling App Sandbox — Entitlement Key Reference (archive)](https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/EnablingAppSandbox.html)
- [App Sandbox Temporary Exception Entitlements (archive)](https://developer.apple.com/library/archive/documentation/Miscellaneous/Reference/EntitlementKeyReference/Chapters/AppSandboxTemporaryExceptionEntitlements.html)
- [NSCalendarsFullAccessUsageDescription | Apple Developer Documentation](https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarsfullaccessusagedescription)
- [NSCalendarsWriteOnlyAccessUsageDescription | Apple Developer Documentation](https://developer.apple.com/documentation/bundleresources/information-property-list/nscalendarswriteonlyaccessusagedescription)
- [Hardened Runtime | Apple Developer Documentation](https://developer.apple.com/documentation/security/hardened-runtime) (accessed 2026-07)
- [Configuring the hardened runtime | Apple Developer Documentation](https://developer.apple.com/documentation/xcode/configuring-the-hardened-runtime)
- WWDC — "What's new in privacy" / "Explore App Sandbox and TCC" sessions (Apple Developer video library, cross-reference current-year session for macOS 14+ Calendar/Reminders split)
- Cross-reference: `reference/distribution.md` (hardened runtime + notarization flow), `reference/macos-xcrun-cli.md` (`codesign --entitlements` inspection), `reference/xpc-helpers.md` (app-group-backed IPC)
