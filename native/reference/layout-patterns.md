# Mac Window Layout Patterns

**Purpose:** Sidebar/toolbar/inspector composition for Mac windows — `NavigationSplitView`, toolbars, `.inspector()`, `.searchable`, `Table`, split panes, and Liquid Glass chrome adoption on macOS Tahoe 26.
**Read when:** Building a sidebar-driven Mac app window, adding a toolbar, adding an inspector panel, or auditing a window's layout against current Mac HIG.

---

## 1. `NavigationSplitView` — 2/3-Column

```swift
// 3-column: sidebar / content list / detail
NavigationSplitView {
    SidebarView(selection: $selectedFolder)
} content: {
    NoteListView(folder: selectedFolder, selection: $selectedNote)
} detail: {
    if let selectedNote {
        NoteDetailView(note: selectedNote)
    } else {
        ContentUnavailableView("No Note Selected", systemImage: "note.text")
    }
}
```

```swift
// 2-column: sidebar / detail
NavigationSplitView {
    SidebarView(selection: $selectedItem)
} detail: {
    DetailView(itemID: selectedItem)
}
```

`NavigationSplitView` is the macOS 13+ replacement for the pre-2022 `NavigationView`-with-`.sidebar` idiom — do not use `NavigationView` for new sidebar layouts. Do not nest `NavigationSplitView` inside a `NavigationStack`; put `NavigationStack` (if needed inside the detail column) *inside* `NavigationSplitView`'s `detail:` closure, never the reverse (known regression across recent OS versions when inverted).

### 1.1 Column Width & Visibility

```swift
NavigationSplitView(columnVisibility: $columnVisibility) {
    SidebarView(selection: $selection)
        .navigationSplitViewColumnWidth(min: 180, ideal: 220, max: 320)
} detail: {
    DetailView()
}
```

- `columnVisibility: Binding<NavigationSplitViewVisibility>` (`.all` / `.doubleColumn` / `.detailOnly` / `.automatic`) — bind it when the app needs to programmatically collapse the sidebar (e.g. a "Hide Sidebar" toolbar button beyond the system-provided one).
- `.navigationSplitViewColumnWidth(min:ideal:max:)` sets resize bounds per column; use `.navigationSplitViewColumnWidth(_:)` with a single value to fix a column's width (common for a content list column that should stay a constant width while sidebar/detail resize).
- `.navigationSplitViewStyle(.balanced | .prominentDetail)` controls how width is redistributed when the window shrinks — `.prominentDetail` keeps the detail column as large as possible, collapsing sidebar/content first.

---

## 2. Sidebar Idioms

```swift
List(selection: $selection) {
    Section("Library") {
        Label("All Notes", systemImage: "tray.full")
            .tag(SidebarItem.all)
        Label("Favorites", systemImage: "star")
            .tag(SidebarItem.favorites)
    }
    Section("Folders") {
        ForEach(folders) { folder in
            Label(folder.name, systemImage: "folder")
                .tag(SidebarItem.folder(folder.id))
        }
    }
}
.listStyle(.sidebar)
```

- `.listStyle(.sidebar)` is what gives a `List` the translucent sidebar background, selection highlight, and section-header styling macOS users expect — a plain `List` in a `NavigationSplitView` sidebar slot looks wrong without it.
- `Section` headers in `.sidebar` style render as the small-caps gray group labels; use them to group navigation destinations by category (Library / Folders / Tags), not as a substitute for a detail-view heading.
- Disclosure groups (`DisclosureGroup` or `OutlineGroup` for recursive trees) nest inside sidebar sections for expandable folder hierarchies:

```swift
List(selection: $selection) {
    OutlineGroup(rootFolders, children: \.subfolders) { folder in
        Label(folder.name, systemImage: "folder")
            .tag(SidebarItem.folder(folder.id))
    }
}
.listStyle(.sidebar)
```

**When NOT to use a sidebar:** a utility window with a single, flat, non-navigational content area (a preferences pane, a small tool palette) should not be forced into `NavigationSplitView` — use a plain `VStack`/`Form` in a `Window` or `Settings` scene instead.

---

## 3. Toolbar

```swift
DetailView()
    .toolbar {
        ToolbarItemGroup(placement: .navigation) {
            Button("Toggle Sidebar", systemImage: "sidebar.left") {
                toggleSidebar()
            }
        }
        ToolbarItem(placement: .primaryAction) {
            Button("New Note", systemImage: "square.and.pencil") { /* ... */ }
        }
        ToolbarItemGroup(placement: .automatic) {
            Button("Share", systemImage: "square.and.arrow.up") { /* ... */ }
            Button("Info", systemImage: "info.circle") { showInspector.toggle() }
        }
    }
```

| Placement | macOS position | Use for |
|-----------|-----------------|---------|
| `.navigation` | Leading edge, alongside the sidebar toggle | Navigation-adjacent controls (back/forward, sidebar toggle) |
| `.primaryAction` | Leading edge (macOS — differs from iOS trailing) | The single most common action for this window |
| `.principal` | Center | Title-replacing content (a segmented control, a search summary) |
| `.status` | Center, secondary weight | Non-interactive or low-emphasis status content |
| `.confirmationAction` | Trailing, same position as `.primaryAction` | Sheet/dialog confirm actions |
| `.cancellationAction` | Leading | Sheet/dialog cancel actions |
| `.destructiveAction` | Trailing, adjacent to confirmation | Destructive sheet actions (paired with `.confirmationAction`) |
| `.automatic` (default) | System-chosen based on context | Default when placement doesn't matter |

`ToolbarItemGroup` clusters related items with system-managed spacing (they visually separate as a unit when the toolbar overflows); use it instead of multiple adjacent `ToolbarItem`s for anything that reads as one control cluster.

`.toolbarRole(.editor | .browser | .automatic)` shapes how the title interacts with toolbar content — `.editor` centers toolbar items and de-emphasizes the title, `.browser` is the default list/detail behavior. Its effect is most visible on iOS/iPadOS; on macOS the title-bar/toolbar-unification behavior is largely system-controlled, so treat this modifier as secondary to placement choices above (unverified — exact macOS-specific behavior of `.toolbarRole` was not independently confirmed against current documentation; verify visually before relying on it for a macOS-specific layout decision).

---

## 4. `.inspector()` — Trailing Panel

```swift
DetailView()
    .inspector(isPresented: $showInspector) {
        NoteInspectorView(note: selectedNote)
            .inspectorColumnWidth(min: 220, ideal: 280, max: 400)
    }
    .toolbar {
        ToolbarItem(placement: .primaryAction) {
            Button("Inspector", systemImage: "sidebar.trailing") {
                showInspector.toggle()
            }
        }
    }
```

- `.inspector()` (macOS 14+) renders as a trailing sidebar-style panel, distinct from the leading `NavigationSplitView` sidebar — use it for contextual metadata/properties of the current selection (file info, formatting controls, AI-assist panel), not as a second navigation surface.
- When applied inside a view that also contains a `NavigationStack`, the inspector extends to the window's full height rather than just the stack's content area — verify this visually if the detail column has its own internal navigation.
- `.inspectorColumnWidth(min:ideal:max:)` mirrors the sidebar column-width modifier from §1.1.

**When NOT to use `.inspector()`:** don't use it as a generic "extra sidebar" for navigation — that's what the `content:` column of a 3-column `NavigationSplitView` is for (§1). Inspector is for *properties of the current selection*, not *another list of things to select*.

---

## 5. `.searchable` — Scoping & Tokens

```swift
DetailView()
    .searchable(text: $searchText, placement: .sidebar, prompt: "Search Notes")
    .searchScopes($searchScope) {
        Text("All").tag(SearchScope.all)
        Text("Titles").tag(SearchScope.titles)
    }
```

- `placement: .sidebar` puts the search field at the top of the sidebar column (the common Mac Mail/Notes-style position); `.toolbar` places it in the window toolbar instead.
- Search tokens (`.searchable(text:tokens:suggestedTokens:token:)`) render as removable rounded-rect chips inside the search field for structured filters (e.g. "tag:work", "from:alice"). On macOS, selecting a suggested token does **not** replace the visible results the way it does on iOS — tokens and results stay visible together, so design the suggestions list accordingly.
- Combine `.searchable` with `.searchScopes` for a segmented "All / Titles / Body" filter that narrows without needing a separate UI element.

---

## 6. `Table` — Sortable, Reorderable Columns

```swift
struct FileRow: Identifiable {
    let id: UUID
    var name: String
    var size: Int
    var modified: Date
}

@State private var files: [FileRow] = []
@State private var sortOrder: [KeyPathComparator<FileRow>] = [.init(\.modified, order: .reverse)]
@State private var selection: Set<FileRow.ID> = []

Table(files, selection: $selection, sortOrder: $sortOrder) {
    TableColumn("Name", value: \.name)
    TableColumn("Size") { row in Text(row.size, format: .byteCount(style: .file)) }
        .width(min: 60, ideal: 90)
    TableColumn("Modified", value: \.modified) { row in Text(row.modified, style: .date) }
}
.onChange(of: sortOrder) { _, newOrder in
    files.sort(using: newOrder)
}
```

- Binding `sortOrder` to an array of `SortComparator` (typically `KeyPathComparator`) makes column headers clickable/sortable; a `TableColumn` built without a `value:` key path has no sort behavior.
- `TableColumnCustomization<RowValue>` (bound via `.tableColumnCustomization(_:)`) persists user-driven column reordering, resizing, and visibility toggles across launches — pair with a stable per-column identifier.
- `Table` is macOS-first (available since macOS 12) and is the correct choice over `List` whenever content is genuinely tabular (Finder-list-view-style, multi-attribute rows) rather than a single-value list.

---

## 7. Split-View / `HSplitView` Equivalents

For non-navigational resizable panes (side-by-side comparison views, a code editor + preview pane) that don't map to the sidebar/detail navigation model, `HSplitView`/`VSplitView` give plain `NSSplitView`-style resizable dividers without navigation semantics:

```swift
HSplitView {
    SourceEditorView(text: $sourceText)
        .frame(minWidth: 300)
    PreviewView(text: sourceText)
        .frame(minWidth: 300)
}
```

`HSplitView`/`VSplitView` are macOS-only (no iOS equivalent) and predate `NavigationSplitView` — reach for them specifically when the two panes are peers (neither is "sidebar", neither drives navigation of the other), which `NavigationSplitView` is not designed to express.

---

## 8. Liquid Glass Adoption (macOS Tahoe 26)

- Recompiling an existing SwiftUI app against the macOS 26 SDK gives `NavigationSplitView` sidebars and `.toolbar` content Liquid Glass automatically — no code changes required for the standard chrome.
- The macOS Tahoe sidebar renders as a floating Liquid Glass panel with rounded corners that reflect/refract underlying content; toolbars adopt the same material and auto-size to content.
- `.backgroundExtensionEffect()` (macOS 26+) lets a view extend visually outside the safe area without clipping, for content that should read as flowing behind the glass sidebar/toolbar.
- **Chrome only** — never apply `.glassEffect()`/`GlassEffectContainer` to content views (document body, list rows, canvas). This mirrors the SKILL-level Liquid Glass scope rule (see `native/SKILL.md` Core Contract and `reference/mac-hig.md`).
- **Pre-26 fallback**: on Sonoma/Sequoia targets, `NavigationSplitView`/`.toolbar` render with the standard (non-glass) macOS sidebar/toolbar material — no fallback code is needed since the glass rendering is automatic-and-additive on 26, not a separate code path, but verify legibility/contrast manually on both OS versions before shipping a design that assumes translucency.

---

## 9. Density & `.controlSize`

```swift
Toolbar()
    .controlSize(.regular)   // .mini / .small / .regular / .large / .extraLarge (macOS 14+)
```

- Default to `.regular` for primary window chrome; `.small` fits inspector panels and dense utility rows where vertical space is at a premium.

| Size | Fits |
|------|------|
| `.mini` | Rare — legacy dense toolbars, stepper-heavy forms |
| `.small` | Inspector rows, secondary toolbars, dense sidebars |
| `.regular` | Default window content |
| `.large` / `.extraLarge` | Prominent call-to-action controls, onboarding |

- `.controlSize` cascades to child controls (buttons, steppers, pickers) within the modified view's hierarchy — set it once at a container level rather than per-control where a whole panel should read as "dense."

---

## 10. Responsive Behavior Across Window Resize

- `NavigationSplitView` collapses columns automatically as the window narrows: 3-column becomes 2-column (content column collapses into a stacked push), then the sidebar collapses into a toggleable overlay below a minimum width — verify column `min` widths (§1.1) are set low enough that this degrades gracefully rather than clipping content.
- `.inspector()` panels do not auto-collapse the same way; provide the toolbar toggle (§4) as the escape hatch when the window is too narrow for sidebar + content + inspector simultaneously.
- Table columns with `.width(min:ideal:max:)` (§6) should always specify a `min` — an unconstrained `Table` column can compress to unreadable widths on a small window.
- Test at the practical Mac minimum window sizes (roughly 600–800pt wide for a utility window, larger for a 3-column document app) rather than only at the design's ideal size.

---

## Sources

- [NavigationSplitView | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/navigationsplitview)
- [Build a SwiftUI app with the new design — WWDC25 Session 323](https://developer.apple.com/videos/play/wwdc2025/323/) — Liquid Glass sidebar/toolbar, `backgroundExtensionEffect` (accessed 2026-07)
- [ToolbarItemPlacement | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/toolbaritemplacement) (accessed 2026-07)
- [Presenting an Inspector with SwiftUI — createwithswift.com](https://www.createwithswift.com/presenting-an-inspector-with-swiftui/)
- [Table | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/table)
- [TableColumnCustomization | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/tablecolumncustomization) (accessed 2026-07)
- [SwiftUI Tables Quick Guide — useyourloaf.com](https://useyourloaf.com/blog/swiftui-tables-quick-guide/)
- [How to add search tokens to a search field — hackingwithswift.com](https://www.hackingwithswift.com/quick-start/swiftui/how-to-add-search-tokens-to-a-search-field)
- [HSplitView | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/hsplitview)
- Mac HIG — Windows, Sidebars, Toolbars (`reference/mac-hig.md` for full chrome audit criteria)
