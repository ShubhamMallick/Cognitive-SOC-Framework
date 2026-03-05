import json
import re
from llm_setup import llm


def generate_authority_explanations(raw, detection, context, risk, coordination, authority_result):
    """
    Generate AI explanations for authority agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in incident response decision making and authority delegation.

Explain the following authority and decision-making metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"final_decision": "Explanation...",
"execution_mode": "Explanation...",
"severity_level": "Explanation...",
"override_triggered": "Explanation...",
"decision_confidence": "Explanation...",
"adaptive_containment_threshold": "Explanation...",
"adaptive_monitoring_threshold": "Explanation..."
}}

Authority Metrics:

Final Decision = {authority_result.get("final_decision")}
Execution Mode = {authority_result.get("execution_mode")}
Severity Level = {authority_result.get("severity_level")}
Override Triggered = {"Yes" if authority_result.get("override_triggered") else "No"}
Decision Confidence = {authority_result.get("decision_confidence")}
Adaptive Containment Threshold = {authority_result.get("adaptive_containment_threshold")}
Adaptive Monitoring Threshold = {authority_result.get("adaptive_monitoring_threshold")}

Coordination Context:
Fused Risk Score: {coordination.get("fused_risk_score")}
System Confidence: {coordination.get("system_confidence")}
Threat Stage: {coordination.get("threat_stage")}
Recommended Action: {coordination.get("recommended_action")}

Risk Context:
Instability Score: {authority_result.get("instability_score")}
Automation Safe: {"Yes" if risk.get("automation_safe") else "No"}

Device Context:
Department: {raw.get("department")}
Criticality Level: {raw.get("criticality_level")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("AUTHORITY LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == authority_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("AUTHORITY LLM ERROR:", e)

        # Fallback explanations
        return {
            "final_decision": (
                "Final decision represents the authoritative determination of incident response action "
                "based on comprehensive risk analysis and system safety considerations. This decision "
                "determines whether to execute automated containment, enable monitoring, or require human review."
            ),

            "execution_mode": (
                "Execution mode specifies the level of automation for the response strategy, ranging from "
                "fully automated containment through semi-automated monitoring to manual human analysis. "
                "This mode ensures appropriate human oversight based on risk complexity and system confidence."
            ),

            "severity_level": (
                "Severity level classifies the incident's overall impact and urgency, guiding resource "
                "allocation and response prioritization. Critical incidents demand immediate action while "
                "lower severity levels allow for more measured and coordinated responses."
            ),

            "override_triggered": (
                "Override triggered indicates when safety protocols have intervened to prevent automated "
                "actions despite high risk scores. This occurs when system instability or model uncertainty "
                "requires mandatory human review to prevent potential false positives or unintended consequences."
            ),

            "decision_confidence": (
                "Decision confidence reflects the reliability of the final authority determination based on "
                "coordinated risk analysis and system stability metrics. Higher confidence enables more "
                "decisive automated responses while lower confidence escalates to human analysis."
            ),

            "adaptive_containment_threshold": (
                "Adaptive containment threshold dynamically adjusts the risk level required for automated "
                "containment based on device context and organizational policies. This threshold adapts "
                "to different departments and criticality levels to optimize response effectiveness."
            ),

            "adaptive_monitoring_threshold": (
                "Adaptive monitoring threshold determines when to enable enhanced monitoring modes based on "
                "device-specific risk profiles and organizational requirements. This threshold ensures "
                "appropriate surveillance levels without overwhelming analysts with unnecessary alerts."
            )
        }
