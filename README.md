# DiscoveryRSI

DiscoveryRSI is a public, model-agnostic agentic core for recursive research-hypothesis improvement. It represents hypotheses as versioned claims with investigation plans, alternatives, evidence, and lineage, then runs a bounded **propose → critique → select → retain** loop.

This repository contains the public agentic system. Private datasets, credentials, internal campaign traces, infrastructure paths, and model-training packages are excluded.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
discovery-rsi --iterations 2
pytest
```

The demo is CPU-only and uses deterministic local adapters. To use a real model, implement the `proposer` and `critic` callables in `DiscoveryLoop`; the core does not require a particular provider or endpoint.

## Core API

- `Candidate`: versioned hypothesis, plan, alternatives, evidence, lineage, score, and critique.
- `DiscoveryLoop`: bounded recursive propose/critique/select/retain orchestration.
- `ReplayBuffer`: append-only JSONL replay for reproducible local runs.
- `Episode`: serialized record of each bounded research interaction.

## Design boundary

The public package provides orchestration contracts and replay. Dataset adapters, model clients, evaluators, and domain-specific tools are intentionally injected by the user. Do not place private patient data, credentials, raw traces, or internal deployment paths in this repository.

## Model release

The DiscoveryRSI 27B RAFT model is released separately from this agentic core. Use the model card and the technical report for checkpoint identity, licensing, inference requirements, and evaluation limitations.

## Citation

Please cite the DiscoveryRSI technical report when using the system or model.
