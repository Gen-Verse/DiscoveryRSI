"""Public, dependency-free Gene Ontology domain adapters.

The adapters turn user-supplied GO pathway and target-annotation records into
structured DiscoveryRSI candidates. They do not bundle a database or fetch
private campaign data; users may prepare records from the current GO release.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from .core import Candidate


def _genes(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({str(v).strip() for v in values if str(v).strip()}))


@dataclass(frozen=True)
class GOPathway:
    term_id: str
    name: str
    genes: tuple[str, ...]
    source: str = "user-supplied"

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> "GOPathway":
        return cls(
            term_id=str(record.get("term_id", "")).strip(),
            name=str(record.get("name", "")).strip(),
            genes=_genes(record.get("genes", [])),
            source=str(record.get("source", "user-supplied")),
        )


@dataclass(frozen=True)
class GOTargetRecord:
    target: str
    term_ids: tuple[str, ...]
    evidence: tuple[str, ...] = ()
    source: str = "user-supplied"

    @classmethod
    def from_record(cls, record: Mapping[str, object]) -> "GOTargetRecord":
        return cls(
            target=str(record.get("target", "")).strip(),
            term_ids=tuple(sorted({str(v).strip() for v in record.get("term_ids", []) if str(v).strip()})),
            evidence=tuple(str(v).strip() for v in record.get("evidence", []) if str(v).strip()),
            source=str(record.get("source", "user-supplied")),
        )


class GOPathwayAdapter:
    """Create pathway-mechanism candidates from a user-supplied GO table."""

    def __init__(self, pathways: Sequence[GOPathway], background_genes: Iterable[str] = ()):
        self.pathways = tuple(pathways)
        self.background_genes = _genes(background_genes)

    @classmethod
    def from_records(cls, records: Iterable[Mapping[str, object]], background_genes: Iterable[str] = ()):
        return cls(tuple(GOPathway.from_record(r) for r in records), background_genes)

    def candidates(self, episode: int = 1, min_genes: int = 2) -> list[Candidate]:
        candidates: list[Candidate] = []
        for index, pathway in enumerate(self.pathways, 1):
            if not pathway.term_id or not pathway.name or len(pathway.genes) < min_genes:
                continue
            background = len(self.background_genes) or len(set(g for p in self.pathways for g in p.genes))
            claim = (f"The {pathway.name} pathway ({pathway.term_id}) is associated with the target phenotype "
                     "through the listed gene set, conditional on the supplied annotation.")
            plan = (f"Compare the pathway gene set ({len(pathway.genes)} genes) with a matched background "
                    f"({background} genes), then test perturbation or held-out association; predefine effect size "
                    "and a null permutation threshold.")
            alternatives = ["Gene-set size or annotation density creates the association.",
                            "A neighboring pathway explains the signal."]
            evidence = [f"GO term: {pathway.term_id}", f"Genes: {', '.join(pathway.genes)}", f"Source: {pathway.source}"]
            candidates.append(Candidate(f"go-pathway-{episode}-{index}", claim, plan, alternatives, evidence))
        return candidates


class GOTargetPrioritizationAdapter:
    """Create testable therapeutic-prioritization candidates from GO annotations."""

    def __init__(self, targets: Sequence[GOTargetRecord], prioritized_terms: Iterable[str] = ()):
        self.targets = tuple(targets)
        self.prioritized_terms = tuple(sorted({str(v).strip() for v in prioritized_terms if str(v).strip()}))

    @classmethod
    def from_records(cls, records: Iterable[Mapping[str, object]], prioritized_terms: Iterable[str] = ()):
        return cls(tuple(GOTargetRecord.from_record(r) for r in records), prioritized_terms)

    def candidates(self, episode: int = 1) -> list[Candidate]:
        candidates: list[Candidate] = []
        for index, target in enumerate(self.targets, 1):
            if not target.target or not target.term_ids:
                continue
            overlap = sorted(set(target.term_ids).intersection(self.prioritized_terms))
            claim = (f"{target.target} should be prioritized for therapeutic follow-up because its GO annotations "
                     f"cover {len(target.term_ids)} pathway term(s)" +
                     (f", including {', '.join(overlap)}." if overlap else "."))
            plan = ("Rank against matched non-target controls using prespecified pathway coverage, expression or "
                    "perturbation evidence, and an out-of-sample outcome; report the rank stability after removing "
                    "each annotation source.")
            alternatives = ["Annotation count favors well-studied targets.",
                            "Target tractability or expression, rather than pathway relevance, drives the rank."]
            evidence = [f"GO terms: {', '.join(target.term_ids)}", *target.evidence, f"Source: {target.source}"]
            candidates.append(Candidate(f"go-target-{episode}-{index}", claim, plan, alternatives, evidence))
        return candidates
