# Document-Based macOS Apps

**Purpose:** `DocumentGroup`/`FileDocument`/`ReferenceFileDocument` (SwiftUI-first path), legacy `NSDocument`/`NSDocumentController`, autosave-in-place + Versions, custom `UTType` export, iCloud document sync, undo integration, package-format documents, untitled-document lifecycle.
**Read when:** Building a document-based Mac app (`document` Recipe).

---

## 1. SwiftUI vs `NSDocument` Decision Table

| Requirement | Use |
|---|---|
| Standard open/save/autosave/Versions, single-window-per-document | `DocumentGroup` + `FileDocument`/`ReferenceFileDocument` |
| Value-type document (struct, `Codable`-friendly) | `FileDocument` |
| Reference-type document (class-based model, incremental edits, undo via mutation) | `ReferenceFileDocument` |
| Custom save panel (accessory views, format picker beyond `UTType` list) | `NSDocument` |
| Multiple windows onto the *same* document (e.g. two views of one spreadsheet) | `NSDocument` (`NSWindowController` fan-out) |
| Custom print/print-preview pipeline | `NSDocument` (`printOperation(withSettings:)`) |
| Custom versioning UI beyond the standard Versions browser | `NSDocument` (`NSDocumentController` overrides) |
| App also ships an iPad/iOS target sharing document logic | `FileDocument`/`ReferenceFileDocument` (portable) |

Default to `DocumentGroup`. Drop to `NSDocument` only when one of the middle rows is a hard requirement — see § 4.

---

## 2. `UTType` Declaration

Every document format needs a `UTType` — declared in Xcode's target editor (writes to `Info.plist` as `UTExportedTypeDeclarations`/`UTImportedTypeDeclarations`) or hand-edited directly.

```xml
<!-- Info.plist: exported (app owns this format) -->
<key>UTExportedTypeDeclarations</key>
<array>
  <dict>
    <key>UTTypeIdentifier</key>
    <string>com.example.myapp.project</string>
    <key>UTTypeConformsTo</key>
    <array>
      <string>public.data</string>
      <string>public.composite-content</string>
    </array>
    <key>UTTypeDescription</key>
    <string>MyApp Project</string>
    <key>UTTypeTagSpecification</key>
    <dict>
      <key>public.filename-extension</key>
      <array><string>myproj</string></array>
      <key>public.mime-type</key>
      <string>application/x-myapp-project</string>
    </dict>
  </dict>
</array>

<key>CFBundleDocumentTypes</key>
<array>
  <dict>
    <key>CFBundleTypeName</key><string>MyApp Project</string>
    <key>LSItemContentTypes</key>
    <array><string>com.example.myapp.project</string></array>
    <key>CFBundleTypeRole</key><string>Editor</string>
    <key>LSHandlerRank</key><string>Owner</string>
  </dict>
</array>
```

- **Conformance chain matters**: conform to `public.composite-content` for package/bundle formats (directory-backed), `public.data` for flat files, `public.json`/`public.plain-text` when the format *is* JSON/text (grants Quick Look, Spotlight preview, and text-editor interop for free).
- **Importing a third-party format** (e.g. reading `.csv` you don't own): declare `UTImportedTypeDeclarations` referencing the existing identifier (`public.comma-separated-values-text`) instead of re-declaring it.
- Register in the `UTType` extension in Swift for use with `FileDocument`:

```swift
import UniformTypeIdentifiers

extension UTType {
    static var myAppProject: UTType {
        UTType(exportedAs: "com.example.myapp.project")
    }
}
```

---

## 3. `FileDocument` / `ReferenceFileDocument` (SwiftUI path)

### `FileDocument` — value types

```swift
import SwiftUI
import UniformTypeIdentifiers

struct ProjectDocument: FileDocument {
    static var readableContentTypes: [UTType] = [.myAppProject]
    static var writableContentTypes: [UTType] = [.myAppProject]

    var project: Project

    init(project: Project = Project()) {
        self.project = project
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        project = try JSONDecoder().decode(Project.self, from: data)
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = try JSONEncoder().encode(project)
        return FileWrapper(regularFileWithContents: data)
    }
}

@main
struct MyApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: ProjectDocument()) { file in
            ProjectView(document: file.$document)
        }
    }
}
```

`ReadConfiguration`/`WriteConfiguration` expose `.file: FileWrapper` and `.contentType: UTType` — inspect `contentType` when `readableContentTypes` covers multiple formats (e.g. legacy + current) to branch decode logic.

### `ReferenceFileDocument` — reference types (undo-friendly, incremental)

Use when the model is a class with fine-grained mutation and you want SwiftUI's `UndoManager` integration to register per-field edits rather than whole-document snapshots.

```swift
final class ProjectDocument: ReferenceFileDocument {
    static var readableContentTypes: [UTType] = [.myAppProject]

    @Published var project: Project

    init(project: Project = Project()) { self.project = project }

    required init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents else {
            throw CocoaError(.fileReadCorruptFile)
        }
        project = try JSONDecoder().decode(Project.self, from: data)
    }

    // Snapshot captures state for the write side without blocking edits during save.
    func snapshot(contentType: UTType) throws -> Project {
        project
    }

    func fileWrapper(snapshot: Project, configuration: WriteConfiguration) throws -> FileWrapper {
        let data = try JSONEncoder().encode(snapshot)
        return FileWrapper(regularFileWithContents: data)
    }
}
```

`snapshot(contentType:)` + `fileWrapper(snapshot:configuration:)` decouple "what gets saved" from "what the user keeps editing" — SwiftUI takes the snapshot on a background queue while `@Published` mutations continue on the main actor.

---

## 4. Legacy `NSDocument` / `NSDocumentController`

Reach for this path per § 1's decision table. Core overrides:

```swift
final class ProjectDocument: NSDocument {
    var project = Project()

    override class var autosavesInPlace: Bool { true }
    override class var preservesVersions: Bool { true }

    override func data(ofType typeName: String) throws -> Data {
        try JSONEncoder().encode(project)
    }

    override func read(from data: Data, ofType typeName: String) throws {
        project = try JSONDecoder().decode(Project.self, from: data)
    }

    override func makeWindowControllers() {
        let windowController = NSStoryboard(name: "Main", bundle: nil)
            .instantiateController(withIdentifier: "DocumentWindow") as! NSWindowController
        addWindowController(windowController)
    }

    // Multi-window-per-document: call makeWindowControllers() again, or
    // construct an additional NSWindowController and addWindowController(_:)
    // without replacing the first — NSDocument tracks all controllers.

    override func printOperation(withSettings printSettings: [NSPrintInfo.AttributeKey: Any]) throws -> NSPrintOperation {
        NSPrintOperation(view: contentView, printInfo: printInfo)
    }
}
```

`NSDocumentController` (usually `NSDocumentController.shared`, subclass only for custom open-panel accessory views or custom recent-documents behavior):

```swift
final class ProjectDocumentController: NSDocumentController {
    override func beginOpenPanel(_ openPanel: NSOpenPanel, forTypes inTypes: [String]?, completionHandler: @escaping (Int) -> Void) {
        let accessory = FormatPickerAccessoryView()
        openPanel.accessoryView = accessory
        super.beginOpenPanel(openPanel, forTypes: inTypes, completionHandler: completionHandler)
    }
}
```

Instantiate the custom controller once, before any document is opened (typically in `applicationWillFinishLaunching`) — `NSDocumentController` is a singleton resolved on first access.

---

## 5. Autosave-in-Place + Versions

- `override class var autosavesInPlace: Bool { true }` (NSDocument) or automatic under `DocumentGroup` — enables silent background saves and removes the "Save" menu item in favor of "Duplicate"/"Revert To".
- `preservesVersions: Bool { true }` opts into the Versions browser (Time Machine-style, `NSDocument.browseDocumentVersions(_:)`).
- Autosave-in-place changes user expectations: there is no "unsaved changes" dialog on close for autosaving documents — closing simply saves. Only prompt for explicit save when `autosavesInPlace` is `false`.
- `DocumentGroup` documents autosave in place by default with no additional configuration; opt out is not exposed — if you need explicit-save semantics, use `NSDocument` with `autosavesInPlace` overridden to `false`.

---

## 6. Undo Integration

| Layer | Mechanism |
|---|---|
| SwiftUI (`DocumentGroup`) | `@Environment(\.undoManager)` — read the document-scoped `UndoManager` inside views; register actions with `undoManager?.registerUndo(withTarget:handler:)` |
| `ReferenceFileDocument` | Same `UndoManager` via environment; mutate `@Published` properties and register the inverse operation per edit for granular undo |
| `NSDocument` | `self.undoManager` (inherited) — call `undoManager?.registerUndo(withTarget:handler:)` inside every mutating method; `NSDocument` auto-wires Edit menu Undo/Redo |

```swift
struct ProjectView: View {
    @Binding var document: ProjectDocument
    @Environment(\.undoManager) private var undoManager

    func rename(to newName: String) {
        let oldName = document.project.name
        undoManager?.registerUndo(withTarget: document) { doc in
            doc.project.name = oldName
        }
        document.project.name = newName
    }
}
```

---

## 7. Open / Recent Documents

- `DocumentGroup` wires File > Open, File > Open Recent, and the dock-icon recent-documents menu automatically from `CFBundleDocumentTypes` + `LSHandlerRank`.
- `NSDocument` path: `NSDocumentController.shared.noteNewRecentDocumentURL(_:)` on manual opens outside the standard open panel flow.
- `LSHandlerRank: Owner` in `CFBundleDocumentTypes` claims the format as this app's default handler for Finder "Open With" and double-click.

---

## 8. iCloud Documents

- Enable the iCloud Documents capability + `NSUbiquitousContainers` in entitlements; store documents under `FileManager.default.url(forUbiquityContainerIdentifier:)`.
- `DocumentGroup` + `FileDocument` work transparently with the ubiquity container — no code change beyond pointing the document's storage location there.
- **`NSFileCoordinator`/`NSFilePresenter`** are required whenever code reads/writes iCloud-backed files *outside* the `NSDocument`/`FileDocument` save pipeline (e.g. a background sync scan) — uncoordinated access risks torn reads during iCloud's own sync writes:

```swift
let coordinator = NSFileCoordinator()
var coordinationError: NSError?
coordinator.coordinate(readingItemAt: fileURL, options: [], error: &coordinationError) { url in
    let data = try? Data(contentsOf: url)
    // ...
}
```

Conform to `NSFilePresenter` for long-lived observers that must react to `presentedItemDidChange()` when iCloud updates a file out from under an open document.

- **Conflict resolution**: iCloud surfaces conflicts as `NSFileVersion.unresolvedConflictVersionsOfItem(at:)`. Present the standard conflict-resolution UI via `NSFileVersion` + the Versions browser, or auto-resolve with `NSFileVersion.removeOtherVersionsOfItem(at:)` after picking a winner — never silently overwrite without checking `isConflict`.

---

## 9. Package (Bundle) Document Formats

For documents that bundle multiple files (assets + metadata), declare a package `UTType` (conforms to `com.apple.package` in addition to your format identifier) and back the document with `FileWrapper(directoryWithFileWrappers:)`:

```swift
func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
    var children: [String: FileWrapper] = [:]
    children["metadata.json"] = FileWrapper(regularFileWithContents: try JSONEncoder().encode(project.metadata))
    children["assets"] = FileWrapper(directoryWithFileWrappers: assetWrappers())
    return FileWrapper(directoryWithFileWrappers: children)
}
```

Finder treats packages as opaque files (no double-click-to-browse) once `com.apple.package` conformance is declared — required for any bundle format the user should not manually poke inside.

---

## 10. Untitled-Document Lifecycle

- `DocumentGroup(newDocument:)` creates the in-memory untitled document immediately on File > New; it is never written to disk until first save (autosave-in-place writes it to a temporary location on first autosave, then moves it on explicit "Save As" naming).
- `NSDocument`: `NSDocumentController.shared.openUntitledDocumentAndDisplay(true)` — the untitled document's `fileURL` is `nil` until the user names it; check `fileURL == nil` before any code path assumes an on-disk location.
- Both paths mark the window as "Untitled" in the title bar with an edited-dot indicator (`isDocumentEdited`) until first save — do not suppress this indicator; it's the standard "unsaved work" affordance under Mac HIG.

---

## Cross-References

- Drag & drop of files onto a document / Services import — `reference/drag-drop-services.md`
- Security-scoped bookmarks for documents outside the sandbox container — `reference/sandbox-entitlements.md`
- `DocumentGroup` scene composition and multi-window behavior — `reference/scenes.md`
- Undo across AppKit-hosted views inside a SwiftUI document — `reference/appkit-interop.md`

---

## Sources

- [Building a document-based app with SwiftUI](https://developer.apple.com/documentation/swiftui/building-a-document-based-app-with-swiftui) — Apple Developer Documentation (accessed 2026-07)
- [ReferenceFileDocument](https://developer.apple.com/documentation/swiftui/referencefiledocument) — Apple Developer Documentation
- [snapshot(contentType:)](https://developer.apple.com/documentation/swiftui/referencefiledocument/snapshot(contenttype:)) — Apple Developer Documentation
- [fileWrapper(snapshot:configuration:)](https://developer.apple.com/documentation/swiftui/referencefiledocument/filewrapper(snapshot:configuration:)) — Apple Developer Documentation
- [NSDocument](https://developer.apple.com/documentation/appkit/nsdocument) — Apple Developer Documentation
- [NSDocumentController](https://developer.apple.com/documentation/appkit/nsdocumentcontroller) — Apple Developer Documentation
- [NSFileCoordinator](https://developer.apple.com/documentation/foundation/nsfilecoordinator) — Apple Developer Documentation
- [NSFilePresenter](https://developer.apple.com/documentation/foundation/nsfilepresenter) — Apple Developer Documentation
- [Uniform Type Identifiers](https://developer.apple.com/documentation/uniformtypeidentifiers) — Apple Developer Documentation
- WWDC20 "Build document-based apps in SwiftUI" — session reference for `DocumentGroup` introduction
