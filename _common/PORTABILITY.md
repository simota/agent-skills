# Portability Guidelines (BSD/GNU Cross-Platform)

> **Tier:** `domain` — activates when the task's subject matches. Precedence: `_common/OPERATIONAL.md` § Contract Precedence.

All scripts and code examples in skill references must run on both **macOS (BSD coreutils)** and **Linux (GNU coreutils)**. CI pipelines typically run on Linux; developers often use macOS. A command that silently differs or fails on one platform is a latent bug.

**Decision Rule:** Write POSIX-portable if possible. When POSIX is insufficient, provide a BSD/GNU dual-path fallback. Never write GNU-only or BSD-only code in shared examples without a fallback.

---

## Approved Portable Helpers

Copy these verbatim into scripts that need cross-platform behavior.

### `sha256_hash()` — Portable SHA-256 (BSD/GNU)

```bash
# Portable SHA-256 hash (BSD shasum / GNU sha256sum)
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$@"
  else
    echo "[ERROR] sha256sum/shasum not found" >&2
    return 1
  fi
}
```

Usage: `sha256_hash file.txt | awk '{print $1}'`

---

### `file_mtime()` — Portable file modification time (epoch seconds)

```bash
# Portable file mtime in epoch seconds (BSD stat -f / GNU stat -c)
file_mtime() {
  stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null || echo 0
}
```

Usage: `age=$(( $(date +%s) - $(file_mtime "$file") ))`

---

### `run_with_timeout()` — Portable timeout (BSD/GNU/perl fallback)

```bash
# Portable timeout: GNU timeout → gtimeout (coreutils via Homebrew) → perl alarm
# Exit codes: 124 on timeout, otherwise child exit code.
run_with_timeout() {
  local sec="$1"; shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "${sec}" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "${sec}" "$@"
  else
    perl -e '
      use strict; use warnings;
      my $timeout = shift @ARGV;
      my $pid = fork();
      if (!defined $pid) { die "fork: $!" }
      if ($pid == 0) { exec { $ARGV[0] } @ARGV or die "exec: $!" }
      local $SIG{ALRM} = sub { kill 9, $pid; waitpid($pid, 0); exit 124 };
      alarm $timeout;
      waitpid($pid, 0);
      exit($? >> 8);
    ' "${sec}" "$@"
  fi
}
```

---

### `find_dirs_with_file()` — Portable find for parent directories

```bash
# Portable alternative to find -printf '%h\0'
# Lists unique parent directories containing <filename>, NUL-separated.
find_dirs_with_file() {
  local root="$1" filename="$2"
  find "${root}" -name "${filename}" -type f \
    | while IFS= read -r f; do dirname "$f"; done \
    | sort -u
}
```

Note: The GNU-only `find -printf '%h\0'` has no POSIX equivalent. Use the `dirname` loop above.

---

### `pcre_search()` — Portable PCRE grep fallback

```bash
# Portable PCRE search: grep -P → perl → python3
# Prints matching file paths (like grep -rl).
pcre_search() {
  local pattern="$1"; shift  # remaining args are paths
  if grep -P "" /dev/null >/dev/null 2>&1; then
    # grep supports -P (GNU grep or macOS grep with PCRE)
    grep -rPl "${pattern}" "$@"
  else
    # Fall back to perl
    perl -le '
      my $pat = shift;
      for my $f (@ARGV) {
        open my $fh, "<", $f or next;
        while (<$fh>) { if (/$pat/) { print $f; last } }
      }
    ' "${pattern}" "$@"
  fi
}
```

---

## BSD vs GNU vs Portable Reference Table

| Command | macOS BSD | Linux GNU | Portable alternative |
|---------|-----------|-----------|----------------------|
| `timeout N cmd` | Not available (use `gtimeout` or `brew install coreutils`) | `timeout N cmd` | `run_with_timeout N cmd` (helper above) |
| `sed -i 's/a/b/' f` | Requires empty string: `sed -i '' 's/a/b/' f` | `sed -i 's/a/b/' f` | `sed -i.bak 's/a/b/' f && rm f.bak` or write to a temp file |
| `stat -c %Y file` | Not supported | `stat -c %Y file` (mtime epoch) | `file_mtime file` (helper above) |
| `stat -f %m file` | `stat -f %m file` (mtime epoch) | Not supported | `file_mtime file` (helper above) |
| `sha256sum file` | Not available (use `shasum -a 256`) | `sha256sum file` | `sha256_hash file` (helper above) |
| `shasum -a 256 file` | `shasum -a 256 file` | Available on most distros, not guaranteed | `sha256_hash file` (helper above) |
| `find . -printf '%h\0'` | Not supported | `find . -printf '%h\0'` | `find_dirs_with_file` (helper above) |
| `date -d '1 day ago'` | Not supported | `date -d '1 day ago'` | `date -v-1d` (BSD) / branch on `uname` |
| `readlink -f file` | Not available pre-12.3 | `readlink -f file` | `python3 -c "import os; print(os.path.realpath('$f'))"` |
| `xargs -r` | Not supported (`-r` = no-op on empty) | `xargs -r` (skip if stdin empty) | `[ -s file ] && xargs ...` |
| `base64 -w0` | Not supported (default is no wrapping) | `base64 -w0` (no wrap) | `base64` (BSD wraps at 76; pipe through `tr -d '\n'` if needed) |
| `grep -P 'pcre'` | Not available (BSD grep has no PCRE) | `grep -P 'pcre'` | `pcre_search` (helper above) or `perl -ne` |
| `ls --color=auto` | Not supported (BSD ls flag is `-G`) | `ls --color=auto` | `if ls --color=auto / >/dev/null 2>&1; then alias ls='ls --color=auto'; else alias ls='ls -G'; fi` |
| `echo -e "text\n"` | Behavior is shell-dependent (`/bin/sh` may print `-e` literally) | Works in bash | `printf '%b\n' "text"` |

---

## Never Use (Prohibited Patterns)

These patterns break on at least one of macOS or Linux and must not appear in shared scripts or SKILL.md examples:

```
grep -P ...             # No POSIX; unavailable on stock macOS (BSD grep)
find ... -printf ...    # GNU find extension; not on macOS
stat -c ...             # GNU stat; use file_mtime() helper instead
stat -f ...             # BSD stat; use file_mtime() helper instead (alone)
shasum -a 256 ...       # BSD only; use sha256_hash() helper
sha256sum ...           # GNU only; use sha256_hash() helper
timeout N cmd           # GNU only; use run_with_timeout() helper
echo -e "..."           # Unreliable across shells; use printf '%b\n' "..."
sed -i 's/.../.../' f  # Fails on macOS (needs empty string arg); use temp file
date -d "..."           # GNU date; fails on macOS
readlink -f ...         # GNU coreutils; unreliable on macOS
xargs -r                # GNU only; use conditional [ -s ] && xargs
ls --color=auto         # GNU ls; use -G on macOS or branch
base64 -w0              # GNU only; use tr -d '\n' | base64 pattern
```

---

## Detection

Find prohibited patterns in the repository:

```bash
# Scan for non-portable commands in shell scripts and .md code blocks
grep -rn \
  -e 'grep -P' \
  -e 'find.*-printf' \
  -e 'stat -c ' \
  -e 'sha256sum' \
  -e 'shasum -a 256' \
  -e 'echo -e' \
  -e 'timeout [0-9]' \
  -e 'date -d' \
  -e 'readlink -f' \
  -e 'xargs -r' \
  -e 'ls --color' \
  -e 'base64 -w' \
  /path/to/skills/
```

Note: Many occurrences are intentional uses inside the `sha256_hash` or `run_with_timeout` helpers themselves — exclude those files when triaging.

---

## Integrating with Existing Scripts

Use the following `run_with_timeout()` (BSD/GNU/perl fallback) as the canonical pattern for new helpers:

```bash
# Canonical run_with_timeout pattern
run_with_timeout() {
  local sec="$1"; shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "${sec}" "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout "${sec}" "$@"
  else
    perl -e '...' "${sec}" "$@"
  fi
}
```

Apply the same `command -v` probe pattern for every platform-sensitive command.

---

## Related Files

- `_common/OPERATIONAL.md` — Shell command rules (BSD-default, portability guidance)
