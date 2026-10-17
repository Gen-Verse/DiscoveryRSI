<div align="center">

<h1>DiscoveryRSI</h1>

<p><strong>Recursively learning to discover valuable hypotheses</strong></p>

<p>
  <a href="https://github.com/Gen-Verse/DiscoveryRSI"><img src="https://img.shields.io/badge/DiscoveryRSI-GitHub-black?logo=github&logoColor=white" alt="DiscoveryRSI GitHub"/></a>
  <a href="https://huggingface.co/Gen-Verse/DiscoveryRSI-27B"><img src="https://img.shields.io/badge/DiscoveryRSI--27B-Hugging%20Face-FFCC00?logo=huggingface&logoColor=black" alt="DiscoveryRSI-27B on Hugging Face"/></a>
  <a href="https://huggingface.co/collections/Gen-Verse/discoveryrsi"><img src="https://img.shields.io/badge/DiscoveryRSI-Collection-FFD21E?logo=huggingface&logoColor=black" alt="DiscoveryRSI collection"/></a>
  <a href="https://foundry-arena.rsi-arena.workers.dev/arena"><img src="https://img.shields.io/badge/Live%20Arena-Watch%20DiscoveryRSI-4C1D95" alt="DiscoveryRSI live arena"/></a>
</p>

</div>

## 🎯 About This Repository

This repository contains the public **DiscoveryRSI** research harness: a model-agnostic system for recursively developing, evaluating, revising, and attributing scientific hypotheses.

DiscoveryRSI turns a research question and available evidence into an explicit hypothesis, investigation plan, alternatives, decision criteria, and falsification conditions. The system preserves the full research path so every revision can be inspected, replayed, and improved.

## 🌟 Introduction

DiscoveryRSI treats a hypothesis as a versioned research object rather than a finished answer. Its core loop is:

- 🔎 **Explore**: identify valuable questions and candidate explanations
- 🧪 **Evaluate**: propose tests, comparators, evidence, and decision criteria
- 🛠️ **Revise**: repair weak designs and incorporate criticism
- 🧬 **Attribute**: connect progress to the behavior that produced it
- 🔁 **Learn**: carry validated improvements into future research paths

A multi-agent research tree can develop, repair, combine, or restart directions as evidence changes. The result is a traceable path from **question → hypothesis → evidence → experiment → revision**.

## 📦 Resources

| **Type** | **Name** | **Link** |
| --- | --- | --- |
| 🤖 Model | **DiscoveryRSI-27B** | [🤗 Hugging Face](https://huggingface.co/Gen-Verse/DiscoveryRSI-27B) |
| 🧰 Code | **DiscoveryRSI harness** | [GitHub](https://github.com/Gen-Verse/DiscoveryRSI) |
| 📚 Collection | **DiscoveryRSI models** | [🤗 Hugging Face](https://huggingface.co/collections/Gen-Verse/discoveryrsi) |
| 📺 Demo | **DiscoveryRSI live arena** | [Open arena](https://foundry-arena.rsi-arena.workers.dev/arena) |
| 🧪 Benchmark | **DFM-Bench workflow evaluation** | [Explore the harness](https://github.com/Gen-Verse/DiscoveryRSI#evidence) |

## 🧠 What DiscoveryRSI does

The public harness includes the portable agentic core, provider adapters, role prompts, tool registry, replay store, campaign manifest, and domain adapters.

It supports research workflows that:

- generate falsifiable, data-aware study plans;
- add controls, measurements, alternatives, and evidence boundaries;
- preserve parent links and revision lineage;
- identify whether an idea was evolved, repaired, crossed over, or restarted;
- replay tool failures, repeated rediscovery, and lost context; and
- evaluate complete research paths instead of isolated text generations.

The system was developed across clinical and population health, therapeutic-target prioritization, disease mechanisms, and population multi-omics. GEO pathway and therapeutic-target adapters are included for user-provided records.

## 📺 Watch the live research loop

PhAI Labs is running a technical livestream that shows a scientific agent move from an open question to a testable research plan, then learn from evidence, critique, and revision.

<a href="https://foundry-arena.rsi-arena.workers.dev/arena"><img src="docs/media/discoveryrsi-live-demo-poster.png" alt="DiscoveryRSI live arena demo" width="100%"></a>

<video controls width="100%" poster="docs/media/discoveryrsi-live-demo-poster.png">
  <source src="docs/media/discoveryrsi-live-demo.mp4" type="video/mp4">
  Your browser can [download the one-minute demo](docs/media/discoveryrsi-live-demo.mp4).
</video>

[**Enter the live research room →**](https://foundry-arena.rsi-arena.workers.dev/arena)

The arena makes the process inspectable: model comparisons, research domains, candidate hypotheses, compiled experiments, and the growing hypothesis tree update as the run progresses.

## 📊 Evidence

In the reported literature comparison, DiscoveryRSI reached a **6.3% reference-actionability rate**, approximately **2.5× the GPT group** and **2.7× Claude**. This retrospective measure asks whether a generated hypothesis can be connected to a concrete research direction in later expert-published work, such as an experimental comparison, a measurement strategy, or a testable evidence gap.

Across two self-improvement rounds, average hypothesis quality rose from **4.86 to 5.39**. In expert review, **41% of DiscoveryRSI-27B revisions improved** and only **12% regressed**. These results are research-process signals and do not replace independent scientific validation.

## 🚀 Quick Start

Clone the repository and install the public harness:

```bash
git clone https://github.com/Gen-Verse/DiscoveryRSI.git
cd DiscoveryRSI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run the deterministic local demo and tests:

```bash
discovery-rsi demo --iterations 2
pytest
```

## 🤖 Connect DiscoveryRSI-27B

The released checkpoint is [`Gen-Verse/DiscoveryRSI-27B`](https://huggingface.co/Gen-Verse/DiscoveryRSI-27B). Serve it behind an OpenAI-compatible endpoint, then point the harness at that endpoint:

```bash
export MODEL_ID=Gen-Verse/DiscoveryRSI-27B
vllm serve "$MODEL_ID" --served-model-name discoveryrsi-27b
```

In a second terminal:

```bash
export DISCOVERY_RSI_BASE_URL=http://localhost:8000/v1
export DISCOVERY_RSI_MODEL=discoveryrsi-27b
export DISCOVERY_RSI_API_KEY=local

discovery-rsi campaign \
  --adapter openai-compatible \
  --manifest configs/research_manifest.json \
  --roles plugins/discovery-rsi/roles \
  --iterations 3 \
  --replay episodes.jsonl
```

The harness can also run with Codex, Claude Code, another OpenAI-compatible endpoint, or any implementation of the `ModelAdapter` protocol.

## 🧪 Research Domains

The public package includes workflows and adapters for:

- clinical and population health;
- therapeutic-target prioritization;
- disease mechanisms;
- population multi-omics; and
- GEO-derived pathway and target records.

Bring only data you are authorized to use. No patient rows, HCC material, UK Biobank material, private campaign traces, credentials, or laboratory infrastructure are bundled.

## ⚠️ Limitations and Responsible Use

DiscoveryRSI can produce plausible but unsupported claims, omit relevant evidence, misread sources, or propose infeasible experiments. Generated hypotheses require expert review, source checking, and independent verification. The system is not a medical device and must not be used to make clinical or other high-stakes decisions without qualified oversight.

## 📝 Citation

If you use DiscoveryRSI or DiscoveryRSI-27B, cite the technical report and link the released model:

```bibtex
@software{discoveryrsi,
  title = {DiscoveryRSI},
  url = {https://github.com/Gen-Verse/DiscoveryRSI},
  note = {Recursive scientific hypothesis discovery and DiscoveryRSI-27B}
}
```

- [Technical report and maintained citation links](https://github.com/Gen-Verse/DiscoveryRSI#citation)
- [DiscoveryRSI-27B model card](https://huggingface.co/Gen-Verse/DiscoveryRSI-27B)
- [PhAI Labs](https://phai-labs.com/)

## 📄 License

Project-owned code is licensed under Apache-2.0. See [LICENSE](LICENSE) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The model license, base-model terms, and dataset attribution requirements are specified separately in the model card.
