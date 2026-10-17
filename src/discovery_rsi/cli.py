from __future__ import annotations
import argparse,json,os
from .core import Candidate, DiscoveryLoop, ReplayBuffer
from .harness import ResearchHarness
from .providers import adapter_from_env

def local_demo(iterations):
    def proposer(n,history): return [Candidate(f"episode-{n}-a","Test whether a signal adds information beyond a baseline.","Compare signal and baseline with uncertainty.",["Measurement artifact"]),Candidate(f"episode-{n}-b","Test whether the signal changes across a prespecified subgroup.","Use held-out subgroup and falsification control.",["Selection bias"])]
    def critic(c): return (2.5 if "baseline" in c.plan else 1.0,"Comparator and alternative recorded.")
    return DiscoveryLoop(proposer,critic,iterations,ReplayBuffer(".discovery-rsi/demo.jsonl")).run()

def main():
    p=argparse.ArgumentParser(prog="discovery-rsi");sub=p.add_subparsers(dest="command")
    d=sub.add_parser("demo");d.add_argument("--iterations",type=int,default=2)
    c=sub.add_parser("campaign");c.add_argument("--adapter",choices=["openai-compatible","codex","claude"],default="openai-compatible");c.add_argument("--iterations",type=int,default=2);c.add_argument("--replay",default="episodes.jsonl")
    args=p.parse_args()
    if args.command=="demo" or args.command is None:
        eps=local_demo(args.iterations)
    else:
        eps=ResearchHarness(adapter_from_env(args.adapter),args.iterations,args.replay).run()
    print(json.dumps({"episodes":[{"number":e.number,"selected_id":e.selected_id,"status":e.status} for e in eps]},indent=2))
