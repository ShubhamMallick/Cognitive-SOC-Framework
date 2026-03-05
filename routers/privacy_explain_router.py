from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.privacy_llm import generate_privacy_explanations

router = APIRouter()


@router.post("/privacy-explain")
async def explain_privacy(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        privacy_result = data.get("privacy", {})

        explanations = generate_privacy_explanations(
            raw,
            detection,
            context,
            privacy_result
        )

        rows = [
            {
                "metric": "Privacy Risk Score",
                "value": privacy_result.get("privacy_risk_score"),
                "explanation": explanations.get("privacy_risk_score")
            },
            {
                "metric": "Breach Level",
                "value": privacy_result.get("breach_level"),
                "explanation": explanations.get("breach_level")
            },
            {
                "metric": "Breach Risk",
                "value": "Yes" if privacy_result.get("breach_risk") else "No",
                "explanation": explanations.get("breach_risk")
            },
            {
                "metric": "Confidence Adjusted",
                "value": privacy_result.get("confidence_adjusted"),
                "explanation": explanations.get("confidence_adjusted")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("PRIVACY ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
