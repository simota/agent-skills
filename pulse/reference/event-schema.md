# Event Schema Design

## Naming Conventions

```
[object]_[action]

Examples:
- user_signed_up
- item_added_to_cart
- checkout_completed
- article_viewed
- subscription_started
```

## Event Structure Template

```typescript
interface AnalyticsEvent {
  // Required
  event_name: string;           // e.g., "checkout_completed"
  timestamp: string;            // ISO 8601 format
  user_id?: string;             // Authenticated user ID
  anonymous_id: string;         // Device/session identifier

  // Context (auto-captured)
  context: {
    page_url: string;
    page_title: string;
    referrer: string;
    user_agent: string;
    locale: string;
    timezone: string;
  };

  // Event-specific properties
  properties: Record<string, unknown>;
}
```

## Common Event Examples

```typescript
// User Signup
{
  event_name: "user_signed_up",
  properties: {
    signup_method: "email" | "google" | "apple",
    referral_source: string,
    plan_type: "free" | "pro" | "enterprise"
  }
}

// Purchase Completed
{
  event_name: "purchase_completed",
  properties: {
    order_id: string,
    total_amount: number,
    currency: "JPY" | "USD",
    item_count: number,
    payment_method: string,
    coupon_code?: string
  }
}

// Feature Used
{
  event_name: "feature_used",
  properties: {
    feature_name: string,
    feature_version: string,
    duration_seconds?: number,
    success: boolean
  }
}

// Content Viewed
{
  event_name: "content_viewed",
  properties: {
    content_id: string,
    content_type: "article" | "video" | "product",
    content_title: string,
    view_duration_seconds: number,
    scroll_depth_percent: number
  }
}
```

## Tracking Plan as Code (2026)

For multi-platform stacks, do not maintain the tracking plan in a wiki — keep it versioned and machine-readable:

| Tool | Role | 2025-2026 status |
|------|------|------------------|
| **Avo** | Tracking-plan repo with type generation, branch workflow, publishes to GA4/Amplitude/Mixpanel/Segment | Active; "Publish to Amplitude Data" integration ([Avo docs](https://www.avo.app/docs/publishing/publishing/amplitude-data)) |
| **Amplitude Data** | Amplitude's own tracking-plan product — formerly **Iteratively**, acquired 2021; Avo publishes into it | Active inside Amplitude |
| **RudderStack — Tracking Plan as Code** | IaC-driven (Terraform-style) governance; manage tracking plans + data catalog declaratively | Launched 2025 ([RudderStack IaC governance](https://www.prnewswire.com/news-releases/rudderstack-accelerates-ai-native-growth-launches-iac-driven-governance-for-trusted-customer-context-302676493.html)) |
| **dbt Semantic Layer** | Defines **metrics** (not events) once, queryable from Tableau, Power BI, Google Sheets, Trino | GA **Oct 2024**; Power BI preview 2025 ([dbt SL docs](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl)) |
| **Cube** | Open-source warehouse-native semantic layer; alternative to dbt SL | Active |
| **Snowplow Iglu** | JSON-Schema registry for self-describing events (license is now **SLULA**, not Apache 2.0 since 2024-01-08) | OSS now restricted; consider **OpenSnowcat** fork for Apache 2.0 ([Snowplow license change](https://snowplow.io/snowplow-oss-license-change)) |

Rule of thumb: the **event** layer (what users do) belongs in a tracking-plan tool (Avo / Amplitude Data / RudderStack). The **metric** layer (what the business decides on) belongs in a semantic layer (dbt SL / Cube). Do not redefine `weekly_active_users` in five BI tools.
