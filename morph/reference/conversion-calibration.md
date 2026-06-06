# Conversion Calibration System (TRANSMUTE)

Purpose: Use this reference after conversion work to record outcomes, evaluate quality trends, and update tool/template heuristics safely — the **cross-conversion** learning loop.
Pair with: `quality-assurance.md` for the **per-conversion** scoring inputs that feed this loop (4-metric weights, A-F grade definitions, verification commands, report template). The Quality_Score block in the record schema below uses the metrics defined there.

## Contents

- Record schema
- Quality thresholds
- Tool effectiveness
- Calibration rules
- Journal format
- Pattern library

## RECORD — Log Conversion Activities

```yaml
Conversion: [conversion-id]
Type: [Markdown→PDF | Markdown→Word | Markdown→HTML | Word→PDF | HTML→PDF | Batch | Other]
Source_Format: [Markdown | Word | HTML | Excel | draw.io | Mermaid]
Target_Format: [PDF | Word | HTML | PNG | SVG]
Tool_Used: [pandoc+xelatex | pandoc+wkhtmltopdf | LibreOffice | Chrome/Puppeteer | mermaid-cli | draw.io-cli]
Template_Used: [corporate-ja | technical-ja | report-ja | minimal | corporate.css | technical.css | print.css | none]
Quality_Score:
  structure: [0-100]
  visual: [0-100]
  content: [0-100]
  metadata: [0-100]
  overall: [0-100]
  grade: [A/B/C/D/F]
Features_Lost: [list]
Japanese_Specific: [yes/no]
Accessibility_Applied: [PDF/UA/WCAG: yes/no]
Processing_Time: [seconds]
Downstream_Handoff: [Guardian/Nexus/Lore/None]
```

## EVALUATE — Quality Thresholds

Per-conversion grade scale (A/B/C/D/F at 90/80/70/60) is defined in `quality-assurance.md`. For **trend interpretation across many conversions**, use the same boundaries: averages ≥ 90 = excellent, 80-89 = maintain current approach, 70-79 = review tool/template choice, < 70 = investigate root causes.

Tool effectiveness:

| Score | Meaning |
|------|---------|
| `> 0.85` | Highly effective for this format pair |
| `0.70-0.85` | Good, context-sensitive |
| `< 0.70` | Underperforming; review alternatives |

Example defaults:

```yaml
markdown_to_pdf:
  pandoc_xelatex: 0.95
  pandoc_wkhtmltopdf: 0.80
  pandoc_lualatex: 0.90
word_to_pdf:
  libreoffice: 0.90
  pandoc: 0.65
html_to_pdf:
  chrome_puppeteer: 0.90
  wkhtmltopdf: 0.80
  pandoc: 0.60
```

## CALIBRATE — Rules

1. Require `3+ conversions` before changing a heuristic.
2. Limit each adjustment to `±0.15`.
3. Decay adjustments `10%` per quarter toward defaults.
4. User-explicit tool preference overrides calibration.

## PROPAGATE — Journal Format

```md
## YYYY-MM-DD - TRANSMUTE: [Conversion Type]

**Conversions assessed**: N
**Average quality**: Grade X (Y/100)
**Key insight**: [description]
**Calibration adjustment**: [tool/template: old -> new]
**Apply when**: [future scenario]
**reusable**: true

<!-- EVOLUTION_SIGNAL
type: PATTERN
source: Morph
date: YYYY-MM-DD
summary: [conversion insight]
affects: [Morph, Scribe, Lore]
priority: MEDIUM
reusable: true
-->
```

## Pattern Library

| Context | Best tool | Best template | Key settings | Quality |
|---------|-----------|---------------|-------------|---------|
| Japanese business doc | `pandoc+lualatex` | `corporate-ja` | Hiragino fonts, `A4`, `25mm` margins | Very High |
| Technical specification | `pandoc+xelatex` | `technical-ja` | code highlighting, TOC, numbered sections | High |
| Quick PDF export | `pandoc+wkhtmltopdf` | none | fast processing, basic styling | Medium |
| Accessible PDF | `pandoc+lualatex` | tagged PDF options | PDF/UA, lang metadata, `12pt` min | High |
| Stakeholder report | `pandoc+lualatex` | `corporate-ja` | TOC, header/footer, watermark | Very High |
