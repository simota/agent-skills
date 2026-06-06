# Deprecation Detection

## npm Audit Commands
```bash
npm outdated              # Check for outdated packages
npm audit                 # Security vulnerabilities
npx npm-check -u          # Interactive update
npx depcheck              # Unused dependencies
```

## Signals of Deprecated Libraries
- No commits in 12+ months
- Open issues without responses
- "Deprecated" in README
- Archived repository
- Major version behind (e.g., React 16 when 19 exists)

## Multi-Ecosystem Detection Commands

### Python
```bash
pip-audit                          # PyPA official; queries OSV + PyUp Safety DB
pip list --outdated                # All outdated packages
python -W all -c "import <mod>"   # Trigger DeprecationWarning at import time
```
Note: PEP 594 removed 19 stdlib modules in Python 3.13 (aifc, cgi, crypt, telnetlib, etc.). Source: [peps.python.org/pep-0594](https://peps.python.org/pep-0594/)

### Go
```bash
govulncheck ./...                  # Google's official Go vulnerability checker
go list -m -u all                  # Show available module upgrades
```
Note: Go 1.24 deprecated `crypto/cipher.NewOFB`, `NewCFBEncrypter`, `NewCFBDecrypter` (unauthenticated; use AEAD or `NewCTR`) and `runtime.GOROOT()`. Source: [go.dev/doc/go1.24](https://go.dev/doc/go1.24)

### Java
```bash
./mvnw versions:display-dependency-updates   # Maven: check outdated deps
./gradlew dependencyUpdates                  # Gradle: check outdated deps
```
Note: JDK 24 permanently disabled `SecurityManager` (JEP 486). JDK 26 removed Applet API entirely (JEP 504). Sources: [openjdk.org/jeps/486](https://openjdk.org/jeps/486), [openjdk.org/jeps/504](https://openjdk.org/jeps/504)

### Node.js / npm
```bash
npm outdated              # Check for outdated packages
npm audit                 # Security vulnerabilities
npm audit signatures      # Verify registry signatures (supply chain)
npx npm-check -u          # Interactive update
npx depcheck              # Unused dependencies
node -e "require('util').isArray([])"  # Verify removed APIs (throws in Node 24+)
```
Note: Node 24 (Active LTS) removed all `util.is*()` helpers and `SlowBuffer`. OpenSSL 3.5 defaults reject keys < 2048-bit RSA/DH and < 224-bit ECC. Source: [nodejs.org deprecated APIs v22](https://nodejs.org/docs/latest-v22.x/api/deprecations.html)

### OSV Scanner (language-agnostic)
```bash
osv-scanner scan --lockfile package-lock.json
osv-scanner scan --lockfile requirements.txt
osv-scanner scan --lockfile go.sum
```
Queries the OSV database aggregating NVD, GitHub Advisory, and ecosystem-specific advisories across npm, PyPI, Go modules, Cargo, Maven, and more.
