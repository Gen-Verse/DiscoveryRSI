from __future__ import annotations
import argparse,json,os
from .core import Candidate, DiscoveryLoop, ReplayBuffer
from .harness import ResearchHarness
from .manifest import ResearchManifest
from .providers import adapter_from_env
from .go_domains import GOPathwayAdapter, GOTargetPrioritizationAdapter

def local_demo(iterations):
    def proposer(n,history): return [Candidate(f"episode-{n}-a","Test whether a signal adds information beyond a baseline.","Compare signal and baseline with uncertainty.",["Measurement artifact"]),Candidate(f"episode-{n}-b","Test whether the signal changes across a prespecified subgroup.","Use held-out subgroup and falsification control.",["Selection bias"])]
    def critic(c): return (2.5 if "baseline" in c.plan else 1.0,"Comparator and alternative recorded.")
    return DiscoveryLoop(proposer,critic,iterations,ReplayBuffer(".discovery-rsi/demo.jsonl")).run()

def _domain_demo(kind, path):
    payload=json.loads(open(path, encoding="utf-8").read())
    if kind == "geo-pathway": adapter=GOPathwayAdapter.from_records(payload.get("pathways", []), payload.get("background_genes", []))
    else: adapter=GOTargetPrioritizationAdapter.from_records(payload.get("targets", []), payload.get("prioritized_terms", []))
    return [c.__dict__ for c in adapter.candidates()]

def main():
    p=argparse.ArgumentParser(prog="discovery-rsi");sub=p.add_subparsers(dest="command")
    d=sub.add_parser("demo");d.add_argument("--iterations",type=int,default=2)
    c=sub.add_parser("campaign");c.add_argument("--adapter",choices=["openai-compatible","codex","claude","claude-code","cloud-code"],default="openai-compatible");c.add_argument("--iterations",type=int,default=2);c.add_argument("--replay",default="episodes.jsonl");c.add_argument("--manifest",default=None);c.add_argument("--roles",default="plugins/discovery-rsi/roles")
    g=sub.add_parser("domain-demo", help="Generate candidates from a public domain input file");g.add_argument("--domain", choices=["geo-pathway", "geo-target-prioritization"], required=True);g.add_argument("--input", required=True, help="JSON file containing user-supplied GEO records")
    args=p.parse_args()
    if args.command=="demo" or args.command is None:
        eps=local_demo(args.iterations); print(json.dumps({"episodes":[{"number":e.number,"selected_id":e.selected_id,"status":e.status} for e in eps]},indent=2))
    elif args.command=="campaign":
        manifest=ResearchManifest.load(args.manifest) if args.manifest else None
        eps=ResearchHarness(adapter_from_env(args.adapter),args.iterations,args.replay,manifest,args.roles).run(); print(json.dumps({"episodes":[{"number":e.number,"selected_id":e.selected_id,"status":e.status} for e in eps]},indent=2))
    else: print(json.dumps({"domain":args.domain,"candidates":_domain_demo(args.domain,args.input)},indent=2))
