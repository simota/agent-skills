# Personal Git Configuration Reference

Purpose: Read this when configuring personal Git — `~/.gitconfig` with aliases, editor, commit template, and credential helper; `~/.gitattributes` and `~/.gitignore_global`; `git-lfs` for binary assets; commit signing (GPG / SSH / Sigstore); local hooks via `core.hooksPath`; and `git-delta` / `git-absorb` integration. Hearth owns **your** global Git setup; team repo hygiene belongs elsewhere.

## Scope Boundary

- **Hearth `git`**: personal `~/.gitconfig`, global ignore, commit signing keys, delta/absorb/LFS client config, personal hooks under `core.hooksPath`.
- **Anvil (elsewhere)**: building Git-based CLI tools or custom subcommands.
- **Latch (elsewhere)**: Claude Code hooks — not Git hooks. "pre-commit hook" = Git; "PreToolUse hook" = Claude Code.
- **Gear (elsewhere)**: team CI commit checks, repo-level workflow enforcement, shared commitlint.
- **Grove (elsewhere)**: repo-committed `.gitattributes` / `.gitignore` / CODEOWNERS.

If the question is "what should I have in `~/.gitconfig`?" → `git`. If it is "what does the team repo require?" → Grove + Gear.

## Config Scope Model

| Scope | File | Flag |
|-------|------|------|
| System | `/etc/gitconfig` | `--system` |
| Global | `~/.gitconfig` or `$XDG_CONFIG_HOME/git/config` | `--global` |
| Local | `<repo>/.git/config` | `--local` |
| Conditional | via `includeIf` directive | — |

## Workflow

```
SCAN   →  detect git version, existing ~/.gitconfig, signing setup,
          credential helper, delta/absorb/git-lfs presence, XDG layout
PLAN   →  pick signing method (SSH/GPG/Sigstore), credential helper,
          decide includeIf split (work vs personal identity)
CRAFT  →  write ~/.gitconfig modularly, set global ignore + attributes,
          configure delta pager, wire core.hooksPath, register signing key
APPLY  →  back up ~/.gitconfig, apply, install git-lfs, set permissions
          (600 on signing keys, 644 on config)
VERIFY →  `git config --list --show-origin`, test commit + signature,
          LFS clone, delta renders diffs, credential helper returns tokens
```

## Minimal `~/.gitconfig`

```ini
[user]
  name = Your Name
  email = you@example.com
  signingkey = ~/.ssh/id_ed25519.pub

[core]
  editor = nvim
  pager = delta
  excludesfile = ~/.config/git/ignore
  attributesfile = ~/.config/git/attributes
  hooksPath = ~/.config/git/hooks

[init]
  defaultBranch = main
[pull]
  rebase = true
[push]
  default = current
  autoSetupRemote = true
[rebase]
  autoStash = true
  autoSquash = true

[commit]
  template = ~/.config/git/commit-template
  gpgsign = true
[tag]
  gpgsign = true
[gpg]
  format = ssh

[credential]
  helper = osxkeychain  # macOS; Linux: libsecret; Windows: manager

[interactive]
  diffFilter = delta --color-only
[delta]
  navigate = true
  line-numbers = true
[merge]
  conflictstyle = zdiff3
[diff]
  algorithm = histogram

[alias]
  st = status -sb
  lg = log --graph --oneline --decorate
  amend = commit --amend --no-edit
  fixup = commit --fixup
  absorb = !git-absorb --and-rebase
```

## Conditional Includes

```ini
[includeIf "gitdir:~/work/"]
  path = ~/.config/git/work.inc
[includeIf "gitdir:~/personal/"]
  path = ~/.config/git/personal.inc
```

Each include can override `user.email`, `user.signingkey`, and `commit.gpgsign` — avoid hard-coding a single email when operating under multiple identities.

## Global Ignore and Attributes

```gitignore
# ~/.config/git/ignore — editor/OS noise and secrets safety net
.DS_Store
*.swp
.vscode/
.idea/
.claude/cache/
.env
.env.*.local
*.pem
*.key
```

```gitattributes
# ~/.config/git/attributes
* text=auto eol=lf
*.{png,jpg,jpeg,gif,webp,pdf,zip,tar,gz,bz2,xz} binary
```

Repo-specific rules stay in-repo (Grove). Global rules cover editor/OS noise + secrets safety net only.

## Signing: SSH vs GPG vs Sigstore

| Method | Setup | Key reuse | When to pick |
|--------|-------|-----------|--------------|
| SSH | Low — reuse existing SSH key | Yes | Default on Git 2.34+, simplest modern path |
| GPG | High — keygen, trust web, agent | Separate key | Required by policy, air-gapped workflows |
| Sigstore / gitsign | Medium — OIDC, short-lived certs | No persistent key | Keyless CI / OSS workflows |

```ini
[gpg]
  format = ssh
[gpg "ssh"]
  allowedSignersFile = ~/.config/git/allowed_signers
[commit]
  gpgsign = true
```

Verify: `git log --show-signature -1`. GitHub "Unverified" means the SSH key is registered as auth-only — register it as a **signing key** separately.

## `git-lfs`, Hooks, `git-delta` / `git-absorb`

| Tool | Role | Hearth action |
|------|------|---------------|
| `git-lfs` | Binary asset tracking | `git lfs install` once; per-repo `.gitattributes` is Grove's concern |
| `core.hooksPath` | Global hook dir | `~/.config/git/hooks` with `pre-commit` running `gitleaks protect --staged` |
| `delta` | Syntax-highlighted diffs | `core.pager = delta` + `interactive.diffFilter` |
| `git-absorb` | Auto-`fixup!` into right historical commit | Alias `absorb`, run before `rebase -i --autosquash` |

Team-enforced hooks use the `pre-commit` framework in-repo (Gear / Grove). `core.hooksPath` is personal safety net, not policy.

## Credential Helper

| OS | Helper |
|----|--------|
| macOS | `osxkeychain` (Keychain) |
| Linux | `libsecret` (Secret Service) |
| Windows | `manager` (Credential Manager) |

Never use `credential.helper = store` — plaintext tokens on disk.

## Anti-Patterns

- `credential.helper = store` — plaintext tokens on disk.
- Hard-coding `user.email` globally with multiple identities — use `includeIf`.
- Signing with a GitHub auth-only key — signatures show "Unverified".
- Symlinking hooks into every repo's `.git/hooks/` — use `core.hooksPath` instead.
- Adding secret scanning only in CI — a pushed secret is already shared. Local `pre-commit` + CI is the right layering.
- Confusing `.gitconfig` hooks with `.claude/settings.json` hooks (Latch).
- Committing `~/.gitconfig` verbatim to a public dotfiles repo — emails / GPG key IDs become fingerprinting signals.

## Handoff

- Per-repo `.gitattributes` / `.gitignore` / CODEOWNERS → `Grove`.
- CI-side commit validation or release automation → `Gear`.
- Git-based CLI tool authoring → `Anvil`.
- Claude Code PreToolUse / PostToolUse hooks (not Git hooks) → `Latch`.
- Signing-key audit or rotation as part of a secret audit → `Sentinel` + Hearth `audit` recipe.
