# TUI Components

**Purpose:** Practical TUI component patterns for prompts, tables, spinners, and progress views across Node.js, Python, Go, and Rust.
**Read when:** Adding terminal interactivity, rich output, or a full-screen TUI to a CLI.

## Contents

- Language/Library Matrix
- Progress Indicators
- Selection Menus
- Table Display
- Rust CLI Full Pattern

## Language/Library Matrix

| Language | Interactive Prompts | Rich Output | Full TUI |
|----------|---------------------|-------------|----------|
| **Node.js** | inquirer, prompts | chalk, ora, cli-table3 | ink v7 |
| **Python** | click, questionary | rich, colorama | textual, urwid |
| **Go** | survey, promptui | color, tablewriter | bubbletea v2 (charm.land/bubbletea/v2), tview |
| **Rust** | dialoguer, inquire | colored, prettytable | ratatui, crossterm |

## Full TUI Framework Selection

| Factor | Ink v7 (Node.js) | Ratatui v0.30+ (Rust) | BubbleTea v2 (Go) | Textual (Python) |
|--------|-----------------|----------------------|-------------------|-----------------|
| **Architecture** | React component tree (Yoga Flexbox) | Immediate-mode rendering | Elm Architecture (Model-Update-View) | Widget tree (CSS-like styling) |
| **Performance** | React reconciler; suitable for interactive CLIs | 30-40% less memory, 15% lower CPU vs Go; no_std for embedded | Cursed Renderer (ncurses-based, 10x faster vs v1), Mode 2026 sync output | Adequate for standard tools |
| **Requirements** | Node.js 22+, React 19.2+ | Rust stable | Go module path: `charm.land/bubbletea/v2` | Python 3.8+, pip |
| **Best for** | Node.js CLIs with rich interactivity, ink-ui component library | High-frequency dashboards, log monitors, editors, embedded TUIs | Standard CLI tools, rapid development | Data science tools, prototyping |
| **Sync output** | Not applicable | Backend-dependent (crossterm) | Built-in Mode 2026 (flicker-free) + Mode 2027 (wide Unicode/emoji layout) | Not applicable |
| **Extras** | `ink-ui` component library, pastel framework, renderToString() | Modularized workspace crates (v0.30+), ratatui::run() API, no_std embedded support | OSC52 clipboard (copy/paste over SSH), progressive keyboard enhancements, pure Lip Gloss v2 | Built-in CSS-like theming; community-maintained open-source since 2025-05 |
| **Source** | [github.com/vadimdemedes/ink](https://github.com/vadimdemedes/ink) | [ratatui.rs/highlights/v030](https://ratatui.rs/highlights/v030/) | [github.com/charmbracelet/bubbletea](https://github.com/charmbracelet/bubbletea/releases/tag/v2.0.0) | [textual.textualize.io](https://textual.textualize.io/) |

> **Ink v7 Breaking Changes:** Requires Node.js 22 and React 19.2+. v6 required Node.js 20. For React concurrent rendering support (opt-in since v6.7), use the `concurrentMode` option. Use `npx create-ink-app` to scaffold new Ink projects. [Source: github.com/vadimdemedes/ink/releases/tag/v7.0.0](https://github.com/vadimdemedes/ink/releases/tag/v7.0.0)

> **Mode 2026 (Synchronized Output):** Terminal standard (`CSI ? 2026 h/l`) that batches render updates atomically, eliminating screen tearing. Supported by Ghostty, Alacritty, and others. BubbleTea v2 enables this by default. Import path: `charm.land/bubbletea/v2`.
>
> **Mode 2027 (Wide Character Handling):** BubbleTea v2 auto-enables mode 2027 on supported terminals, allowing proper rendering of wide Unicode characters and emojis without breaking layout.

> **BubbleTea v2 Breaking API Changes:** `View()` now returns a `tea.View` struct instead of `string`, enabling declarative rendering. All imperative commands (e.g., window title, cursor control) are replaced with declarative fields on the View struct. Import path changed to `charm.land/bubbletea/v2`. Keyboard and mouse APIs were restructured. Existing v1 code requires migration — do not mix v1 patterns with the v2 import. [Source: github.com/charmbracelet/bubbletea/discussions/1374](https://github.com/charmbracelet/bubbletea/discussions/1374)

> **Ratatui v0.30+ Modularized Architecture:** Reorganized from a single monolithic crate into a modular workspace (ratatui-core, ratatui-widgets, etc.), reducing compilation times and enabling flexible dependency management. New `ratatui::run()` API simplifies application setup. no_std support enables use on bare-metal targets (ESP32, STM32H7, PSP, UEFI). [Source: ratatui.rs/highlights/v030](https://ratatui.rs/highlights/v030/)

> **Textual Community Status (2025-05):** Textualize Inc. announced on 2025-05-07 that Textual will continue as a community open-source project. The framework is mature, battle-tested, and actively maintained by Will McGugan. No functionality changes expected. [Source: textual.textualize.io/blog/2025/05/07/the-future-of-textualize](https://textual.textualize.io/blog/2025/05/07/the-future-of-textualize/)

---

## Progress Indicators

### Node.js (ora)

```typescript
import ora from 'ora';

async function withSpinner<T>(task: () => Promise<T>, message: string): Promise<T> {
  const spinner = ora(message).start();
  try {
    const result = await task();
    spinner.succeed();
    return result;
  } catch (error) {
    spinner.fail();
    throw error;
  }
}
```

### Python (rich)

```python
from rich.progress import Progress, SpinnerColumn, TextColumn

def with_progress(tasks: list[tuple[str, Callable]]):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        for description, task in tasks:
            task_id = progress.add_task(description)
            task()
            progress.update(task_id, completed=True)
```

### Go (bubbletea)

```go
type spinnerModel struct {
    spinner spinner.Model
    message string
    done    bool
}

func (m spinnerModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case spinner.TickMsg:
        var cmd tea.Cmd
        m.spinner, cmd = m.spinner.Update(msg)
        return m, cmd
    }
    return m, nil
}
```

### Rust (indicatif)

```rust
use indicatif::{ProgressBar, ProgressStyle};
use std::time::Duration;

fn with_spinner<T, F>(message: &str, task: F) -> T
where F: FnOnce() -> T {
    let spinner = ProgressBar::new_spinner();
    spinner.set_style(
        ProgressStyle::default_spinner()
            .template("{spinner:.cyan} {msg}").unwrap()
    );
    spinner.set_message(message.to_string());
    spinner.enable_steady_tick(Duration::from_millis(100));
    let result = task();
    spinner.finish_with_message(format!("✓ {}", message));
    result
}
```

---

## Selection Menus

### Node.js (inquirer)

```typescript
import inquirer from 'inquirer';

async function selectOption<T extends string>(
  message: string,
  choices: { name: string; value: T }[]
): Promise<T> {
  const { selection } = await inquirer.prompt([
    { type: 'list', name: 'selection', message, choices },
  ]);
  return selection;
}
```

### Python (questionary)

```python
import questionary

def select_option(message: str, choices: list[str]) -> str:
    return questionary.select(message, choices=choices, use_shortcuts=True).ask()
```

### Rust (dialoguer)

```rust
use dialoguer::{theme::ColorfulTheme, Select, Input, Confirm};

fn interactive_setup() -> Result<Config, Box<dyn std::error::Error>> {
    let name: String = Input::with_theme(&ColorfulTheme::default())
        .with_prompt("Project name")
        .default("my-project".into())
        .interact_text()?;

    let template = Select::with_theme(&ColorfulTheme::default())
        .with_prompt("Select template")
        .items(&["minimal", "full", "custom"])
        .default(0)
        .interact()?;

    Ok(Config { name, template })
}
```

---

## Table Display

### Node.js (cli-table3)

```typescript
import Table from 'cli-table3';

function displayTable(headers: string[], rows: string[][]): void {
  const table = new Table({ head: headers, style: { head: ['cyan'] } });
  rows.forEach(row => table.push(row));
  console.log(table.toString());
}
```

### Python (rich)

```python
from rich.console import Console
from rich.table import Table

def display_table(title: str, columns: list[str], rows: list[list[str]]):
    console = Console()
    table = Table(title=title)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)
```

### Rust (tabled)

```rust
use tabled::{Table, Tabled};

#[derive(Tabled)]
struct Row {
    name: String,
    status: String,
    count: u32,
}

fn display_table(rows: Vec<Row>) {
    let table = Table::new(rows).to_string();
    println!("{}", table);
}
```

---

## Rust CLI Full Pattern (Clap)

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "myapp", version, about)]
struct Cli {
    #[arg(short, long, action = clap::ArgAction::Count)]
    verbose: u8,

    #[arg(long)]
    json: bool,

    #[arg(long)]
    no_color: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Initialize a new project
    Init {
        #[arg(short, long)]
        name: Option<String>,
    },
    /// Build the project
    Build {
        #[arg(long)]
        watch: bool,
    },
}

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Init { name } => init_project(name),
        Commands::Build { watch } => build_project(watch),
    }
}
```
