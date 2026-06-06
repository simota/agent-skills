# Commit Conventions & Best Practices

Purpose: Preserve clean, atomic, conventional commits that support bisecting, changelog generation, and readable history.

## Contents

- Conventional Commits
- Atomic commit rules
- Signing guidance
- `commitlint` defaults
- Anti-patterns

## Conventional Commits

Format:

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

| Type | Purpose | SemVer effect |
|------|---------|---------------|
| `feat` | new feature | MINOR |
| `fix` | bug fix | PATCH |
| `docs` | documentation only | none |
| `style` | formatting without behavior change | none |
| `refactor` | restructuring without behavior change | none |
| `perf` | performance improvement | none |
| `test` | add or update tests | none |
| `build` | build system or dependency changes | none |
| `ci` | CI configuration changes | none |
| `chore` | maintenance work | none |
| `revert` | revert a previous commit | context-dependent |

Breaking changes:

```text
feat(api)!: remove deprecated endpoints

BREAKING CHANGE: The /v1/users endpoint has been removed.
Use /v2/users instead.
```

## Atomic Commit Rules

| Rule | Why it matters |
|------|----------------|
| one commit = one logical change | makes revert and review safer |
| each commit should build or pass the relevant checks | preserves bisectability |
| separate formatting from logic | avoids noisy reverts |
| keep subject concise | improves readability in Git tools |
| use imperative mood | matches common Git and changelog conventions |
| explain `why` in the body, not `what` | the diff already shows the `what` |

Preferred length guidance:
- subject target: `<= 50` characters when practical
- hard commitlint limit: `72`
- body line limit: `100`

## Signing Guidance

| Option | Use when | Notes |
|--------|----------|-------|
| `GPG` | broad forge support matters | more setup |
| `SSH` | GitHub/GitLab workflow and existing SSH keys | simpler, requires Git `2.34+` |

Example SSH signing setup:

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true
```

## `commitlint` Defaults

```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100],
  }
};
```

## Anti-Patterns

| Pattern | Problem | Safer alternative |
|---------|---------|-------------------|
| `Update file.rb` | file names are already in the diff | describe intent and impact |
| `Bugfix` or `fix stuff` | unclear scope | name the bug or subsystem |
| repeated `-m` one-liners | weak body quality | open an editor for multi-line messages |
| huge mixed commits | hard to bisect and revert | split into atomic commits |
| formatting + logic together | noisy history | commit separately |
| leftover `WIP` commits | obscures narrative | clean up with interactive rebase before sharing |
