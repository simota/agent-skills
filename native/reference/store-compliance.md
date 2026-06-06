# Store Compliance Guide

**Purpose:** Compliance checklists and implementation patterns for App Store / Google Play guidelines.
**Read when:** Preparing for store submission, implementing IAP, or addressing privacy requirements.

---

## App Store Guidelines (Apple)

### Privacy (Section 5.1)

| Requirement | Implementation |
|-------------|----------------|
| PrivacyInfo.xcprivacy | Required API reason declarations |
| Purpose strings | NSCameraUsageDescription, NSLocationWhenInUseUsageDescription, etc. |
| App Tracking Transparency | ATTrackingManager required when using IDFA |
| Privacy nutrition labels | Declare accurately in App Store Connect |
| Data minimization | Collect only the minimum data necessary |

### In-App Purchase (Section 3.1)

| Rule | Detail |
|------|--------|
| Digital goods via Apple IAP only | External payment links are forbidden (Reader App exception applies) |
| Restore purchases | Place a Restore button on the Settings screen or similar |
| Subscription terms | Disclose duration, price, and auto-renewal before purchase |
| Free trial | Disclose post-trial billing in advance |
| Price display | Show in local currency (obtained from ProductResponse) |

### StoreKit 2 Implementation Pattern

```swift
import StoreKit

@Observable
class SubscriptionManager {
    private(set) var products: [Product] = []
    private(set) var purchasedSubscriptions: [Product] = []

    func loadProducts() async {
        do {
            products = try await Product.products(for: ["com.app.monthly", "com.app.yearly"])
        } catch {
            // Handle error
        }
    }

    func purchase(_ product: Product) async throws -> Transaction? {
        let result = try await product.purchase()
        switch result {
        case .success(let verification):
            let transaction = try checkVerified(verification)
            await transaction.finish()
            await updatePurchasedSubscriptions()
            return transaction
        case .userCancelled, .pending:
            return nil
        @unknown default:
            return nil
        }
    }

    func checkVerified<T>(_ result: VerificationResult<T>) throws -> T {
        switch result {
        case .unverified:
            throw StoreError.failedVerification
        case .verified(let safe):
            return safe
        }
    }
}
```

### Common Rejection Reasons

| Reason | Prevention |
|--------|------------|
| 2.1 Performance - crashes | Test on every supported device size |
| 2.3 Accurate metadata | Screenshots match the actual UI |
| 3.1.1 IAP required | Digital content goes through Apple IAP |
| 4.0 Design - HIG violation | Use SF Symbols, support Dynamic Type |
| 5.1.1 Data collection | Describe PrivacyInfo.xcprivacy accurately |
| 5.1.2 Data use | No use beyond declared purpose |
| 5.1.2(i) third-party AI disclosure | **All three required**: name the AI provider (e.g. "OpenAI GPT-4", not "service providers"); explain the purpose (e.g. "to generate a summary of your message"); obtain explicit user consent before any personal data is sent. Triggered by sending prompts, documents, voice, or behavior data to external LLMs / transcription / moderation services |

---

## Google Play Policy

### Data Safety

| Requirement | Implementation |
|-------------|----------------|
| Data safety form | Declare accurately in Play Console |
| Encryption in transit | HTTPS required |
| Data deletion option | Provide an account deletion feature |
| Families policy | Apps for children carry additional restrictions |

### Google Play Billing

| Rule | Detail |
|------|--------|
| Digital goods via Play Billing | Digital content goes through Google Play Billing |
| Subscription transparency | Show price, duration, and auto-renewal before purchase |
| Grace period | Configure a grace period on payment failure (recommended) |
| Account hold | Handle the account-hold state |

### Billing Implementation Pattern (Kotlin)

```kotlin
class BillingManager(private val activity: Activity) {
    private val billingClient = BillingClient.newBuilder(activity)
        .setListener(purchasesUpdatedListener)
        .enablePendingPurchases()
        .build()

    fun startConnection() {
        billingClient.startConnection(object : BillingClientStateListener {
            override fun onBillingSetupFinished(billingResult: BillingResult) {
                if (billingResult.responseCode == BillingClient.BillingResponseCode.OK) {
                    queryProducts()
                }
            }
            override fun onBillingServiceDisconnected() {
                // Retry connection
            }
        })
    }

    private fun queryProducts() {
        val productList = listOf(
            QueryProductDetailsParams.Product.newBuilder()
                .setProductId("monthly_subscription")
                .setProductType(BillingClient.ProductType.SUBS)
                .build()
        )
        val params = QueryProductDetailsParams.newBuilder()
            .setProductList(productList)
            .build()

        billingClient.queryProductDetailsAsync(params) { billingResult, productDetailsList ->
            // Handle product details
        }
    }
}
```

---

## Cross-Platform Compliance Checklist

| Item | iOS | Android |
|------|-----|---------|
| Privacy declaration | PrivacyInfo.xcprivacy + Nutrition Labels | Data Safety Form |
| Permission rationale | NSUsageDescription strings | shouldShowRequestPermissionRationale |
| IAP implementation | StoreKit 2 | Google Play Billing Library |
| Age rating | App Store rating questionnaire | Content rating questionnaire |
| Accessibility | VoiceOver + Dynamic Type | TalkBack + Font scaling |
| Data deletion | Account deletion feature | Account deletion feature |
| Encryption export | ITSAppUsesNonExemptEncryption | N/A (Google handles) |
