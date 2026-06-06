# CLI Packaging and Distribution Reference

**Purpose:** Ship a CLI through the package managers users already trust (Homebrew, apt, dnf, npm, PyPI, cargo, `go install`), with cross-compiled binaries, signed artifacts, and a functioning update-check path. Get the first install right — fixing a broken release lives in users' shell history forever.
**Read when:** Adding a `pkg` subcommand, authoring a Homebrew formula, generating deb/rpm, cross-compiling releases, signing binaries, or designing an update-check mechanism.

## Scope Boundary

- **Anvil `pkg`**: packaging manifests, cross-compile matrix, signing/attestation, install scripts, update-checker design, distribution-channel selection.
- **Builder (elsewhere)**: the business logic inside the CLI (packaging does not change behaviour).
- **Hearth (elsewhere)**: user-side install into their own dotfiles environment (`brew install` in `~/.zshrc` bootstrap).
- **Gear (elsewhere)**: CI pipeline that runs goreleaser/cross/napi-rs, uploads artifacts, dependency scans of the packaging toolchain itself.
- **Launch (elsewhere)**: release versioning strategy (SemVer/CalVer), changelog authoring, rollout plan, feature-flag gating.

If the request is "build deb/rpm artifacts and publish a Homebrew formula" → `pkg`. If it is "pick next version number and write release notes" → Launch. If it is "wire goreleaser into GitHub Actions" → Gear (with `pkg` owning the manifest content).

## Channel Selection Matrix

| Channel | Ecosystem | Pick when | Skip when |
|---------|-----------|-----------|-----------|
| Homebrew (tap or core) | macOS + Linux developers | Dev-tool CLI, auto-update via `brew upgrade` expected | Windows-primary tool |
| deb / rpm | Server Linux | Distro-native install for ops/SRE consumers | Rapid-release; packaging lag is a tax |
| npm | Node ecosystem / web devs | CLI ships as JS or bundles a Node binary (`pkg`, `sea`) | Large binary (npm has soft size expectations) |
| PyPI | Python ecosystem | CLI is Python; users already have `pip` or `pipx` | Non-Python users ("why do I need Python?") |
| cargo install | Rust devs | Rust CLI, acceptable build-from-source time | Non-Rust users (compile time and toolchain friction) |
| go install | Go devs | Go CLI, users accept `$GOPATH/bin` in PATH | Versioned releases required (`go install` re-resolves) |
| Scoop / winget | Windows | Windows-primary tool | Unix-only dependencies |
| Static binary on releases | All | Universal fallback; curl \| sh install script | Users need auto-update |
| OCI image | Container-first workflows | Tool runs inside containers (linters, scanners) | Interactive TUI — TTY forwarding breaks |

Ship at least two channels. Power users on macOS/Linux expect Homebrew + static tarball; server users expect deb/rpm.

## Cross-Compile Toolchain

| Source language | Recommended tool | Targets it handles cleanly |
|-----------------|------------------|-----------------------------|
| Go | goreleaser | linux/{amd64,arm64}, darwin/{amd64,arm64}, windows/amd64, freebsd |
| Rust | `cross` + `cargo-dist` or `cargo-zigbuild` | aarch64-unknown-linux-gnu, x86_64-apple-darwin, musl targets |
| Node (native addons) | napi-rs | Prebuilt per-platform `.node` binaries published to GitHub releases |
| Python | cibuildwheel | manylinux + macOS universal2 + Windows wheels |

Pin the cross toolchain version in CI. "Latest" silently breaks when the base image rotates (GLIBC version bumps are the classic symptom — user installs on RHEL 8 fail).

Target matrix at minimum: `linux/amd64`, `linux/arm64`, `darwin/amd64`, `darwin/arm64`, `windows/amd64`. Produce both glibc and musl Linux builds for static-binary distribution.

## Homebrew Formula Skeleton

```ruby
class Myapp < Formula
  desc "One-line description under 80 chars"
  homepage "https://github.com/org/myapp"
  version "1.2.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/org/myapp/releases/download/v1.2.0/myapp-darwin-arm64.tar.gz"
      sha256 "..."
    end
    on_intel do
      url "https://github.com/org/myapp/releases/download/v1.2.0/myapp-darwin-amd64.tar.gz"
      sha256 "..."
    end
  end

  def install
    bin.install "myapp"
    generate_completions_from_executable(bin/"myapp", "completion")
    man1.install "myapp.1"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/myapp --version")
  end
end
```

`generate_completions_from_executable` (available in Homebrew) wires `bash/zsh/fish` completions automatically if the CLI implements the `completion` subcommand. Ship the man page or Homebrew's audit complains.

## deb / rpm via nfpm

`nfpm` emits both formats from one YAML, avoiding per-distro boilerplate:

```yaml
name: myapp
version: 1.2.0
maintainer: team@example.com
description: |
  CLI description.
license: MIT
section: utils
contents:
  - src: ./dist/myapp
    dst: /usr/bin/myapp
  - src: ./completion.bash
    dst: /usr/share/bash-completion/completions/myapp
  - src: ./completion.zsh
    dst: /usr/share/zsh/site-functions/_myapp
  - src: ./myapp.1
    dst: /usr/share/man/man1/myapp.1
deb:
  fields:
    Bugs: https://github.com/org/myapp/issues
```

Serve the repo from a signed apt/yum endpoint (cloudsmith, packagecloud, or self-hosted with GPG-signed metadata). `curl | sudo apt-key add` is deprecated — use `/etc/apt/keyrings/myapp.gpg` + `signed-by=` in the sources list.

## Signing and Attestation

| Platform | Required | Tooling |
|----------|---------|---------|
| macOS binaries | Notarization for Gatekeeper | `codesign` + `notarytool`; without it users hit "cannot be opened" dialog |
| Windows binaries | Authenticode signing | EV code-signing cert or Azure Trusted Signing |
| Linux packages | GPG-signed repo metadata | `gpg --detach-sign` on deb Release files, `rpm --addsign` |
| Container images | Cosign keyless (OIDC) | `cosign sign --yes <registry>/<image>:<tag>` |
| Artefact attestation | SLSA provenance | `actions/attest-build-provenance` in GitHub Actions |

Publish checksums (`SHA256SUMS`) and their signature (`SHA256SUMS.sig` or `.intoto.jsonl` attestation) alongside every release. Users installing via `curl | sh` must be able to verify.

## Install Script Best Practices

Curl-pipe-sh is the universal fallback. Make it safe:

```sh
#!/bin/sh
set -eu
# fail fast, fail loud — never `|| true`

REPO="org/myapp"
VERSION="${MYAPP_VERSION:-latest}"
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64) ARCH=amd64 ;;
  aarch64|arm64) ARCH=arm64 ;;
  *) echo "unsupported arch: $ARCH" >&2; exit 1 ;;
esac
# verify checksum, never skip
```

Rules:

1. `set -eu` at the top; never swallow errors.
2. Download checksum and signature; verify before extracting.
3. Install to `$HOME/.local/bin` unless root — no surprise `sudo`.
4. Print the exact install path and how to add it to `PATH`.
5. Re-runnable (idempotent) — second run must be a no-op, not "already exists" error.
6. Support `MYAPP_VERSION=1.2.0` pinning and `DRY_RUN=1`.

## Update-Checker Mechanism

Opt-in, async, privacy-preserving:

| Decision | Recommended |
|----------|-------------|
| When to check | Once per 24h, cached to `$XDG_CACHE_HOME/myapp/update-check.json` |
| What to send | `User-Agent: myapp/<version> (<os>/<arch>)` only — no telemetry |
| Where to fetch | GitHub releases API or static JSON behind CDN |
| How to notify | One-line on stderr after command completes; never block |
| How to disable | `MYAPP_NO_UPDATE_CHECK=1`, `--no-update-check`, and honour `DO_NOT_TRACK=1` |
| In CI | Auto-disable when `CI=1` or stdout is not a TTY |

Never self-update binary files from the CLI — path-traversal, signing, and permissions all break. Delegate to the package manager (`brew upgrade myapp`, `apt upgrade`).

## Anti-patterns

- Publishing to npm a package that contains compiled binaries for only one platform (breaks for every other user).
- `curl | sudo bash` install scripts that do not verify checksums — one compromised CDN hop owns every user.
- Hard-coding `/usr/local/bin` in install scripts (Apple Silicon Homebrew uses `/opt/homebrew/bin`).
- Shipping `darwin/amd64` only and hitting Rosetta for ARM users (slow, and breaks signed-binary flows).
- Leaving debug symbols in the release binary (5x size for no user benefit; strip or use `-s -w`).
- Auto-updating the binary in place without signature verification.
- Forgetting to bump the formula version SHA — `brew install` pulls the old tarball silently.
- Running the update-check synchronously before the command's real work — adds network latency to every invocation.
- Emitting the update-check notice during `--json` output — corrupts the JSON stream.

## Handoff

- **To Launch**: SemVer bump justification, changelog, rollback plan if artifacts are yanked.
- **To Gear**: goreleaser/cargo-dist/napi-rs CI workflow, secret wiring (signing keys, notarization creds), release trigger.
- **To `completion`**: completion install paths per package format.
- **To `config`**: default config path that deb/rpm post-install should create.
- **To Sentinel** (adjacent): supply-chain check — sign every artifact, publish SBOM, attest provenance.
