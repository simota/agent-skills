# osascript & Cross-Language Integration

`osascript` runs AppleScript and JXA from the shell, scripts, and other languages. Prefer files/heredocs over fragile inline one-liners.

## Invocation forms

```bash
# Inline AppleScript
osascript -e 'tell application "Safari" to get URL of front document'

# Multi-line via -e (each line a separate -e)
osascript -e 'tell application "Finder"' -e 'get count of items of desktop' -e 'end tell'

# Script file
osascript automation.applescript

# JXA
osascript -l JavaScript -e 'Application("Safari").windows[0].currentTab.url()'

# JXA REPL (interactive)
osascript -il JavaScript
```

## Shebang scripts

```applescript
#!/usr/bin/osascript
-- chmod +x notify.applescript  →  ./notify.applescript
display notification "Build done" with title "CI"
```

```javascript
#!/usr/bin/osascript -l JavaScript
const app = Application.currentApplication();
app.includeStandardAdditions = true;
app.displayNotification("Build done", { withTitle: "CI" });
```

## Heredoc (reproducible multi-line from shell)

```bash
osascript <<'APPLESCRIPT'
tell application "Music"
    if player state is playing then pause
end tell
APPLESCRIPT
```

Use a **quoted** heredoc delimiter (`'APPLESCRIPT'`) to stop the shell from expanding `$` and backticks inside the script.

## Passing arguments & capturing output

```bash
# Args arrive as `on run argv`
osascript greet.applescript "World"
```
```applescript
on run argv
    return "Hello, " & (item 1 of argv)
end run
```

- **stdout**: the script's `return` value is printed to stdout.
- **exit code**: a script `error` yields a non-zero exit; trap in shell with `if ! osascript … ; then`.
- **stderr**: errors print to stderr — capture with `2>`.

## From Python

```python
import subprocess

def run_osascript(script: str) -> str:
    # Never interpolate untrusted input into `script` — for dynamic values use a
    # script file with `on run argv` and pass them as separate args (below).
    p = subprocess.run(["osascript", "-e", script],
                       capture_output=True, text=True)
    if p.returncode != 0:
        # stderr carries the full error string, e.g.
        # "execution error: Not authorized to send Apple events to … (-1743)"
        raise RuntimeError(p.stderr.strip())
    return p.stdout.strip()

url = run_osascript('tell application "Safari" to get URL of front document')
```

The PyPI `osascript` package wraps this (`run()` returns code/stdout/stderr) but is lightly maintained — `subprocess` is the dependency-free path.

## From Node.js

```js
const { execFile } = require("node:child_process");

function osa(script) {
  return new Promise((resolve, reject) => {
    execFile("osascript", ["-e", script], (err, stdout, stderr) =>
      err ? reject(new Error(stderr || err.message)) : resolve(stdout.trim()));
  });
}
await osa('tell application "Music" to playpause');
```

`node-osascript` exists but `child_process.execFile` (no shell, avoids injection) is the safer default. **Never** build osascript strings from untrusted input via a shell — pass as a discrete arg.

## Quoting cheatsheet

- Shell single-quote the whole `-e` payload; use AppleScript's own `"` inside.
- For dynamic values, pass via `argv` / `on run`, not string concatenation, to avoid quoting bugs and injection.
