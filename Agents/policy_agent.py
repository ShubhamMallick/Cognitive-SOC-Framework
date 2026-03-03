def policy_agent(raw, detection, context):
    """
    Advanced Security Policy & Compliance Agent
    - Continuous violation modeling
    - Context-aware amplification
    - Uncertainty-adjusted enforcement confidence
    """

    # -----------------------------
    # 1️⃣ Normalize Violation Signals
    # -----------------------------

    privilege_signal = raw["privilege_escalation_flag"]
    config_signal = raw["configuration_change_flag"]
    antivirus_signal = raw["antivirus_alert_flag"]

    auth_signal = min(raw["failed_auth_attempts"] / 20.0, 1.0)

    criticality_signal = raw["criticality_level"] / 5.0

    # -----------------------------
    # 2️⃣ Base Compliance Risk
    # -----------------------------

    base_violation_risk = (
        0.3 * privilege_signal +
        0.2 * config_signal +
        0.15 * antivirus_signal +
        0.15 * auth_signal +
        0.2 * criticality_signal
    )

    # -----------------------------
    # 3️⃣ Contextual Prior
    # -----------------------------

    prior = context["final_contextual_risk"]

    # -----------------------------
    # 4️⃣ Detection Influence
    # -----------------------------

    likelihood = detection["anomaly_probability"]
    confidence = 1 - detection["uncertainty_score"]

    posterior = base_violation_risk * likelihood * prior * confidence

    posterior = max(0, min(posterior, 1.0))

    # -----------------------------
    # 5️⃣ Classification
    # -----------------------------

    if posterior >= 0.7:
        level = "CRITICAL"
    elif posterior >= 0.4:
        level = "ELEVATED"
    else:
        level = "NORMAL"

    mandatory_action = level == "CRITICAL"

    return {
        "policy_risk_score": round(posterior, 4),
        "policy_level": level,
        "mandatory_action": mandatory_action
    }