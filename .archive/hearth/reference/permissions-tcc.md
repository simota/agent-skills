# Permissions & TCC (Transparency, Consent, and Control)

Since macOS Mojave (2018), Apple Events between apps are gated by TCC. Designing around consent is half the job of a reliable automation.

## The consent model

- Permission is per **(source app, target app)** pair. The first time process A sends an Apple Event to app B, the user gets one prompt: *"A wants to control B."*
- Denial returns AppleScript **error `-1743`** (`errAEEventNotPermitted`).
- Granted/denied state lives in **System Settings → Privacy & Security → Automation** (the user can revoke later).
- **StandardAdditions** verbs (`display dialog`, `do shell script`, `display notification`, clipboard) run **in-process** and do *not* prompt — *unless* they appear inside a `tell application "Other"` block, which scopes them to that app.

## Permission surfaces

| Capability | Where to grant | Triggered by |
|------------|----------------|--------------|
| Controlling another app | Privacy & Security → **Automation** | `tell application "X"` to a different app |
| UI scripting (clicks/keystrokes) | Privacy & Security → **Accessibility** | `System Events` Processes Suite |
| Reading protected files (Mail, Messages, Desktop, Documents) | Privacy & Security → **Full Disk Access** | file reads in protected locations |

## Handling -1743 gracefully

```applescript
try
    tell application "Notes" to set n to count of notes
on error errMsg number errNum
    if errNum is -1743 then
        return "Grant Automation permission: System Settings > Privacy & Security > Automation > [this app] > enable Notes."
    end if
    error errMsg number errNum
end try
```

## Design rules

1. **Name the consent pairs up front.** List every (source → target) prompt the user will see before they run the script — surprise prompts read as malware.
2. **Minimize target apps.** Each extra `tell` to a new app is another prompt and another revocable permission. Drop apps the task doesn't need.
3. **Keep StandardAdditions in-process.** Put `display dialog` / `do shell script` at the top level, not inside another app's `tell`, to avoid needless prompts.
4. **Never instruct disabling TCC/SIP.** "Just turn off the protection" is not a fix — design within consent. Resetting a stuck grant is `tccutil reset AppleEvents` (the user runs it knowingly), not disabling enforcement. The service name is case-sensitive; if that string is rejected on your macOS version, try `tccutil reset Automation`.
5. **Unattended runs need pre-granted consent.** A launchd/cron/login-item automation cannot answer a prompt — the permission must already be granted (or, in managed fleets, pre-approved via MDM PPPC profiles, which is out of Hearth's scope to deploy).

## Security note

- TCC and the Apple Events consent path have a history of bypass CVEs (e.g., CVE-2025-43530 was reported as an Apple Events-related TCC bypass — verify the exact mechanism and fixed version against [Apple Security Releases](https://support.apple.com/en-us/100100) before citing specifics). Keep macOS patched; never design an automation that *depends* on a TCC bypass.
- Don't author automations whose intent is to evade consent, surveil, or access data without authorization. See `_common/SECURITY.md`.
