# Cross-Agent Handoff Templates

## Trawl → Vector (Small-Scale Execution)

When Trawl determines the crawl scope is Nano tier (< 1K URLs/day, 1-5 domains), hand off to Vector for direct execution.

```yaml
SPIDER_TO_NAVIGATOR_HANDOFF:
  Scope: "Nano tier — single-session scraping sufficient"
  Target:
    urls: ["<target URLs>"]
    domain_count: <number>
    estimated_pages: <number>
  Extraction:
    selectors: "<CSS/XPath selectors or structured data type>"
    output_format: "<JSON/CSV>"
    schema: "<expected output fields>"
  Compliance:
    robots_txt_status: "checked — allowed | restricted | unknown (RFC 9309)"
    rate_limit: "<recommended delay between requests>"
    opt_out_signals: "<any detected: robots / X-Robots-Tag noai / TDMRep / ai.txt / C2PA / Do-Not-Train registry>"
    edge_provider: "<Cloudflare (note default AI block since 2025-07) | Akamai | Fastly | origin>"
    pay_per_crawl_required: "<true | false; if true, route to compliance-architecture#pay-per-crawl>"
  Notes: "<any special handling instructions>"
```

## Trawl → Stream (Data Ingestion Spec)

When Trawl has designed the crawl architecture, hand off the output specification to Stream for downstream ETL/ELT design.

```yaml
SPIDER_TO_STREAM_HANDOFF:
  Data_Contract:
    output_format: "WARC | JSON-Lines | Parquet"
    schema:
      fields: ["url", "content", "timestamp", "status_code", "headers", "content_hash"]
      types: ["string", "string/binary", "int64", "int", "map", "string"]
    volume:
      urls_per_day: <estimated>
      avg_document_size: "<KB/MB>"
      daily_data_volume: "<GB/TB>"
    velocity:
      delivery_mode: "batch (hourly/daily) | streaming (Kafka topic)"
      freshness_slo: "<max age of data>"
    quality:
      dedup_guarantee: "SimHash hamming ≤ 3 filtered | exact URL dedup"
      completeness: "<expected success rate %>"
  Delivery:
    location: "<S3 path / Kafka topic / API endpoint>"
    partitioning: "<by date / domain / content_type>"
    compression: "<gzip / snappy / zstd>"
  Notes: "<any special handling for downstream>"
```

## Trawl → Builder (Implementation Spec)

When the architecture design is approved, hand off to Builder for implementation.

```yaml
SPIDER_TO_BUILDER_HANDOFF:
  Architecture:
    scale_tier: "Small | Medium | Large | Web-scale"
    stack: "<recommended technology stack>"
    topology: "<architecture pattern reference>"
  Components:
    - name: "<component name>"
      responsibility: "<what it does>"
      technology: "<specific library/framework>"
      interfaces: "<input/output contracts>"
  Configuration:
    frontier_type: "<Bloom/Cuckoo/Redis/RocksDB>"
    scheduler: "<token bucket parameters>"
    output_format: "<WARC/JSON-Lines/Parquet>"
    compliance: "<robots.txt parser, rate limits>"
  Reference_Files:
    - "trawl/reference/distributed-architecture.md — topology patterns"
    - "trawl/reference/frontier-design.md — dedup implementation"
    - "trawl/reference/compliance-architecture.md — legal subsystem"
    - "trawl/reference/anti-detection-architecture.md — detection avoidance"
    - "trawl/reference/link-graph.md — link graph design"
    - "trawl/reference/observability.md — monitoring and SLO"
  Constraints:
    - "<performance requirements>"
    - "<compliance requirements>"
    - "<infrastructure constraints>"
```

## Trawl → Scaffold (Infrastructure Requirements)

Hand off infrastructure provisioning requirements to Scaffold.

```yaml
SPIDER_TO_SCAFFOLD_HANDOFF:
  Compute:
    coordinator: "<instance type, count>"
    workers: "<instance type, count, autoscaling policy>"
    total_vcpu: <estimated>
    total_ram_gb: <estimated>
  Storage:
    frontier: "<Redis/RocksDB cluster spec>"
    output: "<S3/GCS bucket, estimated size>"
    logs: "<log storage requirements>"
  Network:
    egress_per_day: "<GB/TB>"
    proxy_infrastructure: "<if applicable>"
  Queue:
    type: "Redis | Kafka"
    spec: "<cluster size, partition count, retention>"
  Monitoring:
    metrics: "<Prometheus/CloudWatch>"
    dashboards: "<Grafana boards needed>"
    alerts: "<SLO-based alerting>"
```

## Trawl → Seek (Index Ingestion Requirements)

Hand off crawled content characteristics to Seek for search index design.

```yaml
SPIDER_TO_SEEK_HANDOFF:
  Corpus:
    estimated_documents: <count>
    avg_document_size: "<KB>"
    content_types: ["HTML text", "PDF text", "JSON-LD structured"]
    languages: ["<primary>", "<secondary>"]
    update_frequency: "<daily / weekly / real-time>"
  Schema:
    fields: ["<field definitions for indexing>"]
    facets: ["<filterable dimensions>"]
  Delivery:
    format: "<JSON-Lines / Parquet>"
    location: "<S3 path / Kafka topic>"
    freshness_slo: "<max staleness>"
```

## Trawl → Beacon (Crawl SLO/SLI Definitions)

Hand off observability requirements to Beacon for monitoring setup.

```yaml
SPIDER_TO_BEACON_HANDOFF:
  SLIs:
    - name: "Crawl throughput"
      metric: "urls_fetched_per_second"
      target: "<target rate>"
    - name: "Fetch success rate"
      metric: "successful_fetches / total_fetches"
      target: "≥ 99%"
    - name: "Frontier depth"
      metric: "pending_urls_count"
      alert: "< 100 (frontier exhaustion) or > 10M (backlog)"
    - name: "Content freshness"
      metric: "max_age_of_crawled_content"
      target: "< <freshness SLO>"
    - name: "Error rate by category"
      metric: "4xx_rate, 5xx_rate, network_error_rate"
      target: "4xx < 5%, 5xx < 1%, network < 0.1%"
  SLOs:
    availability: "<99.5% / 99.0%>"
    throughput: "<URLs/day target>"
    freshness: "<max content age>"
  Dashboards:
    - "Crawl rate (URLs/sec by domain)"
    - "Frontier depth and breadth"
    - "Error rate by category (4xx/5xx/network)"
    - "Cost per URL"
    - "Compliance audit (robots.txt checks, opt-out signals)"
```

## Trawl → Cloak (PII Surface Area Report)

Hand off data governance information when crawled content may contain PII.

```yaml
SPIDER_TO_CLOAK_HANDOFF:
  Data_Categories:
    - category: "<data type>"
      source: "<where in crawled content>"
      pii_risk: "High | Medium | Low"
      treatment: "<how handled in extraction pipeline>"
  Domains:
    sensitive_domains: ["<domains with PII content>"]
    pii_types: ["email", "phone", "address", "name", "photo"]
  Governance:
    retention_policy: "<proposed retention>"
    access_controls: "<who can access crawled PII>"
    anonymization: "<techniques applied>"
  Compliance:
    gdpr_basis: "<legal basis for processing>"
    dpia_required: "Yes | No"
```

## Trawl → Canvas (Architecture Diagrams)

Hand off diagram specifications to Canvas for visualization.

```yaml
SPIDER_TO_CANVAS_HANDOFF:
  Diagram_Type: "architecture | data_flow | topology | sequence"
  Title: "<diagram title>"
  Components:
    - name: "<component name>"
      type: "service | queue | storage | external"
      description: "<brief role>"
  Connections:
    - from: "<source component>"
      to: "<target component>"
      label: "<connection description>"
      style: "solid | dashed"
  Annotations:
    - "<key design decisions to highlight>"
  Format: "Mermaid | ASCII | draw.io"
```

---

## INPUT Handoff Templates (What Trawl Receives)

### Oracle → Trawl (RAG Corpus Requirements)

```yaml
ORACLE_TO_SPIDER_HANDOFF:
  Corpus_Scope:
    target_domains: ["<domain list>"]
    content_types: ["HTML", "PDF", "JSON-LD"]
    languages: ["<primary>", "<secondary>"]
    estimated_corpus_size: "<number of documents>"
  Quality_Requirements:
    freshness_slo: "<max age of content>"
    completeness: "<coverage requirements>"
    dedup_level: "exact | near-duplicate | none"
  Output_Requirements:
    format: "JSON-Lines | Parquet"
    fields: ["url", "content", "metadata", "embedding_text"]
    delivery: "batch | streaming"
```

### Seek → Trawl (Index Ingestion Requirements)

```yaml
SEEK_TO_SPIDER_HANDOFF:
  Index_Requirements:
    field_definitions: ["<fields to index>"]
    facet_dimensions: ["<filterable fields>"]
    update_frequency: "real-time | hourly | daily"
    freshness_slo: "<max staleness>"
  Corpus_Characteristics:
    estimated_documents: <count>
    avg_document_size: "<KB>"
    languages: ["<language list>"]
  Delivery:
    format: "JSON-Lines | Parquet"
    location: "<S3 path / Kafka topic>"
```

### Oath → Trawl (Regulatory Scope)

```yaml
COMPLY_TO_SPIDER_HANDOFF:
  Jurisdictions:
    applicable: ["EU", "US", "JP"]
    primary: "<primary jurisdiction>"
  Data_Categories:
    permitted: ["<allowed data types>"]
    restricted: ["<data types requiring special handling>"]
    prohibited: ["<data types not to collect>"]
  Retention:
    max_retention_days: <number>
    deletion_requirements: "<deletion policy>"
  Compliance_Controls:
    audit_trail_required: true | false
    dpia_required: true | false
    consent_basis: "<legal basis>"
```

### Cloak → Trawl (PII Classification)

```yaml
CLOAK_TO_SPIDER_HANDOFF:
  PII_Categories:
    - category: "<data type (email, phone, name, etc.)>"
      sensitivity: "High | Medium | Low"
      treatment: "mask | hash | exclude | encrypt"
      detection_method: "<regex / NER / field-based>"
  Governance_Requirements:
    anonymization_required: true | false
    pseudonymization_method: "<technique>"
    access_controls: "<role-based restrictions>"
  Data_Flow_Constraints:
    storage_encryption: "at-rest | in-transit | both"
    cross_border_transfer: "allowed | restricted | prohibited"
```
