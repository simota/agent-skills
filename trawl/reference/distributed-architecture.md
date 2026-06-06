# Distributed Crawl Architecture Patterns

## Topology Overview

```
                    ┌─────────────┐
                    │ Coordinator │
                    │  (Scheduler │
                    │  + Frontier)│
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌───▼─────┐ ┌───▼─────┐
        │  Worker 1  │ │ Worker 2│ │ Worker N│
        │ (Domain A) │ │(Domain B│ │(Domain N│
        └─────┬──────┘ └───┬─────┘ └───┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │  Output Sink│
                    │ (S3/GCS/HDFS│
                    └─────────────┘
```

## Architecture Patterns by Scale

### Small Tier: Single-Host Multi-Process

**Stack:** Scrapy + Redis + local storage

```
Components:
- Scrapy scheduler with Redis-backed queue
- Single Redis instance for frontier + seen-set
- Local filesystem or S3 for output
- Supervisor/systemd for process management

Capacity: 1K-50K URLs/day, 5-100 domains
Fault tolerance: Process restart via supervisor
Checkpoint: Redis RDB snapshots every 5 minutes
```

**When to use:** Proof of concept, domain-specific crawls, budget-constrained projects.

### Medium Tier: Coordinator + Worker Fleet

**Stack:** Scrapy-Redis / Crawlee cluster

```
Components:
- Coordinator: URL assignment, frontier management, schedule orchestration
- Workers (2-10): Scrapy/Crawlee instances with domain affinity
- Redis cluster: Frontier + seen-set + domain queues
- S3/GCS: Crawled content output
- Prometheus + Grafana: Monitoring

Capacity: 50K-1M URLs/day, 100-5K domains
Fault tolerance: Heartbeat + requeue on worker failure
Checkpoint: Redis AOF + periodic RDB
Domain assignment: Consistent hashing ring
```

**Design decisions:**
- Domain affinity vs round-robin: Affinity reduces IP blocks, round-robin balances load
- Worker scaling: Horizontal autoscaling based on frontier depth
- Queue overflow: Backpressure via frontier depth threshold (pause seed injection at 10x capacity)

### Large Tier: Kafka-Backed Distributed Crawler

**Stack:** Custom Kafka-backed + RocksDB + object storage

```
Components:
- Kafka topics: URL frontier (partitioned by domain hash), fetch results, extraction output
- Worker fleet (10-100): Stateless fetchers consuming from Kafka
- RocksDB: Per-worker URL seen-set (local, fast, disk-backed)
- Coordinator: Global dedup service, domain budget enforcement
- Object storage: WARC/Parquet output
- Kubernetes: Orchestration + autoscaling

Capacity: 1M-50M URLs/day, 5K-100K domains
Fault tolerance: Kafka consumer group rebalancing, idempotent fetches
Checkpoint: Kafka offsets + RocksDB WAL
Domain assignment: Kafka partition key = hash(domain)
```

**Design decisions:**
- Kafka partition count: Start with 2x expected worker count
- Consumer group: One group for fetching, separate group for extraction
- Backpressure: Consumer lag monitoring, pause production at threshold
- Dedup: Two-tier — local RocksDB (fast, per-worker) + global Bloom filter service (eventual consistency)

### Web-Scale Tier: Fully Distributed

**Stack:** Nutch 1.20+ / Apache StormCrawler 3.x / Common Crawl-style custom (Spark-on-Kubernetes) + S3/HDFS + sharded frontier.

> Note (2026): Nutch 2.x has been EOL since 2020; the active line is Nutch 1.20+ with Hadoop 3 / Spark integration. For greenfield web-scale crawlers, Common Crawl's own pipeline (Spark + WARC + S3) and StormCrawler are more common than Nutch.

```
Components:
- HDFS/S3: URL database (CrawlDB), content store, link database
- MapReduce/Spark: Crawl cycle jobs (generate → fetch → parse → update)
- HBase/Cassandra: URL store with crawl metadata
- ZooKeeper: Coordination, leader election
- Custom frontier: Sharded by domain, replicated for fault tolerance

Capacity: 50M+ URLs/day, 100K+ domains
Fault tolerance: HDFS replication, job retry, checkpoint per MR stage
Domain assignment: Range-based sharding with rebalancing
```

## Worker Fault Tolerance

| Mechanism | Implementation | Recovery Time |
|-----------|---------------|---------------|
| Heartbeat | Worker → Coordinator every 30s | Detect failure in 90s |
| Requeue | Failed URLs back to frontier with retry count | Immediate after detection |
| Checkpoint | Frontier state WAL, flush every 60s | Resume from last checkpoint |
| Idempotent fetch | URL + timestamp dedup at output sink | No duplicate content |
| Graceful shutdown | SIGTERM → drain current fetches → flush state → exit | 30s drain window |

## Domain-to-Worker Assignment

### Consistent Hashing Ring

```
Hash ring with virtual nodes:
- 150 virtual nodes per physical worker
- Hash function: MurmurHash3(domain) → ring position
- On worker add: redistribute only affected domains (~1/N)
- On worker remove: reassign affected domains to next clockwise node

Benefits:
- Minimal redistribution on topology change
- Domain affinity (same domain → same worker → session reuse)
- Even load distribution with virtual nodes
```

### Alternative: Range-Based Sharding

```
Domain alphabet ranges assigned to workers:
- Worker 1: a*-f* domains
- Worker 2: g*-m* domains
- Worker N: remainder

Benefits: Simple, predictable
Drawbacks: Uneven distribution (popular TLDs cluster), requires rebalancing
```

## Checkpoint and Recovery Design

### Write-Ahead Log (WAL) for Frontier

```
WAL entry format:
  { timestamp, operation: ADD|COMPLETE|FAIL, url, domain, priority, retry_count }

Recovery procedure:
1. Load last RDB/AOF snapshot
2. Replay WAL entries after snapshot timestamp
3. Mark in-progress URLs as PENDING (re-fetch)
4. Resume normal operation
```

### Graceful Shutdown Protocol

```
1. SIGTERM received
2. Stop accepting new URLs from frontier
3. Complete in-flight fetches (max 30s)
4. Flush frontier state to disk
5. Commit Kafka offsets / Redis state
6. Report final metrics
7. Exit 0
```

## Network and Infrastructure Estimation

| Scale | Egress/day | Compute | Storage/month | Redis/Kafka |
|-------|-----------|---------|---------------|-------------|
| Small | 1-10 GB | 1 vCPU, 2 GB RAM | 10-100 GB | 1 Redis (512 MB) |
| Medium | 10-200 GB | 4-20 vCPU, 8-40 GB RAM | 100 GB-2 TB | Redis cluster (2-8 GB) |
| Large | 200 GB-5 TB | 40-400 vCPU, 80-800 GB RAM | 2-50 TB | Kafka cluster (3-10 brokers) |
| Web-scale | 5+ TB | 400+ vCPU, 800+ GB RAM | 50+ TB | Kafka + HDFS cluster |
