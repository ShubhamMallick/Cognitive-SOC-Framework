def privacy_agent(raw, detection, context):
    """
    Advanced Privacy & Regulatory Risk Agent
    - Continuous signal modeling
    - Context-aware prior scaling
    - Uncertainty-adjusted confidence
    - Multi-factor breach probability estimation
    """

    # -----------------------------
    # 1️⃣ Normalize Core Signals
    # -----------------------------

    # Network exfiltration intensity
    outbound_signal = min(raw["outbound_traffic_mb"] / 1000.0, 1.0)
    external_ip_signal = min(raw["unique_external_ips"] / 50.0, 1.0)

    # Privilege misuse indicator
    privilege_signal = raw["privilege_escalation_flag"]

    # Sensitive department weighting
    if raw["department"] in ["ICU", "ER", "Radiology"]:
        sensitivity_weight = 1.0
    else:
        sensitivity_weight = 0.5

    # -----------------------------
    # 2️⃣ Base Privacy Exposure Score
    # -----------------------------

    base_exposure = (
        0.4 * outbound_signal +
        0.25 * external_ip_signal +
        0.2 * privilege_signal +
        0.15 * sensitivity_weight
    )

    # -----------------------------
    # 3️⃣ Detection Influence
    # -----------------------------

    likelihood_factor = detection["anomaly_probability"]

    # Reduce effect if model uncertainty is high
    confidence_factor = 1 - detection["uncertainty_score"]

    adjusted_likelihood = likelihood_factor * confidence_factor

    # -----------------------------
    # 4️⃣ Contextual Risk Prior
    # -----------------------------

    contextual_prior = context["final_contextual_risk"]

    # -----------------------------
    # 5️⃣ Posterior Privacy Risk
    # -----------------------------

    privacy_risk_score = base_exposure * adjusted_likelihood * contextual_prior

    # Apply security posture modifier
    privacy_risk_score *= context["security_modifier"]

    # Clamp to [0,1]
    privacy_risk_score = max(0, min(privacy_risk_score, 1.0))

    # -----------------------------
    # 6️⃣ Risk Classification
    # -----------------------------

    if privacy_risk_score >= 0.65:
        breach_level = "HIGH"
    elif privacy_risk_score >= 0.35:
        breach_level = "MEDIUM"
    else:
        breach_level = "LOW"

    breach_risk = breach_level == "HIGH"

    return {
        "privacy_risk_score": round(privacy_risk_score, 4),
        "breach_level": breach_level,
        "breach_risk": breach_risk,
        "confidence_adjusted": round(confidence_factor, 4)
    }