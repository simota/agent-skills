# Growth Consent Integration

Read when implementing Google measurement consent. Generic CTA/JSON-LD examples live in neither this contract nor a separate style guide; use the site's actual schema and tracking plan.

## Purpose-specific consent contract

| Signal | Controlled purpose |
|---|---|
| `analytics_storage` | Analytics-related storage |
| `ad_storage` | Advertising-related storage |
| `ad_user_data` | Sending user data for advertising |
| `ad_personalization` | Personalized advertising |

1. Select basic/advanced behavior with the site's approved privacy/CMP policy. Consent Mode is not a consent collector or proof of a lawful basis; denied storage does not automatically mean zero network traffic.
2. Set explicit defaults before measurement `config`/`event` commands. Where no valid choice exists, this skill uses denied defaults; a timeout never grants consent.
3. Map each signal to the **actual purpose-specific CMP choice**. `acceptedAll === false` means neither “analytics accepted” nor “partial consent.” Unknown/withdrawn purposes stay denied.
4. Apply updates before navigation, persist/restore choices through the approved CMP, and propagate withdrawal. Do not infer one advertising purpose from another.
5. Use the host's supported API: `gtag('consent', 'default'|'update', state)` for gtag; Tag Manager consent templates use `setDefaultConsentState`/`updateConsentState`, not a queued gtag substitute.
6. Test no-choice, accept-all, reject-all, every partial choice, withdrawal, reload and asynchronous CMP initialization. Inspect both storage and outgoing requests; report unverified behavior instead of calling the integration compliant.

Use all four fields explicitly (`'granted' | 'denied'`), with no caller-supplied default override that silently grants an unselected purpose. Keep consent initialization separate from UI analytics events; test that rejection does not itself become a tracked conversion.

## Source at execution time

https://developers.google.com/tag-platform/security/guides/consent — checked 2026-09-17. Verify current API ordering, host-specific consent APIs, basic/advanced behavior and async CMP handling. Do not retain a claimed conversion-recovery percentage or infer legal applicability from the vendor guide.
