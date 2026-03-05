from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from LLM.threat_llm import generate_threat_explanations

router = APIRouter()


@router.post("/threat-explain")
async def explain_threat(request: Request):

    try:

        data = await request.json()

        raw = data.get("raw", {})
        detection = data.get("detection", {})
        context = data.get("context", {})
        threat_result = data.get("threat", {})

        explanations = generate_threat_explanations(
            raw,
            detection,
            context,
            threat_result
        )

        rows = [
            {
                "metric": "Ransomware Probability",
                "value": threat_result.get("ransomware_probability"),
                "explanation": explanations.get("ransomware_probability")
            },
            {
                "metric": "Exfiltration Probability",
                "value": threat_result.get("exfiltration_probability"),
                "explanation": explanations.get("exfiltration_probability")
            },
            {
                "metric": "Dominant Threat",
                "value": threat_result.get("dominant_threat"),
                "explanation": explanations.get("dominant_threat")
            }
        ]

        return JSONResponse({"rows": rows})

    except Exception as e:

        print("THREAT ROUTER ERROR:", e)

        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
