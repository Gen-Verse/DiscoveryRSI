<h1 align="center">DiscoveryRSI</h1>

<p align="center">
  <strong>Recursive research-hypothesis improvement with agentic roles, tools, and replay</strong>
</p>

<p align="center">
  Propose evidence-grounded hypotheses. Critique the design. Select the next experiment. Replay the decision.
</p>

<p align="center">
  <a href="https://github.com/Gen-Verse/DiscoveryRSI">
    <img src="https://img.shields.io/badge/GitHub-DiscoveryRSI-181717?style=for-the-badge&logo=github&logoColor=white" alt="DiscoveryRSI on GitHub">
  </a>
  <a href="https://huggingface.co/collections/Gen-Verse/discoveryrsi">
    <img src="https://img.shields.io/badge/Hugging%20Face-DiscoveryRSI-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black" alt="DiscoveryRSI on Hugging Face">
  </a>
  <a href="https://arena.ai/leaderboard/agent">
    <img src="https://img.shields.io/badge/Live%20Agent%20Arena-Evaluate-4C1D95?style=for-the-badge&logo=livechat&logoColor=white" alt="Live Agent Arena">
  </a>
  <a href="https://github.com/Gen-Verse/DiscoveryRSI/pulls">
    <img src="https://img.shields.io/badge/Development-Open%20source-2EA44F?style=for-the-badge&logo=github&logoColor=white" alt="Open-source development">
  </a>
</p>

<p align="center">
  <a href="#overview">Overview</a> ·
  <a href="#framework">Framework</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#data-and-model-access">Data and Model Access</a> ·
  <a href="#citation">Citation</a>
</p>

## Overview

> A runnable agentic system for recursive research-hypothesis improvement.

DiscoveryRSI represents research hypotheses as versioned claims, investigation plans, evidence, alternatives, scores, and lineage. Its harness runs a bounded recursive loop:

**Propose → Critique → Select → Retain → Replay**

The public package includes the agentic core, replay store, provider adapters, campaign harness, CPU demo, and tests. Private EHR runtime code, internal campaign records, credentials, infrastructure paths, and laboratory deployment files are excluded.

![DiscoveryRSI result highlight](docs/media/discoveryrsi-result-highlight.png)

*Figure 1. Result highlight from the technical report.*

![DiscoveryRSI method](docs/media/discoveryrsi-method.png)

*Figure 2. DiscoveryRSI method overview from the technical report.*

## Quick Start

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

## GEO pathway and therapeutic-prioritization domains

The release includes two dependency-free domain adapters for users working with Gene Ontology (GO) records:

- **GEO disease-pathway analysis** turns a user-supplied table of GEO terms and genes into pathway-mechanism candidates. Each candidate includes a matched-background comparison, a held-out or perturbation test, alternative explanations, and a falsification threshold.
- **GEO therapeutic-target prioritization** turns target-to-term annotations into ranking candidates. The plan tests rank stability against matched controls and annotation-source ablations, while separating pathway relevance from tractability and expression effects.

The adapters consume JSON records prepared by the user. They do not bundle GEO-derived data, call private services, or encode a particular disease. Prepare records from the GEO release and other public sources under their applicable terms, then run:

```bash
discovery-rsi domain-demo --domain geo-pathway --input configs/geo_pathway_demo.json
discovery-rsi domain-demo --domain geo-target-prioritization --input configs/geo_target_prioritization_demo.json
```

The example files are small smoke-test inputs. Replace them with your own gene sets, target annotations, background population, and evidence. The resulting candidates can be passed to `DiscoveryLoop` or the provider-backed harness for model critique and replay.

## Harness, roles, tools, and research manifest

The public release includes the runnable harness and its portable orchestration layer:

```text
src/discovery_rsi/harness.py       propose → critique → select → replay
src/discovery_rsi/manifest.py      campaign question, domains, roles, and tools
src/discovery_rsi/tools.py         explicit tool registry with safe local handlers
src/discovery_rsi/plugin.py        declarative role loading
plugins/discovery-rsi/roles/       lead, generation, critique, evolution, compiler
configs/research_manifest.json     example campaign contract
```

Launch a provider-backed campaign with the manifest and role prompts:

```bash
discovery-rsi campaign \
  --adapter openai-compatible \
  --manifest configs/research_manifest.json \
  --roles plugins/discovery-rsi/roles \
  --iterations 3 \
  --replay episodes.jsonl
```

The harness only sends the prompt, manifest, role excerpts, and candidate context to the selected adapter. It does not discover or upload files automatically. Add a dataset or evidence source through your own adapter, then record its provenance in the candidate evidence fields. The public release contains no clinical dataset, no patient rows, no HCC or UK Biobank material, and no private campaign traces.

### Accessing data and model artifacts

This repository is the agentic system. To run it, clone the repository, install it locally, and provide your own API key or local model command. For biomedical work, prepare your own legally accessible tables, GEO/GO annotations, literature records, or public APIs and pass only the fields needed by your adapter. Keep source data read-only and keep credentials in environment variables or your provider's local credential store.

The DiscoveryRSI 27B checkpoint is distributed separately through the [Gen-Verse Hugging Face collection](https://huggingface.co/collections/Gen-Verse/discoveryrsi) when access is enabled. A checkpoint is optional: the harness can call any OpenAI-compatible endpoint, Codex, Claude, or another adapter implementing `ModelAdapter`. Follow each dataset and model's license, access approval, and citation requirements before downloading or redistributing it.

For GEO disease-pathway and therapeutic-prioritization runs, use the GEO records prepared by the user (for example, a series matrix or differential-expression table) and map them to public Gene Ontology term annotations before invoking `domain-demo`. The example JSON files are synthetic smoke tests, not a downloadable biological dataset.

### Native Codex and Claude Code adapters

The original implementation uses provider-native command runners. The public harness exposes the same two entry points:

```bash
# Codex CLI; uses the local Codex login and a read-only sandbox
export DISCOVERY_RSI_CODEX_MODEL=gpt-6.1-sol
discovery-rsi campaign --adapter codex --manifest configs/research_manifest.json

# Claude Code; uses the native stream interface and public plugin roles
export ANTHROPIC_AUTH_TOKEN=your-token
export DISCOVERY_RSI_CLAUDE_MODEL=claude-sonnet
export DISCOVERY_RSI_PLUGIN_DIR=plugins/discovery-rsi
discovery-rsi campaign --adapter claude-code --manifest configs/research_manifest.json --roles plugins/discovery-rsi/roles
```

The Claude Code runner preserves the native stream JSON protocol, restricted permission mode, no-session persistence, model selection, plugin directory, and role selection. The Codex runner uses `codex exec --json --ephemeral` with a read-only sandbox. Authentication remains local to each CLI; no credential is written to the repository.
