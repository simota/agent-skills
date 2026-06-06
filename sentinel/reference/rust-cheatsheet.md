# Rust Security Audit Cheatsheet — Sentinel

Focused checklist for SAST and code-level security review of Rust codebases. Baseline: **Rust 1.85+ / Edition 2024** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Constructive security stack: [`builder/reference/rust-best-practices.md` §7 Security practices](../../builder/reference/rust-best-practices.md#7-security-practices)
> - Misuse / pitfall catalog (12.1–12.20 + 12.A–12.D): [`builder/reference/rust-anti-patterns.md` §12 Security Pitfalls](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls)
> - `unsafe` UB catalog (9.1–9.20 + 9.A–9.C): [`builder/reference/rust-anti-patterns.md` §9 Unsafe Pitfalls](../../builder/reference/rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes)
> - Canonical UB list, Stacked vs Tree Borrows, SAFETY-comment template: [`builder/reference/rust-language-spec.md` §6 Unsafe Rust](../../builder/reference/rust-language-spec.md#6-unsafe-rust)
> - FFI / ABI rules: [`builder/reference/rust-language-spec.md` §8 FFI / Interop](../../builder/reference/rust-language-spec.md#8-ffi--interop)

**Do not duplicate the catalogs above.** This cheatsheet is the *order* and *triage angle* Sentinel applies; it links rather than restates.

---

## When auditing a Rust codebase, walk this checklist:

### 1. Scope the surface

| Step | Command | Why |
|------|---------|-----|
| 1.1 | `cargo geiger --output-format Json` | Count `unsafe` blocks per dep. A CVSS-7 in a 20%-unsafe crate is far more urgent than the same CVSS in a 0%-unsafe one. |
| 1.2 | `rg -n 'unsafe' --type rust src/` | Locate first-party `unsafe` blocks for line-by-line review. |
| 1.3 | `cargo public-api` | Snapshot the public API — every `pub` item is a semver commitment and an attack surface item. |
| 1.4 | `cargo tree -e features` | Surface unintended feature unification (workspace member A enables `serde` on `foo` → leaks into B). |

### 2. `unsafe` audit protocol

Every `unsafe { ... }` block must have a `// SAFETY:` comment naming each invariant the caller upholds (template: [language-spec §6.5](../../builder/reference/rust-language-spec.md#65-safety-comment-template)). Flag any block missing one — enforce with `clippy::undocumented_unsafe_blocks`.

Walk these patterns in order; each links to the full anti-pattern entry:

1. **Transmute layout assumptions** — `mem::transmute` between non-`#[repr(transparent)]` types is UB even if fields match. See [anti-patterns §9.1](../../builder/reference/rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes), §9.15, §9.B.
2. **Lifetime extension via transmute** — `transmute::<&'a T, &'b T>` to launder lifetimes. Always UB. See §9.2.
3. **Raw pointer aliasing** — `&mut T` co-existing with `*mut T` to the same data. Run Miri (default Stacked Borrows + `-Zmiri-tree-borrows`). See §9.3–9.4 and language-spec §6.3.
4. **`unsafe impl Send` / `Sync`** without proof — sending `Rc`, `Cell`, or thread-local-using types corrupts state. See §9.5.
5. **`Pin` invalidation** — `Pin::get_unchecked_mut` or moving a structurally-pinned field. Reject; require `pin-project` / `pin-project-lite`. See §9.7 and async §4.11.
6. **`Vec::from_raw_parts` / `set_len` / `MaybeUninit::assume_init`** — three of the highest-frequency UB sources. Each has rigid invariants. See §9.9–9.12.
7. **`static mut`** — deprecated in Edition 2024; replace with `LazyLock<Mutex<T>>` or `OnceLock<T>`. See §9.17.
8. **`Box::from_raw` on non-`Box::into_raw` pointers** — deallocator mismatch. See §9.16.
9. **`slice::from_raw_parts(ptr, len)` with wrong `len`** — out-of-bounds read. See §9.12.
10. **Function-pointer transmute across calling conventions** — ABI mismatch is UB. See §9.18.

**Tooling**: `cargo +nightly miri test` for the full suite. CI gate on `cargo miri test --tests` for crates with non-trivial `unsafe`.

### 3. FFI safety

Three rules that cause real CVEs:

| Rule | Check | Reference |
|------|-------|-----------|
| Panics MUST NOT cross an `extern "C"` boundary (UB) | Every `#[unsafe(no_mangle)] pub extern "C" fn` body wrapped in `std::panic::catch_unwind`, OR the function is declared `extern "C-unwind"` and the C side handles it | [language-spec §8](../../builder/reference/rust-language-spec.md#8-ffi--interop), [anti-patterns §9.8, §9.C](../../builder/reference/rust-anti-patterns.md#9-unsafe-pitfalls-high-stakes) |
| FFI struct layout MUST be `#[repr(C)]` or `#[repr(transparent)]` | Default `#[repr(Rust)]` is unspecified — field order and padding can change between compiler versions | language-spec §8 |
| Edition 2024 — `extern` blocks are unsafe to *declare* | `unsafe extern "C" { ... }`; items inside default to `unsafe fn` unless tagged `safe fn` (1.82+) | language-spec §1, §8 |

```rust
// FLAG: panic crossing C ABI is UB
#[unsafe(no_mangle)]
pub extern "C" fn process(x: i32) -> i32 {
    let r = std::panic::catch_unwind(|| {
        assert!(x >= 0);    // would otherwise unwind into C
        x * 2
    });
    r.unwrap_or(-1)         // sentinel; C caller checks
}
```

### 4. Secret hygiene

Six checks; each is a single grep target on a Rust codebase:

| Check | grep / lint | Why |
|-------|-------------|-----|
| 4.1 `Debug` derive on a struct holding secrets | `rg '#\[derive\(.*Debug.*\)\].*\n.*(password\|token\|secret\|key)' --type rust -A 3` | `{:?}` prints secrets into logs and panic messages. See [anti-patterns §12.20](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls). |
| 4.2 Secret types not wrapped in `secrecy::SecretBox` / `SecretString` | Type-check audit for `String` / `Vec<u8>` named password/token/key | `SecretBox<T>` excludes itself from `Debug`/`Display`/`Serialize`. See [best-practices §7.3](../../builder/reference/rust-best-practices.md#7-security-practices). |
| 4.3 Missing `zeroize` on heap-allocated secret memory | grep `#[derive(.*Zeroize` near secret structs | Decommissioned heap pages may retain key material until reuse. See §12.3, §12.18. |
| 4.4 `==` comparison on tokens / MACs / password hashes | `rg '(token\|mac\|hash\|signature)\s*==' --type rust` | Timing oracle — leaks length and prefix. Use `subtle::ConstantTimeEq::ct_eq`. See §12.11, best-practices §7.4. |
| 4.5 Logging via `tracing::info!("{secret}")` / `format!` interpolation | `rg 'info!\|debug!\|trace!\|println!' --type rust \| rg '(token\|password\|secret\|key)'` | Logs land in observability vendors / SIEM. See §12.2. |
| 4.6 `Display` impl on a secret newtype | Audit every `impl Display for` on auth/crypto types | Same risk as `Debug` — use opaque `Display` printing `"[REDACTED]"`. |

**Required minimum for any secret type**:

```rust
use secrecy::{SecretBox, ExposeSecret};
use zeroize::{Zeroize, ZeroizeOnDrop};

// SecretBox handles Debug/Display redaction; Zeroize/ZeroizeOnDrop wipe heap on drop.
#[derive(Zeroize, ZeroizeOnDrop)]
struct ApiKey(SecretBox<String>);

// expose_secret() makes every read site grep-able.
fn auth_header(k: &ApiKey) -> String {
    format!("Bearer {}", k.0.expose_secret())
}
```

### 5. Supply-chain checks

Run as a single CI job. Failing any of these blocks merge.

| Tool | What it catches | Config file |
|------|-----------------|-------------|
| `cargo audit` (RUSTSEC DB) | Published CVEs against pinned crate versions | `audit.toml` |
| `cargo deny check` | Advisory + license + source + bans + duplicates (one tool, four checks) | `deny.toml` |
| `cargo vet` | Reviewed-by-trusted-org provenance (Mozilla, Google, Embark, Bytecode Alliance audit imports) | `supply-chain/{audits,config}.toml` |
| `cargo geiger` | `unsafe` block count per dependency — quarterly review tool | — |

Full CI YAML lives in [best-practices §7.1](../../builder/reference/rust-best-practices.md#7-security-practices). Skeleton:

```yaml
jobs:
  security:
    steps:
      - uses: rustsec/audit-check@v2
      - run: cargo deny check          # advisories + licenses + sources + bans
      - run: cargo vet --locked        # provenance
      - run: cargo clippy -- -D clippy::unwrap_used -D clippy::indexing_slicing \
                              -D clippy::await_holding_lock \
                              -D clippy::undocumented_unsafe_blocks \
                              -D clippy::missing_safety_doc
      # Optional, slow but high-signal:
      - run: cargo +nightly miri test --tests
```

**2026 trusted publishing** (crates.io OIDC, late-2025 rollout): no long-lived `CARGO_REGISTRY_TOKEN` secret — short-lived OIDC token via `rust-lang/crates-io-auth-action@v1`. Adopt for all new publish workflows. See [best-practices §7.8](../../builder/reference/rust-best-practices.md#7-security-practices).

### 6. Command injection / TOCTOU / path traversal

The big three in safe Rust. None are prevented by the borrow checker.

| Class | Audit grep | Reference |
|-------|------------|-----------|
| **Shell injection** | `rg 'Command::new\("(sh\|bash\|cmd\|powershell)"\)' --type rust` | [anti-patterns §12.5, §12.C](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls) |
| **TOCTOU on filesystem** | `rg 'Path.*exists\|metadata' --type rust -B 1 -A 3` looking for subsequent open | §12.4, §12.A |
| **Path traversal** | `rg 'Path::new.*join\|PathBuf.*push' --type rust` near user input | §12.14, §12.D |

```rust
// FLAG: shell metacharacters in user_input → arbitrary command
let _ = Command::new("sh")
    .arg("-c")
    .arg(format!("convert {} out.png", user_input));   // ← injection

// FIX: separate argv slots, no shell
let _ = Command::new("convert").arg(user_input).arg("out.png");
```

```rust
// FLAG: TOCTOU — attacker swaps the file between check and use
if path.exists() {                       // T = time of check
    let f = File::open(path)?;           // U = time of use
}

// FIX: open atomically, branch on Err(NotFound)
match File::open(path) {
    Ok(f) => process(f),
    Err(e) if e.kind() == ErrorKind::NotFound => create_default(),
    Err(e) => Err(e.into()),
}
```

```rust
// FLAG: user_input = "../../etc/passwd" escapes base via join
let p = Path::new("/var/data").join(user_input);

// FIX: canonicalize and verify containment
let candidate = base.join(user_input).canonicalize()?;
if !candidate.starts_with(&base.canonicalize()?) {
    return Err(PathEscape);
}

// BEST: cap-std::Dir — capability-based, cannot escape by construction
let base = Dir::open_ambient_dir("/var/data", cap_std::ambient_authority())?;
let f = base.open(user_input)?;
```

### 7. Untrusted deserialization

| Format | Audit |
|--------|-------|
| **JSON** | Use `serde_json::de::from_reader` with a `Take`-wrapped reader for byte budget. Reject unknown fields where the type allows. |
| **YAML** | Avoid for untrusted input — aliases enable billion-laughs. If unavoidable, use `serde_yaml` with depth limits. |
| **TOML** | Generally safe (no aliases), but apply size limits. |
| **Bincode** | **Never** for untrusted input — trusts size prefixes; attacker says `usize::MAX` → OOM. See [anti-patterns §12.6, §12.16](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls). |
| **Domain invariants** | Deserialize into a flat `Dto` struct, then `TryFrom<Dto>` enforces invariants. See §12.8. |

Body-size cap pattern (`Content-Length` cannot be trusted):

```rust
// FLAG: attacker sends Content-Length: 4_000_000_000 → OOM
let mut buf = Vec::with_capacity(content_length);

// FIX: cap allocation
const MAX_BODY: usize = 8 * 1024 * 1024;
let mut buf = Vec::with_capacity(content_length.min(MAX_BODY));
```

### 8. Crypto stack policy

Sentinel does not author crypto — that is Crypt's domain (see [`crypt/reference/rust-cheatsheet.md`](../../crypt/reference/rust-cheatsheet.md)). The audit-side rules:

| Rule | Reject if you see... |
|------|----------------------|
| TLS uses `rustls`, not `native-tls` | `native-tls` in production deps unless interop with OS trust store is documented requirement |
| Primitives come from RustCrypto, `ring`, or `aws-lc-rs` | Hand-rolled crypto, ad-hoc SHA-1/MD5 use outside known-safe non-crypto contexts |
| Constant-time compare for secrets | `==` on `[u8; 32]` MAC outputs, password hashes, tokens |
| `Argon2id` for password hashing | `bcrypt`, `pbkdf2`, `scrypt` — flag for upgrade path even if not broken |
| CSPRNG via `getrandom` / `OsRng` | `rand::thread_rng()` used for cryptographic key/seed material |

See [best-practices §7.5, §7.6](../../builder/reference/rust-best-practices.md#7-security-practices) for the crate matrix.

### 9. Public API leakage

| Leak | Fix |
|------|-----|
| `Box<dyn Error>` in public API exposes inner types | Concrete `thiserror` enum at crate boundary. See [anti-patterns §5.1](../../builder/reference/rust-anti-patterns.md#5-error-handling-pitfalls). |
| `eprintln!("auth failed for {user}")` writes to stderr where it can be scraped | Use `tracing::error!` with structured fields and redaction filters |
| `Display` impl on error chain printing internal SQL / file paths | Customize `Display` per variant; reserve detailed info for `Debug` and tracing |
| `tracing::info!("{user_input}")` may log injected content / secrets | Use structured fields: `tracing::info!(user_id = %u.id, "login")` — never bare interpolation of untrusted input |
| `unwrap` / `expect` on `env::var("API_KEY")` | Panic message exposes the env var name. See §12.19. |

### 10. Integer arithmetic on attacker-controlled input

```rust
// FLAG: release builds wrap, debug builds panic — both exploitable
let total = price * quantity;

// FIX: explicit policy
let total = price.checked_mul(quantity).ok_or(Overflow)?;
// Or saturating_mul / wrapping_mul if the semantics are intentional
```

Enable in CI:

```toml
# Cargo.toml — for security-critical crates
[profile.release]
overflow-checks = true
```

Or use `clippy::arithmetic_side_effects` to flag every `+`/`-`/`*`/`/` outside explicit `checked_*` / `saturating_*` / `wrapping_*` paths. See [anti-patterns §12.9](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls).

### 11. Regex DoS on attacker-supplied patterns

The `regex` crate is **linear in input × pattern**, but the pattern itself is unbounded — a 1 MB user-supplied regex can pin a CPU.

```rust
// FLAG: user_pattern arrives from HTTP
let re = Regex::new(&user_pattern)?;

// FIX: size + DFA budget
use regex::RegexBuilder;
let re = RegexBuilder::new(&user_pattern)
    .size_limit(1 << 20)        // 1 MB compiled
    .dfa_size_limit(1 << 20)
    .build()?;
```

Or use `regex-lite` for tighter resource bounds. See [anti-patterns §12.7](../../builder/reference/rust-anti-patterns.md#12-security-pitfalls).

### 12. CI security gate — minimum viable

```yaml
# .github/workflows/rust-security.yml
on:
  push: { branches: [main] }
  pull_request:
  schedule: [{ cron: '0 6 * * *' }]   # daily — new CVEs land overnight
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: rustsec/audit-check@v2
        with: { token: ${{ secrets.GITHUB_TOKEN }} }
      - run: cargo deny check
      - run: cargo vet --locked
      - run: |
          cargo clippy --all-targets -- \
            -D warnings \
            -D clippy::unwrap_used \
            -D clippy::indexing_slicing \
            -D clippy::arithmetic_side_effects \
            -D clippy::await_holding_lock \
            -D clippy::await_holding_refcell_ref \
            -D clippy::undocumented_unsafe_blocks \
            -D clippy::missing_safety_doc \
            -D clippy::transmute_ptr_to_ref
  miri:                             # optional, ~10 min, high-signal for unsafe code
    runs-on: ubuntu-latest
    steps:
      - run: rustup +nightly component add miri
      - run: cargo +nightly miri test --tests
```

---

## Triage priorities

When multiple findings stack, rank by:

1. **`unsafe` UB** (Miri-positive or pattern-matching the §9 catalog) — these are exploitable in principle and undefined in practice.
2. **Secret exposure** (Debug/Display/log leaks, missing zeroize) — silent, persistent, often reaches third-party log shippers.
3. **Injection / TOCTOU / traversal** — directly exploitable by untrusted input.
4. **Untrusted deserialization without budget** — OOM and parse-bomb DoS.
5. **Crypto stack deviation** (native-tls, hand-rolled primitives, `==` on secrets) — hand off to Crypt for design-level review.
6. **Supply-chain hygiene** (missing `cargo-deny`, unaudited deps with high geiger score) — preventive, not active exploit.
7. **API leakage** (`Box<dyn Error>`, `eprintln!`) — informational; raises severity of other findings by making them observable.

---

## Sources

- RustSec Advisory DB: https://rustsec.org/
- `cargo-vet` book: https://mozilla.github.io/cargo-vet/
- `cargo-deny` docs: https://embarkstudios.github.io/cargo-deny/
- The Rustonomicon: https://doc.rust-lang.org/nomicon/
- Pitfalls of Safe Rust (corrode): https://corrode.dev/blog/pitfalls-of-safe-rust/
- Rust Security Handbook: https://github.com/yevh/rust-security-handbook
- `secrecy` docs: https://docs.rs/secrecy/
- `zeroize` docs: https://docs.rs/zeroize/
- `subtle` docs: https://docs.rs/subtle/
- `cap-std` (capability-based FS): https://docs.rs/cap-std/
- crates.io trusted publishing: https://blog.rust-lang.org/inside-rust/2025/...
