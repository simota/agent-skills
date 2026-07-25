# Menu Bar & Commands

**Purpose:** Main menu bar construction — `Commands`, HIG-mandated menu structure, keyboard shortcut conventions, focused-value-driven enable/disable, contextual menus, and `MenuBarExtra` interaction rules.
**Read when:** Building or auditing a Mac app's main menu, adding menu commands, wiring keyboard shortcuts, or building a menu-bar-only utility's interaction model.

---

## 1. `Commands` Overview

Attach a `Commands` builder to any scene in the `App` body — it merges into the single main menu bar regardless of which scene it's attached to:

```swift
@main
struct NotesApp: App {
    var body: some Scene {
        WindowGroup { ContentView() }
            .commands {
                NoteCommands()
            }
    }
}

struct NoteCommands: Commands {
    @FocusedValue(\.currentNote) private var currentNote

    var body: some Commands {
        CommandGroup(after: .newItem) {
            Button("New Note from Template…") { /* ... */ }
                .keyboardShortcut("n", modifiers: [.command, .shift])
        }
        CommandMenu("Note") {
            Button("Duplicate") { currentNote?.duplicate() }
                .disabled(currentNote == nil)
        }
    }
}
```

---

## 2. `CommandGroup` / `CommandMenu` / `CommandGroupPlacement`

`CommandGroup(replacing:)` swaps a default system menu item entirely; `CommandGroup(before:)`/`CommandGroup(after:)` insert relative to one. `CommandMenu(_:)` creates an entirely new top-level menu.

```swift
CommandGroup(replacing: .newItem) {
    Button("New Note") { /* ... */ }
        .keyboardShortcut("n")
}

CommandGroup(before: .help) {
    Button("Keyboard Shortcuts…") { /* ... */ }
}
```

### `CommandGroupPlacement` Full Table

| Placement | Default menu location | Typical use |
|-----------|------------------------|-------------|
| `.appInfo` | App menu, top (About) | About panel replacement |
| `.appSettings` | App menu (Settings…) | Custom preferences entry point — usually left to the `Settings` scene default |
| `.appVisibility` | App menu (Hide/Hide Others/Show All) | Rarely customized |
| `.appTermination` | App menu, bottom (Quit) | Custom quit confirmation logic |
| `.systemServices` | App menu (Services) | Services submenu — rarely touched directly |
| `.newItem` | File menu, top (New/Open) | Custom document creation flows |
| `.importExport` | File menu (Import/Export) | Format-specific import/export commands |
| `.saveItem` | File menu (Save/Save As/Revert) | Document save variants |
| `.printItem` | File menu, bottom (Print) | Custom print/export-to-PDF |
| `.undoRedo` | Edit menu, top | Custom undo manager wiring |
| `.pasteboard` | Edit menu (Cut/Copy/Paste) | Custom pasteboard type handling |
| `.textEditing` | Edit menu (Find, Spelling) | Find bar / spell-check customization |
| `.textFormatting` | Format menu | Rich-text formatting commands |
| `.toolbar` | View menu (toolbar visibility toggles) | Rarely customized |
| `.sidebar` | View menu (sidebar toggle) | Rarely customized |
| `.windowArrangement` | Window menu (Minimize/Zoom/Arrange) | Custom window-layout commands |
| `.windowList` | Window menu, bottom (open window list) | Rarely customized |
| `.help` | Help menu | App-specific help entries, keyboard shortcut cheat sheets |

**When NOT to use `CommandGroup(replacing:)`:** if you only need to *add* an item near an existing one, use `.before`/`.after` — `.replacing` removes the system default items entirely, including ones users expect (e.g. replacing `.newItem` drops the standard "Open Recent" submenu unless you rebuild it).

---

## 3. HIG Standard Menu Structure

| Menu | Free for the system (do not rebuild) | Must be built by the app |
|------|----------------------------------------|----------------------------|
| **AppName** | About, Services, Hide/Hide Others/Show All, Quit | Settings… (if using `Settings` scene, wired automatically), custom app-info items |
| **File** | New Window (from `WindowGroup`), Close | New (document type), Open, Open Recent, Save/Save As/Revert/Duplicate, Print, document-specific import/export |
| **Edit** | Undo/Redo (free when using `UndoManager`/`NSTextView`-backed fields), Cut/Copy/Paste/Select All (free for standard text controls) | Find (custom find UI), app-specific edit actions |
| **Format** | — (entire menu is app-defined) | Font, text/rich-content formatting — only include this menu if the app edits formatted content |
| **View** | Toolbar/Sidebar visibility toggles (free when using `.toolbar`/`NavigationSplitView`) | Custom view-mode toggles, zoom |
| **Window** | Minimize, Zoom, Bring All to Front, open-window list (all free from scene infrastructure) | — (rarely needs additions) |
| **Help** | Search field (Spotlight-for-help, see §10) | App-specific help menu items |

Do not port an iOS tab-bar / navigation-title mental model onto this structure — macOS menu commands are the primary discoverability surface for actions that don't fit a toolbar button.

---

## 4. Keyboard Shortcut Conventions

| Shortcut | Reserved for | Do not repurpose |
|----------|---------------|--------------------|
| ⌘N | New (document/window) | — |
| ⌘O | Open | — |
| ⌘S | Save | — |
| ⌘⇧S | Save As | — |
| ⌘W | Close window | — |
| ⌘⇧W | Close all windows (convention, not system-enforced) | — |
| ⌘Q | Quit | — |
| ⌘, | Settings/Preferences | — |
| ⌘Z / ⌘⇧Z | Undo / Redo | — |
| ⌘X / ⌘C / ⌘V | Cut / Copy / Paste | — |
| ⌘A | Select All | — |
| ⌘F | Find | — |
| ⌘P | Print | — |
| ⌘⌥ combos with system-reserved letters (Q, H, M, Tab) | Reserved by macOS (Quit, Hide, Minimize, App Switcher) | Never bind these — SwiftUI does not stop you, but the OS may intercept first |

```swift
Button("New Note") { /* ... */ }
    .keyboardShortcut("n", modifiers: .command)          // ⌘N

Button("New Folder") { /* ... */ }
    .keyboardShortcut("n", modifiers: [.command, .shift]) // ⌘⇧N
```

`.keyboardShortcut(_:modifiers:)` defaults `modifiers` to `.command` — pass `[]` explicitly for a shortcut with no ⌘ (rare, and generally discouraged outside game/tool-palette contexts since it collides with text input).

---

## 5. Focused-Value-Driven Enable/Disable

Commands should disable themselves when there's no valid target, driven by what's focused rather than global app state — this keeps the menu correct across multiple windows.

```swift
private struct CurrentNoteKey: FocusedValueKey {
    typealias Value = Note
}

extension FocusedValues {
    var currentNote: Note? {
        get { self[CurrentNoteKey.self] }
        set { self[CurrentNoteKey.self] = newValue }
    }
}

// In the detail view that owns the concept of "current note":
struct NoteDetailView: View {
    let note: Note
    var body: some View {
        Text(note.title)
            .focusedSceneValue(\.currentNote, note)
    }
}

// In Commands:
struct NoteCommands: Commands {
    @FocusedValue(\.currentNote) private var currentNote

    var body: some Commands {
        CommandMenu("Note") {
            Button("Duplicate") { currentNote?.duplicate() }
                .disabled(currentNote == nil)
        }
    }
}
```

`focusedSceneValue` publishes at scene scope (survives even when no specific subview has keyboard focus) — prefer it over `focusedValue` for document-level "what is the user working on" state; reserve `focusedValue` for view-local focus (e.g. which table row is selected).

---

## 6. Contextual Menus — `.contextMenu`

```swift
List(notes) { note in
    Text(note.title)
        .contextMenu {
            Button("Rename") { /* ... */ }
            Button("Delete", role: .destructive) { /* ... */ }
        }
}
```

Contextual (right-click) menus are a supplement, not a replacement, for main-menu commands — every contextual action a power user needs regularly should also be reachable from the menu bar with a keyboard shortcut. `.contextMenu(forSelectionType:menu:primaryAction:)` (macOS 13+) drives the menu from a `List`/`Table` selection set instead of a single row.

---

## 7. `MenuBarExtra` Interaction Rules

Scene setup lives in `reference/scenes.md` §5 — this section covers interaction conventions once the scene exists.

- `.menu` style items behave like standard menu items: click to invoke, no persistent hover state beyond system menu highlighting.
- `.window` style content must supply its own dismiss trigger (e.g. a close button, or dismissing on the relevant action) — clicking outside the popover dismisses it, but there is no system-provided "Done" affordance.
- Do not nest a `MenuBarExtra` `.window`-style popover more than one level deep with further popovers — this is disorienting and not a native macOS pattern.
- If the app also has regular windows, keep `MenuBarExtra` commands consistent with the main menu (same labels, same keyboard shortcuts where both are reachable) rather than diverging vocabulary.

---

## 8. Help Menu & Spotlight-for-Help

The Help menu automatically gets a search field (Apple calls this "Spotlight for Help" / "Help Search") that searches the app's *actual menu items* by title and highlights them with an animated pointer — this works automatically for any menu item with a title, no extra registration needed for menu search.

```swift
CommandGroup(replacing: .help) {
    Button("NotesApp Help") {
        NSWorkspace.shared.open(URL(string: "https://example.com/help")!)
    }
    Divider()
    Button("Report an Issue…") { /* ... */ }
}
```

Only replace `.help` when adding app-specific help links — the search-field behavior itself is not something the app configures, it is derived from the live menu item tree.

---

## 9. Localization Concerns

- Menu item titles, `CommandMenu` names, and `.contextMenu` labels are `LocalizedStringKey` by default when passed as string literals — ensure `Localizable.strings`/`.xcstrings` entries exist for every command title.
- Keyboard shortcut *letters* should not be blindly translated — `.keyboardShortcut("n")` should generally stay tied to the semantic action; when localizing to a language with a different keyboard layout convention, verify the shortcut is still reachable and doesn't collide with a system shortcut in that locale.
- Menu structure order (File/Edit/View/Window/Help) is fixed by the OS per Mac HIG regardless of locale — do not reorder top-level menus for RTL languages; only text direction and item order *within* a menu adapts.
- Test with "Show Non-localized Strings" or a pseudo-localization pass to catch hard-coded English strings inside `Commands` closures, which is a common miss since command titles are easy to write inline rather than via a strings catalog.

---

## Sources

- [Commands | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/commands)
- [CommandGroupPlacement | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/commandgroupplacement) (accessed 2026-07)
- [CommandMenu | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/commandmenu)
- [FocusedValueKey | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/focusedvaluekey)
- [SwiftUI FocusedValue, macOS Menus, and the Responder Chain — philz.blog](https://philz.blog/swiftui-focusedvalue-macos-menus-and-the-responder-chain/)
- [Commands in SwiftUI — Swift with Majid](https://swiftwithmajid.com/2020/11/24/commands-in-swiftui/)
- [MenuBarExtra | Apple Developer Documentation](https://developer.apple.com/documentation/SwiftUI/MenuBarExtra) (accessed 2026-07)
- Mac HIG — Menus (`reference/mac-hig.md` for full chrome/pointer/shortcut audit criteria)
