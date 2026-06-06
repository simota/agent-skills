# CLI Design Patterns

**Purpose:** Canonical command-line patterns for command structure, flags, help, output, exit codes, completion, and project scaffolding.
**Read when:** Designing a new CLI contract, reviewing an existing command surface, or choosing framework/completion/init patterns.

## Contents

- Command Structure Principles
- Argument Design Patterns
- Standard Flags
- Output Formatting
- Exit Codes
- Error Handling Pattern
- CLI Framework Selection by Language
- Shell Completion
- Project Init Patterns

## Command Structure Principles

```
myapp <command> [subcommand] [options] [arguments]

Examples:
  myapp init                    # No args, interactive setup
  myapp build --watch          # Flag modifies behavior
  myapp deploy staging         # Positional argument
  myapp config set key value   # Nested subcommand
```

## Argument Design Patterns

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Positional** | Required, ordered inputs | `git commit message` |
| **Short flag** | Common options | `-v`, `-f`, `-o` |
| **Long flag** | Descriptive options | `--verbose`, `--force` |
| **Value flag** | Options with values | `--output=file.txt`, `-o file.txt` |
| **Boolean flag** | Toggle behavior | `--dry-run`, `--no-cache` |
| **Repeatable** | Multiple values | `-v -v -v` or `--tag=a --tag=b` |

## Standard Flags (Always Include)

```
--help, -h      # Display help message
--version, -V   # Display version number
--verbose, -v   # Increase output verbosity (repeatable)
--quiet, -q     # Suppress non-essential output
--no-color      # Disable colored output
--json          # Output in JSON format (for scripting)
--no-prompt     # Disable all interactive prompts (for AI agents and automation)
```

---

## Output Formatting

### Human-readable (default)

```
✓ Build completed in 2.3s
  Output: dist/bundle.js (145 KB)

⚠ 2 warnings found:
  - Unused import in src/utils.ts:12
  - Deprecated API in src/api.ts:45
```

### Machine-readable (--json)

```json
{
  "success": true,
  "duration": 2.3,
  "output": { "path": "dist/bundle.js", "size": 148480 },
  "warnings": [
    {"file": "src/utils.ts", "line": 12, "message": "Unused import"},
    {"file": "src/api.ts", "line": 45, "message": "Deprecated API"}
  ]
}
```

---

## Exit Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | Success | Command completed successfully |
| 1 | General error | Unspecified failure |
| 2 | Usage error | Invalid arguments or options |
| 3 | Data error | Invalid input data |
| 126 | Permission denied | Cannot execute |
| 127 | Command not found | Missing dependency |
| 130 | Interrupted | CTRL+C received |

## Error Handling Pattern

```typescript
class CLIError extends Error {
  constructor(
    message: string,
    public exitCode: number = 1,
    public suggestion?: string
  ) {
    super(message);
  }
}

function handleError(error: unknown): never {
  if (error instanceof CLIError) {
    console.error(`Error: ${error.message}`);
    if (error.suggestion) {
      console.error(`Hint: ${error.suggestion}`);
    }
    process.exit(error.exitCode);
  }
  console.error('Unexpected error:', error);
  process.exit(1);
}
```

---

## CLI Framework Selection by Language

| Language | Lightweight (stdlib) | Full-featured | Selection Criteria |
|----------|---------------------|---------------|-------------------|
| **Node.js** | commander | oclif | Single command → commander / Plugin support → oclif |
| **Python** | argparse | typer, click | No deps → argparse / Rich UI → typer |
| **Go** | flag | cobra | Simple script → flag / Production CLI → cobra |
| **Rust** | clap (derive) | clap (builder) | derive macro is usually sufficient |
| **Bun** | commander (compat) | bun native args | Single binary → bun build --compile |
| **Deno** | Deno.args + parseArgs | cliffy | Deno ecosystem → cliffy / Simple → parseArgs |

### Selection Flowchart

```
Q1: Need subcommands?
├─ No → Lightweight (commander/argparse/flag/clap derive)
└─ Yes → Q2

Q2: Need plugin system?
├─ No → Standard (commander/click/cobra/clap)
└─ Yes → oclif (Node.js) or custom

Q3: Primary use in CI/CD?
├─ Yes → Minimize interactive, --yes flag required
└─ No → Consider rich TUI (inquirer/questionary/survey/dialoguer)

Q4: Need single binary distribution?
├─ Yes → Go/Rust (native) or Bun (bun build --compile) or Deno (deno compile)
└─ No → Any framework
```

### Framework Comparison

| Feature | commander | oclif | click | typer | cobra | clap |
|---------|-----------|-------|-------|-------|-------|------|
| Learning curve | Low | Medium | Low | Low | Medium | Medium |
| Subcommands | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auto help | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Completion gen | Manual | ✅ | ✅ | ✅ | ✅ | ✅ |
| Plugin system | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Type safety | △ | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## Shell Completion

### Node.js (Commander.js)

```typescript
program
  .command('completion')
  .description('Generate shell completion script')
  .argument('<shell>', 'Shell type: bash | zsh | fish')
  .action((shell: string) => {
    const appName = 'myapp';
    switch (shell) {
      case 'bash':
        console.log(`
_${appName}_completions() {
  local cur="\${COMP_WORDS[COMP_CWORD]}"
  local commands="init build deploy config help"
  COMPREPLY=($(compgen -W "$commands" -- "$cur"))
}
complete -F _${appName}_completions ${appName}
        `.trim());
        break;
      case 'zsh':
        console.log(`
#compdef ${appName}
_${appName}() {
  local -a commands
  commands=(
    'init:Initialize a new project'
    'build:Build the project'
    'deploy:Deploy to production'
  )
  _describe 'command' commands
}
_${appName} "$@"
        `.trim());
        break;
    }
  });
```

### Go (Cobra — built-in)

```go
// Cobra provides built-in completion generation
var completionCmd = &cobra.Command{
    Use:       "completion [bash|zsh|fish|powershell]",
    Short:     "Generate completion script",
    ValidArgs: []string{"bash", "zsh", "fish", "powershell"},
    Run: func(cmd *cobra.Command, args []string) {
        switch args[0] {
        case "bash":
            cmd.Root().GenBashCompletion(os.Stdout)
        case "zsh":
            cmd.Root().GenZshCompletion(os.Stdout)
        case "fish":
            cmd.Root().GenFishCompletion(os.Stdout, true)
        }
    },
}
```

### Rust (Clap — clap_complete)

```rust
use clap_complete::{generate, Shell};

fn main() {
    let cli = Cli::parse();
    match cli.command {
        Commands::Completion { shell } => {
            generate(shell, &mut Cli::command(), "myapp", &mut io::stdout());
        }
    }
}
```

### Python (Click — built-in)

```bash
# Click has built-in completion support
# Bash: eval "$(_MYAPP_COMPLETE=bash_source myapp)"
# Zsh:  eval "$(_MYAPP_COMPLETE=zsh_source myapp)"
# Fish: eval "$(_MYAPP_COMPLETE=fish_source myapp)"
```

---

## Project Init Patterns

### Common Requirements

| Requirement | Implementation |
|-------------|----------------|
| Non-interactive mode | `--yes` / `-y` flag to skip prompts |
| Existing directory detection | Prevent overwriting non-empty directories |
| Template selection | `--template` / `-t` option |
| Next steps display | Show `cd`, `install`, `run` after creation |

### Node.js (Commander + Inquirer)

```typescript
async function initProject(options: InitOptions): Promise<void> {
  const answers = options.yes
    ? { name: options.name || 'my-project', template: options.template || 'default' }
    : await inquirer.prompt([
        { type: 'input', name: 'name', message: 'Project name:', default: options.name || path.basename(process.cwd()) },
        { type: 'list', name: 'template', message: 'Select template:', choices: ['default', 'minimal', 'full'] },
      ]);

  const projectDir = path.resolve(answers.name);
  if (fs.existsSync(projectDir) && fs.readdirSync(projectDir).length > 0) {
    throw new CLIError(`Directory ${answers.name} is not empty`, 1);
  }

  fs.mkdirSync(projectDir, { recursive: true });
  await scaffoldTemplate(projectDir, answers.template);

  console.log(`✓ Created ${answers.name}`);
  console.log(`\n  cd ${answers.name}\n  npm install\n  npm run dev\n`);
}
```

### Python (Typer)

```python
@app.command()
def init(
    name: Optional[str] = typer.Argument(None),
    template: str = typer.Option("default", "--template", "-t"),
    yes: bool = typer.Option(False, "--yes", "-y"),
):
    if name is None and not yes:
        name = typer.prompt("Project name", default=Path.cwd().name)
    name = name or "my-project"
    project_dir = Path(name).resolve()
    if project_dir.exists() and any(project_dir.iterdir()):
        typer.echo(f"Error: Directory {name} is not empty", err=True)
        raise typer.Exit(1)
    project_dir.mkdir(parents=True, exist_ok=True)
    scaffold_template(project_dir, template)
    typer.echo(f"✓ Created {name}\n\n  cd {name}\n  pip install -e .\n")
```

### Go (Cobra + Survey)

```go
var initCmd = &cobra.Command{
    Use:   "init [name]",
    Short: "Initialize a new project",
    Args:  cobra.MaximumNArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        name := "my-project"
        if len(args) > 0 { name = args[0] }
        yes, _ := cmd.Flags().GetBool("yes")
        if !yes {
            prompt := &survey.Input{Message: "Project name:", Default: name}
            survey.AskOne(prompt, &name)
        }
        // ... scaffold and display next steps
        return nil
    },
}
```

### Rust (Clap + Dialoguer)

```rust
fn init_project(name: Option<String>, template: String, yes: bool) -> Result<()> {
    let project_name = if yes {
        name.unwrap_or_else(|| "my-project".to_string())
    } else {
        Input::with_theme(&ColorfulTheme::default())
            .with_prompt("Project name")
            .default(name.unwrap_or_else(|| "my-project".to_string()))
            .interact_text()?
    };
    // ... scaffold and display next steps
    Ok(())
}
```

### Rust CLI Specifics (2026)

**Error handling & exit codes** — use `anyhow` in the binary (type-erased, `?`-friendly, prints the context chain); keep typed errors (`thiserror`) only in library crates the CLI depends on. Map error categories to distinct exit codes instead of a blanket `1`, and let `main` return `Result` so the runtime prints the chain:

```rust
use std::process::ExitCode;

fn main() -> ExitCode {
    match run() {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("error: {e:#}");          // {:#} prints the full anyhow context chain
            ExitCode::from(match e.downcast_ref::<CliError>() {
                Some(CliError::Usage)  => 2,    // bad invocation (mirror clap's exit code)
                Some(CliError::Config) => 78,   // EX_CONFIG (sysexits.h)
                _ => 1,
            })
        }
    }
}
```

**Async CLIs** — default to `#[tokio::main(flavor = "current_thread")]` for a single-threaded CLI; only opt into the multi-thread runtime when the command does real parallel I/O. The current-thread flavor has lower startup cost and smaller binaries.

**Config precedence** — use `figment` (layered: defaults → file → env → flags) or `confy` (zero-config TOML at the XDG path) instead of hand-rolling merge logic; both deserialize straight into a `serde` struct so validation lives in the type.

**Color & TTY** — honor the `NO_COLOR` env var and `--no-color`, and auto-disable styling when stdout is not a TTY. `owo-colors` with `OwoColorize::if_supports_color` (via `supports-color`) gates styling automatically; `anstream`/`anstyle` (what clap uses) is the lower-level option.

**Binary size** (release profile) — for distributed CLIs, set `lto = true`, `codegen-units = 1`, `panic = "abort"`, `strip = true`, and `opt-level = "z"` in `[profile.release]`; profile the result with `cargo-bloat` before committing to feature-gating.

### Template Engine Patterns

| Language | Engine | Use Case |
|----------|--------|----------|
| **Node.js** | Handlebars, EJS, Mustache | Template files with variable substitution |
| **Python** | Jinja2, Mako | Complex template logic, conditionals |
| **Go** | text/template (stdlib) | Built-in, no dependencies |
| **Rust** | Tera, Handlebars-rust | Jinja2-like or Handlebars-like syntax |
