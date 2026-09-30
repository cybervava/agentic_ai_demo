"""Demo 3: An iterative plan-act-observe agent with a tool-call budget."""
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import execute_tool

load_dotenv()
client = OpenAI()
MODEL = "gpt-5-mini"
TOOL_DESCRIPTIONS = {
    "get_system_metrics": "Retrieve CPU, memory, latency and error metrics.",
    "get_database_status": "Inspect database connections and slow queries.",
    "get_application_logs": "Retrieve recent application errors and warnings.",
    "get_recent_deployments": "Retrieve recent deployments and software changes.",
}
TOOLS = [{
    "type": "function", "name": name, "description": description,
    "parameters": {"type": "object", "properties": {
        "service": {"type": "string", "description": "Application service name"}},
        "required": ["service"], "additionalProperties": False},
    "strict": True,
} for name, description in TOOL_DESCRIPTIONS.items()]

SYSTEM_INSTRUCTIONS = """You are an autonomous IT incident investigation agent.
Use diagnostic tools to investigate incidents. Begin with relevant system
measurements, choose later tools based on observed evidence, and distinguish
confirmed facts from hypotheses. Do not invent measurements or claim causation
without sufficient evidence. Do not modify infrastructure or restart services.
When finished, report the incident summary, evidence, most likely root cause,
remaining uncertainty and recommended next actions."""


def run_agent(user_request, max_iterations=8):
    history = [{"role": "user", "content": user_request}]
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'=' * 50}\nAGENT ITERATION {iteration}\n{'=' * 50}")
        response = client.responses.create(
            model=MODEL, instructions=SYSTEM_INSTRUCTIONS, input=history,
            tools=TOOLS, tool_choice="auto", parallel_tool_calls=False,
        )
        history.extend(response.output)
        tool_calls = [item for item in response.output
                      if item.type == "function_call"]
        if not tool_calls:
            print("\nAGENT FINAL REPORT\n", response.output_text)
            return response.output_text
        for call in tool_calls:
            print(f"\nSelected tool: {call.name}\nArguments: {call.arguments}")
            try:
                result = execute_tool(call.name, json.loads(call.arguments))
            except (ValueError, TypeError) as error:
                result = json.dumps({"error": str(error)})
            print("\nObservation:\n", result)
            history.append({"type": "function_call_output",
                            "call_id": call.call_id, "output": result})
    print("\nMaximum iterations reached.")
    response = client.responses.create(
        model=MODEL,
        instructions=(SYSTEM_INSTRUCTIONS +
                      "\nExecution limit reached. Summarize evidence collected "
                      "so far and identify unresolved questions."),
        input=history, tools=TOOLS, tool_choice="none",
    )
    print(response.output_text)
    return response.output_text


if __name__ == "__main__":
    run_agent("Investigate why payment-service is slow. Use the available "
              "diagnostic tools, identify the likely root cause and "
              "recommend appropriate next actions.")
