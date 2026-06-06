# `/nexus pack` Subcommand

Meta-command that switches the active Claude Code skill profile by rewriting `~/.claude/settings.json` `skills` array from a `~/.claude/profiles/<name>.json` template.

Companion: `_common/SKILL_PACKS.md` (Pack definitions, profile catalog).

## When to Use

- User starts a new workstream and wants to scope skill listing to a domain (web / mobile / security / growth / infra / research / ai-eval / package-author).
- 148-skill default load causes routing confusion or context tax.
- User explicitly requests `/nexus pack <name>`.

## Forms

| Form | Behavior |
|------|----------|
| `/nexus pack` | Display current profile + list available profiles. No write. |
| `/nexus pack list` | Same as above (explicit). |
| `/nexus pack current` | Show only the active profile name. |
| `/nexus pack <name>` | Switch to `<name>`. **Confirms before writing.** |
| `/nexus pack reset` | Restore `skills: "all"`. |
| `/nexus pack restore` | Restore from the most recent backup. |

## Available `<name>` values

Discovered dynamically from `~/.claude/profiles/*.json`. Default-shipped profiles per `_common/SKILL_PACKS.md`:
`web` / `mobile` / `security` / `growth` / `infra` / `research` / `ai-eval` / `package-author` / `all`.

## Phase Contract

| Phase | Action |
|-------|--------|
| PARSE | Extract subcommand form (`list` / `current` / `<name>` / `reset` / `restore`) |
| LOOKUP | If `<name>` given, read `~/.claude/profiles/<name>.json`; validate `skills` field is an array or `"all"` |
| BACKUP | Copy `~/.claude/settings.json` → `~/.claude/settings.json.bak.<unix-timestamp>` (keep last 5) |
| DIFF | Read current `skills` value, compute the set diff against new profile, present to user |
| CONFIRM | `AskUserQuestion` — show diff summary (`+N`, `-M` skills), ask `Apply? [Y/n]` |
| WRITE | On Y, replace `skills` field in `~/.claude/settings.json` |
| NOTIFY | Tell user: "Restart Claude Code (`/exit` then relaunch) for the change to take effect. Verify with `/skills`." |

`/nexus pack list` and `/nexus pack current` skip BACKUP/CONFIRM/WRITE.

## Always

- **Backup before write.** Always create `settings.json.bak.<timestamp>` before any write. Keep the 5 most recent (delete older).
- **Validate profile JSON.** Reject malformed JSON, missing `skills` field, or `skills` value not in `("all" | array of strings)`.
- **Preserve all other settings.json keys.** Only the `skills` key is modified. Hooks, permissions, env, mcpServers, etc. must remain byte-identical except for that one key.
- **Confirm before write.** AskUserQuestion with the +/- diff is mandatory unless user explicitly invoked with `--no-confirm` (CLI affordance, not implemented yet).
- **Show restart instruction.** Claude Code does not hot-reload skill filters; instruct restart.
- **Use absolute path** `~/.claude/settings.json`, not relative.

## Never

- Modify `settings.json` without backup.
- Touch any key other than `skills` (e.g. don't change `permissions`, `hooks`).
- Auto-restart Claude Code (user must do it).
- Persist a profile that fails JSON validation.
- Skip the diff/confirm step in AUTORUN modes (this is a `## Ask First` operation regardless of mode).
- Delete `~/.claude/profiles/<name>.json` files (they are durable templates).

## Diff Presentation Format

```
## Pack switch: <current> → <new>

Adding (N):    skill_a, skill_b, skill_c, ...
Removing (M):  skill_x, skill_y, ...
Unchanged (K): [collapsed; show on request]

Apply? [Y/n]
```

## Implementation Sketch (Internal)

The Nexus skill executes this subcommand inline (no agent spawn — single trivial settings edit per Core Rule #3 exception (a)).

Pseudocode:
```python
profile_path = f"~/.claude/profiles/{name}.json"
profile = json.load(open(expanduser(profile_path)))
assert profile["skills"] == "all" or isinstance(profile["skills"], list)

ts = int(time.time())  # actual: from session start, not Date.now()
settings_path = expanduser("~/.claude/settings.json")
shutil.copy(settings_path, f"{settings_path}.bak.{ts}")

cleanup_old_backups(keep=5)

settings = json.load(open(settings_path))
old_skills = settings.get("skills", "all")
new_skills = profile["skills"]
diff = compute_diff(old_skills, new_skills)
# present diff via AskUserQuestion, await confirmation

settings["skills"] = new_skills
json.dump(settings, open(settings_path, "w"), indent=2)
print("Restart Claude Code to apply. Verify with /skills.")
```

In practice Nexus uses the Bash + Read + Edit tools to achieve the same effect (no Python required).

## Edge Cases

- **Profile file missing** → list available profiles and abort.
- **JSON parse error in settings.json** → abort with "settings.json is malformed; fix manually before retry".
- **User declines confirmation** → no write, no backup retained from this run.
- **Schema URL changed** → preserve `$schema` field verbatim.
- **`skills` is currently an unknown shape (object, etc.)** → treat as "all" for diff purposes; warn user.

## Cross-CLI Mapping

- **Codex CLI**: equivalent is `~/.codex/config.toml` (no skills filter at present, ignored — this subcommand is Claude Code only).
- **agy**: equivalent is `~/.gemini/antigravity-cli/settings.json` (skills filter status unknown — verify before extending).

## Future Work

- `--no-confirm` flag for scripting.
- Profile composition: `/nexus pack web+security` (union of two profiles).
- Per-project profile (`<repo>/.claude/profile.json`) overriding global.
- LEARN: track which packs the user actually uses, recommend default profile per workspace.
