from discovery_rsi.core import Candidate, DiscoveryLoop, ReplayBuffer

def test_loop_selects_and_replays(tmp_path):
    def proposer(n, history): return [Candidate("a", "claim", "baseline plan"), Candidate("b", "claim", "plan")]
    def critic(c): return (1.0 if c.id == "a" else 0.0, "ok")
    replay=ReplayBuffer(tmp_path / "episodes.jsonl")
    episodes=DiscoveryLoop(proposer, critic, 2, replay).run()
    assert [e.selected_id for e in episodes] == ["a", "a"]
    assert len(replay.read()) == 2
