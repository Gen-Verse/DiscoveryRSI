"""Fixed-script candidate/history snapshot tests; never invoke model providers."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from discovery_rsi.core import Candidate, DiscoveryLoop, ReplayBuffer


class ReplaySnapshotTests(unittest.TestCase):
    def test_episodes_keep_their_original_critique_when_candidate_reused(self):
        reused = Candidate("a", "claim", "plan")
        calls = iter((1.0, 2.0))
        loop = DiscoveryLoop(lambda n, h: [reused], lambda c: (next(calls), "scored"), iterations=2)
        episodes = loop.run()
        self.assertEqual([e.candidates[0].score for e in episodes], [1.0, 2.0])

    def test_replay_and_returned_episodes_agree(self):
        reused = Candidate("a", "claim", "plan")
        calls = iter((1.0, 2.0))
        with TemporaryDirectory() as folder:
            replay = ReplayBuffer(Path(folder) / "trace.jsonl")
            episodes = DiscoveryLoop(lambda n, h: [reused],
                                     lambda c: (next(calls), "scored"), 2, replay).run()
            self.assertEqual(
                [e.candidates[0].score for e in episodes],
                [record["candidates"][0]["score"] for record in replay.read()],
            )

    def test_proposer_owned_candidate_is_not_mutated_by_scoring(self):
        reused = Candidate("a", "claim", "plan")
        DiscoveryLoop(lambda n, h: [reused], lambda c: (2.0, "scored")).run()
        self.assertEqual((reused.score, reused.critique), (0.0, ""))

    def test_fresh_candidate_baseline(self):
        episodes = DiscoveryLoop(lambda n, h: [Candidate("a", "claim", "plan")],
                                 lambda c: (1.0, "ok")).run()
        self.assertEqual((len(episodes), episodes[0].selected_id), (1, "a"))


if __name__ == "__main__":
    unittest.main()
