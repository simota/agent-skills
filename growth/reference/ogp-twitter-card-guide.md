# OGP / Social Card Contract

Read when implementing or verifying page-sharing metadata. Keep the installed framework's metadata API; do not copy another framework's component or install a second head manager.

## Required output

- Emit the canonical page URL, object type, title, image and a useful description in the delivered HTML. Resolve image URLs to public absolute HTTPS URLs; do not expose signed/private URLs or user data in metadata.
- Use the Open Graph property names exactly. Keep each image's structured properties immediately after that image; multiple image declarations are ordered preferences.
- Provide image alt text and accurate intrinsic dimensions. Choose artwork/crop for the actual target card, not a supposedly universal platform size.
- For X, select the intended card type and check its current property/asset requirements. Do not conflate a 16:9 image with a 1.91:1 image or assume every consumer has the same size/cache limit.

One format example is sufficient (replace placeholders with escaped page data):

```html
<meta property="og:type" content="website" />
<meta property="og:url" content="https://example.com/page" />
<meta property="og:title" content="Page title" />
<meta property="og:description" content="Page-specific description" />
<meta property="og:image" content="https://example.com/card.png" />
<meta property="og:image:alt" content="Description of the card image" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Page title" />
<meta name="twitter:description" content="Page-specific description" />
<meta name="twitter:image" content="https://example.com/card.png" />
<meta name="twitter:image:alt" content="Description of the card image" />
```

## Verification

Fetch the deployed response as the intended crawler, check canonical/redirect/robots behavior, and fetch the image without a user session. Confirm non-HTML image content, type/dimensions, safe crop and readable text. Inspect the final rendered metadata for duplicates or conflicting layout defaults. For dynamic image endpoints, validate inputs, bound work/output and test Unicode/long titles; a generated URL alone is not proof that the image exists.

Use the target platform's currently available inspector/preview and record the page URL, image URL, retrieval time and preview result. Distinguish stale consumer caches from wrong origin metadata. Do not publish a social post merely to test a card without authorization; report preview verification as unavailable when no permitted inspector exists.

## Canonical sources

- Open Graph fields, types, image grouping and array precedence: https://ogp.me/
- X documentation entry point: https://docs.x.com/overview — locate current Cards guidance and the available preview tool. The former Cards URL redirected here when checked on 2026-09-17; do not treat that redirect as verification of card limits.
- Framework-specific serialization: the official documentation for the **installed version**; inspect the generated HTML rather than maintaining copied Next.js/Helmet tutorials here.

Retrieve platform-specific asset limits and cache-refresh procedures when used; do not retain dated vendor dimension tables as runtime truth.
