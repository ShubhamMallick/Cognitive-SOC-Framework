def impact_agent(raw, detection, context):
    """
    Advanced Impact & Propagation Agent
    - Severity modeling
    - Propagation likelihood
    - Context-aware amplification
    """

    # -----------------------------
    # 1️⃣ Normalize Signals
    # -----------------------------

    criticality_signal = raw["criticality_level"] / 5.0
    outbound_signal = min(raw["outbound_traffic_mb"] / 1000.0, 1.0)
    external_ip_signal = min(raw["unique_external_ips"] / 50.0, 1.0)
    process_signal = min(raw["process_spawn_count"] / 100.0, 1.0)

    # Department sensitivity
    if raw["department"] in ["ICU", "ER"]:
        department_weight = 1.0
    else:
        department_weight = 0.6

    # -----------------------------
    # 2️⃣ Base Impact Score
    # -----------------------------

    base_impact = (
        0.35 * criticality_signal +
        0.25 * outbound_signal +
        0.2 * external_ip_signal +
        0.2 * process_signal
    )

    # -----------------------------
    # 3️⃣ Propagation Modeling
    # -----------------------------

    propagation_factor = (
        0.6 * external_ip_signal +
        0.4 * outbound_signal
    )

    # -----------------------------
    # 4️⃣ Posterior Impact Severity
    # -----------------------------

    prior = context["final_contextual_risk"]
    likelihood = detection["anomaly_probability"]
    confidence = 1 - detection["uncertainty_score"]

    impact_score = base_impact * prior * likelihood * confidence
    impact_score *= department_weight
    impact_score *= (1 + propagation_factor)

    impact_score = max(0, min(impact_score, 1.0))

    # -----------------------------
    # 5️⃣ Classification
    # -----------------------------

    if impact_score >= 0.7:
        severity = "CRITICAL"
    elif impact_score >= 0.4:
        severity = "HIGH"
    else:
        severity = "MODERATE"

    return {
        "impact_score": round(impact_score, 4),
        "severity": severity,
        "propagation_factor": round(propagation_factor, 4)
    }