import json
import re
from llm_setup import llm


def generate_impact_explanations(raw, detection, context, impact_result):
    """
    Generate AI explanations for impact agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in incident impact assessment and threat propagation analysis.

Explain the following impact assessment metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"impact_score": "Explanation...",
"severity": "Explanation...",
"propagation_factor": "Explanation..."
}}

Impact Metrics:

Impact Score = {impact_result.get("impact_score")}
Severity = {impact_result.get("severity")}
Propagation Factor = {impact_result.get("propagation_factor")}

Raw Impact Indicators:
Criticality Level: {raw.get("criticality_level")}
Department: {raw.get("department")}
Outbound Traffic MB: {raw.get("outbound_traffic_mb")}
Unique External IPs: {raw.get("unique_external_ips")}
Process Spawn Count: {raw.get("process_spawn_count")}

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

        print("IMPACT LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == impact_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("IMPACT LLM ERROR:", e)

        # Fallback explanations
        return {
            "impact_score": (
                "Impact score quantifies the overall severity and potential consequences of a security "
                "incident based on device criticality, network activity, and system behavior patterns. "
                "Higher scores indicate greater potential for operational disruption and require "
                "prioritized incident response efforts."
            ),

            "severity": (
                "Severity classification categorizes the incident impact into CRITICAL, HIGH, or MODERATE "
                "levels to guide response prioritization and resource allocation. Critical incidents "
                "demand immediate attention and may require executive notification, while moderate "
                "incidents can follow standard response procedures."
            ),

            "propagation_factor": (
                "Propagation factor assesses the likelihood of threat spread across the network based on "
                "external connections and outbound traffic patterns. Higher values indicate increased "
                "risk of lateral movement or secondary infections, requiring broader containment measures "
                "beyond the initial affected system."
            )
        }
