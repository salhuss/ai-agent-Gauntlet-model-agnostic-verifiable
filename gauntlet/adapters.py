from __future__ import annotations
import os, requests
from typing import Optional, Protocol, List, Dict

class LLM(Protocol):
    def generate(self, messages: List[Dict]) -> str: ...

def _req(env: str) -> str:
    v = os.getenv(env)
    if not v:
        raise RuntimeError(f"Missing env var: {env}")
    return v

class OpenAIAdapter:
    def __init__(self, model: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI(api_key=_req("OPENAI_API_KEY"))
        self.model = model
    def generate(self, messages):
        r = self.client.chat.completions.create(model=self.model, messages=messages, temperature=0.2)
        return r.choices[0].message.content.strip()

class HFAdapter:
    def __init__(self, model: str, endpoint: Optional[str] = None):
        self.model = model
        self.endpoint = endpoint or f"https://api-inference.huggingface.co/models/{model}"
        self.headers = {"Authorization": f"Bearer {os.getenv('HF_API_TOKEN','')}".strip()}
    def generate(self, messages):
        # simple: concat system+user
        text = "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)
        r = requests.post(self.endpoint, headers=self.headers, json={"inputs": text, "parameters":{"max_new_tokens":256,"temperature":0.2}})
        r.raise_for_status()
        j = r.json()
        if isinstance(j, list) and j and "generated_text" in j[0]: return j[0]["generated_text"]
        if isinstance(j, dict) and "generated_text" in j: return j["generated_text"]
        return str(j)

class HTTPAdapter:
    """Custom endpoint expecting: POST {messages:[{role,content}]} -> {text:str}"""
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
    def generate(self, messages):
        r = requests.post(self.endpoint, json={"messages": messages})
        r.raise_for_status()
        return r.json().get("text","")
