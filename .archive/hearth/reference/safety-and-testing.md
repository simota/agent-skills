# Safety, Dry-Run & Testing

Every Hearth `automate` script must be safe to re-run and safe to test. Destructive actions are gated; read paths are validated before delivery.

## Destructive operation catalog

Treat these as destructive — gate behind a dry-run flag or explicit confirmation:

- Mail/Messages: `send`
- Finder/filesystem: `delete`, `move … to trash`, `empty trash`, overwriting files
- Notes/Calendar/Reminders/Contacts: `delete`, bulk `set`/overwrite
- Music/Photos: `delete`, library mutation
- `do shell script` with `rm`, `mv`, `>`, `sudo`, network calls
- System Events: `keystroke`/`click` that commits an irreversible UI action

## Dry-run pattern

```applescript
property DRY_RUN : true  -- default safe; flipped by argv below

on run argv
    if argv contains "--apply" then set DRY_RUN to false
    -- … call your handlers …
end run

on archiveMessage(msg)
    if DRY_RUN then
        log "[DRY-RUN] would archive: " & (subject of msg)
    else
        tell application "Mail" to set mailbox of msg to mailbox "Archive"
    end if
end archiveMessage
```

For shell callers, the flag must be parsed in `on run argv` (osascript has **no** built-in `--dry-run` flag — every token after the script name is raw argv):

```bash
osascript clean.applescript            # DRY_RUN stays true; prints intended actions
osascript clean.applescript --apply    # parsed by `on run argv` → performs them
```

## Idempotency

Re-running must not duplicate or corrupt. Check-before-create:

```applescript
tell application "Notes" to tell account "iCloud"
    if not (exists note "Daily Log") then
        make new note with properties {name:"Daily Log"}
    end if
end tell
```

- Creating events/notes/files: check existence (by name/id) first, or use a stable identifier.
- Toggles (`playpause`): prefer explicit state checks (`if player state is playing`) over blind toggles when the outcome must be deterministic.

## Validating before delivery

1. **Read-only first.** Run the query/read parts with `osascript` and confirm the values are real.
2. **Stub destructive calls.** Keep `DRY_RUN` true; confirm the log lines describe the right actions on the right targets.
3. **Permission smoke test.** Trigger each `tell` once to confirm consent is grantable and `-1743` is handled.
4. **Idempotency check.** Run twice; assert no duplicates / no drift.
5. **Exit codes.** For shell/CI use, confirm errors yield non-zero exit and clear stderr.

## Delivery checklist (attach to every automation)

- [ ] Target apps + scriptability (dictionary vs UI scripting) listed
- [ ] Required TCC permissions named with grant path
- [ ] Destructive actions identified and gated
- [ ] Dry-run validated; idempotency confirmed
- [ ] Exact run command provided
- [ ] No secrets in plaintext (use Keychain via `security find-generic-password`)
- [ ] macOS-version caveats noted if any (e.g., Tahoe Music/TV/Finder regressions)
