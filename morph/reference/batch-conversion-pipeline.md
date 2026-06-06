# Batch Conversion Pipeline Reference

Purpose: Build reproducible, parallel document conversion pipelines for many files / many formats. Cover Pandoc Lua filters (AST transforms), Makefile / Just / Taskfile orchestration, GitHub Actions matrices, parallel execution, version pinning, and integrity manifests.

## Scope Boundary

- **morph `batch`**: Multi-file / multi-format pipelines (this document).
- **morph `md` / `pdf` / `docx` / `epub` / `latex` (elsewhere)**: Single-format depth.
- **Stream (elsewhere)**: ETL data pipelines (different domain).
- **Pipe (elsewhere)**: GitHub Actions internals (this doc covers the conversion-specific layer).
- **Builder (elsewhere)**: Custom CLI tooling beyond this scope.

## Pipeline Anatomy

```
SOURCES        FILTERS              TARGETS
─────────  ──────────────────  ─────────────
*.md       →  Pandoc + Lua  →  *.pdf
              filters           *.docx
                                *.epub
                                *.html
```

Inputs feed Pandoc; Lua filters transform the AST; multiple targets emit per source. Parallelize per file, per target, or both.

## Pandoc Lua Filters

Lua filters operate on Pandoc's AST (after parse, before write). Cleaner than regex string transforms.

```lua
-- normalize-headers.lua: shift all headers down by 1 level
function Header(el)
  el.level = el.level + 1
  return el
end
```

```lua
-- promote-internal-links.lua: turn relative .md links into PDF section refs
function Link(el)
  if el.target:match("%.md$") then
    el.target = el.target:gsub("%.md$", "")
    el.classes:insert("internal-ref")
  end
  return el
end
```

```lua
-- strip-pii.lua: remove paragraphs flagged with class .pii
function Div(el)
  if el.classes:includes("pii") then
    return {}
  end
  return el
end

function Para(el)
  for _, inline in ipairs(el.content) do
    if inline.tag == "Strong" and inline.content[1].text == "[REDACTED]" then
      return pandoc.Para({ pandoc.Str("[content removed]") })
    end
  end
  return el
end
```

Apply:
```bash
pandoc input.md --lua-filter=normalize-headers.lua --lua-filter=strip-pii.lua -o out.pdf
```

Filter order matters; chain explicitly.

## Makefile Orchestration

```makefile
# Pin versions in environment
PANDOC ?= pandoc-3.5
LATEX  ?= xelatex
EPUBCHECK ?= /opt/epubcheck/epubcheck.jar

SOURCES := $(wildcard docs/*.md)
PDFS    := $(SOURCES:docs/%.md=build/pdf/%.pdf)
DOCXS   := $(SOURCES:docs/%.md=build/docx/%.docx)
EPUBS   := $(SOURCES:docs/%.md=build/epub/%.epub)
HTMLS   := $(SOURCES:docs/%.md=build/html/%.html)

ALL := $(PDFS) $(DOCXS) $(EPUBS) $(HTMLS)

.PHONY: all clean validate manifest

all: $(ALL)

build/pdf/%.pdf: docs/%.md filters/*.lua | build/pdf
	$(PANDOC) $< -o $@ \
	  --pdf-engine=$(LATEX) \
	  --lua-filter=filters/normalize-headers.lua \
	  --metadata-file=metadata.yml

build/docx/%.docx: docs/%.md filters/*.lua | build/docx
	$(PANDOC) $< -o $@ \
	  --reference-doc=templates/reference.docx \
	  --lua-filter=filters/normalize-headers.lua

build/epub/%.epub: docs/%.md filters/*.lua | build/epub
	$(PANDOC) $< -o $@ \
	  --css=styles/epub.css \
	  --epub-cover-image=cover.png \
	  --lua-filter=filters/normalize-headers.lua

build/html/%.html: docs/%.md filters/*.lua | build/html
	$(PANDOC) $< -o $@ \
	  --standalone \
	  --css=styles/web.css

build/pdf build/docx build/epub build/html:
	@mkdir -p $@

validate: $(EPUBS)
	@for f in $^; do java -jar $(EPUBCHECK) $$f || exit 1; done

manifest: $(ALL)
	@./scripts/manifest.sh > build/manifest.json

clean:
	rm -rf build/
```

Run with parallelism:
```bash
make -j8 all   # 8 parallel jobs
```

Make handles dependency graph; `-j` parallelizes leaves.

## Just / Taskfile Alternatives

**justfile** (cleaner Make):
```just
default:
    @just --list

build:
    fd '\.md$' docs/ | parallel pandoc {} -o build/pdf/{/.}.pdf

epub source:
    pandoc {{source}} --css=styles/epub.css -o build/epub/{{file_stem(source)}}.epub
```

**Taskfile.yml**:
```yaml
version: "3"
tasks:
  pdf:
    sources: ["docs/*.md"]
    generates: ["build/pdf/*.pdf"]
    cmds:
      - mkdir -p build/pdf
      - |
        for f in {{.SOURCES}}; do
          pandoc "$f" -o "build/pdf/$(basename $f .md).pdf" \
            --pdf-engine=xelatex --lua-filter=filters/normalize.lua
        done
```

## GNU parallel for File Fan-out

```bash
fd '\.md$' docs/ | parallel -j 8 \
  pandoc {} -o build/pdf/{/.}.pdf \
    --pdf-engine=xelatex --lua-filter=filters/normalize.lua
```

`{/.}` strips path and extension. `-j 8` for 8 parallel workers. Handles thousands of files.

## GitHub Actions Matrix

```yaml
name: Build docs
on: [push, pull_request]

jobs:
  build:
    strategy:
      fail-fast: false
      matrix:
        format: [pdf, docx, epub, html]
    runs-on: ubuntu-latest
    container: pandoc/extra:3.5  # pinned Pandoc + LaTeX
    steps:
      - uses: actions/checkout@v4
      - run: make build/${{ matrix.format }}/all
      - uses: actions/upload-artifact@v4
        with:
          name: docs-${{ matrix.format }}
          path: build/${{ matrix.format }}/
```

Matrix parallelizes formats. For per-file fan-out, generate the matrix dynamically:

```yaml
jobs:
  enumerate:
    outputs:
      sources: ${{ steps.list.outputs.sources }}
    steps:
      - uses: actions/checkout@v4
      - id: list
        run: echo "sources=$(fd '\.md$' docs/ | jq -R . | jq -s -c .)" >> $GITHUB_OUTPUT

  build:
    needs: enumerate
    strategy:
      matrix:
        source: ${{ fromJSON(needs.enumerate.outputs.sources) }}
    runs-on: ubuntu-latest
    steps:
      - run: pandoc "${{ matrix.source }}" -o "${{ matrix.source }}.pdf"
```

## Reproducibility

| Layer | Pin |
|-------|-----|
| Pandoc | `pandoc/extra:3.5` Docker tag |
| TeX Live | `texlive/texlive:TL2024-historic` |
| EPUBCheck | versioned jar |
| Custom filters | committed in repo |
| Templates / CSS | committed in repo |
| Fonts | committed or fetched at known SHA |

Container example:
```dockerfile
FROM pandoc/extra:3.5
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /docs
ENTRYPOINT ["make"]
```

## Integrity Manifest

```bash
#!/usr/bin/env bash
# scripts/manifest.sh: emit JSON manifest with input/output checksums
set -euo pipefail

# Portable SHA-256 hash (BSD/GNU compatible). See _common/PORTABILITY.md.
sha256_hash() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$@"
  elif command -v shasum >/dev/null 2>&1; then shasum -a 256 "$@"
  else echo "[ERROR] sha256sum/shasum not found" >&2; return 1; fi
}

cat <<EOF
{
  "generated_at": "$(date -u +%FT%TZ)",
  "tools": {
    "pandoc": "$(pandoc --version | head -1)",
    "xelatex": "$(xelatex --version | head -1)"
  },
  "files": [
EOF

first=true
for src in docs/*.md; do
  name=$(basename "$src" .md)
  for fmt in pdf docx epub html; do
    out="build/$fmt/$name.$fmt"
    [ -f "$out" ] || continue
    [ "$first" = true ] && first=false || echo ","
    cat <<JSON
    {
      "source": "$src",
      "source_sha": "$(sha256_hash "$src" | cut -d' ' -f1)",
      "target": "$out",
      "target_sha": "$(sha256_hash "$out" | cut -d' ' -f1)"
    }
JSON
  done
done

echo "  ]"
echo "}"
```

Manifest enables auditable redistribution and downstream verification.

## Caching

```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pandoc
      ~/.texlive
    key: pandoc-${{ runner.os }}-${{ hashFiles('Makefile', 'filters/*.lua') }}
```

Pandoc has no global cache by default; you cache TeX Live or your own intermediates (`build/` directory keyed on source SHA).

## Error Strategy

```makefile
build/pdf/%.pdf: docs/%.md
	@$(PANDOC) $< -o $@ 2> build/log/$*.log || \
	  (echo "FAIL: $<"; cat build/log/$*.log; exit 1)
```

Per-file logs prevent CI from hiding which doc failed.

## Workflow

```
INVENTORY    →  enumerate sources, formats, filters
             →  identify per-file vs per-format vs per-language axes

FILTERS      →  Lua filters per concern (headers / links / PII / metadata)
             →  chain explicitly; document order
             →  unit-test filters with sample AST

ORCHESTRATOR →  Make / just / Taskfile (local + simple)
             →  GitHub Actions matrix (CI scale)
             →  GNU parallel (per-file fan-out shell)

PIN          →  containers: Pandoc, TeX Live, EPUBCheck
             →  TL editions, font versions
             →  filter SHA in repo

PARALLEL     →  Make -j N for local
             →  matrix.format × matrix.source for CI
             →  per-job log + per-file log

VALIDATE     →  EPUBCheck for EPUBs
             →  PDF/A check for archival PDFs
             →  HTML validator for HTML
             →  link checker (lychee)

MANIFEST     →  JSON with sha256 of source + outputs + tool versions
             →  date + git SHA

CACHE        →  cache TeX Live / fonts in CI
             →  cache build/ keyed on source SHA

DELIVER      →  artifacts (CI) or release ZIP
             →  manifest committed alongside

HANDOFF      →  Pipe: deeper CI / reusable workflows
             →  Builder: filter authoring tooling
             →  Cloak: PII filter design
             →  Stream: if the conversion is part of a data pipeline
```

## Output Template

```markdown
## Batch Conversion Pipeline: [Project]

### Inventory
- Sources: [N markdown files]
- Targets: [pdf, docx, epub, html]
- Filters: [list of Lua filters with purpose]

### Orchestrator
- Tool: [Make / just / Taskfile / GitHub Actions matrix]
- Parallelism: [-j N / matrix size]

### Reproducibility
- Pandoc: [pandoc/extra:3.5]
- TeX Live: [TL2024-historic]
- EPUBCheck: [version]
- Fonts: [committed / pinned at SHA]

### Filter Chain
1. [filter1.lua] — purpose
2. [filter2.lua] — purpose
3. [filter3.lua] — purpose

### Validation
- EPUBCheck: [PASS]
- PDF/A: [PASS / N/A]
- Link check: [PASS]

### Manifest
- Path: build/manifest.json
- Fields: source, source_sha, target, target_sha, tools, generated_at

### CI
- Workflow: .github/workflows/docs.yml
- Cache keys: [list]
- Artifact retention: [days]

### Handoffs
- Pipe: reusable workflows
- Builder: filter authoring helpers
- Cloak: PII filter design
- Stream: if part of data pipeline
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Regex preprocessing instead of Lua filter | Use AST-aware Lua filters |
| Floating Pandoc version | Pin via container or `pandoc-3.5` symlink |
| Sequential conversion in CI | Use matrix or `make -j` for parallelism |
| One global log file | Per-file log; aggregate at the end |
| Caching `~/.cache/pandoc` (which doesn't exist) | Cache TeX Live, fonts, intermediate AST |
| Commit `.pdf` outputs to repo | Build artifacts; only commit sources |
| No EPUBCheck in pipeline | Validation gate before deploy |
| Filter ordering implicit | Document and enforce filter chain order |
| Mutating sources via filters | Filters operate on AST; don't write back to source |
| Single Makefile rule per format duplicating logic | Use pattern rules `%.pdf` |
| No integrity manifest | Generate JSON with SHA + tool versions |
| Manual conversion dance documented in README only | Codify in `make all` |
| Failing fast hides multi-file errors | `fail-fast: false` + per-job log |
| Forgetting `-shell-escape` for minted | Add to engine command; opt in via Makefile var |

## Deliverable Contract

When `batch` completes, emit:

- **Source / target / filter inventory**.
- **Orchestrator** (Makefile / just / Taskfile / GHA workflow).
- **Pinned tool versions** with container or lockfile.
- **Lua filter chain** with order and rationale.
- **Validation gates** (EPUBCheck, link check, PDF/A).
- **Integrity manifest** (JSON with SHAs + tool versions).
- **CI** workflow with matrix + caching.
- **Handoffs**: Pipe, Builder, Cloak, Stream.

## References

- Pandoc — pandoc.org
- Pandoc Lua filters — pandoc.org/lua-filters.html
- pandoc/extra Docker image — hub.docker.com/r/pandoc/extra
- TeX Live Docker — hub.docker.com/r/texlive/texlive
- EPUBCheck — github.com/w3c/epubcheck
- GNU make manual — gnu.org/software/make/manual/
- just — github.com/casey/just
- Taskfile — taskfile.dev
- GNU parallel — gnu.org/software/parallel/
- GitHub Actions matrix — docs.github.com/actions
- lychee link checker — github.com/lycheeverse/lychee
- ISO 32000 / 19005 — PDF / PDF/A
- W3C EPUB 3.3 — w3.org/TR/epub-33/
- "Reproducible Builds" — reproducible-builds.org
- "Pandoc filters in Lua" — Albert Krewinkel (Pandoc maintainer)
