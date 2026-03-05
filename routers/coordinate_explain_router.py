from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.coordinate_llm import generate_coordinate_explanations

router = APIRouter()


@router.post("/coordinate-explain")
async def explain_coordinate(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        policy = data.get("policy", {})
        threat = data.get("threat", {})
        impact = data.get("impact", {})
        privacy = data.get("privacy", {})
        risk = data.get("risk", {})
        coordinate_result = data.get("coordinate", {})

        explanations = generate_coordinate_explanations(
            raw,
            detection,
            context,
            policy,
            threat,
            impact,
            privacy,
            risk,
            coordinate_result
        )

        rows = [
            {
                "metric": "Fused Risk Score",
                "value": coordinate_result.get("fused_risk_score"),
                "explanation": explanations.get("fused_risk_score")
            },
            {
                "metric": "System Confidence",
                "value": coordinate_result.get("system_confidence"),
                "explanation": explanations.get("system_confidence")
            },
            {
                "metric": "Conflict Level",
                "value": coordinate_result.get("conflict_level"),
                "explanation": explanations.get("conflict_level")
            },
            {
                "metric": "Dominant Threat",
                "value": coordinate_result.get("dominant_threat"),
                "explanation": explanations.get("dominant_threat")
            },
            {
                "metric": "Threat Stage",
                "value": coordinate_result.get("threat_stage"),
                "explanation": explanations.get("threat_stage")
            },
            {
                "metric": "Escalation Factor",
                "value": coordinate_result.get("escalation_factor"),
                "explanation": explanations.get("escalation_factor")
            },
            {
                "metric": "Recommended Action",
                "value": coordinate_result.get("recommended_action"),
                "explanation": explanations.get("recommended_action")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("COORDINATE ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
