# Dotfile Management and Security Anti-Patterns

Purpose: Read this when auditing dotfile repositories, secret handling, bootstrap safety, repository layout, or multi-machine drift. Keep the `DF-*` and `RS-*` identifiers intact in findings and handoffs.

## Contents

- [Dotfile-management anti-patterns](#dotfile-management-anti-patterns)
- [Secret-management anti-patterns](#secret-management-anti-patterns)
- [Common secret categories](#common-secret-categories)
- [Repository-structure anti-patterns](#repository-structure-anti-patterns)
- [Multi-machine traps](#multi-machine-traps)
- [How Hearth uses this reference](#how-hearth-uses-this-reference)

## Dotfile-Management Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `DF-01` | Secrets in dotfiles | Tokens and passwords leak into Git history | Move secrets to `local.zsh`, `.envrc`, a secret manager, or encrypted storage |
| `DF-02` | No `.gitignore` strategy | Sensitive paths appear as addable changes | Prefer allowlist-style tracking and keep secret locations ignored |
| `DF-03` | Secret residue in Git history | Deleting the current line does not remove the leaked secret | Revoke immediately, rewrite history, force-push, then audit all history |
| `DF-04` | No backup before change | Config damage is hard to recover | Run `cp file file.bak.$(date +%Y%m%d)` before every edit |
| `DF-05` | Wrong tool for scale | Single-machine setups get over-engineered; multi-machine setups drift | Use `stow` for single-machine, `chezmoi` for multi-machine, bare Git for minimal cases |
| `DF-06` | Stow symlink conflicts | Existing files block adoption | Use `stow --adopt` or move files manually before restowing |
| `DF-07` | No bootstrap script | New-machine setup remains manual and error-prone and can easily exceed `1+ hour` | Provide `install.sh` or `Makefile` for repeatable setup |

## Secret-Management Anti-Patterns

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| Hard-coded API keys | Public repos expose live credentials | Keep secrets out of tracked config and load them from local or secret-backed files |
| SSH keys in the repo | Private keys become recoverable forever | Never track `~/.ssh/`; use encrypted secret tooling if needed |
| Shell history in the repo | Passwords, internal URLs, and tokens leak indirectly | Ignore history files explicitly |
| No pre-commit secret scanning | Leaks reach remote repos before review | Add `gitleaks` or `detect-secrets` to the commit path |
| Delete-only remediation | The secret stays in prior commits | Use `git filter-repo` or equivalent after revocation |
| Credentials in `.gitconfig` | Auth data spreads with dotfile sync | Use credential helpers or `[include]` / `[includeIf]` for local separation |

### Leak-Response Order

```text
Revoke immediately -> rewrite history -> force push -> verify all history
```

## Common Secret Categories

| Category | Example | Detection hint |
|----------|---------|----------------|
| Cloud keys | `AWS_ACCESS_KEY_ID`, service-account JSON | `AKIA[0-9A-Z]{16}` |
| API tokens | GitHub, Slack, Stripe | `ghp_`, `xoxb-`, `sk_live_` |
| SSH private keys | `id_rsa`, `id_ed25519` | `-----BEGIN.*PRIVATE KEY-----` |
| Database URLs | `DATABASE_URL`, `MONGODB_URI` | `://.*:.*@` |
| Personal data | Emails, internal hosts | Email and hostname patterns |

## Repository-Structure Anti-Patterns

| Code | Anti-pattern | Risk | Countermeasure |
|------|--------------|------|----------------|
| `RS-01` | Flat repository structure | Per-tool management becomes difficult | Split into package directories such as `zsh/`, `nvim/`, `ghostty/` |
| `RS-02` | Missing usage notes | Reprovisioning becomes guesswork later | Keep the bootstrap path and structure discoverable in the managed files or scripts |
| `RS-03` | No XDG directory mapping | `stow` packages cannot mirror actual target locations | Mirror XDG paths such as `nvim/.config/nvim/` |
| `RS-04` | Brewfile drift | Installed tools diverge from the tracked file | Run `brew bundle dump` or `brew bundle check` regularly |

## Multi-Machine Traps

| Pattern | Risk | Countermeasure |
|---------|------|----------------|
| Manual sync | Machine drift accumulates over time | Use `chezmoi`, `yadm`, or another tracked sync model |
| No template strategy | OS or host differences end up buried in shell conditionals | Use templates or machine-specific files |
| Work/personal config collision | Work-only identity leaks into personal repos | Use `.gitconfig [includeIf "gitdir:~/work/"]` or equivalent separation |
| Non-idempotent setup | Running bootstrap twice breaks the environment | Make setup scripts safe to re-run |

## How Hearth Uses This Reference

```text
SCAN:
  Screen for DF-01..07, secret patterns, and repository-layout issues

PLAN:
  Choose the smallest safe migration or hardening step

CRAFT:
  Design repository layout, bootstrap scripts, and secret separation

VERIFY:
  Run secret scanning, repository checks, and reproducibility checks
```

### Required Gates

- A detected secret pattern must produce an explicit warning and a remediation path.
- Missing `.gitignore`, missing bootstrap, or flat Stow layout should be called out as fixable structural debt.
- Run `gitleaks` or equivalent secret scanning during verification.
- `Brewfile` drift should trigger `brew bundle check` or `brew bundle dump`.
