import json
import re
from llm_setup import llm


def generate_risk_explanations(raw, detection, context, policy, threat, impact, privacy, risk_result):
    """
    Generate AI explanations for risk & failure agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in risk assessment and system stability analysis.

Explain the following risk and failure analysis metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"instability_score": "Explanation...",
"disagreement_score": "Explanation...",
"volatility_score": "Explanation...",
"automation_safe": "Explanation...",
"failure_mode": "Explanation..."
}}

Risk Metrics:

Instability Score = {risk_result.get("instability_score")}
Disagreement Score = {risk_result.get("disagreement_score")}
Volatility Score = {risk_result.get("volatility_score")}
Automation Safe = {"Yes" if risk_result.get("automation_safe") else "No"}
Failure Mode = {risk_result.get("failure_mode")}

Risk Profile:
Threat Score: {risk_result.get("risk_profile", {}).get("threat_score")}
Impact Score: {risk_result.get("risk_profile", {}).get("impact_score")}
Privacy Score: {risk_result.get("risk_profile", {}).get("privacy_score")}
Policy Score: {risk_result.get("risk_profile", {}).get("policy_score")}
Context Risk: {risk_result.get("risk_profile", {}).get("context_risk")}
Anomaly Probability: {risk_result.get("risk_profile", {}).get("anomaly_probability")}

Detection Context:
Uncertainty Score: {detection.get("uncertainty_score")}

Raw Indicators:
File Entropy Average: {raw.get("file_entropy_avg")}
Outbound Traffic MB: {raw.get("outbound_traffic_mb")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("RISK LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == risk_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("RISK LLM ERROR:", e)

        # Fallback explanations
        return {
            "instability_score": (
                "Instability score measures the overall system stability by combining uncertainty, "
                "agent disagreement, and signal volatility. Higher values indicate potential system "
                "instability that may require manual intervention instead of automated responses."
            ),

            "disagreement_score": (
                "Disagreement score quantifies the variance between different agent risk assessments "
                "including policy, impact, privacy, and threat analysis. High disagreement suggests "
                "conflicting signals that require careful human review before taking action."
            ),

            "volatility_score": (
                "Volatility score evaluates the dynamic nature of security signals such as file entropy "
                "changes and outbound traffic patterns. Elevated volatility indicates rapidly changing "
                "conditions that may indicate active threats or system instability."
            ),

            "automation_safe": (
                "Automation safety flag determines whether current system conditions are suitable for "
                "automated security responses. When disabled, it prevents automated actions that might "
                "cause unintended consequences in unstable or uncertain environments."
            ),

            "failure_mode": (
                "Failure mode classification identifies the primary reason for system instability, "
                "ranging from model uncertainty to agent conflicts or high signal volatility. This "
                "determines the appropriate response strategy and escalation procedures."
            )
        }
