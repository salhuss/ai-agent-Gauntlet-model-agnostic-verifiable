from __future__ import annotations
from typing import Dict, List
from .dsl import extract_plan, Plan
from .tools import calc, read, write, grep, ToolError

TOOL_REGISTRY = {
    "calc": lambda args: calc(args.get("expr","")),
    "read": lambda args: read(args.get("path","")),
    "write": lambda args: write(args.get("path",""), args.get("text","")),
    "grep": lambda args: grep(args.get("pattern",""), args.get("path",""), args.get("ignore_case", True)),
}

SYS = (
"You're an agent that must propose a plan in a strict DSL to solve the user's task.\n"
"Only use tools from {tools}. Keep the plan minimal; each step costs budget.\n"
"Return your plan inside:\n"
"PLAN:\n"
"- tool: <name>\n"
"  args: {key: value}\n"
"...\n"
"END\n"
)

def plan(llm, user_task: str) -> Plan:
    messages = [
        {"role":"system","content": SYS.format(tools=list(TOOL_REGISTRY.keys()))},
        {"role":"user","content": user_task},
    ]
    txt = llm.generate(messages)
    return extract_plan(txt)

def execute(plan: Plan, budget_steps: int = 6) -> Dict:
    log: List[Dict] = []
    remaining = budget_steps
    for i, step in enumerate(plan.steps, 1):
        if remaining <= 0:
            log.append({"step": i, "tool": step.tool, "error": "budget_exhausted"})
            break
        fn = TOOL_REGISTRY.get(step.tool)
        if not fn:
            log.append({"step": i, "tool": step.tool, "error": "unknown_tool"})
            continue
        try:
            out = fn(step.args)
            log.append({"step": i, "tool": step.tool, "args": step.args, "output": out})
        except ToolError as e:
            log.append({"step": i, "tool": step.tool, "args": step.args, "error": str(e)})
        remaining -= 1
    return {"log": log, "used_steps": budget_steps - remaining}
