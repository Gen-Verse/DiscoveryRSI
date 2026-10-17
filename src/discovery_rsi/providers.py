from __future__ import annotations
import json, os, shutil, subprocess
from dataclasses import dataclass
from typing import Protocol, Sequence
from urllib.request import Request, urlopen

class ModelAdapter(Protocol):
    def complete(self, prompt: str) -> str: ...

@dataclass
class OpenAICompatibleAdapter:
    base_url: str; model: str; api_key: str; timeout: float = 120.0
    @classmethod
    def from_env(cls):
        key=os.environ.get("DISCOVERY_RSI_API_KEY")
        if not key: raise RuntimeError("Set DISCOVERY_RSI_API_KEY")
        return cls(os.environ.get("DISCOVERY_RSI_BASE_URL","https://api.openai.com/v1"), os.environ.get("DISCOVERY_RSI_MODEL","gpt-4o-mini"), key)
    def complete(self, prompt: str) -> str:
        body=json.dumps({"model":self.model,"messages":[{"role":"user","content":prompt}],"temperature":0.2}).encode()
        req=Request(self.base_url.rstrip("/")+"/chat/completions", data=body, headers={"Authorization":"Bearer "+self.api_key,"Content-Type":"application/json"})
        with urlopen(req, timeout=self.timeout) as response: return json.loads(response.read())["choices"][0]["message"]["content"]

@dataclass
class CommandAdapter:
    command: Sequence[str]; timeout: float = 300.0
    def complete(self, prompt: str) -> str:
        result=subprocess.run([part.replace("{prompt}",prompt) for part in self.command], text=True, capture_output=True, timeout=self.timeout, check=True)
        return result.stdout.strip()

def _stream_text(stdout: str) -> str:
    plain=[]; structured=[]
    for line in stdout.splitlines():
        line=line.strip()
        if not line: continue
        try: event=json.loads(line)
        except json.JSONDecodeError: plain.append(line); continue
        if isinstance(event, dict):
            for key in ("result", "final", "output", "text"):
                if isinstance(event.get(key), str) and event[key].strip(): structured.append(event[key].strip())
            message=event.get("message")
            if isinstance(message, dict):
                content=message.get("content")
                if isinstance(content, str): structured.append(content.strip())
                elif isinstance(content, list):
                    structured.extend(block["text"].strip() for block in content if isinstance(block,dict) and isinstance(block.get("text"),str))
    return (structured[-1] if structured else "\n".join(plain)).strip()

@dataclass
class ClaudeCodeAdapter:
    executable: str = "claude"; model: str | None = None; plugin_dir: str | None = None; agent: str = "lead"; base_url: str | None = None; auth_env: str = "ANTHROPIC_AUTH_TOKEN"; timeout: float = 900.0
    def complete(self, prompt: str) -> str:
        if not shutil.which(self.executable) and not os.path.isfile(self.executable): raise RuntimeError(f"Claude Code executable not found: {self.executable}")
        token=os.environ.get(self.auth_env)
        if not token: raise RuntimeError(f"Set {self.auth_env} for Claude Code")
        command=[self.executable,"--print","--input-format","stream-json","--output-format","stream-json","--verbose","--permission-prompts","none","--permission-mode","dontAsk","--no-session-persistence","--restricted"]
        if self.plugin_dir: command += ["--plugin-dir",self.plugin_dir]
        if self.agent: command += ["--agent",self.agent]
        if self.model: command += ["--model",self.model]
        env={"PATH":os.environ.get("PATH",""),"LANG":os.environ.get("LANG","C.UTF-8"),self.auth_env:token,"CLAUDE_CODE_DISABLE_AUTO_MEMORY":"1","CLAUDE_CODE_SKIP_PROMPT_HISTORY":"1"}
        if self.base_url: env["ANTHROPIC_BASE_URL"]=self.base_url
        request=json.dumps({"type":"user","session_id":"","message":{"role":"user","content":prompt}})+"\n"
        result=subprocess.run(command,input=request,text=True,capture_output=True,timeout=self.timeout,check=True,env=env)
        text=_stream_text(result.stdout)
        if not text: raise RuntimeError("Claude Code returned no text")
        return text

@dataclass
class CodexAdapter:
    executable: str = "codex"; model: str | None = None; timeout: float = 900.0; sandbox: str = "read-only"
    def complete(self, prompt: str) -> str:
        if not shutil.which(self.executable) and not os.path.isfile(self.executable): raise RuntimeError(f"Codex executable not found: {self.executable}")
        command=[self.executable,"exec","--json","--ephemeral","--sandbox",self.sandbox,"-"]
        if self.model: command[3:3]=["--model",self.model]
        result=subprocess.run(command,input=prompt,text=True,capture_output=True,timeout=self.timeout,check=True)
        text=_stream_text(result.stdout)
        if not text: raise RuntimeError("Codex returned no text")
        return text

def adapter_from_env(kind: str) -> ModelAdapter:
    if kind == "openai-compatible": return OpenAICompatibleAdapter.from_env()
    if kind == "codex": return CodexAdapter(model=os.environ.get("DISCOVERY_RSI_CODEX_MODEL"))
    if kind in {"claude", "claude-code", "cloud-code"}:
        return ClaudeCodeAdapter(executable=os.environ.get("DISCOVERY_RSI_CLAUDE","claude"), model=os.environ.get("DISCOVERY_RSI_CLAUDE_MODEL"), plugin_dir=os.environ.get("DISCOVERY_RSI_PLUGIN_DIR"), agent=os.environ.get("DISCOVERY_RSI_CLAUDE_AGENT","lead"), base_url=os.environ.get("DISCOVERY_RSI_ANTHROPIC_BASE_URL"), auth_env=os.environ.get("DISCOVERY_RSI_CLAUDE_AUTH_ENV","ANTHROPIC_AUTH_TOKEN"))
    raise ValueError(f"Unsupported adapter: {kind}")
