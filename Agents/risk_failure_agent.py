def risk_failure_agent(raw, detection, context, policy, threat, impact, privacy):
    """
    Risk & Failure Analysis Agent
    Evaluates system stability and automation safety BEFORE coordination.
    """

    # -------------------------------------------------------
    # 1️⃣ Extract Core Signals
    # -------------------------------------------------------

    anomaly_prob = detection["anomaly_probability"]
    uncertainty = detection["uncertainty_score"]
    context_risk = context["final_contextual_risk"]

    policy_score = policy.get("policy_risk_score", 0)
    impact_score = impact.get("impact_score", 0)
    privacy_score = privacy.get("privacy_risk_score", 0)

    ransomware_prob = threat.get("ransomware_probability", 0)
    exfiltration_prob = threat.get("exfiltration_probability", 0)

    threat_score = max(ransomware_prob, exfiltration_prob)

    # -------------------------------------------------------
    # 2️⃣ Agent Disagreement Modeling
    # -------------------------------------------------------

    scores = [policy_score, impact_score, privacy_score, threat_score]
    disagreement = max(scores) - min(scores)

    # Normalize disagreement to [0,1]
    disagreement = max(0, min(disagreement, 1.0))

    # -------------------------------------------------------
    # 3️⃣ Volatility Modeling
    # -------------------------------------------------------

    entropy_signal = min(raw["file_entropy_avg"] / 8.0, 1.0)
    outbound_signal = min(raw["outbound_traffic_mb"] / 1000.0, 1.0)

    volatility_score = (
        0.4 * entropy_signal +
        0.4 * outbound_signal +
        0.2 * anomaly_prob
    )

    volatility_score = max(0, min(volatility_score, 1.0))

    # -------------------------------------------------------
    # 4️⃣ Instability Index
    # -------------------------------------------------------

    instability_score = (
        0.4 * uncertainty +
        0.3 * disagreement +
        0.3 * volatility_score
    )

    instability_score = max(0, min(instability_score, 1.0))

    # -------------------------------------------------------
    # 5️⃣ Automation Safety Gate
    # -------------------------------------------------------

    if instability_score < 0.4 and uncertainty < 0.5:
        automation_safe = True
    else:
        automation_safe = False

    # -------------------------------------------------------
    # 6️⃣ Failure Mode Classification
    # -------------------------------------------------------

    if instability_score >= 0.75:
        failure_mode = "SYSTEM_UNSTABLE"

    elif disagreement >= 0.5:
        failure_mode = "AGENT_CONFLICT"

    elif uncertainty >= 0.6:
        failure_mode = "MODEL_UNCERTAIN"

    elif volatility_score >= 0.7:
        failure_mode = "HIGH_SIGNAL_VOLATILITY"

    else:
        failure_mode = "STABLE"

    # -------------------------------------------------------
    # 7️⃣ Structured Output
    # -------------------------------------------------------

    return {
        "instability_score": round(instability_score, 4),
        "disagreement_score": round(disagreement, 4),
        "volatility_score": round(volatility_score, 4),
        "automation_safe": automation_safe,
        "failure_mode": failure_mode,
        "risk_profile": {
            "threat_score": round(threat_score, 4),
            "impact_score": round(impact_score, 4),
            "privacy_score": round(privacy_score, 4),
            "policy_score": round(policy_score, 4),
            "context_risk": round(context_risk, 4),
            "anomaly_probability": round(anomaly_prob, 4)
        }
    }