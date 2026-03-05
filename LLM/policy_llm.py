import json
import re
from llm_setup import llm


def generate_policy_explanations(raw, detection, context, policy_result):
    """
    Generate AI explanations for policy agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in security policy and compliance.

Explain the following policy risk metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"policy_risk_score": "Explanation...",
"policy_level": "Explanation...",
"mandatory_action": "Explanation..."
}}

Policy Metrics:

Policy Risk Score = {policy_result.get("policy_risk_score")}
Policy Level = {policy_result.get("policy_level")}
Mandatory Action = {"Yes" if policy_result.get("mandatory_action") else "No"}

Raw Security Signals:
Privilege Escalation Flag: {raw.get("privilege_escalation_flag")}
Configuration Change Flag: {raw.get("configuration_change_flag")}
Antivirus Alert Flag: {raw.get("antivirus_alert_flag")}
Failed Auth Attempts: {raw.get("failed_auth_attempts")}
Criticality Level: {raw.get("criticality_level")}

Detection Context:
Anomaly Probability: {detection.get("anomaly_probability")}
Uncertainty Score: {detection.get("uncertainty_score")}

Contextual Risk:
Final Contextual Risk: {context.get("final_contextual_risk")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("POLICY LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == policy_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("POLICY LLM ERROR:", e)

        # Fallback explanations
        return {
            "policy_risk_score": (
                "Policy risk score combines multiple security violation signals including privilege escalation, "
                "configuration changes, antivirus alerts, and authentication failures. The score is weighted "
                "by device criticality and considers both detection confidence and contextual risk factors."
            ),

            "policy_level": (
                "Policy level categorizes the severity of policy violations into CRITICAL, ELEVATED, or NORMAL. "
                "CRITICAL violations require immediate mandatory security actions, while ELEVATED violations "
                "warrant increased monitoring and potential intervention."
            ),

            "mandatory_action": (
                "Mandatory action indicates whether automated security responses are required based on policy "
                "risk assessment. When triggered, it ensures immediate containment measures are implemented "
                "without requiring human approval, preventing potential security incidents from escalating."
            )
        }
