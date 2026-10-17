# DiscoveryRSI

> A runnable agentic system for recursive research-hypothesis improvement.

DiscoveryRSI represents research hypotheses as versioned claims, investigation plans, evidence, alternatives, scores, and lineage. Its harness runs a bounded recursive loop:

**Propose → Critique → Select → Retain → Replay**

The public package includes the agentic core, replay store, provider adapters, campaign harness, CPU demo, and tests. Private EHR runtime code, internal campaign records, credentials, infrastructure paths, and laboratory deployment files are excluded.

![DiscoveryRSI result highlight](docs/media/discoveryrsi-result-highlight.png)

*Figure 1. Result highlight from the technical report.*

![DiscoveryRSI method](docs/media/discoveryrsi-method.png)

*Figure 2. DiscoveryRSI method overview from the technical report.*

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m pip install pytest
```

## Run the CPU demo

```bash
discovery-rsi demo --iterations 2
pytest
```

The demo uses deterministic local adapters and requires no model, dataset, GPU, or API key.

## Launch a discovery campaign with an API key

DiscoveryRSI supports any OpenAI-compatible endpoint. Set the endpoint, model, and key in the environment; keys are never stored in configs or source files.

```bash
export DISCOVERY_RSI_BASE_URL=https://api.openai.com/v1
export DISCOVERY_RSI_MODEL=gpt-4o-mini
export DISCOVERY_RSI_API_KEY=your-key
discovery-rsi campaign --adapter openai-compatible --iterations 3 --replay episodes.jsonl
```

The endpoint must provide `/chat/completions`. Each episode records generated candidates, critique scores, selection, lineage, and replay output. The harness does not send local files or private data unless an adapter explicitly includes them in its prompt.

## Codex and Claude adapters

If the Codex or Claude command is installed locally, the same harness can call it through a command adapter:

```bash
export DISCOVERY_RSI_CODEX=codex
discovery-rsi campaign --adapter codex --iterations 2

export DISCOVERY_RSI_CLAUDE=claude
discovery-rsi campaign --adapter claude --iterations 2
```

The public adapter passes a prompt and captures stdout. Authentication, model selection, sandboxing, and tool permissions remain controlled by the local CLI.

## Adapt the harness

Implement the `ModelAdapter` protocol when integrating another provider, or replace the proposer/critic functions for a domain-specific workflow. The `ToolRegistry` and dataset adapter layers should remain outside the core package and receive only the data the user explicitly authorizes.

## EHR boundaries

MIMIC-IV and eICU can be connected through user-supplied adapters subject to their access terms. HCC and UK Biobank code, paths, data, and private source packages are excluded from this release. No dataset is bundled.

## DiscoveryRSI 27B

The DiscoveryRSI 27B RAFT model is released separately from this agentic system. See the [Gen-Verse DiscoveryRSI collection](https://huggingface.co/collections/Gen-Verse/discoveryrsi) for model artifacts when available.

## Layout

```text
src/discovery_rsi/   core loop, replay, harness and provider adapters
configs/             portable configuration examples
examples/            extension guidance
docs/media/          technical-report figures
tests/               CPU tests
```

## License

Apache-2.0. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Citation

Please cite the DiscoveryRSI technical report and model card when using this system or checkpoint.
