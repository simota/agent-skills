# Wire this repository into each CLI's skills directory.
# The repo is the single source of truth; each of its top-level skill directories
# is symlinked into the CLI directory individually, so all three CLIs read one
# working tree instead of separate clones.
#
# Per-entry, not whole-repo: the CLI directory stays a real directory, so skills
# it already carries that this repo does not are left untouched. A name that
# already exists there as a real path is never overwritten — it is skipped and
# reported, and resolving the collision is a manual decision.
#
# Only top-level directories are linked (hidden ones excluded), which covers the
# skills plus `_common/` and `_templates/`: SKILL.md cross-references and the
# inspection scripts resolve through the link to the repo root.
#
# Prerequisite: the repo must already live outside ~/.claude, ~/.codex, ~/.gemini.
# `make link` refuses to link a CLI directory to itself.

REPO       := $(CURDIR)
CLAUDE_DIR := $(HOME)/.claude/skills
CODEX_DIR  := $(HOME)/.agents/skills
AGY_DIR    := $(HOME)/.gemini/antigravity-cli/skills
export REPO CLAUDE_DIR CODEX_DIR AGY_DIR

.DEFAULT_GOAL := help

.PHONY: help link unlink status validate test check hooks \
	link-claude link-codex link-agy \
	unlink-claude unlink-codex unlink-agy

help:
	@echo "make link           symlink this repo's skills into claude / codex / agy"
	@echo "make link-claude    $$CLAUDE_DIR"
	@echo "make link-codex     $$CODEX_DIR"
	@echo "make link-agy       $$AGY_DIR"
	@echo "make unlink[-*]     remove only this installer's links; other skills stay"
	@echo "make status         show the current state of all three"
	@echo ""
	@echo "make validate       run every checker at blocking severity"
	@echo "make test           run all repository regression tests"
	@echo "make check          validate + test — what CI runs"
	@echo "make hooks          install the pre-commit hook that runs make validate"
	@echo ""
	@echo "repo                $$REPO"

# $(1) = exported CLI directory variable. Creates it if absent, then links each top-level
# repo directory into it. Never deletes or overwrites anything it did not create:
# the only removals are links into this repo whose target the repo has dropped.
define do_link
set -e; r=$$(cd "$$REPO" && pwd -P); t="$${$(1)}"; p=$$(dirname "$$t"); \
if [ ! -d "$$p" ] && [ "$(1)" = "CODEX_DIR" ] && [ "$$t" = "$$HOME/.agents/skills" ] && [ -d "$$HOME/.codex" ]; then \
  h=$$(cd "$$HOME" && pwd -P); \
  case "$$h/.agents" in "$$r"|"$$r"/*) echo "ERROR   $$t is inside this repo — refusing to create skill root"; exit 1;; esac; \
  mkdir -p "$$p"; \
fi; \
if [ ! -d "$$p" ]; then echo "skip    $$t — $$p does not exist"; exit 0; fi; \
p=$$(cd "$$p" && pwd -P); \
case "$$p/$$(basename "$$t")" in "$$r"|"$$r"/*) \
  echo "ERROR   $$t is inside this repo — move the repo to an external path first"; exit 1;; esac; \
if [ -L "$$t" ]; then \
  l=$$(readlink "$$t"); \
  if [ "$$l" = "$$r" ]; then rm "$$t"; echo "note    $$t was a whole-repo symlink — replacing it with a directory"; \
  else echo "ERROR   $$t is a symlink to $$l — remove it, then re-run"; exit 1; fi; \
elif [ -e "$$t" ] && [ ! -d "$$t" ]; then echo "ERROR   $$t exists and is not a directory"; exit 1; fi; \
mkdir -p "$$t"; \
case "$$(cd "$$t" && pwd -P)" in "$$r"|"$$r"/*) \
  echo "ERROR   $$t is inside this repo — move the repo to an external path first"; exit 1;; esac; \
nl=0; nk=0; ns=0; np=0; \
for s in "$$r"/*/; do \
  name=$$(basename "$$s"); d="$$t/$$name"; \
  if [ -L "$$d" ]; then \
    if [ "$$(readlink "$$d")" = "$$r/$$name" ]; then nk=$$((nk + 1)); \
    else echo "  skip    $$name — symlink to $$(readlink "$$d")"; ns=$$((ns + 1)); fi; \
  elif [ -e "$$d" ]; then echo "  skip    $$name — real path already there"; ns=$$((ns + 1)); \
  else ln -s "$$r/$$name" "$$d"; nl=$$((nl + 1)); fi; \
done; \
for d in "$$t"/*; do \
  [ -L "$$d" ] || continue; \
  if [ "$$(readlink "$$d")" = "$$r/$$(basename "$$d")" ]; then \
    [ -e "$$d" ] || { rm "$$d"; echo "  prune   $$(basename "$$d") — no longer in the repo"; np=$$((np + 1)); }; \
  fi; \
done; \
echo "linked  $$t — $$nl new, $$nk already linked, $$ns skipped, $$np pruned"
endef

# Removes only the canonical per-entry symlinks created by do_link. A textual
# repo prefix alone also matches aliases and paths escaping through `..`.
define do_unlink
set -e; r=$$(cd "$$REPO" && pwd -P); t="$${$(1)}"; \
p=$$(dirname "$$t"); \
if [ -d "$$p" ]; then \
  p=$$(cd "$$p" && pwd -P); \
  case "$$p/$$(basename "$$t")" in "$$r"|"$$r"/*) \
    echo "ERROR   $$t is inside this repo — refusing to unlink source files"; exit 1;; esac; \
fi; \
if [ -L "$$t" ]; then \
  l=$$(readlink "$$t"); \
  if [ "$$l" = "$$r" ]; then rm "$$t" && echo "unlink  $$t (whole-repo symlink)"; \
  else echo "skip    $$t — symlink to $$l"; fi; \
elif [ ! -d "$$t" ]; then echo "skip    $$t — missing"; \
else \
  case "$$(cd "$$t" && pwd -P)" in "$$r"|"$$r"/*) \
    echo "ERROR   $$t is inside this repo — refusing to unlink source files"; exit 1;; esac; \
  n=0; \
  for d in "$$t"/*; do \
    [ -L "$$d" ] || continue; \
    if [ "$$(readlink "$$d")" = "$$r/$$(basename "$$d")" ]; then rm "$$d"; n=$$((n + 1)); fi; \
  done; \
  echo "unlink  $$t — $$n removed, $$(ls -A "$$t" | wc -l | tr -d " ") entries left"; fi
endef

link: link-claude link-codex link-agy
unlink: unlink-claude unlink-codex unlink-agy

link-claude:
	@$(call do_link,CLAUDE_DIR)
link-codex:
	@$(call do_link,CODEX_DIR)
link-agy:
	@$(call do_link,AGY_DIR)

unlink-claude:
	@$(call do_unlink,CLAUDE_DIR)
unlink-codex:
	@$(call do_unlink,CODEX_DIR)
unlink-agy:
	@$(call do_unlink,AGY_DIR)

status:
	@set -e; r=$$(cd "$$REPO" && pwd -P); total=$$(ls -d "$$r"/*/ | wc -l | tr -d " "); \
	echo "repo    $$r ($$total linkable directories)"; \
	for t in "$$CLAUDE_DIR" "$$CODEX_DIR" "$$AGY_DIR"; do \
	  if [ -L "$$t" ]; then echo "symlink $$t -> $$(readlink "$$t")"; \
	  elif [ -d "$$t" ]; then \
	    n=0; \
	    for d in "$$t"/*; do \
	      [ -L "$$d" ] || continue; \
	      if [ -d "$$d" ] && [ "$$(readlink "$$d")" = "$$r/$$(basename "$$d")" ]; then n=$$((n + 1)); fi; \
	    done; \
	    echo "dir     $$t — $$n/$$total linked, $$(ls -A "$$t" | wc -l | tr -d " ") entries total"; \
	  else echo "none    $$t"; fi; \
	done


# ---------------------------------------------------------------------------
# Checks.
#
# CI runs these on pull requests and pushes to main. The optional local hook
# runs the same checks before a commit, so failures can be caught before push.
# ---------------------------------------------------------------------------

SCRIPTS := $(REPO)/_common/scripts
export SCRIPTS

validate:
	@python3 "$$SCRIPTS/lint-frontmatter.py" --severity error
	@python3 "$$SCRIPTS/lint-frontmatter.py" --severity error --paths "$(REPO)/.claude/skills"
	@python3 "$$SCRIPTS/lint-project-local.py" --severity error
	@python3 "$$SCRIPTS/validate-recipes.py" --severity error
	@python3 "$$SCRIPTS/routing-oracle.py" --severity error
	@python3 "$$SCRIPTS/lint-instructions.py" --severity error
	@python3 "$$SCRIPTS/lint-contracts.py" --severity error
	@python3 "$$SCRIPTS/lint-lessons.py" --severity error
	@python3 "$$SCRIPTS/task-battery-check.py" --severity error
	@if hook=$$(git rev-parse --git-path hooks/pre-commit 2>/dev/null) && [ -x "$$hook" ]; then echo "hooks on"; else \
	  echo "hooks off — run 'make hooks' so these run without being remembered"; fi

# A checker nobody has watched fail is indistinguishable from one that returns
# zero unconditionally. Slower than `validate` because cases exercise broken
# repositories and command-line tools, so the hook runs it when executable
# code, its templates, or the check infrastructure changes — see `hooks` below.
test:
	@python3 -m unittest discover -s "$$SCRIPTS" -p 'test_*.py'

check: validate test

hooks:
	@set -e; hook=$$(git rev-parse --git-path hooks/pre-commit); \
	if [ -L "$$hook" ] || { [ -e "$$hook" ] && ! grep -Fqx '# installed by `make hooks`' "$$hook"; }; then \
	  echo "ERROR   $$hook already exists — preserve or integrate your custom hook before installing"; exit 1; fi; \
	mkdir -p "$$(dirname "$$hook")"; \
	printf '%s\n' \
	  '#!/bin/sh' \
	  '# installed by `make hooks`' \
	  '# Validate the corpus always; run regression tests when executable code,' \
	  '# its templates, or the check infrastructure changes.' \
	  'set -e' \
	  'repo=$$(git rev-parse --show-toplevel)' \
	  'changed=$$(git -C "$$repo" diff --cached --name-only -- _common/scripts/ launch/scripts/ launch/templates/ _templates/learning-loop-kit/_scripts/ .github/workflows/ index.html Makefile requirements-checks.txt)' \
	  '# Check exactly what will be committed, preserving unstaged and untracked work.' \
	  'snapshot=$$(python3 -c '\''import tempfile; print(tempfile.mkdtemp(prefix="agent-skills-index."))'\'')' \
	  'trap '\''rm -rf "$$snapshot"'\'' EXIT' \
	  'trap '\''exit 129'\'' HUP' \
	  'trap '\''exit 130'\'' INT' \
	  'trap '\''exit 143'\'' TERM' \
	  'git -C "$$repo" checkout-index --all --prefix="$$snapshot/"' \
	  'unset $$(git -C "$$repo" rev-parse --local-env-vars)' \
	  'if [ -n "$$changed" ]; then' \
	  '  make -C "$$snapshot" --no-print-directory check' \
	  'else' \
	  '  make -C "$$snapshot" --no-print-directory validate' \
	  'fi' \
	  > "$$hook"; \
	chmod +x "$$hook"; \
	echo "installed $$hook"
