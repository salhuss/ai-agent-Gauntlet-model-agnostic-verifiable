from __future__ import annotations
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ValidationError

# Constrained plan DSL (YAML/JSON-like but we parse from a fenced block)
# Example:
# PLAN:
# - tool: search
#   args: {pattern: "total", path: "report.txt"}
# - tool: calc
#   args: {expr: "(42*3)+5"}
# - tool: write
#   args: {path: "answer.txt", text: "The result is 131."}
# END

class Step(BaseModel):
    tool: Literal["calc","read","write","grep"] = Field(...)
    args: dict = Field(default_factory=dict)
    comment: Optional[str] = None

class Plan(BaseModel):
    steps: List[Step]

def extract_plan(text: str) -> Plan:
    import re, yaml
    m = re.search(r"PLAN:\s*(.*?)\s*END", text, flags=re.S|re.I)
    if not m:
        raise ValueError("No PLAN block found")
    block = m.group(1)
    # attempt YAML list parse
    try:
        data = yaml.safe_load(block)
        if isinstance(data, dict) and "steps" in data:
            data = data["steps"]
        return Plan(steps=[Step(**s) for s in data])
    except Exception as e:
        raise ValueError(f"Bad plan YAML: {e}")
