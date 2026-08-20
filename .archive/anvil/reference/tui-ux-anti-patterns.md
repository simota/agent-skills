# TUI & Terminal UX Anti-Patterns

**Purpose:** Failure patterns for color, navigation, layout, progress indicators, and terminal accessibility.
**Read when:** Reviewing terminal UX, accessibility, keyboard flows, or non-TTY behavior before shipping a TUI.

## Contents

- Seven Color Management Anti-Patterns
- Keyboard Navigation Anti-Patterns
- Layout and Display Anti-Patterns
- Progress Display Anti-Patterns
- Accessibility Anti-Patterns
- How To Use With Anvil

## 1. Seven Color Management Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **TU-01** | **Color-Only Semantics** | Communicating state by color alone | Color-blind users and monochrome terminals lose the meaning of the UI | Pair color with icons or text such as `✓`, `✗`, and `⚠` |
| **TU-02** | **NO_COLOR Ignorance** | Ignoring the `NO_COLOR` environment variable | Accessibility preferences are bypassed and users lose control | Disable color output completely when `NO_COLOR` is set |
| **TU-03** | **True Color Assumption** | Assuming every terminal supports 24-bit color | Old terminals, remote shells, or SSH sessions render unreadable output | Fall back progressively: ANSI 16 colors → 256 colors → true color |
| **TU-04** | **Low Contrast Colors** | Using pale or low-contrast text colors | Text becomes unreadable, especially across light and dark themes | Target WCAG AA contrast (`4.5:1`) and avoid theme-dependent low-contrast palettes |
| **TU-05** | **ANSI Leak** | Emitting ANSI escapes into pipes and redirects | Log files contain `\e[31m` noise and grep results become polluted | Detect TTY with `isatty(stdout)` before enabling escapes |
| **TU-06** | **Hardcoded Colors** | Forcing colors that ignore the terminal theme | Light themes become unreadable and dark themes become blinding | Prefer ANSI semantic colors that follow terminal themes, or detect themes safely |
| **TU-07** | **Excessive Coloring** | Coloring everything until nothing stands out | Priority becomes unclear and output turns into visual noise | Use color only for meaningful states: errors, warnings, success, or emphasis |

---

## 2. Keyboard Navigation Anti-Patterns

```text
Keybinding design traps:

  ❌ Hotkey Overload:
    → Requiring users to memorize 100+ keybindings
    → Example: full Tig fluency demands a very large key vocabulary
    → Fix: bind only the most frequent actions and move the rest behind a command palette or menu

  ❌ Non-Standard Bindings:
    → Ignoring familiar vi/emacs conventions such as `j/k` or `Ctrl+N/P`
    → Navigation feels wrong compared with adjacent tools
    → Fix: support vi/emacs-compatible modes or accept both `hjkl` and arrow keys

  ❌ No Inline Hints:
    → Hiding keybindings in external docs only
    → Users cannot discover features in-context
    → Fix: surface hints inline, for example `[s]hop [a]ccount [q]uit`

  ❌ Context-Blind Help:
    → Showing every keybinding regardless of the current screen
    → The current action set is hard to find
    → Fix: show view-specific help only

  ❌ No Escape Path:
    → Making it unclear how to leave a modal or nested view
    → `q`, `Esc`, and `Ctrl+C` behave inconsistently
    → Fix: keep `Esc` / `q` as a consistent “go back” pattern

  ❌ Destructive Without Confirmation:
    → Triggering destructive actions with one keypress
    → Mistakes are hard or impossible to recover from
    → Fix: add confirmation and, when possible, undo
```

---

## 3. Layout and Display Anti-Patterns

| # | Anti-Pattern | Problem | Signals | Fix |
|---|-------------|---------|---------|-----|
| **LY-01** | **Fixed Width Assumption** | Designing around an 80-column terminal only | Wide screens waste space and narrow screens wrap badly | Read terminal width dynamically and reflow the layout |
| **LY-02** | **Unicode Blindness** | Assuming ASCII width rules for all text | CJK, emoji, and full-width characters break table alignment | Use Unicode width calculation (`wcwidth`) and account for double-width characters |
| **LY-03** | **Scroll Amnesia** | Losing context once content scrolls off-screen | Users cannot recover the list head or understand their position | Show position in the status bar and preserve key results after alternate-screen exits |
| **LY-04** | **Dense Wall of Text** | Printing dense output without spacing or hierarchy | Important items disappear into a block of text | Use section breaks, headings, and whitespace deliberately |
| **LY-05** | **No Responsive Design** | Failing to redraw on terminal resize | The layout breaks after the window changes size | Handle `SIGWINCH` and re-render |

---

## 4. Progress Display Anti-Patterns

```text
Progress display traps:

  ❌ Indeterminate Everything:
    → Showing only a spinner when a percentage is available
    → Users cannot estimate completion
    → Fix: show a progress bar + ETA when measurable; otherwise show a spinner + elapsed time

  ❌ No Output for Long Tasks:
    → Printing nothing for 30+ seconds
    → Users assume the process is hung and press `Ctrl+C`
    → Fix: every long-running task needs at least progress or elapsed-time output

  ❌ Progress Without Context:
    → Showing `42%` without saying what is happening
    → Users cannot tell which stage is active
    → Fix: include both activity and progress, such as `Downloading dependencies... 42% (128/305)`

  ❌ Overwritten Important Info:
    → Letting spinners overwrite warnings or errors
    → Critical information disappears from the screen
    → Fix: keep important messages on dedicated lines and reserve the last line for transient indicators

  ❌ Flicker Hell:
    → Updating the screen too frequently
    → Output becomes visually noisy and hard to read
    → Fix: cap refresh rates around 10-30 fps and use buffered redraws
```

---

## 5. Accessibility Anti-Patterns

```text
Accessibility traps:

  ❌ Screen Reader Hostile:
    → Clearing or repainting the full screen too often
    → Screen readers cannot follow the changes
    → Fix: prefer minimal diff updates and explicit status changes over full wipes

  ❌ TERM=dumb Crash:
    → Sending ANSI control sequences to `TERM=dumb`
    → Low-capability terminals break or show noise
    → Fix: detect `TERM=dumb` / unknown terminals and fall back to plain text

  ❌ Speed-Only Interface:
    → Requiring fast input or relying on prompt timeouts
    → Users with motor impairments cannot complete actions
    → Fix: avoid timeouts or make them generous and optional

  ❌ Mouse-Required TUI:
    → Providing actions that only work with mouse clicks
    → Keyboard-only users lose access to features
    → Fix: provide keyboard shortcuts for every action

  ❌ Tiny Touch Targets:
    → Making clickable targets only one character wide
    → Mouse usage becomes unnecessarily difficult
    → Fix: expand interactive hit areas
```

---

## 6. How To Use With Anvil

```text
Use within Anvil:
  1. Review TU-01 to TU-07 during TEMPER for color and terminal semantics
  2. Review keybinding choices during CAST
  3. Review accessibility and cross-terminal behavior during HARDEN
  4. Review overall TUI polish during PRESENT

Quality gates:
  - Meaning conveyed by color alone → add icons or text (prevent TU-01)
  - `NO_COLOR` ignored → implement environment-variable handling (prevent TU-02)
  - True color assumed everywhere → add ANSI 16-color fallback (prevent TU-03)
  - ANSI escapes leak into pipes → add TTY detection (prevent TU-05)
  - 10+ hotkeys with poor discoverability → consider a command palette (prevent Hotkey Overload)
  - Fixed 80-column layout → make width dynamic (prevent LY-01)
  - 30+ seconds of silence → add visible progress (prevent No Output for Long Tasks)
  - `TERM=dumb` crashes → add a plain-text fallback (prevent TERM=dumb Crash)
```

**Source:** [Command Line Interface Guidelines](https://clig.dev/) · [Jens Roemer: TUI Design](https://jensroemer.com/writing/tui-design/) · [NO_COLOR Standard](https://no-color.org/) · [Chris Yeh: Terminal Colors](https://chrisyeh96.github.io/2020/03/28/terminal-colors.html) · [Alex Chan: Designer's Guide to the Terminal](https://www.alexchantastic.com/designers-guide-to-the-terminal)
