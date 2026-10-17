# DiscoveryRSI

> Recursive research-agent orchestration for developing, comparing, and retaining scientific hypotheses.

DiscoveryRSI is a model-agnostic agentic system for recursive research. It represents a research hypothesis as a versioned claim, investigation plan, evidence record, alternatives, and lineage. A bounded episode then follows:

**Propose → Critique → Select → Retain → Replay**

The public package contains the agentic orchestration core and a deterministic local demo. Model clients, dataset adapters, evaluators, and domain tools are injected through small Python callables so the system can run with a local model, an OpenAI-compatible endpoint, or another provider.

![DiscoveryRSI result highlight](docs/media/discoveryrsi-result-highlight.png)

*Figure 1. Result highlight from the technical report: recursive research improves hypothesis quality, research behavior, and revision progress. Values and evaluation boundaries are defined by the report.*

## Method

![DiscoveryRSI method](docs/media/discoveryrsi-method.png)

*Figure 2. DiscoveryRSI couples multi-agent hypothesis development with evidence, planned investigations, recursive model/harness updates, and rediscovery.*

The core abstractions are:

- `Candidate`: a versioned hypothesis, plan, alternatives, evidence, parents, score, and critique.
- `DiscoveryLoop`: bounded propose/critique/select/retain orchestration.
- `Episode`: an immutable record of one bounded research interaction.
- `ReplayBuffer`: append-only JSONL replay for local reproducibility.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
discovery-rsi --iterations 2
pytest
```

The demo is CPU-only and uses deterministic local adapters. It does not download a model, access private data, or require a provider key.

## Use a real model

Provide a proposer and critic adapter to `DiscoveryLoop`:

```python
from discovery_rsi import Candidate, DiscoveryLoop, ReplayBuffer

loop = DiscoveryLoop(
    proposer=my_proposer,
    critic=my_critic,
    iterations=3,
    replay=ReplayBuffer("episodes.jsonl"),
)
episodes = loop.run()
```

Adapters should keep model credentials outside source files, return structured candidates, and preserve the evidence and alternatives used for each decision. The public core does not assume a particular API, model family, tokenizer, or serving stack.

## EHR and scientific data boundaries

The public system is data-adapter based. Users may provide adapters for public or authorized datasets such as MIMIC-IV and eICU, subject to their own access terms and data-use agreements. Dataset files are never bundled in this repository.

HCC and UK Biobank adapters, paths, data, and internal source packages are intentionally excluded from this public release. Private patient data, credentials, campaign traces, internal seed catalogs, and laboratory infrastructure are not part of the package.

## DiscoveryRSI 27B

The DiscoveryRSI 27B RAFT model is released separately from this agentic core. The public model collection is maintained at [Gen-Verse/DiscoveryRSI](https://huggingface.co/collections/Gen-Verse/discoveryrsi). Use the model card for checkpoint identity, license, inference requirements, and evaluation limitations.

## Repository layout

```text
src/discovery_rsi/   public orchestration core
configs/             local demo configuration
examples/            adapter examples and extensions
tests/               CPU tests
docs/                release and reproducibility notes
```

## Scope and reproducibility

This repository provides the portable agentic contracts and local replay mechanism. The technical report describes the full research protocol, including hypothesis credit assignment, harness replay, recursive deployment, and evaluation boundaries. Reproducing a particular scientific result additionally requires the stated dataset access, model checkpoint, domain adapter, and evaluation protocol.

## License

Apache-2.0. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Citation

Please cite the DiscoveryRSI technical report and the model card when using the system or checkpoint.
