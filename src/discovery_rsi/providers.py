from __future__ import annotations
import json, os, subprocess
from dataclasses import dataclass
from typing import Protocol, Sequence
from urllib.request import Request, urlopen

class ModelAdapter(Protocol):
    def complete(self, prompt: str) -> str: ...

@dataclass
class OpenAICompatibleAdapter:
    base_url: str
    model: str
    api_key: str
    timeout: float = 120.0

    @classmethod
    def from_env(cls) -> "OpenAICompatibleAdapter":
        key=os.environ.get("DISCOVERY_RSI_API_KEY")
        if not key: raise RuntimeError("Set DISCOVERY_RSI_API_KEY")
        return cls(os.environ.get("DISCOVERY_RSI_BASE_URL","https://api.openai.com/v1"), os.environ.get("DISCOVERY_RSI_MODEL","gpt-4o-mini"), key)

    def complete(self, prompt: str) -> str:
        url=self.base_url.rstrip("/")+"/chat/completions"
        body=json.dumps({"model":self.model,"messages":[{"role":"user","content":prompt}],"temperature":0.2}).encode()
        req=Request(url, data=body, headers={"Authorization":"Bearer "+self.api_key,"Content-Type":"application/json"})
        with urlopen(req, timeout=self.timeout) as response:
            data=json.loads(response.read())
        return data["choices"][0]["message"]["content"]

@dataclass
class CommandAdapter:
    """Adapter for a locally installed Codex or Claude command. {prompt} is substituted safely."""
    command: Sequence[str]
    timeout: float = 300.0
    def complete(self, prompt: str) -> str:
        argv=[part.replace("{prompt}",prompt) for part in self.command]
        result=subprocess.run(argv, text=True, capture_output=True, timeout=self.timeout, check=True)
        return result.stdout.strip()

def adapter_from_env(kind: str) -> ModelAdapter:
    if kind == "openai-compatible": return OpenAICompatibleAdapter.from_env()
    if kind == "codex": return CommandAdapter([os.environ.get("DISCOVERY_RSI_CODEX","codex"), "{prompt}"])
    if kind == "claude": return CommandAdapter([os.environ.get("DISCOVERY_RSI_CLAUDE","claude"), "{prompt}"])
    raise ValueError(f"Unsupported adapter: {kind}")
