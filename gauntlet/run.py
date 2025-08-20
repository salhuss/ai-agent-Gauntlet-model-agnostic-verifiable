import typer, json
from pathlib import Path
from .adapters import OpenAIAdapter, HFAdapter, HTTPAdapter
from .agent import plan, execute
from .tasks import TASKS

app = typer.Typer(help="Agent Gauntlet")

def get_adapter(provider: str, model: str, endpoint: str|None):
    if provider == "openai": return OpenAIAdapter(model)
    if provider == "hf": return HFAdapter(model, endpoint)
    if provider == "http":
        assert endpoint, "--endpoint required for provider=http"
        return HTTPAdapter(endpoint)
    raise typer.BadParameter("provider must be openai|hf|http")

@app.command()
def run(
    task: str = typer.Option("sum_file", help=f"One of: {', '.join(TASKS.keys())}"),
    provider: str = typer.Option("openai"),
    model: str = typer.Option("gpt-4o-mini"),
    endpoint: str = typer.Option(None),
    budget_steps: int = typer.Option(5),
    out: str = typer.Option("out"),
):
    out_p = Path(out); out_p.mkdir(parents=True, exist_ok=True)

    mk_task, checker = TASKS[task]
    spec = mk_task()
    llm = get_adapter(provider, model, endpoint)

    # plan
    p = plan(llm, spec["prompt"])
    # execute
    result = execute(p, budget_steps=budget_steps)
    # check
    if isinstance(checker, str):
        from .tasks import sum_file_checker as fn
    else:
        fn = checker
    verdict = fn(spec)

    report = {"task": task, "plan": p.dict(), "exec": result, "verdict": verdict}
    (out_p / f"{task}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    typer.echo(f"✅ {task}: {'PASS' if verdict.get('passed') else 'FAIL'}  — wrote {out}/{task}.json")

if __name__ == "__main__":
    app()
