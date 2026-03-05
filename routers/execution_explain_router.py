from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.execution_llm import generate_execution_explanations

router = APIRouter()


@router.post("/execution-explain")
async def explain_execution(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        authority = data.get("authority", {})
        execution_result = data.get("execution", {})

        explanations = generate_execution_explanations(
            raw,
            detection,
            context,
            authority,
            execution_result
        )

        # Build rows based on execution type
        rows = []

        if "containment_triggered" in execution_result:
            rows = [
                {
                    "metric": "Containment Triggered",
                    "value": "Yes" if execution_result.get("containment_triggered") else "No",
                    "explanation": explanations.get("containment_triggered")
                },
                {
                    "metric": "Actions Executed",
                    "value": execution_result.get("actions_executed", []),
                    "explanation": explanations.get("actions_executed")
                },
                {
                    "metric": "Status",
                    "value": execution_result.get("status"),
                    "explanation": explanations.get("status")
                }
            ]
        elif "escalation" in execution_result:
            rows = [
                {
                    "metric": "Escalation",
                    "value": "Yes" if execution_result.get("escalation") else "No",
                    "explanation": explanations.get("escalation")
                },
                {
                    "metric": "Assigned Queue",
                    "value": execution_result.get("assigned_queue"),
                    "explanation": explanations.get("assigned_queue")
                },
                {
                    "metric": "Ticket Priority",
                    "value": execution_result.get("ticket_priority"),
                    "explanation": explanations.get("ticket_priority")
                },
                {
                    "metric": "Status",
                    "value": execution_result.get("status"),
                    "explanation": explanations.get("status")
                }
            ]
        elif "monitoring_enabled" in execution_result:
            rows = [
                {
                    "metric": "Monitoring Enabled",
                    "value": "Yes" if execution_result.get("monitoring_enabled") else "No",
                    "explanation": explanations.get("monitoring_enabled")
                },
                {
                    "metric": "Monitoring Duration Hours",
                    "value": execution_result.get("monitoring_duration_hours"),
                    "explanation": explanations.get("monitoring_duration_hours")
                },
                {
                    "metric": "Log Level",
                    "value": execution_result.get("log_level"),
                    "explanation": explanations.get("log_level")
                },
                {
                    "metric": "Status",
                    "value": execution_result.get("status"),
                    "explanation": explanations.get("status")
                }
            ]
        elif "action" in execution_result and execution_result.get("action") == "NO_ACTION_REQUIRED":
            rows = [
                {
                    "metric": "Action",
                    "value": execution_result.get("action"),
                    "explanation": explanations.get("action")
                },
                {
                    "metric": "Log Entry",
                    "value": execution_result.get("log_entry"),
                    "explanation": explanations.get("log_entry")
                },
                {
                    "metric": "Status",
                    "value": execution_result.get("status"),
                    "explanation": explanations.get("status")
                }
            ]
        else:
            # Fallback for unknown execution type
            rows = [
                {
                    "metric": "Execution Status",
                    "value": execution_result.get("status", "Unknown"),
                    "explanation": "Execution completed with unknown result type."
                }
            ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("EXECUTION ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
