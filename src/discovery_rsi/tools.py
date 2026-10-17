"""Small, explicit tool registry for public DiscoveryRSI campaigns."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]

class ToolRegistry:
    def __init__(self, tools: list[Tool] | None = None): self._tools={t.name:t for t in (tools or [])}
    def register(self, tool: Tool) -> None:
        if tool.name in self._tools: raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name]=tool
    def names(self) -> tuple[str, ...]: return tuple(sorted(self._tools))
    def describe(self) -> list[dict[str, str]]: return [{"name":t.name,"description":t.description} for t in self._tools.values()]
    def call(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools: raise KeyError(f"unknown tool: {name}")
        return self._tools[name].handler(**kwargs)

def default_registry() -> ToolRegistry:
    r=ToolRegistry()
    r.register(Tool("record_evidence", "Attach a source-backed observation to a candidate.", lambda candidate, evidence: {"candidate":candidate,"evidence":list(evidence)}))
    r.register(Tool("compare", "Describe a prespecified comparator and outcome.", lambda comparator, outcome: {"comparator":comparator,"outcome":outcome}))
    r.register(Tool("falsify", "Record the condition that would count against a claim.", lambda criterion: {"falsification":criterion}))
    return r
