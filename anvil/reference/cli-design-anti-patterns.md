# CLI Design Anti-Patterns

**Purpose:** Failure patterns for flags, arguments, errors, output, help text, and interactive CLI flows.
**Read when:** Auditing a CLI contract, debugging confusing command behavior, or hardening interface UX before release.

## Contents

- Seven Flag Design Anti-Patterns
- Argument Handling Anti-Patterns
- Error Message Anti-Patterns
- Output Design Anti-Patterns
- Help Text Anti-Patterns
- Interactive Mode Anti-Patterns
- How To Use With Anvil

## 1. Seven Flag Design Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **CD-01** | **Namespace Pollution** | Assigning single-letter flags to rarely used options | Meaningless short flags like `-x` and `-z` multiply, and future flag additions become difficult | Reserve short flags for frequent options only; keep the rest long-form (`--long-name`) |
| **CD-02** | **Secret Exposure via Flags** | Accepting secrets via flags such as `--token=xxx` | `ps` or process inspection exposes credentials | Use environment variables, config files, stdin, or a `--token-file` pattern |
| **CD-03** | **Position-Dependent Flags** | A flag means different things before and after a subcommand | `app --verbose run` behaves differently from `app run --verbose` | Interpret flags consistently regardless of position |
| **CD-04** | **Ambiguous Abbreviation** | Allowing arbitrary subcommand abbreviations | `app d` could mean `delete` or `deploy`; future commands create breaking changes | Disallow implicit abbreviation or define explicit aliases |
| **CD-05** | **Flag Overload** | Packing 20+ flags into one command | `--help` no longer fits on one screen; users cannot find the right flag | Split into subcommands, move advanced options into config, and use progressive disclosure |
| **CD-06** | **Missing Standard Flags** | Omitting common flags such as `--help`, `--version`, `--verbose`, or `--quiet` | Users cannot rely on familiar CLI conventions | Always provide standard flags: `-h`, `-V`, `-v`, `-q`, `--no-color`, `--json` |
| **CD-07** | **Boolean Negation Gap** | Shipping `--color` without `--no-color` | Users cannot disable default behavior; CI output breaks | Provide `--no-xxx` for every meaningful boolean flag |

---

## 2. Argument Handling Anti-Patterns

```text
Argument design traps:

  ❌ Multiple Positional Args:
    → Using 3+ positional arguments such as `app <source> <destination> <format>`
    → Order is hard to memorize and mistakes are hard to spot
    → Fix: Keep at most two positional args; convert the rest to flags
      Example: `app <source> --dest X --format Y`

  ❌ Implicit Stdin:
    → Waiting on stdin silently even when attached to a TTY
    → Users think the CLI is hung
    → Fix: Detect TTY; if stdin is required, explain it and exit quickly

  ❌ No Dash Convention:
    → Failing to support `-` for stdin/stdout
    → The CLI cannot participate in shell pipelines
    → Fix: Accept `-` anywhere a file path is expected

  ❌ Catch-All Subcommand:
    → Guessing the closest subcommand when input is unknown
    → The wrong command can run unintentionally
    → Fix: Fail explicitly and add a `Did you mean ...?` suggestion
```

---

## 3. Error Message Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **EM-01** | **Stack Trace Dump** | Showing a full stack trace by default | Errors print 20+ lines of internal details and hide the actionable message | Show a user-facing error only; gate stack traces behind `--debug` |
| **EM-02** | **No Actionable Suggestion** | Exiting with messages like `Error: invalid input` | Users do not know what to fix next | Include what failed, how to fix it, and where to get more detail |
| **EM-03** | **Stdout Pollution** | Printing errors to stdout | Pipelines treat error text as normal output | Send errors, warnings, and logs to stderr |
| **EM-04** | **Silent Failure** | Exiting without any visible error | Users miss the failure entirely and cannot debug it | Always emit an error message to stderr and return a non-zero exit code |
| **EM-05** | **Exit Code Anarchy** | Returning exit code `1` for every failure mode | Scripts cannot distinguish usage errors from dependency failures | Define exit codes by category: `1=general`, `2=usage`, `126=permission`, `127=missing command` |

---

## 4. Output Design Anti-Patterns

```text
Output formatting traps:

  ❌ One Format Fits All:
    → Only shipping decorated, human-readable output
    → Scripts and pipes cannot parse results
    → Fix: Add `--json` and switch output style based on TTY detection

  ❌ Color Without Escape Control:
    → Printing ANSI escapes into redirected output and pipes
    → Log files end up with `\e[31m` noise
    → Fix: Detect TTY, honor `NO_COLOR`, and support `--no-color`

  ❌ Animation in CI:
    → Showing spinners or progress bars in non-TTY environments
    → CI logs fill with control characters
    → Fix: Downgrade to simple line-based status output outside interactive terminals

  ❌ Verbose Default:
    → Dumping too much information on normal execution
    → Important information gets buried
    → Fix: Keep defaults concise; expand detail behind `--verbose`

  ❌ End-Truncation:
    → Placing the important summary at the top and noise at the end
    → The last visible terminal lines are meaningless
    → Fix: End with summary, status, and next actions
```

---

## 5. Help Text Anti-Patterns

```text
Help design traps:

  ❌ Help Dump:
    → `-h` prints every command and option in exhaustive detail
    → Output exceeds 100 lines and users cannot scan it
    → Fix: Keep `-h` concise, use `--help` or docs for the full reference

  ❌ No Examples:
    → Only describing flags without showing real usage
    → Users must guess the intended invocation
    → Fix: Put 2-3 practical examples near the top of help output

  ❌ Inconsistent Help:
    → `-h` and `--help` disagree
    → Users lose trust in the help system
    → Fix: Make them identical or define a clear short-vs-long split

  ❌ No Next Step:
    → Errors and completions never suggest what to do next
    → Users get stuck after each action
    → Fix: Recommend related commands and next steps

  ❌ Hidden Features:
    → Shipping undocumented flags or environment variables
    → Important capabilities are undiscoverable
    → Fix: Document all public flags and env vars, and offer shell completion
```

---

## 6. Interactive Mode Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **IM-01** | **Prompt in Pipe** | Showing interactive prompts while stdin is piped | Scripts hang and CI jobs stall | Detect TTY; in non-interactive mode, fail clearly or use safe defaults |
| **IM-02** | **No Bypass Flag** | Omitting `--yes` or `--no-input` | Automation cannot skip prompts | Provide `--yes` / `-y` to bypass prompts |
| **IM-03** | **Password Echo** | Displaying password input on screen | Sensitive input is exposed to shoulder surfing and logs | Disable terminal echo for secrets |
| **IM-04** | **No Escape** | Ignoring `Ctrl+C` during prompts | Users cannot cancel safely | Add signal handling and graceful exits |
| **IM-05** | **Destructive Default** | Defaulting destructive prompts to “yes” | A single Enter press triggers dangerous actions | Make destructive prompts default to “no” or require a confirmation string |

---

## 7. How To Use With Anvil

```text
Use within Anvil:
  1. Review CD-01 to CD-07 during BLUEPRINT to stress-test flag design
  2. Review argument handling and help text during CAST
  3. Review output and interactive mode during TEMPER
  4. Review error handling and exit codes during HARDEN

Quality gates:
  - 10+ short flags → likely namespace pollution (prevent CD-01)
  - Secrets accepted via flags → move to stdin, env vars, or files (prevent CD-02)
  - 3+ positional args → recommend flag conversion (prevent Multiple Positional Args)
  - Default stack traces on errors → limit to `--debug` (prevent EM-01)
  - Errors without fixes → add actionable suggestions (prevent EM-02)
  - Errors written to stdout → move them to stderr (prevent EM-03)
  - Prompts active in CI → add TTY detection and `--no-input` / `--yes` (prevent IM-01)
  - Destructive confirmation defaults to yes → switch to no and strengthen confirmation (prevent IM-05)
```

**Source:** [Command Line Interface Guidelines](https://clig.dev/) · [Atlassian: 10 Design Principles for Delightful CLIs](https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis) · [Better CLI](https://bettercli.org/) · [Shopify: CLI Error Handling](https://shopify.github.io/cli/cli/error_handling.html)
