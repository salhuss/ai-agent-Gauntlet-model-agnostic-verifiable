# ai-agent-Gauntlet-model-agnostic-verifiable
A tiny, verifiable, model-agnostic agent that plans with a constrained mini-DSL, executes tools under a budget, and produces a scorecard per task. Think “agent research harness” more than a chatbot toy.

agent-gauntlet/
  README.md
  requirements.txt
  gauntlet/
    __init__.py
    adapters.py       # model-agnostic providers
    dsl.py            # plan DSL schema + parser
    tools.py          # calculator, file io, regex search
    agent.py          # plan -> execute loop with budget
    tasks.py          # tasks + verifiers
    run.py            # CLI entry
