# Agent Gauntlet — Constrained, Verifiable, Model-Agnostic Agent

An agent that **plans with a strict mini-DSL**, executes **sandboxed tools** under a **budget**, and produces **verifiable scorecards** per task.

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

Run (examples)

# OpenAI
export OPENAI_API_KEY=sk-...
python -m gauntlet.run run --task sum_file --provider openai --model gpt-4o-mini

# Hugging Face Inference
export HF_API_TOKEN=hf_...
python -m gauntlet.run run --task sum_file --provider hf --model mistralai/Mixtral-8x7B-Instruct-v0.1

Plan DSL

Return plans inside a fenced block:
PLAN:
- tool: read
  args: {path: "workspace/numbers.txt"}
- tool: calc
  args: {expr: "42+13+5"}
- tool: write
  args: {path: "workspace/answer.txt", text: "60"}
END


Tasks
	•	sum_file: agent must read a file, compute a sum, and write the answer.
More tasks easy to add in tasks.py with a checker.

---

## How to extend (fast ideas)
- Add tools: `http_get`, `json_select`, `csv_sum`, `shell` (sandboxed).
- Add **cost-aware budget**: track estimated tokens/req.
- Add tasks with **multi-step constraints** and **partial credit**.
- Log **trajectory JSONL** for research.



