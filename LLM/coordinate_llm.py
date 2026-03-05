import json
import re
from llm_setup import llm


def generate_coordinate_explanations(raw, detection, context, policy, threat, impact, privacy, risk, coordinate_result):
    """
    Generate AI explanations for coordination engine results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in multi-agent coordination and incident response orchestration.

Explain the following coordination and risk fusion metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"fused_risk_score": "Explanation...",
"system_confidence": "Explanation...",
"conflict_level": "Explanation...",
"dominant_threat": "Explanation...",
"threat_stage": "Explanation...",
"escalation_factor": "Explanation...",
"recommended_action": "Explanation..."
}}

Coordination Metrics:

Fused Risk Score = {coordinate_result.get("fused_risk_score")}
System Confidence = {coordinate_result.get("system_confidence")}
Conflict Level = {coordinate_result.get("conflict_level")}
Dominant Threat = {coordinate_result.get("dominant_threat")}
Threat Stage = {coordinate_result.get("threat_stage")}
Escalation Factor = {coordinate_result.get("escalation_factor")}
Recommended Action = {coordinate_result.get("recommended_action")}

Structured Profile:
Threat Score: {coordinate_result.get("structured_profile", {}).get("threat_score")}
Impact Score: {coordinate_result.get("structured_profile", {}).get("impact_score")}
Privacy Score: {coordinate_result.get("structured_profile", {}).get("privacy_score")}
Policy Score: {coordinate_result.get("structured_profile", {}).get("policy_score")}
Context Risk: {coordinate_result.get("structured_profile", {}).get("context_risk")}
Anomaly Probability: {coordinate_result.get("structured_profile", {}).get("anomaly_probability")}

Risk Context:
Instability Score: {coordinate_result.get("instability_score")}
Failure Mode: {coordinate_result.get("failure_mode")}

Raw Indicators:
File Entropy Average: {raw.get("file_entropy_avg")}
Outbound Traffic MB: {raw.get("outbound_traffic_mb")}
Privilege Escalation Flag: {raw.get("privilege_escalation_flag")}
Criticality Level: {raw.get("criticality_level")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("COORDINATE LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == coordinate_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("COORDINATE LLM ERROR:", e)

        # Fallback explanations
        return {
            "fused_risk_score": (
                "Fused risk score combines multiple agent assessments including threat, impact, "
                "privacy, and policy analysis into a unified risk metric. This integrated approach "
                "provides a comprehensive view of overall security posture across all analysis domains."
            ),

            "system_confidence": (
                "System confidence reflects the reliability of the fused risk assessment by considering "
                "detection model certainty, agent agreement, and system stability factors. Higher "
                "confidence enables more decisive automated responses while lower confidence "
                "triggers human review processes."
            ),

            "conflict_level": (
                "Conflict level indicates the degree of disagreement between different security agents "
                "regarding threat severity and risk assessment. High conflict levels suggest complex "
                "situations requiring careful human analysis rather than automated decision making."
            ),

            "dominant_threat": (
                "Dominant threat classification identifies the primary attack vector based on comparative "
                "analysis of ransomware and data exfiltration indicators. This determination helps "
                "prioritize specific containment and remediation strategies appropriate to the threat type."
            ),

            "threat_stage": (
                "Threat stage categorizes the current attack progression from low risk monitoring "
                "through suspicious activity to critical compromise states. This temporal assessment "
                "guides the urgency and intensity of incident response measures."
            ),

            "escalation_factor": (
                "Escalation factor quantifies risk amplification based on critical indicators such as "
                "high entropy files combined with outbound traffic or privilege escalation with anomalies. "
                "This factor increases the overall risk score when multiple concerning signals align."
            ),

            "recommended_action": (
                "Recommended action provides the optimal response strategy based on fused risk analysis, "
                "system confidence, and automation safety considerations. Actions range from safe pass "
                "through adaptive monitoring to immediate automated containment or forced human review."
            )
        }
