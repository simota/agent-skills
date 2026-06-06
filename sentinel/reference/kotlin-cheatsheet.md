# Kotlin Security Audit Cheatsheet — Sentinel

Focused checklist for SAST and code-level security review of Kotlin codebases (JVM and KMP server-side). Baseline: **Kotlin 2.3+ / K2 compiler** with **2.4 EAP outlook** (2026-05).

> Source-of-truth references (full catalog lives in Builder):
> - Null safety / `!!` / `lateinit` pitfalls: [`builder/reference/kotlin-anti-patterns.md` §1 Null Safety Pitfalls](../../builder/reference/kotlin-anti-patterns.md#1-null-safety-pitfalls)
> - Coroutines pitfalls (`GlobalScope`, `runBlocking`, leak detection): [`builder/reference/kotlin-anti-patterns.md` §2 Coroutines Pitfalls](../../builder/reference/kotlin-anti-patterns.md#2-coroutines-pitfalls)
> - Java interop pitfalls (`@JvmField`, platform types, `@Throws`): [`builder/reference/kotlin-anti-patterns.md` §7 Java Interop Pitfalls](../../builder/reference/kotlin-anti-patterns.md#7-java-interop-pitfalls)
> - Class hierarchy (`open` vs `final`, Spring component pitfalls): [`builder/reference/kotlin-anti-patterns.md` §4 Class Hierarchy Pitfalls](../../builder/reference/kotlin-anti-patterns.md#4-class-hierarchy-pitfalls)
> - Gradle / KSP / Compose-plugin pitfalls: [`builder/reference/kotlin-anti-patterns.md` §13 Gradle / KSP Pitfalls](../../builder/reference/kotlin-anti-patterns.md#13-gradle--ksp-pitfalls)
> - Coroutines language spec (cancellation, dispatchers): [`builder/reference/kotlin-language-spec.md` §4 Coroutines](../../builder/reference/kotlin-language-spec.md#4-coroutines--suspend-dispatchers-structured-concurrency)
> - Production library matrix incl. crypto / logging: [`builder/reference/kotlin-best-practices.md` §10 Production Library Matrix](../../builder/reference/kotlin-best-practices.md#10-production-library-matrix-2026-baseline)
> - Detekt / Ktlint rule index: [`builder/reference/kotlin-anti-patterns.md` Appendix A](../../builder/reference/kotlin-anti-patterns.md#appendix-a--detekt--ktlint-rule-quick-lookup-index)

**Do not duplicate the catalogs above.** This cheatsheet is the *order* and *triage angle* Sentinel applies on JVM-Kotlin and server-Kotlin code; it links rather than restates.

Companion cheatsheets (same agent):
- Concurrency / race conditions: see `siege` concurrency recipe (absorbed from specter)
- Crypto stack design: [`crypt/reference/kotlin-cheatsheet.md`](../../crypt/reference/kotlin-cheatsheet.md)

**Android scope note**: Android-specific patterns (Permission, SecurityException, WebView JS-bridge, EncryptedSharedPreferences, StrongBox/Hardware-backed Keystore) are handled by the **`native`** skill. This file covers cross-platform Kotlin and server-side JVM concerns only.

---

## When auditing a Kotlin codebase, walk this checklist:

### 1. Scope the surface

| Step | Command | Why |
|------|---------|-----|
| 1.1 | `./gradlew :app:dependencies --configuration runtimeClasspath` | Resolved dep graph — every transitive pulls in attack surface. |
| 1.2 | `rg -n '!!\|lateinit ' --type kotlin -g '!*Test*'` | `!!` and `lateinit` access before init are the two most common NPE+crash producers. See [anti-patterns §1](../../builder/reference/kotlin-anti-patterns.md#1-null-safety-pitfalls). |
| 1.3 | `rg -n 'runBlocking\|GlobalScope' --type kotlin -g '!*Test*'` | Hot-thread DoS + leaked coroutines. See [anti-patterns §2](../../builder/reference/kotlin-anti-patterns.md#2-coroutines-pitfalls). |
| 1.4 | `rg -n '@JvmField\|@JvmStatic\|@Throws' --type kotlin` | Java-interop surface — every annotation exposes Kotlin internals. |
| 1.5 | `find . -name 'libs.versions.toml' -o -name 'gradle.properties'` | Version-catalog pinning + Gradle property hardening. |

### 2. `!!` force-unwrap / `lateinit` audit

**Production code** must justify every `!!`. **Test code** (`src/test/`, `src/commonTest/`, `*Test.kt`, Kotest `*Spec.kt`) may use `!!` freely — assert-fast is desirable.

| Pattern | Production verdict | Reference |
|---------|--------------------|-----------|
| `value!!` on a `var T?` field | Reject — race-y; pair with `requireNotNull(value) { "ctx" }` and a documented assertion | [anti-patterns §1](../../builder/reference/kotlin-anti-patterns.md#1-null-safety-pitfalls) |
| `value!!` immediately after smart-cast guard | Often redundant K2 catches it — keep guard, drop `!!`. See K2 smart-cast in §10.A. |
| `lateinit var token: String` accessed before assignment | `UninitializedPropertyAccessException` — late-binding NPE; not caught at compile time. Use `Delegates.notNull<T>()` for primitives, nullable + `requireNotNull` for refs. |
| `as` (unchecked cast) on `Any?` from JSON / reflection | Reject. Use `as?` then `requireNotNull`. |
| `!!` on platform type from Java | Replace with explicit annotation in Java side (`@NotNull`) OR `?` + handler. Platform types are silent NPE producers. See §7 of anti-patterns. |

**Decision matrix** (from [anti-patterns §1.A](../../builder/reference/kotlin-anti-patterns.md#1a-requirenotnull-vs-checknotnull-vs--decision-matrix)):

| Want | Use | Why |
|------|-----|-----|
| Bug → IllegalArgumentException (caller's fault) | `requireNotNull(x) { "ctx" }` | Documented contract violation |
| Bug → IllegalStateException (state's fault) | `checkNotNull(x) { "ctx" }` | Documented invariant violation |
| Cosmic ray → NullPointerException | `x!!` | No, never. Use require/check. |

**Detekt enforcement** ([anti-patterns Appendix A](../../builder/reference/kotlin-anti-patterns.md#appendix-a--detekt--ktlint-rule-quick-lookup-index)):

```yaml
# detekt.yml
potential-bugs:
  UnsafeCallOnNullableType:
    active: true
  UnsafeCast:
    active: true
  LateinitUsage:
    active: true
    ignoreOnClassesPattern: '.*Test'
```

### 3. `runBlocking` in production code path

`runBlocking` parks a thread until the coroutine completes. On a hot path (request handler, framework callback), it blocks a server worker → easy DoS.

| Location | Verdict |
|----------|---------|
| `main()` entry of a CLI | Acceptable — runs once at startup |
| Top-level test setup | Acceptable |
| Inside `@Bean` / `@Service` method called per-request | **Reject** — pins request thread until inner suspend finishes |
| Inside Compose composable (server-rendered) | **Reject** |
| Bridge from sync Java framework into coroutine code | Acceptable only with a bounded executor (`Dispatchers.IO.limitedParallelism(n)`); see [best-practices §3.4](../../builder/reference/kotlin-best-practices.md#34-dispatchersiolimitedparallelismn-for-bounded-pools) |
| Inside another `suspend fun` (nested runBlocking) | **Reject — deadlock risk** if both share the dispatcher; see [anti-patterns §2.A](../../builder/reference/kotlin-anti-patterns.md#2a-visual-launch-vs-async-exception-propagation) |

**Detekt**: `coroutines:RedundantSuspendModifier`, custom rule `RedundantRunBlocking`.

### 4. Coroutine scope leaks

`GlobalScope` and unbound `MainScope()` are coroutine leaks waiting to happen.

| Pattern | Verdict |
|---------|---------|
| `GlobalScope.launch { ... }` in app code | **Reject** — coroutine outlives any cancellation surface; resource leak; in tests, leaks across test boundaries | [anti-patterns §2](../../builder/reference/kotlin-anti-patterns.md#2-coroutines-pitfalls) |
| `MainScope()` created and never `.cancel()`-ed | Reject in lifecycle-bound code. Required: tie scope to component lifecycle (`onDestroy` → `cancel()`). |
| `CoroutineScope(Job())` standalone | Audit ownership — who calls `cancel()`? |
| `CoroutineScope(SupervisorJob() + Dispatchers.IO)` in DI container | Acceptable when DI lifecycle manages cancellation explicitly |
| `viewModelScope` / `lifecycleScope` (Android) / Ktor `application` scope | Acceptable — framework-managed |

**Detekt**: `coroutines:GlobalCoroutineUsage` (catches `GlobalScope.launch`/`.async`).

### 5. Java interop surface

Every Java-visible Kotlin declaration is reachable by Java reflection / JNI / serialization — surfaces that bypass Kotlin's invariants.

| Pattern | Audit |
|---------|-------|
| `@JvmField val token: String` | Exposes the backing field. Java code (or reflection) reads it directly without going through any custom getter — leaks internal state. Reject for secrets. |
| `@JvmField` on `var` containing mutable state | Java can write directly, bypassing Kotlin's invariants. Reject. |
| `class Foo` (default `final`) called from Java with reflection | Cannot be subclassed — verify no `Class.forName(...).newInstance()` patterns try to subclass it |
| `@Throws(IOException::class)` for cross-language exception flow | Required for Java callers to use checked exception. Audit that the declared exceptions match what the function actually throws. |
| Platform types (`String!`) from Java | Silent NPE producers. Require Java side to annotate with `@NotNull`/`@Nullable` (or JSR-305 / Jetbrains annotations). |
| `lateinit var` exposed to Java | Java sees a plain field — `UninitializedPropertyAccessException` becomes confusing for Java callers |
| `@JvmSynthetic` on Kotlin-only API | Acceptable — hides from Java |

Reference: [anti-patterns §7 Java Interop Pitfalls](../../builder/reference/kotlin-anti-patterns.md#7-java-interop-pitfalls).

### 6. Kotlin reflection (`kotlin.reflect`)

`kotlin-reflect.jar` (~3 MB) is opt-in. Use only for trusted code; never reflect over untrusted class names.

| Pattern | Verdict |
|---------|---------|
| `Class.forName(userInput)` | **Reject categorically** — reflection-based class loading from user input is RCE class |
| `KClass<*>.createInstance()` over user-controlled type | Same — reject |
| `KCallable<*>.call(...)` on a `KFunction` resolved from untrusted name | Reject |
| `KClass<*>.memberProperties.find { it.name == userInput }` | Acceptable IF target class is a closed sealed hierarchy with no sensitive members |
| `@Serializable` deserialization with `Json { classDiscriminator = "@type" }` polymorphic | **High risk** — see §7 below |

### 7. Kotlinx serialization untrusted input audit

Each `kotlinx.serialization` `Json {}` instance has a hardening configuration. Untrusted-input audits:

| Config knob | Default | Hardened |
|-------------|---------|----------|
| `ignoreUnknownKeys` | `false` (strict — good) | Keep `false` for untrusted input. Setting `true` to "be permissive" allows attackers to smuggle fields that later code may read. |
| `isLenient` | `false` | Keep `false`. `true` accepts unquoted strings, comments, etc. — parser fuzzing surface. |
| `allowSpecialFloatingPointValues` | `false` | Keep `false` for protocol safety. |
| `coerceInputValues` | `false` | Keep `false` for strict typing. |
| `prettyPrint` | `false` | N/A for input security |
| `useArrayPolymorphism` | `false` (default) | Keep `false`; array-polymorphism enables type-name in the wire format |

**Polymorphic deserialization** is the #1 RCE class:

```kotlin
// FLAG: closedPolymorphic still requires every concrete type to be registered,
// but a sealed hierarchy with a constructor that runs side effects on init
// becomes an injection sink.
@Serializable
sealed class Command {
    @Serializable @SerialName("exec") data class Exec(val cmd: String) : Command() {
        init { Runtime.getRuntime().exec(cmd) }   // ← attacker-triggerable
    }
}
```

**Audit rule**: deserialization-time side effects are unsafe. Constructors and `init {}` blocks of `@Serializable` classes must be pure. Move side effects to a post-decode step.

Reference: kotlinx-serialization docs on `SerializersModule` + polymorphism.

### 8. Spring Boot Kotlin pitfalls

Spring's CGLIB-based proxy creation **requires** beans/components be `open` (or use `kotlin-spring` compiler plugin to auto-open them).

| Pattern | Audit |
|---------|-------|
| `@Component class FooService` without `kotlin-spring` plugin | Final by default → Spring proxy fails at startup. Use `kotlin-spring` to auto-open `@Component`/`@Service`/`@Repository`/`@Controller`/`@Configuration` |
| `@Transactional fun foo()` on a `final` method | Transaction proxy can't override → `@Transactional` silently ignored. Use `kotlin-spring`. |
| `@Bean fun foo(): T = ...` in non-open `@Configuration` class | Same — `kotlin-spring` resolves this. |
| `@ConfigurationProperties` on `data class` | Requires `kotlin-jvm` ≥ 1.4 + `@ConstructorBinding`. Audit for missing constructor binding (silently null fields). |
| Public mutable Spring `@Value` injection | Mutable injection bypasses immutability invariants. Prefer constructor injection with `val`. |

Reference: [anti-patterns §4 Class Hierarchy Pitfalls](../../builder/reference/kotlin-anti-patterns.md#4-class-hierarchy-pitfalls).

### 9. KSP2 generated code review

KSP2 (Kotlin Symbol Processing 2) generates source at compile time. The generated code is **referenced** but invisible in IDE/git unless you specifically open `build/generated/ksp/`.

| Pattern | Audit |
|---------|-------|
| KSP processor with network access (codegen that fetches schema at compile time) | Reject — supply-chain risk; pull schema deterministically from a versioned dep |
| KSP processor running shell commands | Reject |
| Generated code referenced from main module without inspection | Periodically `find build/generated/ksp/ -name '*.kt' \| xargs head -n 40` for sanity check |
| KSP version unpinned (`libs.versions.toml`) | Reject — KSP version mismatch with Kotlin compiler causes silent codegen drift |

Reference: [anti-patterns §13 Gradle / KSP Pitfalls](../../builder/reference/kotlin-anti-patterns.md#13-gradle--ksp-pitfalls).

### 10. Ktor server auth interceptor placement

Ktor's `Authentication` plugin must be `install()`-ed and **routes wrapped in `authenticate { ... }`** to be enforced. Forgetting either leaves routes open.

```kotlin
fun Application.module() {
    install(Authentication) {
        bearer("auth-bearer") {
            authenticate { token -> verifyJwt(token) }
        }
    }
    routing {
        authenticate("auth-bearer") {        // ← REQUIRED wrapper
            get("/protected") { /* ... */ }
        }
        get("/public") { /* ... */ }         // intentionally open
    }
}
```

| Audit | How |
|-------|-----|
| Every protected route inside `authenticate("name") { ... }` | `rg -n 'get\("\|post\("\|put\("\|delete\("' --type kotlin -B 5` then verify enclosing scope |
| `install(Authentication) { ... }` called before `routing { ... }` | Plugin ordering matters; install must precede the route definitions that depend on it |
| No `respond(HttpStatusCode.OK, secretPayload)` outside `authenticate` blocks | Grep for response writes near sensitive data without auth wrapper |
| Status pages plugin masks internal exceptions | `install(StatusPages) { exception<Throwable> { call, _ -> call.respondText("error") } }` — verify the masking doesn't hide auth bypass errors needed for SOC monitoring |

Reference: Ktor `Authentication` docs.

### 11. Logging secrets — `kotlin-logging` lazy eval gotcha

`io.github.oshai:kotlin-logging` provides `logger.info { "msg $expensiveCall()" }` — the **lambda form** is lazy and the message expression isn't computed at non-enabled levels.

| Pattern | Verdict |
|---------|---------|
| `logger.info("token=$secret")` (string form) | Evaluates `secret` regardless of log level; if the appender forwards to file/SaaS, secret hits disk | Reject |
| `logger.info { "token=$secret" }` (lambda form) | Still evaluates when `info` is enabled (almost always). **Lazy ≠ redacted.** Reject for secrets. |
| `logger.debug { "token=$secret" }` in dev only | Debug logs frequently leak to prod via env mistakes. Reject. |
| `logger.info("user logged in")` with no interpolation | Acceptable |
| Structured logging via SLF4J + MDC for secrets | Reject — MDC values are serialized to JSON in modern stacks; secret hits OpenSearch/Splunk |

```kotlin
// FLAG: lazy lambda doesn't redact, it just defers
logger.info { "Authenticating with $accessToken" }

// FIX: don't log the secret at all; log the fact
logger.info { "Authentication attempt for user=${user.id}" }
```

Audit grep:

```sh
rg -n 'logger\.(info|debug|trace|warn|error)' --type kotlin | rg -iE '(token|password|secret|key|credential|api[_-]?key)'
```

### 12. Configuration secrets

| Pattern | Verdict |
|---------|---------|
| `application.yml` with `db.password: ${DB_PASSWORD}` resolving from env | Acceptable |
| Hard-coded API key in `application.properties` committed to git | Reject |
| `System.getenv("PROD_SECRET")` with no fallback | Acceptable; verify no `?: "default-value"` accidentally checked in |
| Decrypting Jasypt-encrypted properties at startup | Acceptable; verify the master key is **not** also in the repo |
| Spring Cloud Config Server contacted unauthenticated | Reject — config server must require mTLS or bearer auth |
| Secrets in Kubernetes Secret with `data:` (base64) instead of `stringData:` | base64 is encoding, not encryption; rotate via External Secrets / Sealed Secrets / Vault |

### 13. JVM-level security flags (server-side Kotlin)

| Flag | Audit |
|------|-------|
| `java.security.manager` enabled? | SecurityManager is deprecated for removal post-JDK 21 — do not rely on it for new code |
| `JEP 411` (SecurityManager-less era) — alternative isolation | Document the threat model that replaces SM (containers, gVisor, language-level audit) |
| `-XX:+DisableAttachMechanism` | Prevents jcmd / jattach attach in containers — defense in depth |
| `-Djdk.tls.client.protocols=TLSv1.3` | Pin TLS minimum |
| `-Djdk.tls.disabledAlgorithms=…,3DES_EDE_CBC,…` | Audit `java.security` for the disabled-algorithms list; add cipher families EOL'd between baseline JDK and 2026 |
| `--enable-preview` in production | Reject; preview APIs may change |
| Native image / GraalVM specific reachability metadata | Verify reflective access for `kotlin-reflect` users is declared explicitly |

### 14. CI gate — Detekt security profile

```yaml
# detekt.yml
potential-bugs:
  active: true
  UnsafeCallOnNullableType: { active: true }
  UnsafeCast: { active: true }
  LateinitUsage: { active: true, ignoreOnClassesPattern: '.*Test' }
  UnreachableCode: { active: true }
  WrongEqualsTypeParameter: { active: true }

coroutines:
  active: true
  GlobalCoroutineUsage: { active: true }
  RedundantSuspendModifier: { active: true }
  SuspendFunWithCoroutineScopeReceiver: { active: true }

style:
  ForbiddenComment:
    active: true
    values:
      - 'TODO:'
      - 'FIXME:'
      - 'HACK:'
      - 'XXX:'
    # Custom: flag CVE references stuck in TODOs
    excludes: []

# .github/workflows/kotlin-security.yml
- run: ./gradlew detekt --auto-correct=false
- run: ./gradlew dependencyCheckAnalyze    # OWASP Dependency-Check
- run: ./gradlew :app:dependencies | tee deps.txt
- run: |
    # Verify no SNAPSHOT versions in production-bound configurations
    grep -E 'SNAPSHOT' deps.txt && exit 1 || true
- run: |
    # libs.versions.toml hygiene
    grep -E '"(\d+\.)?\d+(\.\d+)?(-SNAPSHOT|-EAP)"' gradle/libs.versions.toml && exit 1 || true
```

---

## Triage priorities

When multiple findings stack, rank by:

1. **`!!` / `lateinit` on attacker-influenced data** — DoS via NPE, sometimes type-confusion-led RCE on `as` cast.
2. **`runBlocking` on hot path** — single attacker-crafted request pins a worker; saturate worker pool for DoS.
3. **`GlobalScope.launch` / orphan coroutine scope** — silent task continuation past cancellation; sensitive data work continues after auth context tear-down.
4. **`@Serializable` polymorphic deserialization with side-effecting `init {}`** — classic deserialization RCE class.
5. **Ktor route missing `authenticate { }` wrapper** — direct authn bypass.
6. **`@JvmField` on secret or invariant-holding fields** — Java reflection / JNI bypass.
7. **Spring `@Transactional` on `final` method (missing `kotlin-spring`)** — silently no-op transactions, data-integrity risk.
8. **Untrusted `Class.forName` / `KClass.createInstance`** — direct RCE.
9. **Secret logging via `kotlin-logging`** (string or even lambda form interpolating secrets) — silent persistent leak.
10. **`Json { ignoreUnknownKeys = true, isLenient = true }` on untrusted input** — parser-laxity attack surface.
11. **KSP processor with network / shell access** — supply-chain via build process.
12. **JDK / library SNAPSHOT versions** in production builds — silent dep drift.

---

## Sources

- Kotlin coroutines — exception handling: https://kotlinlang.org/docs/exception-handling.html
- Kotlin coroutines — cancellation and timeouts: https://kotlinlang.org/docs/cancellation-and-timeouts.html
- Kotlinx serialization — JSON configuration: https://kotlinlang.org/api/kotlinx.serialization/kotlinx-serialization-json/
- Ktor server — Authentication: https://ktor.io/docs/server-authentication.html
- Spring Boot — Kotlin support: https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.kotlin
- `kotlin-spring` compiler plugin: https://kotlinlang.org/docs/all-open-plugin.html#spring-support
- KSP (Kotlin Symbol Processing): https://kotlinlang.org/docs/ksp-overview.html
- Detekt rule catalog: https://detekt.dev/docs/rules/overview/
- OWASP Dependency-Check Gradle plugin: https://jeremylong.github.io/DependencyCheck/dependency-check-gradle/
- `kotlin-logging`: https://github.com/oshai/kotlin-logging
- OWASP Application Security Verification Standard (ASVS): https://owasp.org/www-project-application-security-verification-standard/
- JEP 411 (deprecate SecurityManager for removal): https://openjdk.org/jeps/411
