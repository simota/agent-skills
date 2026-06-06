# Fuzz Testing Guide

Purpose: Use this file for coverage-guided fuzzing setup, corpus management, sanitizer integration, crash triage, and continuous fuzzing in CI under Siege's `fuzz` subcommand. Fuzzing discovers reachable crashes and memory-safety bugs by feeding mutated input into instrumented binaries and tracking new coverage — it complements unit tests and mutation testing rather than replacing them.

## Scope Boundary

- **Siege `fuzz`**: coverage-guided fuzzing of parsers, decoders, protocol handlers, native code paths, and security-sensitive surfaces. Corpus + sanitizer + crash triage + CI loop.
- **Radar (elsewhere)**: standard unit-test coverage gaps, edge-case tests, flaky-test repair. If "coverage is low" means line/branch coverage on normal tests, route to Radar.
- **Mint (elsewhere)**: structured test-data factory, fixture generation, deterministic seed datasets. If the need is "generate valid realistic records for tests," route to Mint. Fuzz corpora should be seeded from Mint fixtures when a valid-input grammar exists.
- **Attest (elsewhere)**: spec compliance and AC verification. Fuzzing is a bug-hunting tool, not a conformance tool.
- **Voyager (elsewhere)**: E2E user journey testing. Fuzzing never clicks through a UI flow.

If the goal is "find inputs that crash / hang / corrupt memory" → `fuzz`. If it is "ensure valid inputs meet the spec" → Attest.

## Tool Selection

| Tool | Pick when | Skip when |
|------|-----------|-----------|
| AFL++ | C/C++ native code, forkserver speed, persistent mode, best mutator library | Pure managed-language code (no instrumentation hooks) |
| libFuzzer | In-process fuzzing for C/C++, tight integration with Clang sanitizers | Multi-process targets, stateful servers |
| go-fuzz / Go native `testing.F` | Go 1.18+, built-in `FuzzXxx` functions, no external runtime | Pre-1.18 Go, need custom mutators |
| cargo-fuzz | Rust, libFuzzer backend, integrates with `#[no_coverage]` and sanitizers | Stable-only toolchain (cargo-fuzz needs nightly) |
| Jazzer | JVM (Java/Kotlin/Scala), libFuzzer-compatible, autofuzz of method signatures | Non-JVM targets |
| Atheris | Python, libFuzzer-compatible, catches `Exception` as bug by default | Async-heavy Python, native-extension-heavy paths |
| OSS-Fuzz | Open-source project wanting free continuous fuzzing at Google scale | Closed-source or private-internal projects |
| ClusterFuzzLite | Self-hosted continuous fuzzing in CI, CIFuzz action | No CI budget for multi-hour fuzz runs |

Default for a new C/C++ target: **AFL++ with ASan+UBSan**. For Rust: **cargo-fuzz with ASan**. For Go: **native `testing.F`** before reaching for external tools.

## Workflow

```
DEFINE   →  pick target function (parser / deserializer / protocol handler / auth path)
         →  state invariants that MUST hold (no crash, no OOM, no UB, no infinite loop)
         →  choose sanitizer set (ASan, UBSan, TSan, MSan) — never enable all at once
         →  set time budget (PR: <5min, nightly: 1-4h, continuous: 24h+)

PREPARE  →  write harness: one function, deterministic, <1ms/exec preferred
         →  seed corpus from real inputs, unit test fixtures, or Mint factory output
         →  add dictionary (magic bytes, keywords, tokens) for structured formats
         →  instrument build with coverage + sanitizer

EXECUTE  →  warm up with seed corpus
         →  monitor exec/sec, new coverage, unique crashes
         →  rotate sanitizer combos across runs (ASan+UBSan one pass, TSan another)

ANALYZE  →  minimize crashes with afl-tmin / cargo-fuzz tmin
         →  deduplicate by stack hash, not by input bytes
         →  triage: security vs robustness vs known-bug vs false-positive

REPORT   →  crash summary with minimized input, stack, sanitizer verdict, severity
         →  corpus delta (new coverage reached), hand off fix to Builder
         →  CI job config recommendation
```

## Harness Rules

The harness is the contract between corpus input and target code. A bad harness silently hides bugs.

1. **Single entry, deterministic**: one `LLVMFuzzerTestOneInput` / `fuzz_target!` / `FuzzXxx` per target. No global state between invocations.
2. **Fast**: aim for <1ms/exec. Strip network I/O, disk I/O, random sleeps. Replace time/rand with fixed values.
3. **No early returns that mask bugs**: don't `if (len < 10) return 0;` — that hides the short-input path from the fuzzer.
4. **Assert invariants explicitly**: use `assert()` inside the harness for "this should never be true" properties. A failing assert counts as a crash.
5. **Rebuild when target changes**: harness + target must share the same sanitizer flags and coverage instrumentation.

## Corpus Management

| Corpus type | Source | Role |
|-------------|--------|------|
| Seed corpus | real samples, unit-test fixtures, Mint output | Starting coverage — never empty-start a campaign |
| Minimized corpus | `afl-cmin` / `cargo fuzz cmin` output | Smallest set preserving same coverage — commit this to repo |
| Crash corpus | minimized crashing inputs | Regression corpus — add to CI fuzz-smoke stage |
| Dictionary | format tokens, magic bytes, keywords | Boosts structure-aware mutation for JSON, HTTP, SQL, protobufs |

Commit the **minimized corpus** to the repo (usually under `fuzz/corpus/<target>/`). Never commit the raw queue directory — it grows unbounded and bloats git.

## Sanitizer Integration

| Sanitizer | Finds | Overhead | Combine with |
|-----------|-------|----------|--------------|
| ASan (AddressSanitizer) | heap/stack/global OOB, UAF, double-free | 2-3x | UBSan |
| UBSan (UndefinedBehaviorSanitizer) | integer overflow, null deref, invalid cast | ~1.5x | ASan |
| TSan (ThreadSanitizer) | data races, lock inversion | 5-15x | standalone |
| MSan (MemorySanitizer) | use of uninitialized memory | 3x | standalone |
| LSan (LeakSanitizer) | memory leaks at exit | minimal | included in ASan |

**Never combine ASan + MSan** — they instrument the same memory layout incompatibly. **Never combine ASan + TSan** — redzone conflicts. Rotate sanitizer profiles across nightly runs instead.

## Crash Triage

```
1. Minimize:  afl-tmin -i crash-input -o minimized -- ./target
2. Dedupe:    hash stack frames (top 3-5), not input bytes
3. Classify:
   - Security-critical: ASan heap OOB, UAF, stack overflow → P0, security handoff
   - Correctness:       assertion, UBSan signed overflow → P1-P2, Builder handoff
   - Robustness:        OOM, timeout, unbounded recursion → P2-P3, may be WONTFIX
   - False positive:    test harness bug, sanitizer quirk → fix harness, not target
4. Check reproducibility: 3x re-run with same input + same build
5. Add to crash-regression corpus
```

## Continuous Fuzzing in CI

Two-tier pattern:

```yaml
# .github/workflows/fuzz.yml
fuzz-smoke:                    # PR tier: <5 min budget
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: google/clusterfuzzlite/actions/build_fuzzers@main
      with: { sanitizer: address }
    - uses: google/clusterfuzzlite/actions/run_fuzzers@main
      with: { fuzz-seconds: 300, mode: code-change }

fuzz-nightly:                  # Nightly tier: 1-4h budget
  schedule: [{ cron: '0 2 * * *' }]
  strategy:
    matrix: { sanitizer: [address, undefined, thread] }
  steps:
    - uses: google/clusterfuzzlite/actions/run_fuzzers@main
      with: { fuzz-seconds: 3600, mode: batch, sanitizer: ${{ matrix.sanitizer }} }
```

For long-lived open-source projects, prefer **OSS-Fuzz onboarding** over self-hosted — it gives 24/7 execution, automatic bisection, and ClusterFuzz backend for free.

## Anti-Patterns

- Seeding with an empty corpus — wastes hours rediscovering trivial coverage the seed corpus would have given in seconds.
- Running without a sanitizer — the fuzzer will find crashes as-is, but most heap bugs look like "exit code 0" without ASan.
- Enabling ASan + MSan + TSan simultaneously — they conflict; run separate profiles.
- Deduping crashes by raw input bytes — two different inputs often hit the same bug, inflating triage backlog.
- Committing the raw `queue/` or `crashes/` directory to git — use a minimized corpus artifact instead.
- Treating fuzz coverage as code-coverage replacement — fuzz coverage measures reachability, not assertion density. Pair with Radar's unit tests.
- Forgetting to rebuild the harness after target changes — stale instrumentation silently reports stale results.
- Running PR-tier fuzz for >5min — destroys developer feedback loop; push long runs to nightly.
- Ignoring "no new coverage" for 1h+ — either the harness is saturated or it is stuck. Stop and inspect, don't keep burning CPU.

## Handoff

**To Builder:**
- Minimized crashing input, stack trace, sanitizer verdict, suspected root cause line.
- Whether the crash is security-relevant (ASan heap OOB → yes; UBSan signed overflow → depends).
- Regression-corpus path for the new test case.

**To Radar:**
- Crash inputs that should become unit-test cases (once fixed).
- Coverage gaps fuzzing exposed that normal tests miss.

**To Mint:**
- Valid-input shapes discovered during harness work — may update factory grammar.

**To Sentinel / Probe:**
- Security-critical findings (RCE-shaped, auth-bypass-shaped) that need deeper SAST / DAST follow-up.

**Escape hatches / follow-ups:**
- `#TODO(agent): onboard to OSS-Fuzz` if project is open-source and unfunded for CI.
- `#TODO(agent): rotate sanitizer matrix` if only ASan has ever been run.
