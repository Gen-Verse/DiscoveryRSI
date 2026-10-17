from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from .core import Candidate, DiscoveryLoop, ReplayBuffer
from .manifest import ResearchManifest
from .plugin import load_roles
from .providers import ModelAdapter
from .tools import ToolRegistry, default_registry

@dataclass
class ResearchHarness:
    """Runnable propose/critique/select harness with manifest, roles and tools."""
    adapter: ModelAdapter
    iterations: int = 2
    replay_path: str = "episodes.jsonl"
    manifest: ResearchManifest | None = None
    roles_dir: str | None = None
    tools: ToolRegistry = field(default_factory=default_registry)

    def _context(self) -> str:
        m=self.manifest
        if not m: return ""
        roles=load_roles(self.roles_dir) if self.roles_dir else {}
        role_text="; ".join(f"{k}: {v.instructions[:240]}" for k,v in roles.items())
        return (f" Research manifest: {json.dumps(m.to_dict(), ensure_ascii=False)}."
                f" Available tools: {json.dumps(self.tools.describe(), ensure_ascii=False)}."
                f" Role instructions: {role_text or 'use the manifest roles'}.")

    def _candidates(self, number: int, history: list[Candidate]):
        parent=history[-1].id if history else "none"
        question=(self.manifest.question if self.manifest else "Generate falsifiable research hypotheses.")
        limit=self.manifest.max_candidates if self.manifest else 2
        prompt=("You are the DiscoveryRSI research lead. Return JSON with a list named candidates. "
                "Each candidate must contain claim, plan, alternatives (list), evidence (list). "
                f"Research question: {question}. Episode {number}; parent={parent}. "
                f"Generate at most {limit} falsifiable research hypotheses."+self._context())
        raw=self.adapter.complete(prompt)
        try:data=json.loads(raw);items=data["candidates"]
        except Exception:items=[{"claim":raw[:400],"plan":"Define a comparator, measurement and falsification criterion.","alternatives":[],"evidence":[]}]
        return [Candidate(f"episode-{number}-{i+1}",x.get("claim",""),x.get("plan",""),x.get("alternatives",[]),x.get("evidence",[]),[parent] if parent!="none" else []) for i,x in enumerate(items[:limit])]

    def _critique(self, candidate: Candidate):
        prompt=("You are a scientific critic. Score this proposal from 0 to 10 and return JSON "
                "with score and critique. Require a concrete comparator, measurable outcome, "
                "alternative explanation, and falsification rule.\n"+json.dumps({"claim":candidate.claim,"plan":candidate.plan,"alternatives":candidate.alternatives})+self._context())
        raw=self.adapter.complete(prompt)
        try:data=json.loads(raw);return float(data.get("score",0)),str(data.get("critique",raw))
        except Exception:return 0.0,raw[:500]

    def run(self):
        loop=DiscoveryLoop(lambda n,h:self._candidates(n,list(h)),self._critique,self.iterations,ReplayBuffer(self.replay_path))
        return loop.run()
