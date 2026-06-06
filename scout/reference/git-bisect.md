# Scout Git Bisect Reference

**Purpose:** Commit-level regression isolation workflow and guardrails.
**Read when:** The issue looks like a regression and `git bisect` is faster than wider code archaeology.

## Contents

- Basic workflow
- Finding the good commit
- Automation
- Skip and recovery rules
- Best practices

## Basic Bisect Workflow

```bash
git bisect start
git bisect bad
git bisect good <commit-hash>

# test current checkout
git bisect good   # if bug is NOT present
git bisect bad    # if bug IS present

git bisect reset
```

## Finding the Good Commit

```bash
git log --oneline -20
git log --oneline --since="2024-01-01" --until="2024-01-15"
git log --oneline --author="name"
git tag --list
```

## Automated Bisect

```bash
git bisect start
git bisect bad HEAD
git bisect good v1.0.0
git bisect run ./test-bug.sh
```

Rules for `test-bug.sh`:

- exit `0` when the current commit is good
- exit non-zero when the bug is present
- keep the verification method identical on every step

## Complex Cases

```bash
git bisect skip
git bisect start -- src/components/
git bisect log > bisect-log.txt
git bisect replay bisect-log.txt
```

## Best Practices

- Ensure the bug is reproducible before starting.
- Prefer a quick deterministic test.
- Stash or commit local changes first.
- Use `skip` for commits that do not build.
- Verify the final culprit commit before reporting it as causal.
