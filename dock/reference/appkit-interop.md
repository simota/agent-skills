# SwiftUI ↔ AppKit Interop

**Purpose:** `NSViewRepresentable`/`NSViewControllerRepresentable` full lifecycle, Coordinator pattern, `NSHostingView`/`NSHostingController` for the reverse direction, backing-`NSWindow` access, `@NSApplicationDelegateAdaptor` and delegate hooks SwiftUI lacks, first-responder/focus bridging, decision table for common Mac controls, retain-cycle/update-loop pitfalls, performance notes.
**Read when:** Bridging AppKit into SwiftUI or vice versa (`appkit` Recipe).

---

## 1. `NSViewRepresentable` — Full Lifecycle

```swift
struct WrappedTextView: NSViewRepresentable {
    @Binding var text: String

    func makeNSView(context: Context) -> NSTextView {
        let textView = NSTextView()
        textView.delegate = context.coordinator
        textView.string = text
        textView.isRichText = false
        textView.font = .systemFont(ofSize: 13)
        return textView
    }

    func updateNSView(_ nsView: NSTextView, context: Context) {
        // Guard against feedback loops: only write when the value actually diverged.
        if nsView.string != text {
            nsView.string = text
        }
    }

    static func dismantleNSView(_ nsView: NSTextView, coordinator: Coordinator) {
        nsView.delegate = nil   // break the delegate reference before teardown
    }

    func sizeThatFits(_ proposal: ProposedViewSize, nsView: NSTextView, context: Context) -> CGSize? {
        // Return nil to defer to nsView's intrinsicContentSize / Auto Layout.
        guard let width = proposal.width else { return nil }
        let size = nsView.sizeThatFits(NSSize(width: width, height: .greatestFiniteMagnitude))
        return CGSize(width: width, height: size.height)
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    final class Coordinator: NSObject, NSTextViewDelegate {
        var parent: WrappedTextView
        init(_ parent: WrappedTextView) { self.parent = parent }

        func textDidChange(_ notification: Notification) {
            guard let textView = notification.object as? NSTextView else { return }
            parent.text = textView.string
        }
    }
}
```

| Method | Called | Responsibility |
|---|---|---|
| `makeNSView(context:)` | Once, on first appearance | Construct the view, wire the Coordinator as delegate/target |
| `updateNSView(_:context:)` | On every SwiftUI state change touching the representable's inputs | Push new values in; **must** guard against re-triggering the delegate callback that feeds back into SwiftUI state (infinite update loop) |
| `dismantleNSView(_:coordinator:)` | Once, on removal from the hierarchy | Break delegate/target-action references, invalidate timers/observers |
| `sizeThatFits(_:nsView:context:)` | During SwiftUI layout, when the representable participates in SwiftUI's layout protocol (macOS 13+) | Report intrinsic size back to SwiftUI; return `nil` to let Auto Layout / `intrinsicContentSize` decide |

`NSViewControllerRepresentable` mirrors this exactly with `makeNSViewController`/`updateNSViewController`/`dismantleNSViewController` — use it when the AppKit side is naturally a controller (owns a full `NSViewController` lifecycle, `viewDidLoad`, child-VC composition) rather than a standalone view.

---

## 2. Coordinator Pattern

The `Coordinator` is the delegate/target-action bridge — AppKit's delegate protocols and target-action expect a Cocoa object, not a SwiftUI `View` struct (which is a value type re-created every render). Rules:

- Coordinator owns a **weak-free** reference back to `parent` only if `parent` is a struct copy captured at `makeCoordinator()` time — update it via `updateNSView`'s `context.coordinator.parent = self` if the Coordinator needs the *current* representable, not the one at creation time.
- Never let the Coordinator hold a strong reference to the `NSView` itself if the view also strong-references the Coordinator as delegate — that specific pair is fine (both are reference types with a normal delegate pattern, not a cycle SwiftUI needs to break), but avoid adding a third strong link (e.g. a Combine subscription capturing both) that outlives `dismantleNSView`.
- One Coordinator per representable instance — do not share a Coordinator across multiple `makeNSView` calls.

---

## 3. `NSHostingView` / `NSHostingController` — the Reverse Direction

For embedding SwiftUI inside an AppKit-hosted app (menu bar item content, a panel in an otherwise-AppKit app, incremental SwiftUI migration):

```swift
let hostingController = NSHostingController(rootView: SettingsPane())
hostingController.sizingOptions = [.preferredContentSize]   // NSHostingSizingOptions — auto-updates preferredContentSize from SwiftUI's ideal size
window.contentViewController = hostingController
```

```swift
// Lower-level: NSHostingView directly inside a manually-constructed NSView hierarchy
let hostingView = NSHostingView(rootView: SidebarContent())
hostingView.frame = containerView.bounds
hostingView.autoresizingMask = [.width, .height]
containerView.addSubview(hostingView)
```

`NSHostingSizingOptions` (macOS 13+) controls how the hosting controller reflects SwiftUI's ideal content size into Auto Layout / `preferredContentSize`:

The type has exactly three members — there is no `.standardBounds` and no `.minSize`:

| Option | Effect |
|---|---|
| `.intrinsicContentSize` | Publishes an `intrinsicContentSize` driven by SwiftUI content — lets Auto Layout size the hosting view |
| `.maxSize` | Reflects SwiftUI's maximum size into the hosting view's layout |
| `.preferredContentSize` | Updates `NSViewController.preferredContentSize` — useful when the hosting controller sits inside a popover/sheet that sizes to content |

Choose `.intrinsicContentSize` when the hosting view lives inside an Auto Layout-managed AppKit hierarchy; `.preferredContentSize` when it's the content of an `NSPopover` or a sheet that should shrink-to-fit.

---

## 4. Accessing the Backing `NSWindow` from SwiftUI

SwiftUI views don't have direct `NSWindow` access. Bridge via a zero-size `NSViewRepresentable` that reads `view.window` once inserted into the hierarchy:

```swift
struct WindowAccessor: NSViewRepresentable {
    let onWindow: (NSWindow?) -> Void

    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async { onWindow(view.window) }   // window is nil at makeNSView time; defer
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {}
}

struct ContentView: View {
    var body: some View {
        MainContent()
            .background(WindowAccessor { window in
                window?.titlebarAppearsTransparent = true
            })
    }
}
```

The `view.window` reference is `nil` during `makeNSView` (the view isn't yet inserted into a window's view hierarchy) — always read it on the next run-loop turn via `DispatchQueue.main.async` or in `updateNSView` where it is reliably non-nil after first layout.

---

## 5. `@NSApplicationDelegateAdaptor` and Delegate Hooks SwiftUI Lacks

```swift
@main
struct MyApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {
        WindowGroup { ContentView() }
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDockMenu(_ sender: NSApplication) -> NSMenu? {
        let menu = NSMenu()
        menu.addItem(withTitle: "New Note", action: #selector(newNote), keyEquivalent: "")
        return menu
    }

    func application(_ application: NSApplication, open urls: [URL]) {
        // Finder "Open With" / double-click on a registered document type when
        // DocumentGroup's own routing isn't in play (e.g. non-document URL schemes)
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        false   // menu-bar-only or document apps typically want `false`
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        true    // Dock-icon click with no visible windows: reopen last window
    }

    @objc private func newNote() { /* ... */ }
}
```

SwiftUI's `Scene`/`App` API has no equivalent for: Dock menu customization, `applicationShouldTerminateAfterLastWindowClosed`, reopen-on-Dock-click, and raw `open urls:`/Apple Event handling outside `DocumentGroup`'s own type-routed opening. `@NSApplicationDelegateAdaptor` is the sanctioned bridge — do not fight SwiftUI's app lifecycle with a parallel `NSApplicationMain` entry point.

---

## 6. First-Responder / Focus Bridging

- SwiftUI's `@FocusState` and AppKit's first-responder chain (`NSWindow.firstResponder`) are **separate systems** that do not automatically sync when an `NSViewRepresentable` is in play.
- To make an AppKit-hosted `NSTextView` participate in SwiftUI's focus system, drive `becomeFirstResponder()`/`resignFirstResponder()` from `updateNSView` in response to a `@FocusState` binding:

```swift
func updateNSView(_ nsView: NSTextView, context: Context) {
    if isFocused, nsView.window?.firstResponder !== nsView {
        nsView.window?.makeFirstResponder(nsView)
    }
}
```

- Conversely, to report AppKit-side focus changes back into SwiftUI, implement `NSTextViewDelegate.textDidBeginEditing`/`textDidEndEditing` in the Coordinator and mutate the bound `@FocusState` (via a `Binding<Bool>` passed into the representable).

---

## 7. Decision Table — SwiftUI-Native vs Must-Drop-to-AppKit

| Control | SwiftUI-native? | Notes |
|---|---|---|
| Rich text editing (attributed strings, custom text attachments) | No — `NSViewRepresentable(NSTextView)` | `TextEditor` (macOS 12+) covers plain-text-only editing; `AttributedString` in `TextEditor` (macOS 14+) covers basic formatting but not custom `NSTextAttachment`/layout managers |
| Outline view (`NSOutlineView`) with disclosure, drag-reorder, custom row views | Partial — `List` + `DisclosureGroup` covers most cases | Drop to `NSOutlineView` only for column-based outlines or `NSOutlineViewDataSource`-driven virtualized trees beyond `List`'s scale |
| Split view with custom divider styling/behavior | Yes | `NavigationSplitView`/`HSplitView` cover standard cases; drop to `NSSplitViewController` only for custom divider hit-testing or collapse animations SwiftUI doesn't expose |
| Toolbar with fully custom `NSToolbarItem` (e.g. `NSSearchToolbarItem`, custom `NSView`-backed items with nonstandard sizing behavior) | Partial | SwiftUI `.toolbar` covers `ToolbarItem`/`ToolbarItemGroup` with SwiftUI content; drop to `NSToolbar`/`NSToolbarDelegate` for items requiring AppKit-only toolbar item classes |
| Sheets / panels (`NSSavePanel`, `NSOpenPanel`, custom accessory views) | Partial | `.fileImporter`/`.fileExporter` cover the common case; custom accessory views on the panel require AppKit `NSOpenPanel` directly (see `reference/documents.md` § 4) |
| Standard table (`List` with columns) | Yes | `Table` (macOS 12+) covers sortable multi-column data; drop to `NSTableView` only for cell-based (not row-based) rendering or `NSTableViewDataSource` virtualization at very large row counts |
| Color/font pickers | Yes | `ColorPicker`, `.font` environment cover standard cases; `NSFontPanel`/`NSColorPanel` still needed for full system panel parity in professional creative apps |
| Popovers with custom sizing behavior | Yes | `.popover()` covers most cases; `NSPopover` directly only when `NSHostingSizingOptions.preferredContentSize` isn't sufficient control |

Default to the SwiftUI-native column; treat "Partial"/"No" rows as the explicit trigger for `NSViewRepresentable`.

---

## 8. Retain-Cycle and Update-Loop Pitfalls

- **Update loop**: `updateNSView` writing back into a `@Binding` unconditionally, which SwiftUI re-renders, which calls `updateNSView` again — always diff before writing (see § 1's `if nsView.string != text` guard).
- **Retain cycle**: Coordinator closures capturing `self` (the representable struct) strongly are fine (structs don't retain-cycle), but Coordinator closures capturing the `NSView`/`NSViewController` *and* being retained *by* that same view (e.g. stored as an `objc_setAssociatedObject`) can leak if not cleared in `dismantleNSView`.
- **Timer/observer leaks**: any `Timer`, `NotificationCenter` observer, or Combine `AnyCancellable` created in `makeNSView`/`makeCoordinator` must be invalidated/cancelled in `dismantleNSView` — SwiftUI does not automatically tear these down.
- **Delegate double-wiring**: re-assigning `nsView.delegate = context.coordinator` inside `updateNSView` on every call is harmless but wasteful; assign once in `makeNSView` unless the Coordinator identity can change (it normally can't within one representable's lifetime).

---

## 9. Performance Notes

- `updateNSView`/`updateNSViewController` fire on every SwiftUI state change that invalidates the parent view, not just changes to the representable's own bound values — keep the body of these methods cheap (diff-and-return-early), especially for representables inside frequently-updating containers (e.g. a `List` row).
- `NSHostingView`/`NSHostingController` re-render SwiftUI content through the same diffing engine as any other SwiftUI subtree — embedding a SwiftUI view inside an AppKit hierarchy does not bypass SwiftUI's own performance characteristics (see `native/reference/apple-perf.md` for general SwiftUI render-cost guidance).
- Prefer a single `NSHostingController` boundary over many small ones scattered through an AppKit hierarchy — each hosting boundary has its own SwiftUI environment/update cycle, and excessive fragmentation multiplies diffing overhead without benefit.
- For `NSViewRepresentable`-wrapped scroll/collection views at large item counts, rely on the AppKit view's native virtualization (`NSTableView`/`NSOutlineView`/`NSCollectionView` cell reuse) rather than trying to make SwiftUI reproduce it — this is a primary reason to drop to AppKit in the first place (§ 7).

---

## Cross-References

- Rendering/perf budget details, general SwiftUI render-cost profiling — `native/reference/apple-perf.md`
- Document window controllers (`NSDocument` multi-window fan-out) — `reference/documents.md` § 4
- Custom `NSDraggingSource`/`NSDraggingDestination` views — `reference/drag-drop-services.md` § 4

---

## Sources

- [NSViewRepresentable](https://developer.apple.com/documentation/swiftui/nsviewrepresentable) — Apple Developer Documentation (accessed 2026-07)
- [NSViewControllerRepresentable](https://developer.apple.com/documentation/swiftui/nsviewcontrollerrepresentable) — Apple Developer Documentation
- [NSHostingController](https://developer.apple.com/documentation/swiftui/nshostingcontroller) — Apple Developer Documentation
- [NSHostingSizingOptions](https://developer.apple.com/documentation/swiftui/nshostingsizingoptions) — Apple Developer Documentation
- [NSHostingView](https://developer.apple.com/documentation/swiftui/nshostingview) — Apple Developer Documentation
- [NSApplicationDelegateAdaptor](https://developer.apple.com/documentation/swiftui/nsapplicationdelegateadaptor) — Apple Developer Documentation
- [NSApplicationDelegate](https://developer.apple.com/documentation/appkit/nsapplicationdelegate) — Apple Developer Documentation
- WWDC "Interfacing with UIKit / AppKit" family of sessions — general representable lifecycle reference
