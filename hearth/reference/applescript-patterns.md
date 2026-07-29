# AppleScript Core Patterns

Foundational idioms and per-app recipes. Prefer dictionary terms over UI scripting always.

## Reading an app's dictionary (sdef)

Before scripting an unfamiliar app, inspect its scripting dictionary:

```bash
# Dump the scripting definition to inspect supported terms
sdef /System/Applications/Mail.app | less
# Or open the dictionary in Script Editor: File > Open Dictionary…
osascript -e 'tell application "System Events" to get name of every application process'
```

If `sdef` returns little or nothing, the app is non- or partially-scriptable → see `ui-scripting.md`.

## Structure: tell blocks

```applescript
tell application "Finder"
    set selectedItems to selection as alias list
    repeat with anItem in selectedItems
        set name of anItem to "renamed-" & (name of anItem)
    end repeat
end tell
```

- Keep one `tell application "X"` per app. Nesting `tell` to a *second* app inside the first triggers a separate TCC consent — scope deliberately.
- Use `tell application "System Events"` only for UI scripting or process/OS-level queries.

## Error handling

```applescript
try
    tell application "Mail" to send theMessage
on error errMsg number errNum
    if errNum is -1743 then
        return "Automation permission denied. Grant in System Settings > Privacy & Security > Automation."
    end if
    error errMsg number errNum -- re-raise unknown errors
end try
```

## Per-app recipes

### Finder
```applescript
tell application "Finder"
    set deskItems to count of items of desktop
    set frontPath to (target of front Finder window) as alias
end tell
```

### Safari (front-tab URL)
```applescript
tell application "Safari" to set u to URL of front document
-- JXA equivalent: Application('Safari').windows[0].currentTab.url()
-- ('URL' in the dictionary bridges to url() in JXA — JXA lowercases all-caps acronyms)
```

### Mail (compose, do not auto-send unless confirmed)
```applescript
tell application "Mail"
    set m to make new outgoing message with properties {subject:"Hi", content:"Body", visible:true}
    tell m to make new to recipient with properties {address:"a@example.com"}
    -- send m   -- DESTRUCTIVE: gate behind confirmation/dry-run
end tell
```

### Notes
```applescript
tell application "Notes"
    tell account "iCloud"
        make new note at folder "Notes" with properties {name:"Title", body:"<div>HTML body</div>"}
    end tell
end tell
```

### Calendar
```applescript
tell application "Calendar"
    tell calendar "Home"
        make new event with properties {summary:"Standup", start date:(current date), end date:(current date) + 30 * minutes}
    end tell
end tell
```

### Music
```applescript
tell application "Music"
    set currentTrack to name of current track
    playpause
end tell
```

### System / clipboard / notifications
```applescript
set the clipboard to "copied text"
display notification "Done" with title "Hearth" sound name "Glass"
-- display notification needs Notifications enabled for the running app
-- (Terminal / Script Editor) in System Settings > Notifications, or it silently no-ops
do shell script "echo hello"   -- StandardAdditions, runs in-process
```

## Hub-app glue (multi-app workflow)

Pick one "hub" tell block as the orchestration owner and pass plain values (strings, lists, dates) between app blocks — never share live app object references across `tell` boundaries.

```applescript
-- Read in one app, act in another, passing only a string
tell application "Safari" to set theURL to URL of front document
tell application "Notes" to tell account "iCloud" to ¬
    make new note at folder "Notes" with properties {name:"Saved link", body:theURL}
```
