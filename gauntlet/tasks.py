from __future__ import annotations
from typing import Dict, Callable
import os, json

Task = Dict[str, str]

def task_sum_file() -> Task:
    # writes an input file; agent must read & compute sum
    os.makedirs("workspace", exist_ok=True)
    with open("workspace/numbers.txt","w") as f:
        f.write("42\n13\n5\n")
    return {
        "name": "sum_file",
        "prompt": "Compute the sum of integers in workspace/numbers.txt and write the answer into workspace/answer.txt as a single number.",
        "check_path": "workspace/answer.txt",
        "checker": "sum_file_checker",
    }

def sum_file_checker(_: Task) -> Dict:
    try:
        with open("workspace/answer.txt") as f:
            val = f.read().strip()
        ok = val == "60"
        return {"passed": ok, "expect": "60", "got": val}
    except Exception as e:
        return {"passed": False, "error": str(e)}

TASKS = {
    "sum_file": (task_sum_file, sum_file_checker),
}
