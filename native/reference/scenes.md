# SwiftUI macOS Scene Architecture

**Purpose:** Scene composition for Mac apps — `WindowGroup`, `Window`, `Settings`, `MenuBarExtra`, multi-window identity, state restoration, and the AppKit escape hatch.
**Read when:** Scaffolding a new Mac app's `App` struct, adding a second window type, building a menu-bar-only utility, or wiring window restoration.

---

## 1. Scene Type Decision Table

| Scene | Use for | Instances | Read next |
|-------|---------|-----------|-----------|
| `WindowGroup` | Main document/content window, duplicable by the user (⌘N / Window > New Window) | Many (one per `openWindow` call or Dock menu "New Window") | §2 |
| `WindowGroup(for:)` | Value-identified windows — one window per data item (e.g. one per note, one per project) | Many, keyed by value | §2.1 |
| `Window` | Exactly one instance — a dashboard, a fixed-purpose utility panel | Single, `openWindow(id:)` only re-focuses it | §3 |
| `Settings` | App preferences — always available via ⌘, regardless of which scene has focus | Single, OS-managed | §4 |
| `MenuBarExtra` | Menu-bar-resident app or companion UI, with or without a Dock icon | Single, lives in the menu bar | §5 |
| `DocumentGroup` | File-backed documents (`FileDocument`/`ReferenceFileDocument`, or legacy `NSDocument`) | Many, one per open file | `reference/documents.md` |
| `UtilityWindow` (unverified — no confirmed public SwiftUI scene type as of this writing; use `Window` + `.windowStyle(.hiddenTitleBar)` or an `NSPanel` bridged via `NSViewControllerRepresentable`) | Floating tool palette that stays above the main window | — | §6 |

**When NOT to use `WindowGroup`:** if the app only ever needs one window of a kind (a preferences-like dashboard, a single status monitor), use `Window` — `WindowGroup` implicitly wires up "New Window" duplication that doesn't make sense for a singleton surface.

---

## 2. `WindowGroup`

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .windowResizability(.contentSize)
        .defaultSize(width: 900, height: 600)
        .defaultPosition(.center)
    }
}
```

- `.windowResizability(.contentSize | .contentMinSize | .automatic)` — constrains resize behavior to the root view's intrinsic size. `.contentSize` locks the window to exactly fit content (good for fixed-layout utility windows); `.automatic` (default) lets the system pick.
- `.defaultSize(width:height:)` / `.defaultPosition(_:)` set the first-launch geometry only — subsequent launches restore the user's last size/position unless restoration is disabled.
- `.windowStyle(.automatic | .titleBar | .hiddenTitleBar | .plain)` — `.hiddenTitleBar` gives a borderless-look window that still supports drag/resize; pair with `.toolbar` content for a unified-look chrome per Mac HIG (`reference/mac-hig.md`).

### 2.1 Value-Based Windows — `WindowGroup(for:)`

Register a window group keyed by an `Identifiable`/`Codable` value so each value gets its own window, and re-opening the same value re-focuses the existing window instead of duplicating it.

```swift
WindowGroup("Note", for: Note.ID.self) { $noteID in
    if let noteID {
        NoteDetailView(noteID: noteID)
    } else {
        EmptyNoteView()
    }
}
```

Open one from anywhere in the hierarchy via the `openWindow` environment action:

```swift
struct SidebarRow: View {
    @Environment(\.openWindow) private var openWindow
    let note: Note

    var body: some View {
        Button("Open in New Window") {
            openWindow(value: note.id)
        }
    }
}
```

Close the current window with `dismissWindow`:

```swift
@Environment(\.dismissWindow) private var dismissWindow
// ...
Button("Close", role: .destructive) { dismissWindow() }
```

`openWindow(id:)` targets a `Window`/`WindowGroup` by string ID instead of by value — use it for the fixed-purpose singleton case (§3). `openWindow` is available from macOS 13; `dismissWindow` from macOS 14.

---

## 3. `Window` — Single-Instance Scenes

```swift
Window("Activity Monitor", id: "activity-monitor") {
    ActivityMonitorView()
}
.defaultSize(width: 500, height: 700)
```

Calling `openWindow(id: "activity-monitor")` a second time re-focuses the existing window rather than creating a duplicate — the defining behavior difference from `WindowGroup`.

---

## 4. `Settings` Scene

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
        Settings {
            SettingsView()
        }
    }
}
```

- Always reachable via **App Name > Settings…** (⌘,) regardless of which window has focus — SwiftUI wires the menu item automatically; do not hand-build a `CommandGroup(replacing: .appSettings)` unless replacing this default entirely (see `reference/menu-commands.md` §2 for the full placement table).
- Structure `SettingsView` as a `TabView` with one pane per settings category, per Mac HIG (General / Accounts / Advanced, etc.) — see `reference/mac-hig.md`.
- `Settings` is macOS/visionOS-only; the scene type does not exist on iOS.

---

## 5. `MenuBarExtra`

```swift
@main
struct TimerApp: App {
    var body: some Scene {
        MenuBarExtra("Timer", systemImage: "timer") {
            TimerMenuView()
        }
        .menuBarExtraStyle(.window)
    }
}
```

| Style | Rendering | Fits |
|-------|-----------|------|
| `.menu` (default) | Standard macOS menu — text, `Button`, `Divider`, `Toggle` only; button styles and images are ignored to match native menu chrome | Simple command lists |
| `.window` | Popover-style window from the menu bar icon; full SwiftUI view hierarchy, controls, layout | Rich status/control surfaces (player controls, dashboards) |

For a menu-bar-only app (no Dock icon, no regular window), pair `MenuBarExtra` with an agent-app activation policy — see §7. For a companion menu bar item alongside a normal windowed app, no activation-policy change is needed; the `MenuBarExtra` scene coexists with `WindowGroup`.

---

## 6. `DocumentGroup` (Pointer)

Document-based scenes are fully covered in `reference/documents.md` (`DocumentGroup` + `FileDocument`/`ReferenceFileDocument`, legacy `NSDocument`, autosave-in-place, iCloud sync). Not duplicated here.

---

## 7. Agent / Accessory Apps

An app with no Dock icon and no menu bar of its own (menu-bar-utility, background helper) sets `LSUIElement` in `Info.plist`:

```xml
<key>LSUIElement</key>
<true/>
```

This maps to `NSApplication.ActivationPolicy.accessory` at runtime — no Dock tile, no app menu bar, but the app can still open windows and be activated programmatically or by clicking a window it owns.

| Policy | Dock icon | Menu bar | Can open windows |
|--------|-----------|----------|-------------------|
| `.regular` (default) | Yes | Yes | Yes |
| `.accessory` (`LSUIElement=true`) | No | No | Yes |
| `.prohibited` | No | No | No |

To switch policy at runtime (e.g. an app that starts as menu-bar-only and becomes regular when a window opens):

```swift
NSApp.setActivationPolicy(.regular)
```

---

## 8. State Restoration

| Mechanism | Scope | Use for |
|-----------|-------|---------|
| `@SceneStorage` | Per-window UI state (selected tab, scroll position, sidebar selection) | Small, `Codable`-primitive values tied to one window's lifetime |
| `NSUserActivity` (`.handlesExternalEvents` / `.userActivity(_:)`) | Cross-process handoff and deeper restoration (Handoff, Siri, Spotlight continuation) | Restoring *which document/value* a window was showing, not just UI chrome |

```swift
struct ContentView: View {
    @SceneStorage("selectedSidebarItem") private var selection: String?

    var body: some View {
        NavigationSplitView {
            SidebarView(selection: $selection)
        } detail: {
            DetailView(itemID: selection)
        }
        .userActivity("com.example.notes.viewing") { activity in
            activity.addUserInfoEntries(from: ["noteID": selection ?? ""])
        }
    }
}
```

`WindowGroup(for:)` scenes (§2.1) get value-based restoration for free — the system persists which values had open windows and reopens them on relaunch, without additional `NSUserActivity` wiring, as long as the value type is `Codable`.

`.handlesExternalEvents(matching:)` on a `WindowGroup`/`Window` scene restricts which incoming `NSUserActivity`/URL events that scene instance accepts — pair it with `.onOpenURL` or `.onContinueUserActivity` on the root view to route the payload.

---

## 9. `NSApplicationDelegateAdaptor`

SwiftUI's `App` protocol has no hook for several AppKit lifecycle events (`applicationDidFinishLaunching` timing guarantees, `applicationShouldTerminate` with async work, `NSApplicationDelegate` door/dock-icon-click behavior, custom URL scheme registration edge cases). Bridge in an `NSApplicationDelegate` when one of these is required:

```swift
final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Register global hotkeys, XPC listeners, etc. before the first window shows.
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        false  // menu-bar apps typically want to stay alive with no windows open
    }
}

@main
struct NotesApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}
```

Do not reach for this to replicate things SwiftUI scenes already do (window creation, restoration, `Commands`) — only for delegate callbacks with no SwiftUI equivalent.

---

## 10. AppKit Escape Hatch — Direct `NSWindow` Access

When a SwiftUI modifier doesn't expose a needed `NSWindow` property (custom titlebar accessory view, `NSWindow.collectionBehavior` for Stage Manager/Spaces, window level for always-on-top), reach into AppKit directly rather than fighting SwiftUI:

```swift
struct WindowAccessor: NSViewRepresentable {
    let configure: (NSWindow) -> Void

    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async {
            if let window = view.window { configure(window) }
        }
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {}
}

// Usage: .background(WindowAccessor { $0.collectionBehavior.insert(.canJoinAllSpaces) })
```

Alternatively, enumerate `NSApp.windows` from anywhere (a Commands action, an `NSApplicationDelegate` method) to locate a specific window by title or by an associated `NSHostingController`'s root view type. Prefer the `WindowAccessor`-style targeted bridge over broad `NSApp.windows` scanning where the call site already knows which window it owns.

Full AppKit interop patterns (`NSViewRepresentable`, `NSHostingView`/`NSHostingController`, Coordinator pattern, "when SwiftUI isn't enough" decision criteria) → `reference/appkit-interop.md`. Do not duplicate that content here.

---

## Sources

- [WindowGroup | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/windowgroup) (accessed 2026-07)
- [Window | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/window)
- [MenuBarExtra | Apple Developer Documentation](https://developer.apple.com/documentation/SwiftUI/MenuBarExtra) (accessed 2026-07)
- [Work with windows in SwiftUI — WWDC24 Session 10149](https://developer.apple.com/videos/play/wwdc2024/10149/)
- [NSApplication.ActivationPolicy | Apple Developer Documentation](https://developer.apple.com/documentation/appkit/nsapplication/activationpolicy) — `.regular` / `.accessory` / `.prohibited` (accessed 2026-07)
- [NSApplicationDelegateAdaptor | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/nsapplicationdelegateadaptor)
- [Build a SwiftUI app with the new design — WWDC25 Session 323](https://developer.apple.com/videos/play/wwdc2025/323/) — macOS Tahoe scene/chrome context
- [Scenes types in a SwiftUI Mac app — nilcoalescing.com](https://nilcoalescing.com/blog/ScenesTypesInASwiftUIMacApp/)
