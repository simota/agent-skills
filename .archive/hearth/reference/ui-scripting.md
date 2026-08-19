# UI (GUI) Scripting

Last resort for apps with no/partial AppleScript dictionary. Simulates clicks and keystrokes via the **System Events Processes Suite** over the macOS **Accessibility framework**.

## When (and when not) to use

- ✅ App exposes no scriptable term for the action you need.
- ✅ A one-off menu/button action that has no dictionary equivalent.
- ❌ A dictionary term exists — always prefer it (UI scripting breaks on layout/locale changes, window state, and OS updates).

## Prerequisite: Accessibility permission

UI scripting is **disabled by default**. The controlling process (e.g., Terminal, Script Editor, or the app running osascript) must be added to **System Settings → Privacy & Security → Accessibility** (admin auth required). Without it, calls fail.

```applescript
-- Guarded check before UI scripting
tell application "System Events"
    if not (UI elements enabled) then
        return "Enable Accessibility for this app in System Settings > Privacy & Security > Accessibility."
    end if
end tell
```

⚠️ On Ventura and later, `UI elements enabled` reflects the legacy global switch; per-bundle Accessibility grants may still block UI scripting even when it returns `true`. Treat it as a hint, not a guarantee — wrap actual UI calls in `try … on error` and surface the error code as the authoritative diagnostic.

## Core patterns

```applescript
tell application "TextEdit" to activate
tell application "System Events"
    tell process "TextEdit"
        -- Click a menu item by path
        click menu item "New" of menu "File" of menu bar 1
        -- Keystroke + modifiers
        keystroke "s" using {command down}
        -- Target a button in the frontmost window
        click button "Save" of sheet 1 of window 1
        -- Read UI to assert state before acting
        set winTitle to title of window 1
    end tell
end tell
```

## Reliability rules

1. **Activate first.** UI scripting acts on the frontmost app — `activate` the target, and add a short settle delay only if needed (`delay 0.2`), not blind long sleeps.
2. **Query before you click.** Read `exists`, `title`, or `value` to confirm the element is present rather than clicking by blind coordinates.
3. **Avoid hardcoded coordinates.** Reference elements by role/name/index, never screen pixels.
4. **Localize-aware.** Menu/button names differ by system language — parameterize or detect them.
5. **Inspect the hierarchy.** Use Accessibility Inspector (Xcode) or `entire contents of window 1` to discover element paths.

```applescript
-- Discover element structure
tell application "System Events" to tell process "Safari"
    entire contents of window 1
end tell
```
