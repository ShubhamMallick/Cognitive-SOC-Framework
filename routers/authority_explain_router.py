from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.authority_llm import generate_authority_explanations

router = APIRouter()


@router.post("/authority-explain")
async def explain_authority(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        risk = data.get("risk", {})
        coordination = data.get("coordinate", {})
        authority_result = data.get("authority", {})

        explanations = generate_authority_explanations(
            raw,
            detection,
            context,
            risk,
            coordination,
            authority_result
        )

        rows = [
            {
                "metric": "Final Decision",
                "value": authority_result.get("final_decision"),
                "explanation": explanations.get("final_decision")
            },
            {
                "metric": "Execution Mode",
                "value": authority_result.get("execution_mode"),
                "explanation": explanations.get("execution_mode")
            },
            {
                "metric": "Severity Level",
                "value": authority_result.get("severity_level"),
                "explanation": explanations.get("severity_level")
            },
            {
                "metric": "Override Triggered",
                "value": "Yes" if authority_result.get("override_triggered") else "No",
                "explanation": explanations.get("override_triggered")
            },
            {
                "metric": "Decision Confidence",
                "value": authority_result.get("decision_confidence"),
                "explanation": explanations.get("decision_confidence")
            },
            {
                "metric": "Adaptive Containment Threshold",
                "value": authority_result.get("adaptive_containment_threshold"),
                "explanation": explanations.get("adaptive_containment_threshold")
            },
            {
                "metric": "Adaptive Monitoring Threshold",
                "value": authority_result.get("adaptive_monitoring_threshold"),
                "explanation": explanations.get("adaptive_monitoring_threshold")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("AUTHORITY ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
