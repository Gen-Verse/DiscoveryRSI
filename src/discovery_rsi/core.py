from __future__ import annotations
from copy import deepcopy
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Callable, Iterable, Sequence

@dataclass
class Candidate:
    """A versioned research hypothesis and its investigation plan."""
    id: str
    claim: str
    plan: str
    alternatives: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    parents: list[str] = field(default_factory=list)
    score: float = 0.0
    critique: str = ""

@dataclass
class Episode:
    """One bounded propose--critique--select--retain interaction."""
    number: int
    candidates: list[Candidate]
    selected_id: str | None
    status: str = "completed"

class ReplayBuffer:
    """Append-only JSON replay store for reproducible local experiments."""
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, episode: Episode) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(episode), ensure_ascii=False) + "\n")

    def read(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]

class DiscoveryLoop:
    """Model-agnostic DiscoveryRSI loop. Adapters supply proposal and critique functions."""
    def __init__(self, proposer: Callable[[int, Sequence[Candidate]], Iterable[Candidate]],
                 critic: Callable[[Candidate], tuple[float, str]],
                 iterations: int = 1, replay: ReplayBuffer | None = None):
        if iterations < 1:
            raise ValueError("iterations must be positive")
        self.proposer, self.critic, self.iterations, self.replay = proposer, critic, iterations, replay
        self.history: list[Candidate] = []

    def run(self) -> list[Episode]:
        episodes=[]
        for number in range(1, self.iterations + 1):
            # Keep episode records stable even if a proposer reuses or returns
            # a history-owned Candidate: critic annotations must not mutate
            # earlier episodes, replay snapshots, or proposer-owned objects.
            candidates=[deepcopy(c) for c in self.proposer(number, tuple(self.history))]
            if not candidates:
                episodes.append(Episode(number, [], None, "no_candidates")); continue
            for candidate in candidates:
                candidate.score, candidate.critique = self.critic(candidate)
            selected=max(candidates, key=lambda c: (c.score, c.id))
            self.history.append(selected)
            episode=Episode(number, candidates, selected.id)
            episodes.append(episode)
            if self.replay:
                self.replay.append(episode)
        return episodes
