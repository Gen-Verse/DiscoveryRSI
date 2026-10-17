"""Portable role/plugin loading; plugins are declarative Markdown files."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Role:
    name: str
    instructions: str

def load_roles(directory: str | Path) -> dict[str, Role]:
    root=Path(directory); roles={}
    if not root.exists(): return roles
    for path in sorted(root.glob("*.md")):
        roles[path.stem]=Role(path.stem, path.read_text(encoding="utf-8"))
    return roles
