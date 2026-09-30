"""Reproducible, simulated IT diagnostic tools. No real infrastructure is changed."""
import json


def get_system_metrics(service: str):
    return {"service": service, "cpu_usage": 32, "memory_usage": 58,
            "response_time_ms": 2400, "normal_response_time_ms": 200,
            "error_rate_percent": 12, "database_latency_ms": 1850}


def get_database_status(service: str):
    return {"service": service, "database": "payments_db",
            "active_connections": 100, "max_connections": 100,
            "waiting_requests": 45, "slow_queries": 28,
            "status": "connection_pool_exhausted"}


def get_application_logs(service: str):
    return {"service": service, "logs": [
        "ERROR: Database connection timeout",
        "WARN: Connection pool exhausted",
        "ERROR: Payment request exceeded timeout",
        "INFO: Retry attempt failed"]}


def get_recent_deployments(service: str):
    return {"service": service, "deployments": [{
        "version": "v2.4.1", "change": "Updated database connection handling",
        "deployed_minutes_ago": 35}]}


AVAILABLE_TOOLS = {
    "get_system_metrics": get_system_metrics,
    "get_database_status": get_database_status,
    "get_application_logs": get_application_logs,
    "get_recent_deployments": get_recent_deployments,
}


def execute_tool(name, arguments):
    if name not in AVAILABLE_TOOLS:
        return json.dumps({"error": f"Unknown tool: {name}"})
    try:
        return json.dumps(AVAILABLE_TOOLS[name](**arguments))
    except Exception as error:
        return json.dumps({"error": str(error)})
