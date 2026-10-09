# Autocomplete / Suggest Design Reference

Purpose: Design a search-as-you-type / suggestion subsystem that returns ranked completions within a sub-50ms P99 latency budget. The suggest index is a separate low-latency subsystem — not a shortcut on top of the main retrieval index — because its analyzer, query shape, and serving tier differ.

## Scope Boundary

- **Seek `suggest`**: autocomplete / search-as-you-type — prefix matching, typo tolerance, suggestion ranking, sub-50ms latency subsystem.
- **Seek `fulltext` (separate)**: main full-text retrieval — full query, BM25, analyzer pipeline tuned for recall + precision, 100-500ms budget.
- **Seek `rerank` (separate)**: second-stage re-ranking for main retrieval; typically too slow for autocomplete.

If the user is still typing and expects live results → `suggest`. If the user has pressed Enter → `fulltext`. They usually share a term dictionary but almost never share an index.

## Index Strategy

| Strategy | Engine support | Best for | Trade-off |
|----------|---------------|----------|-----------|
| Edge n-gram analyzer | ES / OpenSearch | Generic prefix search, fielded | Larger index (~3-5x); supports filters |
| Completion suggester (FST) | ES / OpenSearch | Single-field suggestions, weighted | No filter support pre-7.x, limited typos |
| Search-as-you-type field | ES 7+ | Hybrid prefix + infix | Middle-ground, simpler than custom n-gram |
| Trie / FST in memory | Redis / custom | Extreme low-latency, <5ms | No filtering, hard to update incrementally |
| Typesense / Meilisearch | Built-in typo-tolerant prefix | Out-of-the-box suggest + main search | Less control over ranking |
| Algolia | Managed | Zero-ops, instant search UI | Vendor cost at scale |

Default: **edge-n-gram + completion suggester combo** on Elasticsearch — suggester for fast top-N, edge-n-gram for fielded fallback / faceted suggest.

## Edge N-gram Example

```json
{
  "settings": {
    "analysis": {
      "analyzer": {
        "suggest_index_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding", "edge_ngram_filter"]
        },
        "suggest_search_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      },
      "filter": {
        "edge_ngram_filter": { "type": "edge_ngram", "min_gram": 1, "max_gram": 20 }
      }
    }
  },
  "mappings": {
    "properties": {
      "title_suggest": {
        "type": "text",
        "analyzer": "suggest_index_analyzer",
        "search_analyzer": "suggest_search_analyzer"
      }
    }
  }
}
```

Critical: use the n-gram analyzer **only at index time**. Applying it at search time explodes the query into every prefix and tanks relevance.

## Typo Tolerance

| Technique | How | When to use |
|-----------|-----|-------------|
| Levenshtein automaton | ES fuzzy query (`fuzziness: AUTO`) | Built-in; edit distance 1-2 |
| BK-tree | Custom in-memory dictionary | Standalone suggestion service |
| symspell | Precomputed deletion dictionary, O(1) lookup | High-QPS, fixed dictionary, single language |
| SymSpellPy / compact tries | Same, embedded | Edge / mobile suggest |

Rule: enable fuzziness only after 3+ characters typed — fuzzy on 1-2 chars returns noise. Cap edit distance at 2 (edit distance 3+ over a short prefix matches almost any term).

## Ranking Signals

Suggestions need their own scoring separate from main BM25. Common signals:

- **Popularity**: historical query frequency (log-scaled).
- **Recency**: trending boost for last 24h / 7d.
- **User personalization**: past queries, clicked categories, location.
- **Context**: current category / facet, session prior queries.
- **Business weight**: merchandised / promoted terms.

Store as a `weight` field on the completion suggester or as a rescore function. Avoid hard rules ("always show X first") — they compound into stale suggestions.

## Latency Budget

| Stage | P99 budget |
|-------|-----------|
| Network (keystroke debounce → server) | 10-20ms |
| Index lookup (prefix + fuzzy) | 5-20ms |
| Re-rank / personalize | 5-15ms |
| Network (server → render) | 5-15ms |
| **Total keystroke-to-render** | **<50ms** |

Degradation order when over budget:
1. Disable personalization.
2. Drop fuzziness to edit distance 1.
3. Reduce top-K (10 → 5).
4. Bypass rescore and serve raw suggester output.

Do **not** trigger a request on every keystroke. Debounce 80-150ms client-side; cancel in-flight requests on new keystrokes.

## Anti-Patterns

- Using the main `fulltext` index for suggestions — BM25 and analyzer tuned for recall, not for fast prefix.
- Applying edge-n-gram as the search-time analyzer (query explodes into every prefix).
- Fuzzy matching on 1-character prefixes (returns junk).
- No debounce — 10 keystrokes fire 10 backend requests.
- No cache layer — popular prefixes should hit a CDN / Redis before the search engine.
- Mixing "did you mean" spell correction into the suggest pipeline — keep them separate; spell correction runs post-enter, not mid-keystroke.
- Shipping suggestions without click logging — you cannot tune ranking without suggestion-acceptance data.

## Paired Deliverables

Every `suggest` design ships:

1. Suggest-index mapping (separate from main index).
2. Query template: prefix clause + fuzzy clause + filters.
3. Ranking feature list and weights.
4. Latency budget table with degradation order.
5. Client-side debounce + cancellation strategy.
6. Logging schema for suggestion acceptance (prefix, shown, selected, position).

## Handoff

- To `Builder`: client-side debounce / cancellation, keyboard navigation (arrow / enter / escape), ARIA listbox roles.
- To `Stream`: suggestion-acceptance log ingestion.
- To `eval` (Seek): suggestion-specific metrics — suggestion acceptance rate, Mean Reciprocal Rank of accepted suggestion, prefix-to-selection latency.
- To `Palette`: interaction polish — keyboard handling, result-group visual hierarchy, empty state.
- Main retrieval after Enter stays in `fulltext` — cross-link, never merge.
