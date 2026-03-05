from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.context_llm import generate_context_explanations

router = APIRouter()


@router.post("/context-explain")
async def explain_context(request: Request):

    try:

        data = await request.json()

        context = data.get("context", {})
        detection = data.get("detection", {})
        features = data.get("raw_features", {})

        explanations = generate_context_explanations(
            context,
            detection,
            features
        )

        rows = [
            {
                "metric": "Base Risk",
                "value": context.get("base_risk"),
                "explanation": explanations.get("base_risk")
            },
            {
                "metric": "Asset Modifier",
                "value": context.get("asset_modifier"),
                "explanation": explanations.get("asset_modifier")
            },
            {
                "metric": "Network Modifier",
                "value": context.get("network_modifier"),
                "explanation": explanations.get("network_modifier")
            },
            {
                "metric": "Security Modifier",
                "value": context.get("security_modifier"),
                "explanation": explanations.get("security_modifier")
            },
            {
                "metric": "Final Contextual Risk",
                "value": context.get("final_contextual_risk"),
                "explanation": explanations.get("final_contextual_risk")
            },
            {
                "metric": "Risk Band",
                "value": context.get("risk_band"),
                "explanation": explanations.get("risk_band")
            },
            {
                "metric": "Confidence Band",
                "value": context.get("confidence_band"),
                "explanation": explanations.get("confidence_band")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )