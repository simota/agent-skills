# JXA — JavaScript for Automation

JXA (introduced OS X Yosemite, 2014) is the official JavaScript binding for the Open Scripting Architecture. It sits on the **same Apple Events foundation** as AppleScript — an *alternative*, not a replacement, and not "near-native" (it cannot do arbitrary Cocoa/C without ObjC bridging caveats).

## When to prefer JXA over AppleScript

| Prefer JXA | Prefer AppleScript |
|------------|--------------------|
| Heavy string/JSON/array manipulation | Readable app `tell` workflows |
| Caller/team is JS-fluent | Broadest example/Stack Overflow coverage |
| Reusing JS logic or `JSON.parse/stringify` | Apps documented primarily in AppleScript |
| Programmatic object/property access | Natural-language readability for handoff |

## Idioms

```javascript
// Get an app reference
const Safari = Application("Safari");
const url = Safari.windows[0].currentTab.url();

// Standard Additions (notifications, dialogs, shell)
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.displayNotification("Done", { withTitle: "Hearth" });
app.doShellScript("echo hi");

// System Events (UI scripting / processes)
const se = Application("System Events");
const procs = se.processes.name();

// Iterate Finder selection
const Finder = Application("Finder");
const sel = Finder.selection();
sel.forEach(item => console.log(item.name()));
```

Key differences from browser/Node JS:
- App methods are **function calls**: `win.currentTab.url()` not `win.currentTab.url`.
- `Application("X")` is lazy — no Apple Event sent until you call a property/method.
- Use `ObjC.import('Foundation')` for Cocoa bridging, but keep it minimal — this is where "JXA can do anything native" claims overreach.

## Converting AppleScript ↔ JXA (behavior-preserving)

```applescript
tell application "Safari" to set u to URL of front document
```
↔
```javascript
const u = Application("Safari").windows[0].currentTab.url();
```

Conversion rules:
1. `tell application "X" … end tell` → `const X = Application("X")` then method calls.
2. Property reads become **calls**: `name of x` → `x.name()`.
3. `make new T at container with properties {…}` → `container.T({...}).make()` (root objects) or `app.make({new: 'T', withProperties: {…}, at: container})`. The `.push()`-into-collection shorthand works for *some* apps (Notes, Reminders) but is **not** the general rule — it breaks for Mail/Calendar; prefer `.make()`.
4. StandardAdditions verbs (`display dialog`, `do shell script`) require `includeStandardAdditions = true`.
5. Flag any term with no clean equivalent rather than silently dropping behavior.
