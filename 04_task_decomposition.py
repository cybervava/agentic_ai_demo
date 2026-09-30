"""Demo 4: Plan tasks, execute each with the agent, and synthesize a report."""
import importlib.util
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

module_path = Path(__file__).resolve().parent / "03_autonomous_agent.py"
spec = importlib.util.spec_from_file_location("autonomous_agent", module_path)
agent_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent_module)
run_agent = agent_module.run_agent

load_dotenv()
client = OpenAI()
MODEL = "gpt-5-mini"


def create_plan(user_request):
    response = client.responses.create(
        model=MODEL,
        instructions=("You are an IT operations planning agent. Break the "
                      "request into 2 to 4 actionable investigation tasks, "
                      "each with a clear objective. Order tasks logically "
                      "and do not invent incident evidence."),
        input=user_request,
        text={"format": {"type": "json_schema", "name": "investigation_plan",
                         "strict": True,
                         "schema": {"type": "object", "properties": {
                             "tasks": {"type": "array", "items": {"type": "string"}}},
                             "required": ["tasks"], "additionalProperties": False}}},
    )
    tasks = json.loads(response.output_text)["tasks"][:4]
    if not tasks:
        raise ValueError("The planner returned no tasks.")
    return tasks


def execute_plan(tasks):
    results = []
    previous_findings = []
    for index, task in enumerate(tasks, start=1):
        print(f"\n{'=' * 60}\nEXECUTING TASK {index}\n{'=' * 60}\n{task}")
        context = "\n\n".join(previous_findings) or "None"
        task_request = (f"Current task: {task}\n\nFindings from previous tasks: "
                        f"{context}\n\nInvestigate payment-service. Use diagnostic "
                        "tools as needed. Summarize evidence and uncertainty.")
        result = run_agent(task_request, max_iterations=6)
        results.append({"task": task, "result": result})
        previous_findings.append(f"Task: {task}\nResult: {result}")
    return results


def generate_report(user_request, results):
    response = client.responses.create(
        model=MODEL,
        instructions=("You are an IT incident reporting specialist. Use only "
                      "supplied findings. Include executive summary, key "
                      "observations, likely root cause, supporting evidence, "
                      "uncertainty and recommended actions. Distinguish "
                      "observations from hypotheses."),
        input=(f"Original request:\n{user_request}\n\nInvestigation results:\n"
               f"{json.dumps(results, indent=2)}"),
    )
    return response.output_text


if __name__ == "__main__":
    request = ("Investigate why payment-service is slow. Identify the most "
               "likely root cause, examine whether a recent deployment may "
               "have contributed, and prepare a management report with "
               "recommended actions.")
    print("\nCREATING EXECUTION PLAN")
    tasks = create_plan(request)
    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task}")
    results = execute_plan(tasks)
    print("\n" + "=" * 60 + "\nFINAL INCIDENT REPORT\n" + "=" * 60)
    print(generate_report(request, results))
