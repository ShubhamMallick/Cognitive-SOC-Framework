from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.risk_llm import generate_risk_explanations

router = APIRouter()


@router.post("/risk-explain")
async def explain_risk(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        policy = data.get("policy", {})
        threat = data.get("threat", {})
        impact = data.get("impact", {})
        privacy = data.get("privacy", {})
        risk_result = data.get("risk", {})

        explanations = generate_risk_explanations(
            raw,
            detection,
            context,
            policy,
            threat,
            impact,
            privacy,
            risk_result
        )

        rows = [
            {
                "metric": "Instability Score",
                "value": risk_result.get("instability_score"),
                "explanation": explanations.get("instability_score")
            },
            {
                "metric": "Disagreement Score",
                "value": risk_result.get("disagreement_score"),
                "explanation": explanations.get("disagreement_score")
            },
            {
                "metric": "Volatility Score",
                "value": risk_result.get("volatility_score"),
                "explanation": explanations.get("volatility_score")
            },
            {
                "metric": "Automation Safe",
                "value": "Yes" if risk_result.get("automation_safe") else "No",
                "explanation": explanations.get("automation_safe")
            },
            {
                "metric": "Failure Mode",
                "value": risk_result.get("failure_mode"),
                "explanation": explanations.get("failure_mode")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("RISK ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
