# AI / GPU Workload Cost Reference

Purpose: Subcommand-scoped methodology for AI/ML cost optimization across training and inference workloads. Models GPU SKU economics (H100 / H200 / A100 / L40S / T4), separates training-vs-inference cost profiles, evaluates spot/preemptible viability with checkpoint cadence, and quantifies the cost impact of model quantization, batching, and serving topology. Delivers FinOps for FMOps — unit economics in cost per 1K tokens, cost per 1K requests, and cost per training-run.

## Scope Boundary

- **ledger `gpu-cost`**: GPU/accelerator workload cost — SKU selection, training/inference split, spot strategy, quantization impact, serving topology economics.
- **ledger `rightsizing` (elsewhere)**: general-compute CPU/memory rightsizing. Does NOT apply to GPU — utilization signals (SM occupancy, GPU memory, tokens/sec) differ fundamentally.
- **ledger `ri-sp` (elsewhere)**: commitment products. `gpu-cost` recommends GPU coverage targets (cap at 1y, 20-40% baseline); `ri-sp` executes the purchase plan.
- **ledger `estimate` (elsewhere)**: IaC cost projection. For GPU workloads, `gpu-cost` provides the per-token / per-request unit-cost overlay that `estimate` lacks.
- **oracle (elsewhere)**: model selection, prompt design, RAG architecture. Oracle owns "which model"; `gpu-cost` owns "what does that choice cost per 1K tokens."
- **scaffold (elsewhere)**: IaC for GPU clusters (EKS GPU node pools, SageMaker endpoints, Vertex AI). `gpu-cost` provides the topology + sizing; Scaffold provisions.
- **beacon (elsewhere)**: GPU-utilization SLO (SM occupancy floor, p95 inference latency). `gpu-cost` consumes Beacon's latency budget when sizing batch vs realtime.

## Workflow

```
INTAKE     →  classify workload: training (batch/continuous) vs inference (realtime/batch/async)
           →  capture model size (params), context length, throughput target, latency SLO

PROFILE    →  collect 14-30d GPU metrics: SM occupancy, mem utilization, tokens/sec, p95 latency
           →  separate training and inference series — never average them

SKU MATCH  →  map workload to SKU tier (see GPU SKU table); reject undersized & oversized
           →  check spot/preemptible availability and historical interruption rate per region

OPTIMIZE   →  apply tactic stack: quantization, batching, KV-cache sharing, MIG/MPS, speculative decoding
           →  for training: checkpoint cadence vs spot interruption rate

UNITIZE    →  compute cost per 1K tokens (LLM), cost per 1K requests (inference), cost per epoch (training)
           →  attribute by tenant / model / endpoint when multi-tenant

HANDOFF    →  Scaffold: GPU node pool / endpoint IaC; Beacon: GPU SLO + cost-per-token alert;
           →  Oracle: feasible quantization / serving choices given cost envelope
```

## GPU SKU Pricing & Workload Fit

| SKU | Mem (HBM) | On-demand $/hr (USD, approx) | Spot discount | Best workload |
|-----|-----------|------------------------------|---------------|---------------|
| H200 | 141 GB | $10-13 | 50-70% | 70B+ training, long-context inference |
| H100 80GB | 80 GB | $4-12 | 50-70% | 13B-70B training, high-throughput inference |
| H100 NVL / SXM | 94 GB | $5-13 | 50-70% | LLM inference with KV-cache pressure |
| A100 80GB | 80 GB | $2-5 | 60-80% | 7B-30B training, established inference |
| A100 40GB | 40 GB | $1.5-4 | 60-80% | Mid-size training, fine-tuning |
| L40S | 48 GB | $1-2 | 50-70% | Inference, fine-tuning, graphics+AI |
| L4 | 24 GB | $0.7-1.2 | 60-80% | Cost-efficient inference, video AI |
| T4 | 16 GB | $0.35-0.6 | 60-80% | Light inference, embeddings, classic CV |
| Inferentia2 / Trainium | varies | 30-50% lower | n/a | AWS-locked, Neuron-compatible models |
| TPU v5e / v5p | varies | competitive | preempt: 60-80% | JAX/PyTorch on GCP |

Prices vary by region, contract, and provider — treat as order-of-magnitude. Always re-check at decision time.

## Training vs Inference Cost Profile

| Dimension | Training | Inference (realtime) | Inference (batch) |
|-----------|----------|---------------------|-------------------|
| Pricing model | Spot + checkpoint | RI/SP for floor + on-demand | Spot + queue |
| Utilization target | 80%+ SM occupancy | 40-70% (latency headroom) | 80%+ |
| Interruption tolerance | Yes (with checkpointing) | None | Yes |
| Right-size signal | Throughput (samples/sec) | p95 latency + cost/1K req | Throughput + cost/1K req |
| Spot savings realized | 50-70% (after rework loss) | 0% (rarely viable) | 50-70% |
| Commitment fit | 1y RI for steady fleet floor | 1y RI/SP for predictable QPS | None — Spot dominates |
| Unit cost | $/training run, $/epoch | $/1K requests, $/1K tokens | $/1M items processed |

## Spot / Preemptible Strategy

| Workload | Spot viability | Checkpoint cadence | Expected savings |
|----------|---------------|--------------------|------------------|
| Pre-training (large LLM) | High | 5-15 min | 50-70% net of rework |
| Fine-tuning (LoRA/QLoRA) | High | 10-30 min | 60-75% |
| RLHF / DPO training | Medium | 5-10 min | 40-60% (reward model recompute cost) |
| Realtime inference | None | n/a | n/a — use on-demand or RI |
| Batch inference | High | per-batch idempotent | 50-70% |
| Embedding generation | High | per-shard idempotent | 60-80% |
| Hyperparameter sweep | High | per-trial | 60-80% |

Rule: checkpoint cadence ≈ (mean time between interruptions / 4). If MTBI is 60 min, checkpoint every 15 min — limits worst-case rework to 15 min per interruption.

## Quantization & Optimization Cost Impact

| Technique | Memory saving | Throughput gain | Quality cost | Cost/1K-token impact |
|-----------|---------------|-----------------|--------------|---------------------|
| FP16 baseline | 1.0× | 1.0× | baseline | baseline |
| BF16 | 1.0× | 1.0× | ~baseline | ~baseline |
| INT8 (W8A8) | 0.5× | 1.5-2× | <1% on most | -40 to -55% |
| INT4 (W4A16, GPTQ/AWQ) | 0.25× | 1.3-1.7× | 1-3% degradation | -50 to -65% |
| FP8 (H100/H200 native) | 0.5× | 1.8-2.5× | <1% | -45 to -60% |
| Speculative decoding | 1.0× | 1.5-3× (latency-bound) | none | -30 to -55% |
| Continuous batching | 1.0× | 2-5× (QPS-bound) | none | -50 to -75% |
| KV-cache sharing (PagedAttention) | -30 to -50% mem | 2-3× | none | -40 to -60% |
| MIG (A100/H100 partitioning) | n × small slice | n × isolated | none | -30 to -50% on small models |

## Anti-Patterns

- Applying CPU rightsizing thresholds to GPUs — "CPU < 40%" logic does not map. GPU rightsizing reads SM occupancy, HBM utilization, and tokens/sec, not GPU% alone.
- Treating training and inference as one workload — fundamentally different utilization shapes, pricing models, and SLO constraints. Always split before optimizing.
- Buying 3-year RIs on GPU SKUs — model architecture and SKU velocity (H100 -> H200 -> B200 within 18 months) make multi-year locks high-risk. Cap GPU commitments at 1 year.
- Running realtime inference on Spot — interruption mid-request violates latency SLOs. Spot belongs in training and batch inference only.
- Quantizing without quality eval — INT4 saves 50-65% but can degrade 1-3% on benchmarks; for production, gate on eval suite (Oracle owns the eval). Cost wins are meaningless if the model fails its task.
- Reporting cost per GPU-hour as the unit — not actionable for product teams. Always derive cost per 1K tokens (LLM), cost per 1K requests (inference), or cost per training run (training).
- Provisioning H100 for 7B-class models — over-provisioned HBM wastes 40-60% of cost. Match SKU to model size; L40S/L4 often beats H100 on $/throughput for small models.
- Ignoring KV-cache memory in capacity planning — long-context inference (>32K tokens) is memory-bound, not compute-bound; SKU selection driven by cache footprint, not raw FLOPS.
- Skipping continuous batching on inference — static batching wastes 50-75% of GPU. vLLM / TGI / TensorRT-LLM continuous batching is the default, not an optimization.

## Handoff

- **To Scaffold**: GPU node-pool IaC (taints/tolerations, MIG/MPS config), endpoint topology (single vs multi-replica, autoscaler config), spot interruption handler.
- **To Beacon**: GPU SLO (SM occupancy floor, p95 latency, cost-per-1K-tokens budget); cost-anomaly rule on token-throughput-vs-cost ratio.
- **To Oracle**: feasible quantization / serving choices given cost envelope; cost-per-1K-tokens ceiling per model tier.
- **To Ledger `ri-sp`**: GPU-baseline commitment plan (1y, 20-40% coverage on inference floor only).
- **To Atlas**: AI platform topology view — training cluster, inference fleet, eval pipeline as separate cost centers.
