"""Portable research manifest for a DiscoveryRSI campaign."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
import json
from pathlib import Path
from typing import Any, Mapping

@dataclass(frozen=True)
class ResearchManifest:
    name: str
    question: str
    domains: tuple[str, ...] = ()
    roles: tuple[str, ...] = ("scientist", "critic", "selector")
    tools: tuple[str, ...] = ("record_evidence", "compare", "falsify")
    evidence_policy: str = "user-supplied"
    max_candidates: int = 2
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ResearchManifest":
        if not str(data.get("name", "")).strip(): raise ValueError("manifest.name is required")
        if not str(data.get("question", "")).strip(): raise ValueError("manifest.question is required")
        n=int(data.get("max_candidates", 2))
        if n < 1: raise ValueError("manifest.max_candidates must be positive")
        return cls(str(data["name"]), str(data["question"]), tuple(map(str, data.get("domains", []))), tuple(map(str, data.get("roles", cls.roles))), tuple(map(str, data.get("tools", cls.tools))), str(data.get("evidence_policy", cls.evidence_policy)), n, dict(data.get("metadata", {})))

    @classmethod
    def load(cls, path: str | Path) -> "ResearchManifest":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_dict(self) -> dict[str, Any]: return asdict(self)
