# Sweep Exclusion Patterns Reference

Purpose: directories and files that should not be scanned or should not be deleted.

## Directories To Exclude From Scan

```text
# Package managers
node_modules/
vendor/
.venv/
venv/
__pycache__/

# Version control
.git/
.svn/
.hg/

# Build outputs
dist/
build/
out/
.next/
.nuxt/

# IDE / editor
.idea/
.vscode/
*.swp
*.swo

# Cache
.cache/
.parcel-cache/
.turbo/
```

## Files Never To Delete

```text
# Critical project files
LICENSE*
LICENCE*
CHANGELOG*
SECURITY*
CONTRIBUTING*

# Lock files
package-lock.json
yarn.lock
pnpm-lock.yaml
Gemfile.lock
poetry.lock
go.sum

# Environment files
.env*
*.local

# Git files
.gitignore
.gitattributes
.gitmodules

# CI / CD
.github/
.gitlab-ci.yml
.circleci/
Jenkinsfile
```

## `.sweepignore` Template

```text
# Project-specific exclusions for Sweep

# Vendored code
src/vendor/

# Generated code
src/generated/

# Legacy code under migration
src/legacy/

# Public assets loaded dynamically
public/images/icons/

# Runtime-loaded localization files
locales/
```
