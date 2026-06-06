# CLI Config File Design Reference

**Purpose:** Design a predictable, debuggable config layer for CLIs: precedence chain, file format, discovery path, schema validation, and secrets handling. The config surface is part of the CLI contract — breaking it silently corrupts scripts and CI.
**Read when:** Adding `config` subcommand or config-file support to a CLI, picking between YAML/TOML/JSON/INI, following XDG Base Directory, adding schema validation, or auditing secrets-in-config risks.

## Scope Boundary

- **Anvil `config`**: CLI tool config-file design, precedence chain, discovery path, XDG compliance, schema validation, `config get/set/edit/validate` subcommand UX.
- **Builder (elsewhere)**: feature/business-logic layer that consumes the loaded config struct (e.g., reads `database.url` and opens a connection).
- **Hearth (elsewhere)**: personal dotfile authoring for the user's shell/editor/terminal (zsh/tmux/neovim/ghostty) — not CLI app config.
- **Gear (elsewhere)**: CI pipeline env var injection, secrets provisioning, Docker config mounting.
- **Launch (elsewhere)**: breaking-change deprecation policy for config keys across releases.

If the request is "how should my CLI discover and validate its config?" → `config`. If it is "tune my personal `.zshrc`" → Hearth. If it is "inject SECRET into CI runs" → Gear.

## Precedence Chain (Canonical Order)

```
flag  >  env var  >  project config  >  user config  >  system config  >  default
```

Higher overrides lower. The CLI must expose the resolved source for every key:

```
$ myapp config get database.url --show-source
postgres://...   (source: env MYAPP_DATABASE_URL)
```

Without source visibility users cannot debug "why is this value X?" — a common support burden. Provide a `config debug` or `config show --sources` subcommand.

## File Format Trade-offs

| Format | Strengths | Weaknesses | Pick when |
|--------|-----------|-----------|-----------|
| TOML | Unambiguous, comments, typed, standard Rust/Python ecosystem | Less familiar to JS devs, weak nested list ergonomics | CLI is Rust/Python; config is mostly flat key/value |
| YAML | Familiar, nested structures, comments | Norway problem (`no` → false), indentation errors, tag injection CVEs | DevOps-adjacent CLIs (k8s/helm tooling) where users already know YAML |
| JSON | Universal parser, schema-validation mature (JSON Schema) | No comments, no trailing commas, verbose | Machine-generated config, interop with other tools |
| JSON5 / JSONC | JSON + comments + trailing commas | Non-standard, extra dependency | When JSON familiarity matters but humans edit it |
| INI | Simple, low dependency | No nesting, no lists, ambiguous types | Tiny config with flat keys; `.gitconfig`-style |

Default recommendation: **TOML** for new Rust/Python CLIs, **JSON5** for Node, **YAML** only when the user base already expects it.

## Discovery Order (XDG Base Directory Spec)

Unix:

```
1. $MYAPP_CONFIG            (explicit override)
2. --config <path>          (flag)
3. ./.myapp.toml            (project-local)
4. $XDG_CONFIG_HOME/myapp/config.toml       (default: ~/.config/myapp/config.toml)
5. /etc/xdg/myapp/config.toml               (system, optional)
6. Built-in defaults
```

macOS: follow XDG (use `~/.config/myapp/`) — do not use `~/Library/Application Support/` unless the tool is a GUI. Most CLI tools (git, gh, kubectl) use XDG on macOS.

Windows:

```
1. %MYAPP_CONFIG%
2. --config <path>
3. .\.myapp.toml
4. %APPDATA%\myapp\config.toml   (roaming) or %LOCALAPPDATA% (machine-local)
5. Built-in defaults
```

Respect `$XDG_CONFIG_HOME` if set; only fall back to `~/.config/` if unset. Do not invent a new dotfile at the home root (`~/.myapprc`) for new tools — users accumulate clutter.

## RC vs `config.toml`

| Pattern | When | Notes |
|---------|------|-------|
| `~/.myapprc` | Legacy parity with long-standing tools (`~/.bashrc`) | Avoid for new tools; pollutes `$HOME` |
| `~/.config/myapp/config.toml` | New tools following XDG | Users can back up `~/.config/` as one unit |
| `$PWD/.myapp.toml` | Project-scoped override | Must be committed-safe (no secrets) |
| `pyproject.toml` / `package.json` section | CLI is a dev tool inside an existing language ecosystem | Lower friction than a new file; Ruff, Black, Biome follow this |

Project-local config should layer on top of user-level — never replace it wholesale. Merge semantics: deep-merge objects, replace arrays (the default most users expect).

## Schema Validation

Unvalidated config produces the worst error messages. Pick one:

- **TOML + serde (Rust)**: `#[derive(Deserialize)]` gives typed parsing with line-number errors.
- **JSON Schema (any language)**: ship a `schema.json`, validate at load time, show the failing JSON pointer.
- **Pydantic / dataclasses (Python)**: field validators with informative errors.
- **Zod / valibot (Node)**: structural parsing + shape inference.

Minimum acceptable behaviour on invalid config:

1. Non-zero exit (code 2: usage error).
2. Error message names the file, key path, and expected type.
3. `myapp config validate` runs the same check without running the command.

Ship a `config init` that emits a commented template — discoverability beats documentation.

## Secrets-in-Config Anti-patterns

Config files land in dotfiles repos, backup systems, and support bundles. Treat them as public.

- ❌ Plaintext API keys, database passwords, or OAuth tokens in `config.toml`.
- ❌ Instructing users to commit the config file with tokens in place.
- ❌ Reading secrets via `config get` into shell history without `--unmask` explicitness.
- ❌ Logging the whole config struct at startup (secrets leak to CI logs).
- ✅ Reference secrets by env var: `token = "${env:MYAPP_TOKEN}"` with explicit interpolation documented.
- ✅ Offer a system keychain adapter (`keyring` on Python, `keyring-rs` on Rust, `keytar` on Node).
- ✅ Redact secret-typed fields in `config show`, `config debug`, and doctor output by default.
- ✅ Support `_file` suffix convention: `token_file = "/run/secrets/myapp_token"` reads from disk, mirroring Docker/systemd.

## `config` Subcommand UX

```
myapp config                          # show effective merged config (redacted)
myapp config get <key>                # one value, with --show-source
myapp config set <key> <value>        # write to user-level file by default
myapp config unset <key>
myapp config edit                     # open $EDITOR on the user file
myapp config path                     # print resolved file path (scriptable)
myapp config validate [path]          # schema-check a file
myapp config init                     # emit commented template
```

`set` must round-trip (preserve comments/order if the format allows). For TOML use `toml_edit`, for YAML use `ruamel.yaml`; plain serde/json dumps destroy comments.

## Anti-patterns

- Silently creating `~/.myapp/` on first run without telling the user.
- Ignoring `$XDG_CONFIG_HOME` and hard-coding `~/.config/`.
- Merging project config by replacing instead of layering — users lose user-level preferences.
- Validating config lazily inside feature code, producing cryptic runtime errors mid-command.
- Treating environment variables as a special second-class path (no precedence doc, no `show-source`).
- Shipping a new dotfile at `$HOME` root in 2026.
- Refusing to start when the config has an unknown key — breaks forward compatibility; warn instead.

## Handoff

- **To Builder**: typed config struct with resolution source per field.
- **To Launch**: deprecation plan when a config key is renamed (keep old key reading for one minor version, warn on use).
- **To Gear**: env-var naming convention (`MYAPP_<KEY>` with `__` as nesting separator) for CI injection.
- **To `completion`**: dynamic completion for `config get`/`set` keys from the loaded schema.
- **To `pkg`**: default system config install path (`/etc/xdg/myapp/config.toml`) for deb/rpm post-install.
