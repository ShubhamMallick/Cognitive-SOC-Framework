def threat_agent(raw, detection, context):
    """
    Advanced Threat Intelligence Agent
    - Multi-threat probability modeling
    - Interaction-based amplification
    - Context-aware scaling
    """

    # -----------------------------
    # 1️⃣ Normalize Signals
    # -----------------------------

    entropy_signal = min(raw["file_entropy_avg"] / 8.0, 1.0)
    encrypted_signal = raw["encrypted_extension_ratio"]
    rename_signal = min(raw["file_rename_count"] / 2000.0, 1.0)

    outbound_signal = min(raw["outbound_traffic_mb"] / 1000.0, 1.0)
    external_ip_signal = min(raw["unique_external_ips"] / 50.0, 1.0)
    dns_signal = min(raw["dns_request_count"] / 200.0, 1.0)

    privilege_signal = raw["privilege_escalation_flag"]

    # -----------------------------
    # 2️⃣ Ransomware Probability
    # -----------------------------

    ransomware_prob = (
        0.35 * entropy_signal +
        0.3 * encrypted_signal +
        0.2 * rename_signal +
        0.15 * privilege_signal
    )

    # Interaction boost
    if entropy_signal > 0.7 and outbound_signal > 0.6:
        ransomware_prob += 0.1

    # -----------------------------
    # 3️⃣ Data Exfiltration Probability
    # -----------------------------

    exfiltration_prob = (
        0.4 * outbound_signal +
        0.3 * external_ip_signal +
        0.2 * dns_signal +
        0.1 * privilege_signal
    )

    # -----------------------------
    # 4️⃣ Context & Detection Scaling
    # -----------------------------

    prior = context["network_modifier"]
    likelihood = detection["anomaly_probability"]
    confidence = 1 - detection["uncertainty_score"]

    ransomware_prob *= prior * likelihood * confidence
    exfiltration_prob *= prior * likelihood * confidence

    ransomware_prob = max(0, min(ransomware_prob, 1.0))
    exfiltration_prob = max(0, min(exfiltration_prob, 1.0))

    dominant_threat = (
        "RANSOMWARE"
        if ransomware_prob > exfiltration_prob
        else "DATA_EXFILTRATION"
    )

    return {
        "ransomware_probability": round(ransomware_prob, 4),
        "exfiltration_probability": round(exfiltration_prob, 4),
        "dominant_threat": dominant_threat
    }