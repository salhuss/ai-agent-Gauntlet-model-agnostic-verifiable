from __future__ import annotations
from typing import Tuple
import re, os, math

class ToolError(Exception): ...

def calc(expr: str) -> str:
    # safe eval: numbers + operators only
    if not re.match(r"^[\d\.\s\+\-\*\/\(\)]+$", expr):
        raise ToolError("Unsafe expression")
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        raise ToolError(str(e))

def read(path: str, max_bytes: int = 20000) -> str:
    if not os.path.exists(path): raise ToolError("File not found")
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read(max_bytes)

def write(path: str, text: str) -> str:
    d = os.path.dirname(path) or "."
    os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return f"Wrote {len(text)} bytes to {path}"

def grep(pattern: str, path: str, ignore_case: bool = True) -> str:
    flags = re.I if ignore_case else 0
    txt = read(path)
    hits = [line for line in txt.splitlines() if re.search(pattern, line, flags)]
    return "\n".join(hits[:200])
