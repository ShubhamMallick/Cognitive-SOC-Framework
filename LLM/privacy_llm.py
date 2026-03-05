import json
import re
from llm_setup import llm


def generate_privacy_explanations(raw, detection, context, privacy_result):
    """
    Generate AI explanations for privacy agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in privacy protection and regulatory compliance.

Explain the following privacy risk assessment metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"privacy_risk_score": "Explanation...",
"breach_level": "Explanation...",
"breach_risk": "Explanation...",
"confidence_adjusted": "Explanation..."
}}

Privacy Metrics:

Privacy Risk Score = {privacy_result.get("privacy_risk_score")}
Breach Level = {privacy_result.get("breach_level")}
Breach Risk = {"Yes" if privacy_result.get("breach_risk") else "No"}
Confidence Adjusted = {privacy_result.get("confidence_adjusted")}

Raw Privacy Indicators:
Department: {raw.get("department")}
Outbound Traffic MB: {raw.get("outbound_traffic_mb")}
Unique External IPs: {raw.get("unique_external_ips")}
Privilege Escalation Flag: {raw.get("privilege_escalation_flag")}

Detection Context:
Anomaly Probability: {detection.get("anomaly_probability")}
Uncertainty Score: {detection.get("uncertainty_score")}

Contextual Risk:
Final Contextual Risk: {context.get("final_contextual_risk")}
Security Modifier: {context.get("security_modifier")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("PRIVACY LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == privacy_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("PRIVACY LLM ERROR:", e)

        # Fallback explanations
        return {
            "privacy_risk_score": (
                "Privacy risk score evaluates the potential for sensitive data exposure based on "
                "network activity patterns, privilege escalation, and department sensitivity. "
                "Higher scores indicate increased likelihood of privacy violations that could "
                "result in regulatory penalties or reputational damage."
            ),

            "breach_level": (
                "Breach level categorizes privacy risk into HIGH, MEDIUM, or LOW classifications "
                "to determine appropriate response measures and regulatory notification requirements. "
                "High breach levels typically require immediate containment and may trigger "
                "mandatory reporting obligations under privacy regulations."
            ),

            "breach_risk": (
                "Breach risk indicates whether the assessed privacy violation meets threshold criteria "
                "for formal breach declaration and regulatory reporting. When flagged, it signals "
                "that the incident likely involves unauthorized access to sensitive information "
                "requiring comprehensive incident response and notification procedures."
            ),

            "confidence_adjusted": (
                "Confidence adjusted factor reflects how much the detection model's uncertainty "
                "has been factored into the privacy risk assessment. Higher values indicate "
                "greater confidence in the anomaly detection, resulting in more reliable "
                "privacy risk evaluations and reduced false positive classifications."
            )
        }
