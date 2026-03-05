from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.audit_llm import generate_audit_explanations

router = APIRouter()


@router.post("/audit-explain")
async def explain_audit(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        risk = data.get("risk", {})
        coordination = data.get("coordinate", {})
        authority = data.get("authority", {})
        execution = data.get("execution", {})
        audit_result = data.get("audit", {})

        explanations = generate_audit_explanations(
            raw,
            detection,
            context,
            risk,
            coordination,
            authority,
            execution,
            audit_result
        )

        rows = [
            {
                "metric": "Final Decision",
                "value": audit_result.get("final_decision"),
                "explanation": explanations.get("final_decision")
            },
            {
                "metric": "Execution Mode",
                "value": audit_result.get("execution_mode"),
                "explanation": explanations.get("execution_mode")
            },
            {
                "metric": "Severity Level",
                "value": audit_result.get("severity_level"),
                "explanation": explanations.get("severity_level")
            },
            {
                "metric": "Override Triggered",
                "value": "Yes" if audit_result.get("override_triggered") else "No",
                "explanation": explanations.get("override_triggered")
            },
            {
                "metric": "Decision Confidence",
                "value": audit_result.get("decision_confidence"),
                "explanation": explanations.get("decision_confidence")
            },
            {
                "metric": "Adaptive Containment Threshold",
                "value": audit_result.get("adaptive_containment_threshold"),
                "explanation": explanations.get("adaptive_containment_threshold")
            },
            {
                "metric": "Adaptive Monitoring Threshold",
                "value": audit_result.get("adaptive_monitoring_threshold"),
                "explanation": explanations.get("adaptive_monitoring_threshold")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("AUDIT ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
