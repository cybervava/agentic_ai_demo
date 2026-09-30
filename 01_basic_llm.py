"""Demo 1: An LLM without access to diagnostic tools."""
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    instructions=("You are an experienced IT operations engineer. "
                  "Do not invent system measurements or claim to have "
                  "inspected systems you cannot access."),
    input=("Our payment application is responding slowly. "
           "Investigate the issue and identify its root cause."),
)
print(response.output_text)
