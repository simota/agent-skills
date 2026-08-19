# Authorization in the Retrieval Layer

Purpose: design who may see a result, not only which result ranks first. Retrieval quality and retrieval
authorization are separate properties of the same pipeline, and a design that only states the first ships
the second by accident.

**Read when:** the corpus is not uniformly readable by every requester — multi-tenant, per-team, per-role,
per-region, or any customer data. Skip only when every document in the index is visible to every user of
the search, and say so explicitly rather than leaving it unstated.

**Scope boundary.** This file covers authorization *inside the retrieval path* — index layout, filtering,
chunk and cache boundaries, revocation lag. Tenant architecture, RLS, and provisioning stay with `Schema[tenant]`.
PII classification, consent, and retention stay with `Cloak`. Regulatory control mapping stays with `Canon[regulatory]`.
Static code flaws stay with `Sentinel`. Route there for depth; the design decisions below still belong in
the retrieval spec.

---

## 1. Retrievable and disclosable are different questions

The indexer usually reads more than any requester may. That is normally correct — it is how one index
serves many audiences — and it is why "the search returned it" is never evidence "this user may see it".

Collapsing the two produces the standard failure: a support engineer asks about customer A's outage, the
indexer can read every customer's tickets, semantic similarity surfaces customer B's near-identical ticket,
and the answer masks the customer name while leaving configuration values and timestamps that identify them.
Nothing in the ranking stack was wrong. The authorization step was never in it.

**Do not compress these into one flag.** A retrieval design states each separately:

| Question | Decided by |
|---|---|
| Can the indexer read the source? | source system permission |
| Should this document be in this index at all? | index partition policy |
| May this requester retrieve it? | end-user authorization at query time |
| May this content be shown, quoted, or cited? | disclosure policy on the answer path |
| May an agent act on it? | tool/action authorization, separate from all the above |

Reading permission never implies disclosure permission, and disclosure never implies action permission.

---

## 2. Where the filter goes — three placements, layered

Authorization can be enforced at index time, at search time, or after retrieval. These are not
alternatives to choose between; each catches what the others cannot, and a production design usually uses
all three with different jobs.

| Placement | What it does | Fails at | Use it for |
|---|---|---|---|
| **Index-time** | separate index / partition / collection per boundary; excluded content is never in the index queried | fine-grained per-user ACLs — the partition count explodes | strong, stable boundaries: tenant, region/residency, public-vs-internal, highly restricted classes |
| **Search-time** | mandatory filter canon built from the requester's identity, applied in the engine query | filter omission on any code path; engine filter limitations; approximate-search pre/post-filter semantics; timing side channels | group- and attribute-based access that changes often |
| **Post-retrieval** | policy engine authorizes each candidate after the engine returns it | unauthorized documents still entered candidate generation, scoring, reranking, **and logs** before being dropped | final defense and citation-time recheck — never as the only layer |

**Recommended composition:** partition the strong boundaries at index time, constrain candidates at search
time, and confirm once more after retrieval. State which layer enforces which boundary in the spec; a
boundary that no layer names is unenforced.

**Choose the partition strategy by blast radius, not by performance.**

| Strategy | Strength | Cost | Choose when |
|---|---|---|---|
| Physical index separation | a filter bug cannot cross the boundary; separate backups, keys, and residency | index count, ops, cross-boundary queries, capacity planning | regulated boundaries, strong tenant isolation |
| Namespace / logical partition | one cluster, simpler ops | an implementation bug **can** cross it — this is not physical isolation | the platform can prove enforcement |
| Shared index + mandatory filter | flexible, efficient, cross-cutting queries | a single omitted filter is a full breach | filter application is centralized and tested |
| Precomputed entitlement view | fastest queries | permission changes are slow and complex to apply | the entitlement set is stable |

The deciding inputs are the **maximum exposure if misconfigured**, residency, encryption-key separation,
deletability, and audit requirements — not document count or p95.

---

## 3. Mandatory filters are built from session state, never from the query

The filter that enforces authorization must not be reachable by anything the user or the model can write.

```
final_filter = AND(mandatory, sanitize(requested))
```

- `mandatory` is derived only from authenticated session context — subject, groups, active tenant, purpose.
- `requested` is the user's or the model's filter, sanitized and intersected. It can narrow, never widen.
- A query rewriter, an LLM-generated filter, or a "search with these constraints" tool argument is always
  `requested`. It cannot remove or relax `mandatory`.

**Authorize before reranking, not after.** Reranking is expensive and its output is what gets shown; an
unauthorized candidate that reaches the reranker has already cost money and entered the trace. Order the
pipeline: retrieve → authorize → rerank → assemble.

**Rank fusion must not rescue a prohibited candidate.** RRF and weighted fusion operate over the
*authorized* candidate set. If the authorized pool is too small after filtering, widen the search or run
another query — never backfill from the rejected set to fill `top_k`.

**Never fall open under pressure.** If the policy service times out, the request fails closed for protected
content. "The result set is empty" and "search is slow" are not availability incidents that justify
dropping the filter — and the automatic-relaxation path must not exist to be triggered.

---

## 4. ACL resolution is three-valued

`Resolved` / `Denied` / `Unknown`. Unknown arises constantly in practice: the connector failed, a group is
unresolvable, the source's permission model has no mapping, the policy version is missing.

**Unknown is not Public and not Internal.** Quarantine the document out of the production index, or deny it
at query time. A document whose ACL cannot be determined is not eligible to answer an authoritative
question — at most it is discoverable to those who already have broad access.

Never trade authorization certainty for availability. That trade is invisible when it succeeds and
unrecoverable when it fails.

**Deriving ACLs into the index** — four representations, each with a different lag/size trade-off:

| Representation | Mechanism | Trade-off |
|---|---|---|
| Policy reference | chunk carries `access_policy_ref`; policy engine consulted at query time | freshest; adds a call to the query path |
| Attribute snapshot | object attributes needed for evaluation are stored in the index | fast; attributes go stale |
| Principal token | the requester carries the set of resources/groups they can reach, used as a filter | scales with the user, not the corpus; token size grows |
| Precomputed entitlement | materialized allow lists | fastest reads; permission changes are expensive to propagate |

Flattening nested groups into a literal allowed-user list is the failure mode all four exist to avoid: it
grows without bound and its update lag becomes the revocation lag. Whichever is chosen, record
`acl_version` and `evaluated_at` on every authorization decision — without them a past decision cannot be
explained or reproduced.

---

## 5. Chunk, parent, and summary inherit the strictest policy

A derived unit may never be more permissive than what it came from.

- **A chunk carries its source document's ACL.** Not a default, not the collection's.
- **Do not union allow sets when merging fragments.** Union widens. Compose by intersection, or keep the
  fragments separate. A merged chunk that anyone in either source's audience can read is a new disclosure.
- **Deny conditions survive composition.** A deny that applies to one fragment applies to anything
  containing it.
- **Expanding to parent context re-opens the question.** Attaching a parent section or the whole document
  means authorizing the parent, not the chunk that matched.
- **A summary inherits the strictest policy in its source set.** One restricted source makes the whole
  summary restricted.
- **Citation resolution is authorized too**, for the same principal. A citation link that resolves without
  a permission check is a second retrieval path with no filter on it.
- **Do not chunk across an internal ACL boundary.** If sections of one document have different
  permissions, the boundary between them is a chunk boundary.
- **Deduplication must not merge across authorization.** Two fragments with identical text but different
  ACLs, tenants, or authority are not duplicates. Content equality is not authorization equality, and a
  hash-based dedup that keeps one copy silently republishes the stricter one under the looser policy.

**Embeddings are not anonymized data.** Inversion and membership-inference risk are real and model
dependent; treat the vector store, its payloads, and index metadata as carrying the sensitivity of their
source. Apply the same access control, tenant separation, and deletion obligations you apply to the text.

---

## 6. Cache keys carry the authorization context

Any cache on the retrieval path — candidate lists, parent fragments, reranker outputs, citation previews,
assembled context, final answers — is a bypass unless its key includes who is asking under what policy.

```
cache_key = hash(
    normalized_query,
    subject_or_entitlement_set,   # not the bare user id — groups change
    active_tenant,
    purpose,
    policy_version,
    corpus_generation,
    acl_generation,
    retrieval_plan_id             # a config change must not read a stale entry
)
```

- **A user id alone is insufficient** — it does not change when the user's groups or purpose change.
- **Cache TTL must not exceed the permission-propagation SLO.** A 1-hour cache under a 5-minute revocation
  target means a 55-minute hole.
- **Re-authorize on cache hit.** The cached payload is candidate content, not an authorization decision.
- **Negative results expire too.** A cached deny outlives a legitimate grant.
- **Shared semantic caches must not store sensitive queries** — the query text is itself disclosure.
- **Keep a reverse index from source to cache entries.** A key that is only a forward hash cannot be
  invalidated when a source document is deleted or reclassified. Store `source_refs` on the entry, or a
  reverse map; without one, deletion and revocation cannot reach the cache at all.

---

## 7. Revocation is the SLI, and it is not done at the index

Permission *removal* is the direction that matters. Grants that arrive late are an inconvenience; removals
that arrive late are the breach.

```
permission_propagation_delay = t_enforced_everywhere - t_source_acl_change
```

Define "everywhere" explicitly, because a shorter definition measures a weaker property. The stages:

| Stage | Event |
|---|---|
| T0 | subject loses the entitlement in the directory |
| T1 | source system commits the ACL change |
| T2 | connector captures the change event |
| T3 | index entries and caches are invalidated |
| T4 | retrieval returns deny |
| T5 | **citation resolution returns deny** |
| T6 | **delegated tool/agent actions are refused** |

An SLO that stops at T4 leaves two live paths. Measure to T6.

**Prioritize shrink over grow.** Route revocation events to a high-priority path, and enforce at the policy
engine immediately rather than waiting for reindexing. On SLO breach, fail the affected collection closed.

**Inject the realistic failures into the test**: dropped events, out-of-order events, a warm cache, and a
backup restore that reintroduces old permissions.

---

## 8. Test the disclosure surface, not just the body text

An ACL test that only asserts "the forbidden text is absent from the answer" passes systems that leak.
Existence is disclosure.

Assert across **title, snippet, result count, facet counts, suggestions, citations, error messages,
response timing, cache behavior, and tool output**.

**Positive** — authorized retrieval works: the permitted user gets the current document; a newly added
group member gains access within the SLO; tenant-internal sharing works between the intended users.

**Negative** — the boundary holds: an identically-titled document in another tenant is unreachable;
content only the indexer can read is unreachable; a removed group member cannot reach it through a warm
cache; parent expansion does not pull in an unauthorized parent; opening a citation URL directly still
enforces the source ACL; result counts and facets do not reveal the existence of filtered documents.

**Race** — the boundary holds while it moves: the ACL changes mid-query; deletion races a cache hit; the
policy service switches versions and old and new decisions coexist; a group update lands during a
long-running agent session that already holds retrieved context.

**Cross-tenant fixtures specifically:** place identical titles and identical bodies in two tenants; issue
the byte-identical query from each; warm the cache from one and query from the other; include colliding
group ids across tenants; cover batch and async retrieval paths; and confirm error text and result counts
do not distinguish "does not exist" from "not permitted to you".

---

## 9. Failure modes, detection, response

| Failure | Detection | Response |
|---|---|---|
| ACL missing at ingestion | ingestion validation | quarantine; do not index |
| Policy service unavailable | health check / timeout | fail closed for protected content |
| Group membership stale | directory version lag | refresh; shorten cache TTL |
| Mandatory filter omitted | query-trace invariant — every protected query carries the filter | block the request and alert |
| Cross-tenant candidate observed | tenant assertion on every candidate | drop; incident if it reached a response |
| Unauthorized citation | final citation authorization check | remove the answer or abstain |
| ACL changed after context was built | compare policy version at assembly vs at answer | rebuild the context |

Log the authorization decision, not the content: subject, policy version, `acl_version`, reason codes,
decision, and **candidate counts before and after the policy filter**. That pair (e.g. `23 → 7`) is the
cheapest available signal that the filter is doing anything at all; a run where the counts are always equal
is a filter that never fires.

---

## 10. What the retrieval spec must state

Add to the deliverable in `seek`'s Output Requirements whenever the corpus is not uniformly public:

1. The boundaries that exist (tenant, role, region, classification) and which placement enforces each.
2. The partition strategy and the blast radius if its filter is misconfigured.
3. The ACL representation, and where `acl_version` / `evaluated_at` are recorded.
4. The mandatory-filter construction, and proof the model cannot influence it.
5. Chunk, parent, and summary inheritance rules.
6. Every cache on the path, its key composition, its TTL, and its invalidation route.
7. The permission-propagation SLO, stated to T6, with the revocation-priority rule.
8. The disclosure-surface test matrix (positive / negative / race), including cross-tenant fixtures.
9. The `Unknown`-ACL policy.

**Handoffs:** tenant architecture and RLS → `Schema[tenant]`. PII classification, consent, retention, deletion
obligations → `Cloak`. Control mapping and audit evidence → `Canon[regulatory]`. Adversarial validation of the
boundary → `Breach` / `Probe`. Permission-propagation SLI instrumentation → `Beacon`.
