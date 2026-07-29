# XPC, Helper Tools, and Background Components

Production reference for privilege separation and background execution on macOS: in-bundle XPC services, the modern `SMAppService` registration API, Login Items UX, privileged-helper lifecycle, and the surviving `launchd` plist keys. Companion to `reference/sandbox-entitlements.md` § 7 (app-group containers, the usual IPC substrate feeding these) and `reference/distribution.md` (signing order for embedded XPC services).

> Scope: XPC services, `SMAppService`-registered agents/daemons/login items, and the decision of where code should run. Endpoint Security / System Extensions are named only as a boundary (§ 6) — full design is out of Native's macOS scope.

---

## 1. XPC Services (In-Bundle, `NSXPCConnection`)

An in-bundle XPC service is a `.xpc` bundle inside `Contents/XPCServices/` of the host app, launched on-demand by `launchd` and torn down when idle. It runs as the **same user** as the host app (no privilege elevation) — its value is process isolation (crash containment, sandboxing a risky dependency) rather than running as root.

### 1.1 Service Side

```swift
// HelperService.swift — the exported object
@objc protocol HelperServiceProtocol {
    func processFile(at path: String, reply: @escaping (Bool) -> Void)
}

final class HelperService: NSObject, HelperServiceProtocol, NSXPCListenerDelegate {
    func listener(_ listener: NSXPCListener, shouldAcceptNewConnection newConnection: NSXPCConnection) -> Bool {
        newConnection.exportedInterface = NSXPCInterface(with: HelperServiceProtocol.self)
        newConnection.exportedObject = self
        newConnection.resume()
        return true
    }

    func processFile(at path: String, reply: @escaping (Bool) -> Void) {
        reply(FileManager.default.fileExists(atPath: path))
    }
}

let delegate = HelperService()
let listener = NSXPCListener.service()
listener.delegate = delegate
listener.resume()
```

### 1.2 Host Side

```swift
let connection = NSXPCConnection(serviceName: "com.example.myapp.HelperService")
connection.remoteObjectInterface = NSXPCInterface(with: HelperServiceProtocol.self)
connection.resume()

let proxy = connection.remoteObjectProxyWithErrorHandler { error in
    print("XPC error: \(error)")
} as? HelperServiceProtocol

proxy?.processFile(at: "/path/to/file") { exists in
    print("exists: \(exists)")
}
```

### 1.3 `NSXPCInterface` Allowed Classes

Any method argument or reply parameter that is a collection or custom object must be declared via `setClasses(_:for:argumentIndex:ofReply:)` — XPC's `NSSecureCoding` boundary rejects undeclared classes at runtime rather than at compile time:

```swift
let interface = NSXPCInterface(with: HelperServiceProtocol.self)
interface.setClasses(
    NSSet(array: [NSArray.self, NSString.self, NSDictionary.self]) as! Set<AnyHashable>,
    for: #selector(HelperServiceProtocol.processManifest(_:reply:)),
    argumentIndex: 0,
    ofReply: false
)
```

Prefer primitive types (`String`, `Data`, `Bool`, `Int`) or `Codable` structs serialized to `Data` over the class-declaration dance where the protocol surface allows it — it sidesteps this entire category of runtime failure.

### 1.4 Codesigning-Requirement Peer Validation

An XPC service should not blindly trust whatever process connected to it. Pin the expected peer's code-signing identity:

```swift
let requirement = "identifier \"com.example.myapp\" and anchor apple generic and certificate leaf[subject.OU] = \"TEAMID1234\""
do {
    try connection.setCodeSigningRequirement(requirement)
} catch {
    connection.invalidate()
}
```

- `setCodeSigningRequirement(_:)` (Foundation, `NSXPCConnection`) validates the *peer's* signature against the requirement string — call it before `resume()`/trusting any incoming call.
- For an in-bundle service reached only via `NSXPCListener.service()`, `launchd` already guarantees only the host app bundle can spin it up, but explicit peer validation remains defense-in-depth against connection-hijacking scenarios and is required practice for any privileged helper (§ 4).

---

## 2. Modern Swift XPC — `XPCSession` / `XPCListener`

macOS 14+ (Sonoma) introduced a Swift-native XPC API as an alternative to `NSXPCConnection`'s Objective-C-interface-protocol pattern — message-based rather than proxy-based, with `Codable` payloads.

```swift
// Listener side (macOS 14+)
let listener = try XPCListener(service: "com.example.myapp.HelperService") { request in
    request.accept { message in
        let payload: String = try message.decode()
        return XPCReceivedMessage.from(reply: "processed: \(payload)")
    }
}

// Session side (macOS 14+)
let session = try XPCSession(xpcService: "com.example.myapp.HelperService")
let reply = try await session.send(message: "hello")
let text: String = try reply.decode()
```

- Where available (host and helper both targeting macOS 14+), this is generally the more ergonomic path for new code — no `@objc` protocol, no `NSXPCInterface` class-allowlisting.
- `NSXPCConnection` remains necessary when the codebase has a Objective-C-bridged protocol surface already, targets pre-14 macOS, or needs the proxy-object calling convention some existing code depends on.
- `(unverified)` — confirm exact `XPCListener`/`XPCSession` initializer signatures against the Swift/Foundation version actually pinned in the project; the API surface has continued to evolve since introduction.

---

## 3. `SMAppService` — Agent/Daemon/Login-Item Registration

`SMAppService` (macOS 13+) replaces `SMJobBless` and manual `launchctl load` for registering background components. All four registration types are managed through one API surface.

| Type | Registers | Runs as |
|---|---|---|
| `.agent(plistName:)` | A LaunchAgent | The logged-in user |
| `.daemon(plistName:)` | A LaunchDaemon | root (requires user authentication at registration) |
| `.loginItem(identifier:)` | A login item (helper `.app` launched at login, no daemon/agent plist) | The logged-in user |
| `.mainApp` | The host app itself, as a login item | The logged-in user |

```swift
// Main app as a login item
try SMAppService.mainApp.register()
try SMAppService.mainApp.unregister()
let status = SMAppService.mainApp.status  // .notRegistered / .enabled / .requiresApproval / .notFound

// A bundled LaunchAgent
let agent = SMAppService.agent(plistName: "com.example.myapp.agent.plist")
try agent.register()
try agent.unregister()
```

### 3.1 Bundled-Plist Layout (Replaces `SMJobBless`/`launchctl load`)

Agent/daemon plists ship **inside the app bundle**, not written to `/Library/LaunchAgents` or `/Library/LaunchDaemons` by an installer script:

```
MyApp.app/
└── Contents/
    ├── MacOS/MyApp
    ├── Library/
    │   ├── LaunchAgents/com.example.myapp.agent.plist
    │   └── LaunchDaemons/com.example.myapp.daemon.plist
    └── ...
```

`SMAppService` reads the plist from this in-bundle location at `register()` time and handles the system-side install/move itself — the app never manually copies plists into `/Library/Launch*` or shells out to `launchctl load`. This is the core replacement behavior: `SMJobBless`-era code that wrote `/Library/PrivilegedHelperTools/` and `/Library/LaunchDaemons/` by hand is legacy.

### 3.2 Status and Approval

```swift
switch SMAppService.mainApp.status {
case .notRegistered: // never registered
case .enabled:       // registered and running
case .requiresApproval: // registered, but user must approve in System Settings → Login Items
case .notFound:       // (daemon/agent) plist missing or malformed
@unknown default: break
}
```

- `.requiresApproval` is the common post-`register()` state on first run — the call succeeds, but the user must flip the toggle in **System Settings → General → Login Items & Extensions** before the component actually launches. Direct the user there (no programmatic bypass): `SMAppService.openSystemSettingsLoginItems()`.
- Daemon registration additionally triggers a Touch ID/password authentication prompt (installing a LaunchDaemon requires root).

### 3.3 Helper Install / Update / Uninstall Lifecycle

- **Install**: bundle the plist (§ 3.1), call `register()` at first launch or on-demand when the feature needing the helper is first used (don't force it at every app launch if the feature is optional).
- **Update**: because the plist and the helper binary both live inside the app bundle, a normal app update (new `.app` on disk) *is* the helper update — there is no separate helper-versioning install step the way `SMJobBless`-era privileged helpers in `/Library/PrivilegedHelperTools/` required. `launchd` picks up the new binary the next time the agent/daemon is (re)launched.
- **Uninstall**: call `unregister()` before the app is deleted if a clean teardown matters (stops the agent/daemon and removes its "known" status); if the user simply drags the `.app` to Trash without unregistering first, `launchd`/`SMAppService` reconcile against the missing bundle over time, but explicit `unregister()` on an in-app "Quit and Remove Helper" flow is the better UX.
- **Versioning**: no separate version negotiation API — if the helper's IPC protocol changes, version-tag messages yourself (e.g. an XPC handshake exchanging a protocol version before real work) so an old-helper/new-app or new-helper/old-app mismatch fails cleanly rather than silently misbehaving.

---

## 4. Login Items UX and User-Approval Behavior

- Registering via `SMAppService` (any type) surfaces the component in **System Settings → General → Login Items & Extensions**, listed under the *host app's* name — users see and control it there, not buried in a separate installer-managed location.
- First-registration commonly lands in `.requiresApproval` (§ 3.2) — design onboarding UX that (a) explains why the toggle exists before triggering it, and (b) deep-links to System Settings rather than assuming the user finds it unprompted.
- Users can disable a login item directly in System Settings without going through the app — the app must therefore poll or re-check `.status` on launch/resume rather than assuming a registered state stays enabled forever.

---

## 5. `launchd` Plist Keys That Still Matter

Even though `SMAppService` owns install-location and registration mechanics, the plist content itself still follows classic `launchd.plist` schema:

| Key | Purpose | Notes |
|---|---|---|
| `Label` | Unique reverse-DNS identifier for the job | Must match the plist filename convention and the identifier passed to `SMAppService.agent(plistName:)` |
| `RunAtLoad` | Launch immediately on registration/login, rather than waiting for `MachServices`-triggered activation | Set for agents that must be always-running vs. on-demand XPC services |
| `KeepAlive` | Relaunch the job if it exits | Can be a bool or a dict (`SuccessfulExit`, `Crashed`, etc.) for conditional relaunch policy |
| `MachServices` | Advertises a Mach service name the job listens on, enabling on-demand launch when a client connects | Standard for XPC-style on-demand agents/daemons rather than `RunAtLoad` long-runners |
| `ProcessType` | Scheduling hint to the kernel (`Background`, `Standard`, `Adaptive`, `Interactive`) | `Background` for low-priority housekeeping agents avoids competing with foreground app responsiveness |
| `ProgramArguments` | Executable path + args | Path resolves inside the app bundle for `SMAppService`-registered jobs |
| `StandardOutPath` / `StandardErrorPath` | Redirect stdout/stderr for debugging | Avoid leaving these pointed at world-writable paths in shipped daemons |

---

## 6. Endpoint Security / System Extensions — Pointer Only (Out of Scope)

Endpoint Security (`EndpointSecurity.framework`, kernel-adjacent event monitoring) and System Extensions (network filters, DriverKit, the extension categories that replace kernel extensions) are a materially different architecture — separate entitlements (`com.apple.developer.endpoint-security.client`), separate approval flow (`OSSystemExtensionManager`, user approval in System Settings → Privacy & Security → Extensions), and typically require a dedicated Apple entitlement grant request beyond standard Developer Program enrollment. This is named here only as a boundary: if a feature needs kernel-level event visibility or a network content filter, that is a distinct design track outside standard XPC/`SMAppService` helper patterns — do not improvise it as "just another XPC service."

---

## 7. Debugging XPC

| Technique | Command / API |
|---|---|
| Stream unified log for the service | `log stream --predicate 'subsystem == "com.example.myapp.HelperService"'` (or process/sender-based predicate if the service doesn't emit its own subsystem) |
| Inspect connection-invalidation causes | Implement `NSXPCConnection.invalidationHandler` and `interruptionHandler` — invalidation fires on unrecoverable failure (peer crashed, codesigning-requirement rejection, service unregistered), interruption fires on a recoverable drop (peer restarted) that can be retried with a fresh connection |
| Common invalidation causes | Peer process crashed; `setCodeSigningRequirement` check failed; the `.xpc` bundle's `Info.plist` `CFBundleIdentifier` doesn't match the `serviceName` requested; sandbox denies the Mach lookup (missing `application-groups` or `temporary-exception.mach-lookup.global-name`) |
| List running XPC-launched jobs | `launchctl list \| grep <label-prefix>` |
| Inspect a registered `SMAppService` job's plist as installed | `launchctl print gui/$(id -u)/<Label>` |

---

## 8. Decision Table — In-Process vs. XPC Service vs. Launch Agent vs. Daemon

| Need | Choice |
|---|---|
| Isolate a risky/crash-prone dependency (parser, codec, third-party lib) without privilege change | In-bundle XPC service (§ 1–2) |
| Run a sandboxed self-updater's download/install steps (Sparkle) | In-bundle XPC service, per `reference/distribution.md` § 7 |
| Background task that should keep running while the app itself may not be | `SMAppService.agent` (LaunchAgent) — user-level, no elevation |
| Task requiring root (system-level file access, privileged installs, low-level device control) | `SMAppService.daemon` (LaunchDaemon) — expect an auth prompt at registration |
| "Launch my app automatically at login" | `SMAppService.mainApp` — simplest case, no separate plist/binary |
| Menu-bar-only helper the user expects to see toggle in Login Items | `SMAppService.loginItem` (separate helper `.app`) or `.mainApp` if the helper *is* the whole app |
| No isolation/privilege need, just calling a function | Stay in-process — XPC has real IPC latency/complexity cost; do not reach for it by default |
| Kernel-level monitoring or network content filtering | Out of scope (§ 6) — Endpoint Security / System Extension design track, not a helper-tool decision |

---

## Sources

- [Service Management | Apple Developer Documentation](https://developer.apple.com/documentation/servicemanagement) (accessed 2026-07)
- [SMAppService | Apple Developer Documentation](https://developer.apple.com/documentation/servicemanagement/smappservice)
- [NSXPCConnection | Apple Developer Documentation](https://developer.apple.com/documentation/foundation/nsxpcconnection)
- [NSXPCInterface | Apple Developer Documentation](https://developer.apple.com/documentation/foundation/nsxpcinterface)
- [setCodeSigningRequirement(_:) | Apple Developer Documentation](https://developer.apple.com/documentation/foundation/nsxpcconnection/3943309-setcodesigningrequirement)
- [XPC | Apple Developer Documentation](https://developer.apple.com/documentation/xpc) — modern `XPCSession`/`XPCListener` Swift API, macOS 14+ (verify exact initializer signatures against pinned SDK)
- [Endpoint Security | Apple Developer Documentation](https://developer.apple.com/documentation/endpointsecurity) — boundary reference only, § 6
- [About System Extensions | Apple Developer Documentation](https://developer.apple.com/documentation/systemextensions)
- WWDC — "Meet Service Management for launchd" (SMAppService introduction) / "What's new in XPC" (modern XPCSession/XPCListener) — Apple Developer video library, cross-reference the session for the macOS version pinned in the project
- Cross-reference: `reference/sandbox-entitlements.md` § 7 (app-group containers as IPC substrate), `reference/distribution.md` § 4 (deep-signing order covering embedded XPC services), `reference/macos-xcrun-cli.md` (`codesign -dv --entitlements -` for inspecting a shipped `.xpc` bundle)
