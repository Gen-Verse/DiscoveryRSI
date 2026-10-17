from __future__ import annotations
import json
from dataclasses import dataclass
from .core import Candidate, DiscoveryLoop, Episode, ReplayBuffer
from .providers import ModelAdapter

@dataclass
class ResearchHarness:
    adapter: ModelAdapter
    iterations: int = 2
    replay_path: str = "episodes.jsonl"

    def _candidates(self, number: int, history: list[Candidate]):
        parent=history[-1].id if history else "none"
        prompt=("You are the DiscoveryRSI research lead. Return JSON with a list named candidates. "
                "Each candidate must contain claim, plan, alternatives (list), evidence (list). "
                f"Episode {number}; parent={parent}. Generate two falsifiable research hypotheses.")
        raw=self.adapter.complete(prompt)
        try:data=json.loads(raw);items=data["candidates"]
        except Exception:items=[{"claim":raw[:400],"plan":"Define a comparator, measurement and falsification criterion.","alternatives":[],"evidence":[]}]
        return [Candidate(f"episode-{number}-{i+1}",x.get("claim",""),x.get("plan",""),x.get("alternatives",[]),x.get("evidence",[]),[parent] if parent!="none" else []) for i,x in enumerate(items)]

    def _critique(self, candidate: Candidate):
        prompt=("You are a scientific critic. Score this proposal from 0 to 10 and return JSON "
                "with score and critique. Require a concrete comparator, measurable outcome, "
                "alternative explanation, and falsification rule.\n"+json.dumps({"claim":candidate.claim,"plan":candidate.plan,"alternatives":candidate.alternatives}))
        raw=self.adapter.complete(prompt)
        try:data=json.loads(raw);return float(data.get("score",0)),str(data.get("critique",raw))
        except Exception:return 0.0,raw[:500]

    def run(self):
        loop=DiscoveryLoop(lambda n,h:self._candidates(n,list(h)),self._critique,self.iterations,ReplayBuffer(self.replay_path))
        return loop.run()
