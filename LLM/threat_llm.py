import json
import re
from llm_setup import llm


def generate_threat_explanations(raw, detection, context, threat_result):
    """
    Generate AI explanations for threat agent results using LLM
    """

    prompt = f"""
You are a cybersecurity SOC analyst specializing in threat intelligence and malware analysis.

Explain the following threat assessment metrics clearly and concisely.

IMPORTANT RULES:
- Do NOT repeat the metric values or labels.
- Do NOT return numbers.
- Provide explanations only.
- Each explanation must contain 2–3 sentences.

Return ONLY JSON in this format:

{{
"ransomware_probability": "Explanation...",
"exfiltration_probability": "Explanation...",
"dominant_threat": "Explanation..."
}}

Threat Metrics:

Ransomware Probability = {threat_result.get("ransomware_probability")}
Exfiltration Probability = {threat_result.get("exfiltration_probability")}
Dominant Threat = {threat_result.get("dominant_threat")}

Raw Threat Indicators:
File Entropy Average: {raw.get("file_entropy_avg")}
Encrypted Extension Ratio: {raw.get("encrypted_extension_ratio")}
File Rename Count: {raw.get("file_rename_count")}
Outbound Traffic MB: {raw.get("outbound_traffic_mb")}
Unique External IPs: {raw.get("unique_external_ips")}
DNS Request Count: {raw.get("dns_request_count")}
Privilege Escalation Flag: {raw.get("privilege_escalation_flag")}

Detection Context:
Anomaly Probability: {detection.get("anomaly_probability")}
Uncertainty Score: {detection.get("uncertainty_score")}

Contextual Risk:
Network Modifier: {context.get("network_modifier")}
"""

    try:

        # Correct LangChain invocation
        response = llm.invoke([
            {"role": "user", "content": prompt}
        ])

        content = response.content if hasattr(response, "content") else str(response)

        print("THREAT LLM RESPONSE:", content)

        # Extract JSON safely
        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if not json_match:
            raise ValueError("No JSON found in response")

        explanations = json.loads(json_match.group())

        # Prevent numeric echo or value repetition
        for key, value in explanations.items():
            if isinstance(value, (int, float)) or value == threat_result.get(key):
                explanations[key] = "Explanation generation failed. Please retry."

        return explanations

    except Exception as e:

        print("THREAT LLM ERROR:", e)

        # Fallback explanations
        return {
            "ransomware_probability": (
                "Ransomware probability assesses the likelihood of ransomware infection based on "
                "file system behaviors such as high entropy files, encrypted extensions, and mass "
                "file renaming. These indicators suggest malicious encryption activities typical of "
                "ransomware campaigns targeting data for extortion."
            ),

            "exfiltration_probability": (
                "Data exfiltration probability evaluates suspicious outbound network traffic patterns "
                "including unusual data volumes, connections to external IP addresses, and abnormal "
                "DNS activity. These behaviors may indicate unauthorized data transfers or "
                "command-and-control communications with remote servers."
            ),

            "dominant_threat": (
                "Dominant threat classification identifies the most likely attack vector between "
                "ransomware and data exfiltration based on comparative probability analysis. "
                "This determination helps prioritize incident response efforts and allocate "
                "security resources to the most probable threat scenario."
            )
        }
