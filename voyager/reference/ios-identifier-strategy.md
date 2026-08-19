# Accessibility Identifier Strategy

Purpose: Design and audit the `accessibilityIdentifier` taxonomy that every Voyager[ios] query depends on. Identifiers are the contract between the shipping Swift code and the test suite — get the taxonomy right once, and refactors, localization, and copy edits stop breaking tests.

Contents:
- Taxonomy convention (`screen.section.element`)
- SwiftUI: `.accessibilityIdentifier()`
- UIKit: `isAccessibilityElement` + `accessibilityIdentifier`
- Accessibility Inspector verification workflow
- Gap-list audit template
- Common pitfalls

## Taxonomy Convention: `screen.section.element`

Every identifier follows a three-segment dot path: **screen** (the feature/view controller), **section** (a logical grouping within the screen), **element** (the specific control).

```
login.email.field
login.password.field
login.submit.button
login.error.label

checkout.summary.total
checkout.summary.promoCodeField
checkout.payment.applePayButton
checkout.payment.cardNumberField

orders.row                 // repeated identifier for list cells — see "Repeated Identifiers" below
orders.row.total
orders.empty.state
```

- Lowercase, dot-separated, `camelCase` within a segment if a segment name needs multiple words (`promoCodeField`, not `promo_code_field` or `promo-code-field`).
- **screen** matches the feature name Native uses in code/PRs, not an arbitrary abbreviation — a shared vocabulary prevents translation drift between the app team and the test suite.
- **section** is optional for flat screens (`login.submit.button` is fine without a section); required once a screen has more than ~5 elements or repeating structural groups (header/body/footer, form sections, tab content).
- Reserve numeric suffixes (`login.field.1`) for genuinely unordered/anonymous repeated content only; prefer a semantic section name (`checkout.shipping.field`, `checkout.billing.field`) whenever the fields differ in meaning.

### Repeated Identifiers (List / Collection Cells)

Cells in a list legitimately share one identifier — that is expected and queried via `matching(identifier:).element(boundBy:)` or filtered by a child element's text:

```swift
// Convention: the row shares one identifier, children carry role identifiers
app.cells.matching(identifier: "orders.row").element(boundBy: 0)
app.cells.matching(identifier: "orders.row").element(boundBy: 0).staticTexts["orders.row.total"]
```

Do not synthesize a unique identifier per row index at data-generation time (`"orders.row.\(index)"`) — that couples the identifier to list position instead of role, and breaks the moment sort order changes.

## SwiftUI: `.accessibilityIdentifier()`

```swift
struct LoginView: View {
    @State private var email = ""
    @State private var password = ""

    var body: some View {
        VStack(spacing: 16) {
            TextField("Email", text: $email)
                .accessibilityIdentifier("login.email.field")

            SecureField("Password", text: $password)
                .accessibilityIdentifier("login.password.field")

            Button("Sign In") { /* ... */ }
                .accessibilityIdentifier("login.submit.button")
        }
    }
}
```

- Apply `.accessibilityIdentifier(_:)` directly on the interactive view, not on a container `VStack`/`HStack` wrapping it — SwiftUI's accessibility tree collapses containers by default, and an identifier on the wrong node silently fails to resolve in XCUITest.
- For `ForEach`-generated rows, derive the identifier from a stable model property (an ID or slug), not the array index:
  ```swift
  ForEach(orders) { order in
      OrderRow(order: order)
          .accessibilityIdentifier("orders.row.\(order.id)")
  }
  ```
  This trades the "shared identifier + `boundBy`" pattern for a queryable-by-ID pattern — pick one convention per screen and keep it consistent.
- Custom `ViewModifier`s that compose several controls must forward `.accessibilityIdentifier` to the correct child, not to the modifier's own wrapping view — verify with Accessibility Inspector after adding a new modifier, not by inspection of the SwiftUI code alone.

## UIKit: `isAccessibilityElement` + `accessibilityIdentifier`

```swift
final class LoginViewController: UIViewController {
    private let emailField = UITextField()
    private let submitButton = UIButton(type: .system)

    override func viewDidLoad() {
        super.viewDidLoad()
        emailField.accessibilityIdentifier = "login.email.field"
        submitButton.accessibilityIdentifier = "login.submit.button"
    }
}
```

- Standard `UIKit` controls (`UITextField`, `UIButton`, `UILabel`) are `isAccessibilityElement = true` by default — setting `accessibilityIdentifier` is sufficient.
- Custom composite views (a `UIView` subclass drawing its own content) default to `isAccessibilityElement = false` and are invisible to XCUITest until explicitly opted in:
  ```swift
  final class RatingStarsView: UIView {
      override init(frame: CGRect) {
          super.init(frame: frame)
          isAccessibilityElement = true
          accessibilityIdentifier = "review.ratingStars.control"
      }
      required init?(coder: NSCoder) { fatalError() }
  }
  ```
- `UITableViewCell` / `UICollectionViewCell` subclasses: set the identifier on the cell itself in `awakeFromNib()` or `init`, and set role identifiers on labeled subviews (`titleLabel.accessibilityIdentifier = "orders.row.total"`) — mirror the SwiftUI repeated-identifier convention above.
- `UIStackView` and other pure layout containers should stay `isAccessibilityElement = false` (the default) so XCUITest reaches into their arranged subviews instead of stopping at the container.

## Accessibility Inspector Verification Workflow

Do not trust identifier assignment by code review alone — layout containers, custom modifiers, and SwiftUI accessibility merging can silently swallow an identifier.

1. Build and run the app on a simulator (`Xcode → Product → Run`, or boot via `xcrun simctl`).
2. Open **Xcode → Open Developer Tool → Accessibility Inspector**.
3. Point the inspector's target picker at the running simulator.
4. Use the crosshair tool to select each element under test; confirm the **Identifier** field in the inspector matches the taxonomy exactly (case-sensitive).
5. For a fast batch check, capture the recorded UI hierarchy from Xcode's UI Recording session (`XCUIApplication().debugDescription` printed at breakpoint, or the recorder's live element outline) and diff it against the taxonomy doc.
6. Any element missing an identifier, or resolving to an unexpected accessibility label instead, goes on the gap list below.

## Gap-List Audit Template

Output of the `identifier` recipe. One row per screen; file gaps to Native before authoring brittle text-based queries around them.

| Screen | Element | Current State | Proposed Identifier | Priority | Owner |
|--------|---------|---------------|----------------------|----------|-------|
| Login | Email field | Has identifier (`login.email.field`) | — | — | — |
| Login | "Forgot password?" link | No identifier, `UIButton` with only a title label | `login.forgotPassword.link` | High (blocks flow test) | Native |
| Checkout | Promo code field | Custom `UIView` subclass, `isAccessibilityElement = false` | `checkout.summary.promoCodeField` | High | Native |
| Orders | Row swipe-to-delete button | System-provided swipe action, no custom identifier possible | N/A — query via `.buttons["Delete"]` label fallback, documented exception | Low | — |

- **Priority**: High = blocks an in-scope test flow now; Medium = needed for planned coverage; Low = nice-to-have, defer.
- **Owner**: Native for retrofit; Voyager[ios] for label-fallback exceptions that are acceptable (system-provided UI Voyager[ios] cannot annotate).

## Common Pitfalls

- Setting `accessibilityIdentifier` on a `VStack`/`HStack`/`UIStackView` container expecting it to apply to children — it does not; set it on the leaf control.
- Localizing `accessibilityLabel` but forgetting `accessibilityIdentifier` is a separate, non-localized property — confusing the two leads teams to (wrongly) avoid identifiers "because they'll break in other languages." Identifiers are English/stable by convention; labels can localize freely.
- Reusing the same identifier for two different elements on the same screen (copy-paste from another Screen Object) — `XCUIElementQuery` then returns an ambiguous match and the first-hit wins silently.
- Assigning identifiers only to elements the current test suite happens to need, rather than the full taxonomy for the screen — the gap surfaces later as an emergency Native handoff mid-sprint instead of during a planned audit.
- SwiftUI accessibility identifier applied above a `.disabled(true)` or conditionally-hidden modifier chain — verify the identifier still resolves when the control is disabled if a test needs to assert `isEnabled == false`.

## Cross-References

- `reference/xcuitest-patterns.md` — how Screen Objects consume the identifiers this file designs.
- `reference/screenshot-strategies.md` — screenshots taken against screens with an incomplete identifier taxonomy still work, but flaky queries upstream of the capture will fail first.
