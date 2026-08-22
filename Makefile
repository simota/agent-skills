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
CODEX_DIR  := $(HOME)/.codex/skills
AGY_DIR    := $(HOME)/.gemini/antigravity-cli/skills

.DEFAULT_GOAL := help

.PHONY: help link unlink status validate test check hooks \
	link-claude link-codex link-agy \
	unlink-claude unlink-codex unlink-agy

help:
	@echo "make link           symlink this repo's skills into claude / codex / agy"
	@echo "make link-claude    $(CLAUDE_DIR)"
	@echo "make link-codex     $(CODEX_DIR)"
	@echo "make link-agy       $(AGY_DIR)"
	@echo "make unlink[-*]     remove only the links into this repo; other skills stay"
	@echo "make status         show the current state of all three"
	@echo ""
	@echo "make validate       run every checker at blocking severity"
	@echo "make test           prove the checkers catch things (slower)"
	@echo "make check          validate + test — what CI runs"
	@echo "make hooks          install the pre-commit hook that runs make validate"
	@echo ""
	@echo "repo                $(REPO)"

# $(1) = CLI skills directory. Creates it if absent, then links each top-level
# repo directory into it. Never deletes or overwrites anything it did not create:
# the only removals are links into this repo whose target the repo has dropped.
define do_link
r=$$(cd "$(REPO)" && pwd -P); t="$(1)"; p=$$(dirname "$$t"); \
if [ ! -d "$$p" ]; then echo "skip    $$t — $$p does not exist"; exit 0; fi; \
if [ -L "$$t" ]; then \
  l=$$(readlink "$$t"); \
  if [ "$$l" = "$$r" ]; then rm "$$t"; echo "note    $$t was a whole-repo symlink — replacing it with a directory"; \
  else echo "ERROR   $$t is a symlink to $$l — remove it, then re-run"; exit 1; fi; \
elif [ -e "$$t" ] && [ ! -d "$$t" ]; then echo "ERROR   $$t exists and is not a directory"; exit 1; fi; \
mkdir -p "$$t"; \
if [ "$$(cd "$$t" && pwd -P)" = "$$r" ]; then \
  echo "ERROR   $$t is this repo itself — move the repo to an external path first"; exit 1; fi; \
nl=0; nk=0; ns=0; np=0; \
for s in "$$r"/*/; do \
  name=$$(basename "$$s"); d="$$t/$$name"; \
  if [ -L "$$d" ]; then \
    if [ "$$(readlink "$$d")" = "$$r/$$name" ]; then nk=$$((nk + 1)); \
    else echo "  skip    $$name — symlink to $$(readlink "$$d")"; ns=$$((ns + 1)); fi; \
  elif [ -e "$$d" ]; then echo "  skip    $$name — real path already there"; ns=$$((ns + 1)); \
  else ln -sfn "$$r/$$name" "$$d"; nl=$$((nl + 1)); fi; \
done; \
for d in "$$t"/*; do \
  [ -L "$$d" ] || continue; \
  case "$$(readlink "$$d")" in "$$r"/*) \
    [ -e "$$d" ] || { rm "$$d"; echo "  prune   $$(basename "$$d") — no longer in the repo"; np=$$((np + 1)); };; \
  esac; \
done; \
echo "linked  $$t — $$nl new, $$nk already linked, $$ns skipped, $$np pruned"
endef

# Removes only symlinks that point into this repo. Anything else in the CLI
# directory — real skills, links elsewhere — is counted and left alone.
define do_unlink
r=$$(cd "$(REPO)" && pwd -P); t="$(1)"; \
if [ -L "$$t" ]; then \
  l=$$(readlink "$$t"); \
  if [ "$$l" = "$$r" ]; then rm "$$t" && echo "unlink  $$t (whole-repo symlink)"; \
  else echo "skip    $$t — symlink to $$l"; fi; \
elif [ ! -d "$$t" ]; then echo "skip    $$t — missing"; \
else \
  n=0; \
  for d in "$$t"/*; do \
    [ -L "$$d" ] || continue; \
    case "$$(readlink "$$d")" in "$$r"/*) rm "$$d"; n=$$((n + 1));; esac; \
  done; \
  echo "unlink  $$t — $$n removed, $$(ls -A "$$t" | wc -l | tr -d " ") entries left"; fi
endef

link: link-claude link-codex link-agy
unlink: unlink-claude unlink-codex unlink-agy

link-claude:
	@$(call do_link,$(CLAUDE_DIR))
link-codex:
	@$(call do_link,$(CODEX_DIR))
link-agy:
	@$(call do_link,$(AGY_DIR))

unlink-claude:
	@$(call do_unlink,$(CLAUDE_DIR))
unlink-codex:
	@$(call do_unlink,$(CODEX_DIR))
unlink-agy:
	@$(call do_unlink,$(AGY_DIR))

status:
	@r=$$(cd "$(REPO)" && pwd -P); total=$$(ls -d "$$r"/*/ | wc -l | tr -d " "); \
	echo "repo    $$r ($$total linkable directories)"; \
	for t in "$(CLAUDE_DIR)" "$(CODEX_DIR)" "$(AGY_DIR)"; do \
	  if [ -L "$$t" ]; then echo "symlink $$t -> $$(readlink "$$t")"; \
	  elif [ -d "$$t" ]; then \
	    n=0; \
	    for d in "$$t"/*; do \
	      [ -L "$$d" ] || continue; \
	      case "$$(readlink "$$d")" in "$$r"/*) n=$$((n + 1));; esac; \
	    done; \
	    echo "dir     $$t — $$n/$$total linked, $$(ls -A "$$t" | wc -l | tr -d " ") entries total"; \
	  else echo "none    $$t"; fi; \
	done


# ---------------------------------------------------------------------------
# Checks.
#
# CI runs these too, but its hard-fail steps are gated on `pull_request` and this
# repository commits to main directly — so on the path actually used, CI reports
# and the hook is what blocks. `make hooks` is therefore not optional tooling;
# it is where the budgets are enforced (`_common/VALUES.md` §2).
# ---------------------------------------------------------------------------

SCRIPTS := $(REPO)/_common/scripts

validate:
	@python3 $(SCRIPTS)/lint-frontmatter.py --severity error
	@python3 $(SCRIPTS)/validate-recipes.py --severity error
	@python3 $(SCRIPTS)/routing-oracle.py --severity error
	@python3 $(SCRIPTS)/lint-instructions.py --severity error
	@python3 $(SCRIPTS)/lint-contracts.py --severity error
	@python3 $(SCRIPTS)/lint-lessons.py --severity error
	@python3 $(SCRIPTS)/task-battery-check.py --severity error
	@if [ -x "$(REPO)/.git/hooks/pre-commit" ]; then echo "hooks on"; else \
	  echo "hooks off — run 'make hooks' so these run without being remembered"; fi

# A checker nobody has watched fail is indistinguishable from one that returns
# zero unconditionally. Slower than `validate` because each case runs the real
# script against a broken copy of the repository, so the hook runs it only when
# a checker changed — see `hooks` below.
test:
	@python3 $(SCRIPTS)/test_checkers.py

check: validate test

hooks:
	@mkdir -p "$(REPO)/.git/hooks"
	@printf '%s\n' \
	  '#!/bin/sh' \
	  '# installed by `make hooks`' \
	  '# Checkers always. The checker *tests* only when a checker changed: they' \
	  '# cost ~20s, and a commit that slow is one people start bypassing.' \
	  'set -e' \
	  'repo="$(REPO)"' \
	  'if git diff --cached --name-only | grep -q "^_common/scripts/"; then' \
	  '  exec make -C "$$repo" --no-print-directory check' \
	  'fi' \
	  'exec make -C "$$repo" --no-print-directory validate' \
	  > "$(REPO)/.git/hooks/pre-commit"
	@chmod +x "$(REPO)/.git/hooks/pre-commit"
	@echo "installed $(REPO)/.git/hooks/pre-commit"
