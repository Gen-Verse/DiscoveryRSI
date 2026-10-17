from __future__ import annotations
import argparse, json
from .core import Candidate, DiscoveryLoop, ReplayBuffer

def demo(iterations: int) -> dict:
    def proposer(number, history):
        parent=[history[-1].id] if history else []
        return [Candidate(f"episode-{number}-a", "Measure whether the proposed signal adds information beyond a baseline.", "Compare a prespecified signal with a baseline and report uncertainty.", ["The signal is a measurement artifact."], parents=parent), Candidate(f"episode-{number}-b", "Test whether the proposed signal changes across a relevant subgroup.", "Use a held-out subgroup and a falsification control.", ["The association reflects selection."], parents=parent)]
    def critic(candidate):
        score=2.0 + (0.5 if "baseline" in candidate.plan else 0.0) + (0.25 if candidate.alternatives else 0.0)
        return score, "Includes a comparator and an explicit alternative."
    episodes=DiscoveryLoop(proposer, critic, iterations, ReplayBuffer(".discovery-rsi/demo.jsonl")).run()
    return {"episodes": [{"number":e.number,"selected_id":e.selected_id,"status":e.status} for e in episodes]}

def main():
    parser=argparse.ArgumentParser(description="Run the public DiscoveryRSI local demo")
    parser.add_argument("--iterations", type=int, default=2)
    args=parser.parse_args(); print(json.dumps(demo(args.iterations), indent=2))

if __name__ == "__main__": main()
