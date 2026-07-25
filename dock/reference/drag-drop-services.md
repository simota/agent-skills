# Drag & Drop, Pasteboard, and Services

**Purpose:** `Transferable` + `.draggable`/`.dropDestination`, `NSItemProvider` bridging, raw `NSPasteboard`, `NSFilePromiseProvider`, `NSDraggingSource`/`NSDraggingDestination` (AppKit path), Copy/Paste + Edit-menu wiring, macOS Services, `NSSharingServicePicker`, Quick Look preview extensions.
**Read when:** Building drag & drop, clipboard, or Services-menu integration (`dragdrop` Recipe).

---

## 1. `Transferable` — SwiftUI-First Path

`Transferable` (introduced WWDC22) is the modern data-interchange protocol backing `.draggable`, `.dropDestination`, `ShareLink`, and system copy/paste in SwiftUI. Prefer it over raw `NSItemProvider`/`NSPasteboard` unless a representation SwiftUI doesn't expose is required (§ 5).

### Conformance styles

| Representation | Use for |
|---|---|
| `ProxyRepresentation` | Delegate to an existing `Transferable`/`Codable` property (e.g. expose a `URL` or `String` view of a richer type) |
| `CodableRepresentation` | Struct/enum data that round-trips through `Codable`, tagged with a `UTType` |
| `FileRepresentation` | On-disk file — exports/imports a `URL`, SwiftUI copies the file itself during drag |
| `DataRepresentation` | Raw `Data` blobs (images, custom binary formats) |

```swift
import CoreTransferable
import UniformTypeIdentifiers

struct Note: Codable, Transferable {
    var title: String
    var body: String

    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .myAppNote)
        ProxyRepresentation(exporting: \.title)   // fallback: plain-text export of just the title
    }
}

struct Attachment: Transferable {
    let fileURL: URL

    static var transferRepresentation: some TransferRepresentation {
        FileRepresentation(exportedContentType: .pdf) { attachment in
            SentTransferredFile(attachment.fileURL)
        } importing: { received in
            Attachment(fileURL: received.file)
        }
    }
}
```

List multiple representations to offer format fallbacks — SwiftUI negotiates with the drop target/receiving app in declaration order, most-specific first.

### `.draggable` / `.dropDestination`

```swift
struct NoteRow: View {
    let note: Note

    var body: some View {
        Text(note.title)
            .draggable(note) {
                NoteDragPreview(note: note)   // custom preview; omit for the default snapshot
            }
    }
}

struct NoteList: View {
    @State private var notes: [Note] = []

    var body: some View {
        List(notes) { NoteRow(note: $0) }
            .dropDestination(for: Note.self) { droppedNotes, location in
                notes.append(contentsOf: droppedNotes)
                return true   // return false to reject and animate the drop back
            }
    }
}
```

`dropDestination(for:action:isTargeted:)` adds an `isTargeted` binding for hover-state styling; `dropDestination(for:isEnabled:action:)` gates acceptance dynamically (e.g. disable drop while a save is in flight).

### Multi-item drags

`.draggable` on a `ForEach`/`List` row participates automatically in multi-item drag when the user has a multi-selection active — SwiftUI bundles the `Transferable` payload for every selected row. No extra API; ensure the selection binding (`List(selection:)`) is wired so the drag knows what's selected.

---

## 2. `NSItemProvider` Bridging

`Transferable` is backed by `NSItemProvider` under the hood. When interoperating with AppKit code or third-party APIs still on the old protocol, bridge explicitly:

```swift
// Transferable -> NSItemProvider (for APIs expecting the legacy type)
let provider = NSItemProvider(object: NSString(string: note.title))

// NSItemProvider -> Transferable-style loading (AppKit drag destination receiving from SwiftUI-originated drag)
provider.loadDataRepresentation(forTypeIdentifier: UTType.myAppNote.identifier) { data, error in
    guard let data else { return }
    let note = try? JSONDecoder().decode(Note.self, from: data)
}
```

---

## 3. Raw `NSPasteboard`

Needed for: multi-pasteboard workflows (find pasteboard), custom pasteboard types without a `Transferable` conformance, or reading pasteboard contents outside a drag/drop gesture (e.g. a paste button that isn't backed by SwiftUI's `PasteButton`).

| Pasteboard | Purpose |
|---|---|
| `NSPasteboard.general` | Standard copy/paste |
| `NSPasteboard(name: .drag)` | Active drag operations (system-managed; rarely accessed directly) |
| `NSPasteboard(name: .find)` | Shared Find-panel search term across apps |

```swift
// Write
let pb = NSPasteboard.general
pb.clearContents()
pb.setString(note.title, forType: .string)
pb.setData(try! JSONEncoder().encode(note), forType: NSPasteboard.PasteboardType("com.example.myapp.note"))

// Read
if let title = pb.string(forType: .string) { /* ... */ }
```

`NSPasteboard.PasteboardType` values should mirror the app's `UTType` identifiers for consistency with the `Transferable`/Uniform Type Identifiers path (`reference/documents.md` § 2).

### Promised files — `NSFilePromiseProvider`

For drag sources that generate the file lazily (expensive render, network fetch) rather than materializing it up front:

```swift
final class NoteFilePromiseProvider: NSFilePromiseProvider, NSFilePromiseProviderDelegate {
    var note: Note!

    override init() {
        super.init()
        self.delegate = self
    }

    func filePromiseProvider(_ filePromiseProvider: NSFilePromiseProvider, fileNameForType fileType: String) -> String {
        "\(note.title).mynote"
    }

    func filePromiseProvider(_ filePromiseProvider: NSFilePromiseProvider, writePromiseTo url: URL, completionHandler: @escaping (Error?) -> Void) {
        do {
            try JSONEncoder().encode(note).write(to: url)
            completionHandler(nil)
        } catch {
            completionHandler(error)
        }
    }
}
```

`NSFilePromiseProvider` requires a serial `OperationQueue` (set via `.operationQueue`) to serialize the write callback — the drop destination (e.g. Finder) invokes it after the user releases the drag.

---

## 4. `NSDraggingSource` / `NSDraggingDestination` (AppKit Path)

Drop to this only when: a custom `NSView`-based list/canvas needs per-pixel drop-target computation, or drag behavior (spring-loading, custom cursor feedback, `NSDraggingSession` formation control) that `.draggable`/`.dropDestination` doesn't expose.

```swift
final class CanvasView: NSView, NSDraggingSource, NSDraggingDestination {
    func draggingSession(_ session: NSDraggingSession, sourceOperationMaskFor context: NSDraggingContext) -> NSDragOperation {
        context == .withinApplication ? .move : .copy
    }

    override func draggingEntered(_ sender: NSDraggingInfo) -> NSDragOperation {
        sender.draggingPasteboard.canReadObject(forClasses: [NSString.self], options: nil) ? .copy : []
    }

    override func performDragOperation(_ sender: NSDraggingInfo) -> Bool {
        guard let items = sender.draggingPasteboard.readObjects(forClasses: [NSString.self], options: nil) else { return false }
        // handle drop
        return true
    }
}
```

Register accepted types once, typically in `awakeFromNib`/`init`: `registerForDraggedTypes([.string, .fileURL])`.

---

## 5. Copy/Paste + Edit-Menu Wiring

SwiftUI wires standard Edit-menu Copy/Paste/Cut automatically for text controls (`TextField`, `TextEditor`). For custom data:

```swift
struct NoteEditor: View {
    @FocusedValue(\.selectedNote) private var selectedNote

    var body: some View {
        ContentView()
            .copyable([selectedNote?.title ?? ""])   // enables Edit > Copy for non-text selection
            .pasteDestination(for: Note.self) { notes in
                // handle pasted Note payloads
            }
    }
}
```

`.copyable`/`.pasteDestination` (SwiftUI, macOS 13+) route through the same `Transferable` conformance as drag & drop — one conformance covers copy/paste, drag/drop, and `ShareLink`.

For `NSDocument`-based apps, Copy/Cut/Paste route through `NSResponder`'s `copy(_:)`/`cut(_:)`/`paste(_:)` action methods — override on the first responder (typically the document's main view or window controller).

---

## 6. macOS Services

Services let the app both **provide** actions to other apps' Services menus and **consume** services others provide.

### Registering a service (`NSServices` in Info.plist)

```xml
<key>NSServices</key>
<array>
  <dict>
    <key>NSMenuItem</key>
    <dict><key>default</key><string>Add to MyApp Notes</string></dict>
    <key>NSMessage</key><string>addToNotes</string>
    <key>NSPortName</key><string>MyApp</string>
    <key>NSSendTypes</key>
    <array><string>NSStringPboardType</string></array>
  </dict>
</array>
```

```swift
final class ServiceProvider: NSObject {
    @objc func addToNotes(_ pasteboard: NSPasteboard, userData: String, error: AutoreleasingUnsafeMutablePointer<NSString>) {
        guard let text = pasteboard.string(forType: .string) else { return }
        // create a note from `text`
    }
}

// App launch:
NSApp.servicesProvider = ServiceProvider()
```

### Sharing out — `NSSharingServicePicker`

```swift
let picker = NSSharingServicePicker(items: [note.title, noteFileURL])
picker.show(relativeTo: sourceButton.bounds, of: sourceButton, preferredEdge: .minY)
```

SwiftUI equivalent for outbound sharing is `ShareLink` (backed by `Transferable`) — prefer `ShareLink` unless anchoring to a specific `NSView`/toolbar item is required.

---

## 7. Quick Look Preview Extension (Basics)

A Quick Look preview extension (separate `.appex` target, `QLPreviewProvider`) renders the app's custom document format in Finder's Quick Look/Gallery view without launching the app:

```swift
final class PreviewProvider: QLPreviewProvider, QLPreviewingController {
    func providePreview(for request: QLFilePreviewRequest) async throws -> QLPreviewReply {
        let reply = QLPreviewReply(fileURL: request.fileURL)
        return reply
    }
}
```

Register the extension's supported `UTType`s (matching § 1 of `reference/documents.md`) in the extension target's Info.plist under `QLSupportedContentTypes`. Full preview-rendering pipeline design (custom drawing vs delegating to `fileURL`) is out of scope here — this is the wiring, not the rendering.

---

## 8. Security-Scoped Access for Dropped Files

Files dropped from outside the sandbox (Finder, another app) arrive as security-scoped URLs when the app is sandboxed. Call `startAccessingSecurityScopedResource()` before reading, and persist a bookmark if access must survive beyond the current drop handler.

```swift
.dropDestination(for: URL.self) { urls, _ in
    for url in urls {
        guard url.startAccessingSecurityScopedResource() else { continue }
        defer { url.stopAccessingSecurityScopedResource() }
        // read file
    }
    return true
}
```

Full bookmark lifecycle (persisting across launches, stale-bookmark refresh) → `reference/sandbox-entitlements.md`.

---

## Cross-References

- Security-scoped bookmarks, Powerbox-mediated pickers — `reference/sandbox-entitlements.md`
- Document file formats / `UTType` declaration — `reference/documents.md`
- `NSViewRepresentable` bridging for custom AppKit drag views hosted in SwiftUI — `reference/appkit-interop.md`

---

## Sources

- [Adopting drag and drop using SwiftUI](https://developer.apple.com/documentation/SwiftUI/Adopting-drag-and-drop-using-SwiftUI) — Apple Developer Documentation (accessed 2026-07)
- [Transferable](https://developer.apple.com/documentation/coretransferable/transferable) — Apple Developer Documentation
- [dropDestination(for:action:isTargeted:)](https://developer.apple.com/documentation/swiftui/view/dropdestination(for:action:istargeted:)) — Apple Developer Documentation
- [NSFilePromiseProvider](https://developer.apple.com/documentation/appkit/nsfilepromiseprovider) — Apple Developer Documentation
- [Supporting Drag and Drop Through File Promises](https://developer.apple.com/documentation/appkit/supporting-drag-and-drop-through-file-promises) — Apple Developer Documentation
- [NSPasteboard](https://developer.apple.com/documentation/appkit/nspasteboard) — Apple Developer Documentation
- [NSDraggingSource](https://developer.apple.com/documentation/appkit/nsdraggingsource) / [NSDraggingDestination](https://developer.apple.com/documentation/appkit/nsdraggingdestination) — Apple Developer Documentation
- [NSSharingServicePicker](https://developer.apple.com/documentation/appkit/nssharingservicepicker) — Apple Developer Documentation
- [QLPreviewProvider](https://developer.apple.com/documentation/quicklookui/qlpreviewprovider) — Apple Developer Documentation
- WWDC22 "Meet Transferable" — session reference for `Transferable` introduction
