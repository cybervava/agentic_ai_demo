"""Demo 2: One forced function call, followed by an evidence-based answer."""
import json
from dotenv import load_dotenv
from openai import OpenAI
from tools import execute_tool

load_dotenv()
client = OpenAI()

tool_schema = {
    "type": "function", "name": "get_system_metrics",
    "description": "Retrieve performance metrics for a service.",
    "parameters": {"type": "object", "properties": {
        "service": {"type": "string", "description": "Application service name"}},
        "required": ["service"], "additionalProperties": False},
    "strict": True,
}
user_request = ("Check the performance of payment-service "
                "and identify any abnormal metrics.")
response = client.responses.create(
    model="gpt-5-mini", input=user_request, tools=[tool_schema],
    tool_choice={"type": "function", "name": "get_system_metrics"},
)

for item in response.output:
    if item.type == "function_call":
        print("\nTool selected:", item.name)
        print("Arguments:", item.arguments)
        result = execute_tool(item.name, json.loads(item.arguments))
        print("\nTool result:", result)
        final_response = client.responses.create(
            model="gpt-5-mini",
            input=[{"role": "user", "content": user_request},
                   *response.output,
                   {"type": "function_call_output", "call_id": item.call_id,
                    "output": result}],
            tools=[tool_schema], tool_choice="none",
        )
        print("\nFinal analysis:", final_response.output_text)
