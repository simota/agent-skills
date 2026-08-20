# Cross-Platform Patterns

**Purpose:** Cross-platform patterns for configuration paths, precedence, platform and shell detection, signal handling, and CI-aware terminal behavior.
**Read when:** Making a CLI work consistently across Windows, macOS, Linux, shells, TTY/non-TTY environments, or config-loading scenarios.

## Contents

- XDG Base Directory Specification
- Configuration Priority
- Platform Detection
- Platform-Specific Config Directories
- Shell Detection
- Signal Handling

## XDG Base Directory Specification

```typescript
import os from 'os';
import path from 'path';

interface ConfigPaths {
  config: string;   // User configuration
  data: string;     // User data
  cache: string;    // Cache files
  state: string;    // State files (logs, history)
}

function getXDGPaths(appName: string): ConfigPaths {
  const home = os.homedir();
  return {
    config: process.env.XDG_CONFIG_HOME
      ? path.join(process.env.XDG_CONFIG_HOME, appName)
      : path.join(home, '.config', appName),
    data: process.env.XDG_DATA_HOME
      ? path.join(process.env.XDG_DATA_HOME, appName)
      : path.join(home, '.local', 'share', appName),
    cache: process.env.XDG_CACHE_HOME
      ? path.join(process.env.XDG_CACHE_HOME, appName)
      : path.join(home, '.cache', appName),
    state: process.env.XDG_STATE_HOME
      ? path.join(process.env.XDG_STATE_HOME, appName)
      : path.join(home, '.local', 'state', appName),
  };
}
```

---

## Configuration Priority (Precedence)

```
Priority (highest to lowest):
1. CLI arguments       --port 3000
2. Environment vars    MYAPP_PORT=3000
3. Local config        .myapprc (current directory)
4. User config         ~/.config/myapp/config.json
5. System config       /etc/myapp/config.json
6. Built-in defaults   Hardcoded fallbacks
```

### Unified Config Loader (Node.js)

```typescript
import { z } from 'zod';

const ConfigSchema = z.object({
  port: z.number().default(3000),
  host: z.string().default('localhost'),
  verbose: z.boolean().default(false),
});

type Config = z.infer<typeof ConfigSchema>;

function loadConfig(cliArgs: Partial<Config>): Config {
  let config: Partial<Config> = {};
  // Load files (lowest → highest priority)
  for (const file of ['/etc/myapp/config.json', getXDGPaths('myapp').config + '/config.json', '.myapprc']) {
    const loaded = tryLoadJson(file);
    if (loaded) config = { ...config, ...loaded };
  }
  // Environment variables
  if (process.env.MYAPP_PORT) config.port = parseInt(process.env.MYAPP_PORT);
  if (process.env.MYAPP_HOST) config.host = process.env.MYAPP_HOST;
  // CLI args (highest priority)
  config = { ...config, ...filterUndefined(cliArgs) };
  return ConfigSchema.parse(config);
}
```

### Python Config Loader

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Config:
    port: int = 3000
    host: str = 'localhost'
    verbose: bool = False

def load_config(cli_args: dict) -> Config:
    config = {}
    for config_file in [Path('/etc/myapp/config.json'), get_xdg_config_home() / 'myapp/config.json', Path('.myapprc')]:
        if config_file.exists():
            with open(config_file) as f:
                config.update(json.load(f))
    if port := os.environ.get('MYAPP_PORT'): config['port'] = int(port)
    config.update({k: v for k, v in cli_args.items() if v is not None})
    return Config(**config)
```

### RC File Formats

| Format | File Names | Use Case |
|--------|-----------|----------|
| JSON | `.myapprc`, `myapp.config.json` | Structured config |
| YAML | `.myapprc.yaml` | Human-friendly |
| TOML | `.myapprc.toml` | Rust ecosystem |
| JS/TS | `myapp.config.js`, `myapp.config.ts` | Dynamic config |

---

## Platform Detection

### Node.js

```typescript
function getPlatform(): 'windows' | 'macos' | 'linux' | 'unknown' {
  switch (os.platform()) {
    case 'win32': return 'windows';
    case 'darwin': return 'macos';
    case 'linux': return 'linux';
    default: return 'unknown';
  }
}

function isTTY(): boolean { return process.stdout.isTTY === true; }

function isCI(): boolean {
  return !!(process.env.CI || process.env.GITHUB_ACTIONS || process.env.GITLAB_CI || process.env.CIRCLECI);
}
```

### Python

```python
def get_platform() -> str:
    if sys.platform == 'win32': return 'windows'
    elif sys.platform == 'darwin': return 'macos'
    return 'linux'

def is_tty() -> bool: return sys.stdout.isatty()
def is_ci() -> bool: return bool(os.environ.get('CI') or os.environ.get('GITHUB_ACTIONS'))
```

### Go

```go
func GetPlatform() string { return runtime.GOOS }

func IsTTY() bool {
    fi, _ := os.Stdout.Stat()
    return (fi.Mode() & os.ModeCharDevice) != 0
}

func IsCI() bool {
    return os.Getenv("CI") != "" || os.Getenv("GITHUB_ACTIONS") != ""
}
```

---

## Platform-Specific Config Directories

### Node.js

```typescript
function getConfigDir(appName: string): string {
  if (process.platform === 'win32')
    return path.join(process.env.APPDATA || os.homedir(), appName);
  if (process.platform === 'darwin')
    return path.join(os.homedir(), 'Library', 'Application Support', appName);
  return path.join(process.env.XDG_CONFIG_HOME || path.join(os.homedir(), '.config'), appName);
}
```

### Go

```go
func GetConfigDir(appName string) string {
    switch runtime.GOOS {
    case "windows":
        return filepath.Join(os.Getenv("APPDATA"), appName)
    case "darwin":
        home, _ := os.UserHomeDir()
        return filepath.Join(home, "Library", "Application Support", appName)
    default:
        if xdg := os.Getenv("XDG_CONFIG_HOME"); xdg != "" {
            return filepath.Join(xdg, appName)
        }
        home, _ := os.UserHomeDir()
        return filepath.Join(home, ".config", appName)
    }
}
```

---

## Shell Detection

```typescript
type ShellType = 'bash' | 'zsh' | 'fish' | 'powershell' | 'cmd' | 'unknown';

function detectShell(): ShellType {
  const shell = process.env.SHELL;
  if (shell) {
    if (shell.includes('bash')) return 'bash';
    if (shell.includes('zsh')) return 'zsh';
    if (shell.includes('fish')) return 'fish';
  }
  if (process.platform === 'win32') {
    if (process.env.PSModulePath) return 'powershell';
    return 'cmd';
  }
  return 'unknown';
}

function getShellRcFile(): string {
  const home = os.homedir();
  switch (detectShell()) {
    case 'bash': return path.join(home, '.bashrc');
    case 'zsh': return path.join(home, '.zshrc');
    case 'fish': return path.join(home, '.config', 'fish', 'config.fish');
    case 'powershell': return path.join(home, 'Documents', 'PowerShell', 'Microsoft.PowerShell_profile.ps1');
    default: return path.join(home, '.profile');
  }
}
```

---

## Signal Handling

### Node.js

```typescript
let isShuttingDown = false;

async function cleanup(): Promise<void> {
  if (isShuttingDown) return;
  isShuttingDown = true;
  console.log('\nCleaning up...');
  await db?.close();
  tempFiles.forEach(f => fs.unlinkSync(f));
}

process.on('SIGINT', async () => { await cleanup(); process.exit(130); });
process.on('SIGTERM', async () => { await cleanup(); process.exit(143); });
process.on('uncaughtException', (err) => { console.error('Fatal:', err.message); process.exit(1); });
process.on('unhandledRejection', (reason) => { console.error('Unhandled rejection:', reason); process.exit(1); });
```

### Python

```python
import signal, sys, atexit

_cleanup_done = False

def cleanup():
    global _cleanup_done
    if _cleanup_done: return
    _cleanup_done = True
    print('\nCleaning up...')

def signal_handler(signum, frame):
    cleanup()
    sys.exit(128 + signum)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
atexit.register(cleanup)
```

### Go

```go
func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

    errChan := make(chan error, 1)
    go func() { errChan <- run(ctx) }()

    select {
    case sig := <-sigChan:
        cancel()
        cleanup()
        if sig == syscall.SIGINT { os.Exit(130) }
        os.Exit(143)
    case err := <-errChan:
        if err != nil { fmt.Fprintf(os.Stderr, "Error: %v\n", err); os.Exit(1) }
    }
}
```

### Rust

```rust
use ctrlc;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let running = Arc::new(AtomicBool::new(true));
    let r = running.clone();
    ctrlc::set_handler(move || {
        eprintln!("\nReceived Ctrl+C, shutting down...");
        r.store(false, Ordering::SeqCst);
    })?;
    while running.load(Ordering::SeqCst) { do_work()?; }
    cleanup();
    std::process::exit(130);
}
```

### Tokio (Async Rust)

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);
    let shutdown = shutdown_tx.clone();
    tokio::spawn(async move {
        signal::ctrl_c().await.expect("Failed to listen for Ctrl+C");
        let _ = shutdown.send(());
    });
    let mut shutdown_rx = shutdown_tx.subscribe();
    tokio::select! {
        result = run_server() => { if let Err(e) = result { std::process::exit(1); } }
        _ = shutdown_rx.recv() => { cleanup().await; std::process::exit(130); }
    }
    Ok(())
}
```
