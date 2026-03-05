from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.impact_llm import generate_impact_explanations

router = APIRouter()


@router.post("/impact-explain")
async def explain_impact(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        impact_result = data.get("impact", {})

        explanations = generate_impact_explanations(
            raw,
            detection,
            context,
            impact_result
        )

        rows = [
            {
                "metric": "Impact Score",
                "value": impact_result.get("impact_score"),
                "explanation": explanations.get("impact_score")
            },
            {
                "metric": "Severity",
                "value": impact_result.get("severity"),
                "explanation": explanations.get("severity")
            },
            {
                "metric": "Propagation Factor",
                "value": impact_result.get("propagation_factor"),
                "explanation": explanations.get("propagation_factor")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("IMPACT ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
