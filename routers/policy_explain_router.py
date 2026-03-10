from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.policy_llm import generate_policy_explanations

router = APIRouter()


@router.post("/policy-explain")
async def explain_policy(request: Request):

    try:

        data = await request.json()

        policy_result = data.get("policy", {})

        explanations = generate_policy_explanations(
            {},
            {},
            {},
            policy_result
        )

        rows = [
            {
                "metric": "Policy Risk Score",
                "value": policy_result.get("policy_risk_score"),
                "explanation": explanations.get("policy_risk_score")
            },
            {
                "metric": "Policy Level",
                "value": policy_result.get("policy_level"),
                "explanation": explanations.get("policy_level")
            },
            {
                "metric": "Mandatory Action",
                "value": "Yes" if policy_result.get("mandatory_action") else "No",
                "explanation": explanations.get("mandatory_action")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("POLICY ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
