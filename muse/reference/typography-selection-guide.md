# Typography Selection Delta

Purpose: Muse-specific decision and verification contract. Typeface classifications and pairing theory are model-known.

## Selection Contract

1. Read existing brand, design-token, and licensed-asset constraints before proposing fonts.
2. Name `2-3` candidates and tie each to the intended brand traits and actual content language.
3. Validate body readability, display distinctiveness, required weights, glyph coverage, numerals, punctuation, and fallback behavior at real sizes.
4. Verify licensing and delivery rights for the target environment.
5. Prefer one family or a deliberate display/body pair; add a family only when it creates measurable hierarchy or brand value.

Inter, Roboto, Arial, and system fonts are not universal bans. They are weak *default display choices* when differentiation is required, but remain valid when the existing product, platform convention, performance target, or brand system calls for them.

## Performance And Accessibility

- Measure compressed font payload and rendered CLS against the project's budgets; do not impose universal size or file-count thresholds.
- Subset only after confirming all required languages and symbols.
- Use `font-display` deliberately and test fallback metric compatibility.
- Preload only fonts proven critical above the fold.
- Check contrast, line height, line length, zoom behavior, and legibility for the target scripts.

## Output

Provide:

- brand and language requirements
- candidate comparison and selected rationale
- display/body/mono roles and token mapping
- weights, styles, axes, fallbacks, and source/license
- loading plan with measured budget impact
- screenshots or representative specimens at actual breakpoints when implementation exists

Reject fashionable font lists without project evidence, fixed personality-to-font mappings, and arbitrary bans presented as accessibility or performance facts.
