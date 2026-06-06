# LaTeX Typesetting Reference

Purpose: Produce academic and book-length output via LaTeX / XeLaTeX / LuaLaTeX, or modern Typst. Cover engine selection (multilingual / CJK / RTL), document classes (article / book / memoir / KOMA-Script), bibliography (BibTeX vs biblatex), reproducibility (TeX Live / nix-tex), and Pandoc Markdown → LaTeX bridge.

## Scope Boundary

- **morph `latex`**: LaTeX / Typst typesetting (this document).
- **morph `pdf` (elsewhere)**: PDF generation in general (may delegate here).
- **morph `md` (elsewhere)**: Markdown → format dispatch.
- **Builder (elsewhere)**: Custom LaTeX package authoring.

## Engine Selection

| Engine | When | Notes |
|--------|------|-------|
| **pdfLaTeX** | English / Latin scripts only | Fastest; no Unicode / OpenType fonts |
| **XeLaTeX** | Multilingual, CJK, RTL, OpenType | Default for non-English; uses fontspec |
| **LuaLaTeX** | Programmatic typesetting, OpenType, Lua scripting | Slower than XeLaTeX; future of TeX |
| **Typst** | Modern alternative; fast incremental compile | Not LaTeX-compatible; growing ecosystem (2025+) |

For Japanese: XeLaTeX with `bxjsarticle` / `ltjsarticle` (LuaLaTeX), or LuaLaTeX with `luatexja-preset`.
For Arabic / Hebrew: XeLaTeX with `polyglossia` (replaces babel for non-Latin).

## Document Classes

| Class | Use case |
|-------|----------|
| `article` | Short papers, reports |
| `book` | Books, theses (chapter-based) |
| `report` | Mid-length reports with chapters |
| `memoir` | Books with rich customization |
| `KOMA-Script` (`scrartcl`, `scrbook`) | European typography traditions; modern defaults |
| `tufte-latex` | Side-note layouts (Edward Tufte style) |
| `IEEEtran` / `acmart` / `elsarticle` / `springer` | Conference / journal templates |

Choose conference-specific class when submitting to one; their style files are mandatory.

## Minimal XeLaTeX Document

```latex
\documentclass[12pt,a4paper]{article}

\usepackage{fontspec}
\usepackage{polyglossia}
\setdefaultlanguage{english}
\setotherlanguage{japanese}

\setmainfont{Noto Serif}
\setsansfont{Noto Sans}
\setmonofont{Noto Sans Mono}

\usepackage{microtype}
\usepackage{geometry}
\geometry{margin=25mm}

\usepackage{biblatex}
\addbibresource{refs.bib}

\title{Document Title}
\author{Jane Doe}
\date{\today}

\begin{document}
\maketitle
\tableofcontents

\section{Introduction}
Body text here.

\printbibliography
\end{document}
```

Compile:
```bash
xelatex doc.tex && biber doc && xelatex doc.tex && xelatex doc.tex
```

Or via `latexmk`:
```bash
latexmk -xelatex -bibtex doc.tex
```

## Bibliography: BibTeX vs biblatex

| | BibTeX | biblatex |
|---|--------|----------|
| Backend | bibtex | biber (recommended) |
| Unicode | poor | full (with biber) |
| Style customization | hard | flexible (via `biblatex-*` styles) |
| Modern features | limited | rich (filtering, multiple bibs, citation modes) |

Default biblatex+biber for new work. Use BibTeX only if a journal style mandates it.

```latex
% biblatex with author-year
\usepackage[backend=biber,style=authoryear,sorting=nyt]{biblatex}
\addbibresource{refs.bib}

% in body
\textcite{knuth1984} or \parencite{knuth1984}
```

`refs.bib`:
```bibtex
@article{knuth1984,
  author    = {Donald E. Knuth},
  title     = {Literate Programming},
  journal   = {The Computer Journal},
  volume    = {27},
  number    = {2},
  pages     = {97--111},
  year      = {1984},
  doi       = {10.1093/comjnl/27.2.97},
}
```

## Math Typesetting

```latex
\usepackage{amsmath}    % display math, align*, etc.
\usepackage{amssymb}    % \mathbb, \mathcal
\usepackage{mathtools}  % refinements over amsmath
\usepackage{unicode-math}  % XeLaTeX/LuaLaTeX: Unicode math, OpenType math fonts
\setmathfont{Latin Modern Math}
```

```latex
\begin{equation}
  E = m c^2 \label{eq:emc2}
\end{equation}

Refer to \eqref{eq:emc2}.

\begin{align*}
  f(x) &= \sum_{i=0}^{\infty} \frac{x^i}{i!} \\
       &= e^x
\end{align*}
```

## Code Listings

```latex
\usepackage{listings}      % older, simpler
\usepackage{minted}        % requires Pygments + --shell-escape; better
% or
\usepackage{lstautogobble}

\begin{minted}{python}
def hello(name):
    print(f"Hello, {name}")
\end{minted}
```

`minted` requires `--shell-escape`:
```bash
xelatex -shell-escape doc.tex
```

## Tables

```latex
\usepackage{booktabs}      % \toprule, \midrule, \bottomrule
\usepackage{tabularx}      % flexible width
\usepackage{longtable}     % multi-page tables
\usepackage{siunitx}       % aligned numbers, units

\begin{tabular}{l S[table-format=4.2] r}
\toprule
Item & {Cost} & Count \\
\midrule
A    & 12.50 & 10 \\
B    & 100.00 & 5 \\
\bottomrule
\end{tabular}
```

## Figures

```latex
\usepackage{graphicx}
\usepackage{caption}
\usepackage{subcaption}

\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.7\textwidth]{plot.pdf}
  \caption{Caption.}
  \label{fig:plot}
\end{figure}
```

PDF figures preferred (vector); PNG only for raster.

## Pandoc Markdown → LaTeX

```bash
pandoc paper.md \
  -o paper.pdf \
  --pdf-engine=xelatex \
  --citeproc \
  --bibliography=refs.bib \
  --csl=ieee.csl \
  --variable=mainfont:"Noto Serif" \
  --variable=geometry:margin=25mm \
  --number-sections \
  --toc
```

For more LaTeX control, generate `.tex` and edit:
```bash
pandoc paper.md -o paper.tex --standalone --template=template.tex
```

## Typst (Modern Alternative)

```typst
#set document(title: "My Document", author: "Jane Doe")
#set page(paper: "a4", margin: 25mm)
#set text(font: "Noto Serif", size: 11pt, lang: "en")

= Introduction

Body text with #emph[emphasis] and #strong[strong].

$ E = m c^2 $

#figure(
  image("plot.png", width: 70%),
  caption: [A figure caption.],
) <plot>

See @plot.

#bibliography("refs.bib", style: "ieee")
```

Compile: `typst compile doc.typ`. Sub-second incremental builds. Native multilingual.

## Reproducibility

Pin TeX Live edition:
```dockerfile
FROM texlive/texlive:TL2024-historic
COPY . /work
WORKDIR /work
RUN latexmk -xelatex -bibtex doc.tex
```

Or via Nix:
```nix
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  buildInputs = [
    (pkgs.texlive.combine {
      inherit (pkgs.texlive) scheme-medium fontspec biblatex biber latexmk;
    })
  ];
}
```

Always commit `.bib`, source `.tex`, and config; never commit `.pdf` (build artifact).

## Workflow

```
SOURCE      →  Markdown / native .tex / Typst

ENGINE      →  decide: pdfLaTeX / XeLaTeX / LuaLaTeX / Typst
            →  driver: language, fonts, build speed

CLASS       →  article / book / report / KOMA-Script / journal-specific

PACKAGES    →  microtype + geometry + booktabs (always)
            →  amsmath + mathtools + unicode-math (if math)
            →  biblatex + biber (citations)
            →  hyperref (last; clickable PDF)
            →  cleveref (after hyperref; smart \cref)

BIB         →  biblatex + biber default
            →  CSL via Pandoc only when citeproc fits
            →  refs.bib in repo

BUILD       →  latexmk (handles run loop)
            →  or container/Nix for reproducibility
            →  pin TeX Live edition

VALIDATE    →  no LaTeX warnings (overfull boxes, undefined refs)
            →  PDF/A if archival
            →  Search must work; copy/paste must yield text not gibberish

DELIVER     →  PDF + sources committed
            →  README with build command

HANDOFF     →  Builder: custom .sty / .cls
            →  Cloak: scrub PII from PDF metadata
            →  morph `pdf`: PDF/A archival pipeline
```

## Output Template

```markdown
## LaTeX Package: [Document]

### Engine + Class
- Engine: [XeLaTeX / LuaLaTeX / pdfLaTeX / Typst]
- Class: [article / scrbook / IEEEtran / ...]
- Rationale: [language, target venue, length]

### Source Layout
- main.tex (preamble + \input{} chapters)
- chapters/*.tex
- refs.bib
- figures/ (vector PDF preferred)
- latexmkrc

### Required Packages
[full preamble or list]

### Bibliography
- Style: [author-year / numeric / journal-specific]
- Backend: biber
- Source: refs.bib (N entries)

### Build
\`\`\`bash
latexmk -xelatex -bibtex main.tex
\`\`\`

### Reproducibility
- TeX Live: [edition]
- Container: [Dockerfile / Nix / N/A]

### Validation
- LaTeX warnings: [count, severity]
- Overfull/Underfull boxes: [count]
- Citation completeness: [N/M]
- PDF text-search: [pass/fail]
- PDF/A if archival: [yes/no]

### Handoffs
- Builder: custom .sty for repeat use
- Cloak: PDF metadata sanitization
- morph `pdf`: PDF/A archival
```

## Anti-Patterns

| Anti-pattern | Fix |
|--------------|-----|
| Manual section numbering | Use `\section` etc.; let LaTeX number |
| Inline raster math screenshots | Use real LaTeX math; copy/paste must work |
| `inputenc{utf8}` with XeLaTeX | XeLaTeX is Unicode native; remove inputenc |
| BibTeX with biblatex | Use biber backend; set `backend=biber` |
| `\bf` / `\it` (legacy) | Use `\textbf` / `\textit` / `\emph` |
| `tabular` with `\hline` everywhere | Use booktabs (`\toprule` etc.) |
| `\\` to force line breaks for layout | Use semantic paragraphs; LaTeX handles spacing |
| Ignoring overfull-box warnings | Treat as bugs; rewrite or `\sloppy` selectively |
| Loading `hyperref` first | Load near-last; many packages tweak it |
| No `latexmk` / `latexmkrc` | Manual run loops break; use latexmk |
| PNG figures everywhere | Prefer PDF / SVG / TikZ vector |
| `\textsuperscript{...}` for footnote | Use `\footnote{...}` |
| Hard-coded TeX Live version not pinned | Pin via container/Nix; reproducibility |
| Bib without DOI | Add DOI per modern citation practice |
| `pdfLaTeX` for Japanese | Use XeLaTeX/LuaLaTeX with CJK packages |

## Deliverable Contract

When `latex` completes, emit:

- **Engine choice** with rationale.
- **Document class** selection.
- **Source layout** with file structure.
- **Preamble** (packages + load order).
- **Bibliography** strategy (biber + style).
- **Build command** (latexmk).
- **Reproducibility** plan (container / Nix).
- **Validation report** (warnings, overfull, PDF/A).
- **Handoffs**: Builder, Cloak, morph `pdf`.

## References

- *The LaTeX Companion* (3rd ed., 2023) — Mittelbach, Fischer
- *LaTeX: A Document Preparation System* — Lamport
- TeX Live — tug.org/texlive/
- LaTeX3 / expl3 documentation — latex-project.org
- biblatex / biber — github.com/plk/biblatex
- KOMA-Script — komascript.de
- LuaLaTeX docs — luatex.org
- XeLaTeX / fontspec — ctan.org/pkg/fontspec
- polyglossia — ctan.org/pkg/polyglossia
- unicode-math — ctan.org/pkg/unicode-math
- Typst — typst.app, github.com/typst/typst
- Pandoc LaTeX writer — pandoc.org/MANUAL.html#latex
- Overleaf documentation — learnoverleaf.com (good gradient)
- TeX Live Docker — hub.docker.com/r/texlive/texlive
- TUG — tug.org (TeX Users Group)
- ISO 32000 — PDF specification
- ISO 19005 — PDF/A archival
