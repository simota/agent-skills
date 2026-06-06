# Sweep Cleanup Target Catalog Reference

Purpose: candidate categories, detection signals, and verification hints for cleanup proposals.

## Contents

1. Dead code
2. Orphan assets
3. Unused dependencies
4. Build artifacts and temp files
5. Duplicate files
6. Configuration remnants

## Dead Code

**Indicators**
- Source files with no imports or requires
- Exported functions or classes with zero external usage
- Tests for deleted source files
- Stories or docs for removed components
- Commented-out code or files marked `old`, `backup`, or `deprecated`

**Verify by**
1. Building an import graph
2. Checking entry points and public exports
3. Searching for dynamic references
4. Reviewing recent git history

## Orphan Assets

**Indicators**
- Images, icons, fonts, or static files with no code, CSS, or HTML reference
- Placeholder assets never integrated
- Duplicate logo or image variants

**Verify by**
1. Scanning asset directories
2. Searching filename references across code and styles
3. Checking `url()` usage in CSS/SCSS
4. Verifying build or bundler includes

## Unused Dependencies

**Indicators**
- Packages declared but never imported
- Tooling dependencies for removed workflows
- Peer or dev dependencies no longer referenced

**Verify by**
1. Parsing dependency manifests
2. Searching imports and requires
3. Checking scripts and config files
4. Confirming CI or build usage

## Build Artifacts And Temp Files

**Indicators**
- Committed files that match `.gitignore`
- Generated output in the source tree
- Cache, log, or temporary files tracked by mistake

**Common examples**
- `dist/`, `build/`, `out/`
- `.cache/`
- `*.log`, `*.tmp`, `*.bak`
- partial `node_modules/` commits

## Duplicate Files

**Indicators**
- Identical content stored under different names
- Copy-pasted utilities across features
- Vendored files duplicated instead of imported

**Verify by**
1. Grouping files by size and hash
2. Confirming which copy is canonical
3. Checking import paths before removing duplicates

## Configuration Remnants

**Indicators**
- Config files for tools no longer used
- Environment files for deprecated services
- CI or deployment config for removed workflows

**Verify by**
1. Mapping each config file to its tool or service
2. Checking scripts, CI, hooks, and IDE integration
3. Confirming no active environment or deployment dependency
