# Agentic AI Systems — four progressive demonstrations

These examples use **real OpenAI API requests** and **simulated IT operations data**.
No production infrastructure is accessed or modified. API usage may incur charges.

## Setup (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Debian/Ubuntu, install `python3-venv` first if `python3 -m venv` fails.

Edit `.env` and enter your OpenAI API key. Do not commit or share the key.

## Run in order

```bash
python 01_basic_llm.py
python 02_tool_calling.py
python 03_autonomous_agent.py
python 04_task_decomposition.py
```

- **Demo 1:** LLM-only incident response.
- **Demo 2:** Forced function call and tool-result interpretation.
- **Demo 3:** Autonomous plan–act–observe loop and iterative tool selection.
- **Demo 4:** Structured task planning, sequential execution and final synthesis.

The fourth demo dynamically imports `03_autonomous_agent.py` because Python
cannot use a numbered filename in a conventional `from ... import` statement.

## Wow-factor experiment

In `tools.py`, change `get_system_metrics()` to report CPU 98, memory 91,
response time 3200 and database latency 35. Change `get_database_status()` to
report 28 active connections, 0 waiting requests and `healthy` status.
Rerun Demo 3 and compare the investigation and conclusions.

## Notes

Model wording and tool selection can vary between runs. These examples are
instructional; production systems need stronger validation, timeouts, auditing,
permission controls and human approval for destructive actions.
