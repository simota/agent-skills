# Japanese Typography Guide

Purpose: Use this reference when converting Japanese documents that require correct line breaking, fonts, page sizes, encoding, ruby, or vertical writing.

## Contents

- Kinsoku basics
- Line heights and font sizes
- Fonts
- Pandoc and tool settings
- Page sizes and margins
- Quality checklist

## Kinsoku Basics

Preserve Japanese readability:

- Do not leave prohibited punctuation at line start.
- Do not split inseparable character pairs or proper nouns mid-word.
- Use `markdown+east_asian_line_breaks` when line-breaking behavior matters.

## Line Heights And Font Sizes

| Element | Recommendation |
|--------|----------------|
| Body text | `1.7-1.8em` |
| Headings | `1.3em` |
| Tables | `1.3em` |
| H1 | `18-24pt` |

## Fonts

Recommended families:

- `Hiragino Mincho ProN`
- `Hiragino Sans`
- `Noto Serif CJK JP`
- `Noto Sans CJK JP`

Rules:

- Keep document encoding as `UTF-8`.
- Choose fonts with full Japanese glyph coverage.

## Pandoc And Tool Settings

```sh
# LuaLaTeX
pandoc input.md -o output.pdf \
  --pdf-engine=lualatex \
  -V mainfont="Hiragino Mincho ProN"

# XeLaTeX
pandoc input.md -o output.pdf \
  --pdf-engine=xelatex \
  -V mainfont="Hiragino Mincho ProN"

# wkhtmltopdf
wkhtmltopdf \
  --encoding UTF-8 \
  --page-size A4 \
  --margin-top 25mm \
  --margin-bottom 25mm \
  --margin-left 25mm \
  --margin-right 25mm \
  input.html output.pdf
```

For encoding repair:

```sh
iconv -f SHIFT_JIS -t UTF-8 input.md > input_utf8.md
```

## Ruby And Vertical Writing

- Ruby is supported via HTML or Markdown extensions when the toolchain allows it.
- Vertical writing requires explicit LaTeX or CSS support and should be treated as a special-case configuration.

## Common Page Sizes And Margins

| Name | Size | Typical use |
|------|------|-------------|
| A4 | `210 x 297 mm` | business standard |
| B5 | `182 x 257 mm` | books, magazines |
| A5 | `148 x 210 mm` | small books |

| Type | Top | Bottom | Left | Right |
|------|-----|--------|------|-------|
| Report | `25mm` | `25mm` | `25mm` | `25mm` |
| Book | `20mm` | `25mm` | `20mm` | `15mm` |
| Thesis | `30mm` | `25mm` | `30mm` | `25mm` |

## Quality Checklist

- [ ] Kinsoku rules look acceptable
- [ ] Line height is `1.7-1.8` for body text
- [ ] Fonts are embedded and correct
- [ ] Page size is appropriate (`A4` by default for business docs)
- [ ] Encoding is `UTF-8`
