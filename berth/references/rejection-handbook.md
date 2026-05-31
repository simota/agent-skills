# Rejection & Policy-Strike Handbook

**Purpose:** Interpret a rejection or policy strike, classify it, produce remediation, and navigate Resolution Center / appeals.
**Read when:** Running the `reject` recipe.

---

## Step 1 — Classify

| Class | Signal | Path |
|-------|--------|------|
| **Metadata-fixable** | Screenshots/description/category/age-rating issue; nothing wrong with the binary | Fix metadata in the console; resubmit (often no new binary needed). |
| **Binary-fixable** | Crash, missing capability (account deletion, login parity), permission misuse, privacy-declaration gap | Fix in the build (`Native`), update declarations, upload new build, resubmit. |
| **Guideline dispute** | You believe the reviewer misread the app or the guideline | Reply in Resolution Center with evidence; escalate only with factual grounds. |

> **Never resubmit unchanged.** Repeated identical submissions waste the review gate and can escalate scrutiny.

---

## Step 2 — Interpret the Reason

- Apple cites a **guideline section** (e.g., 2.1, 4.3, 5.1.1(v)) — map it via `app-store-connect.md`.
- Google cites a **policy** (e.g., Data safety, Background location, Families) — map it via `play-console.md`.
- Extract the *specific* objection, not the category. "5.1.1" alone is not actionable; "missing in-app account deletion" is.

---

## Step 3 — Remediate

Produce, per objection:
1. The exact requirement (cite section/policy + the actionable rule).
2. The concrete change (binary, declaration, or metadata).
3. The owner (`Native` for code, `Berth` for declarations/metadata, `Cloak` for data-map corrections).
4. Whether a new binary or only a resubmission is needed.

---

## Step 4 — Reply (Resolution Center / Play)

Reply only when the change is done **or** you have a genuine factual clarification.

**Good reply (clarification):**
> "Account deletion is available at Settings → Account → Delete Account (screenshot attached). Steps to reach it from the demo account: …"

**Good reply (dispute with grounds):**
> "The flagged screen is gated behind the `pro_user` entitlement; the demo account `review@…` now has it enabled. Please re-test — the feature is fully functional, not placeholder."

**Bad reply (avoid):** arguing the guideline is wrong without a fix or evidence; vague "please reconsider"; resubmitting with no change.

---

## Step 5 — Escalate (only with grounds)

| Store | Escalation |
|-------|-----------|
| Apple | **App Review Board** appeal for a guideline-application dispute; or request a guideline interpretation. |
| Google | **Policy appeal** via the Console policy-status / app-status flow; provide evidence of compliance or correction. |

Escalation is for genuine misapplication, not for skipping a real fix.

---

## Common Rejection → Fix Quick Map

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| "We were unable to access the gated feature" | Missing/broken demo account | Provide working credentials + steps in App Review info / App access. |
| "Privacy details / Data safety inaccurate" | Declared ≠ actual (often an SDK) | Reconcile with `Cloak` data map; declare SDK-collected data. |
| iOS auto-rejected on upload | Missing Privacy Manifest Required-Reason API | Add `PrivacyInfo.xcprivacy` entries; ensure SDK manifests present. |
| "App is a duplicate / spam" (4.3) | Template-farm or near-identical app | Differentiate substantively or consolidate. |
| "Purchase must use IAP/Play Billing" | Digital goods via external payment | Route through store billing or qualify for an entitlement. |
| Android "sensitive permission not justified" | Unused/over-broad permission | Remove, scope down, or file the declaration form. |
| "Account creation requires deletion" | No in-app deletion path | Add deletion (iOS); add deletion + web URL (Android). |

---

## Repeat-Rejection Pattern

If the same app is rejected ≥2× on related grounds, journal the pattern in `.agents/berth.md` (e.g., "this app's SDK X always triggers Data safety mismatch") so future submissions pre-empt it. Do not log routine one-off rejections.
