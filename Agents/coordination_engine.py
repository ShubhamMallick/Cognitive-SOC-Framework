def coordination_engine(raw, detection, context, policy, threat, impact, privacy, risk):
    """
    Risk-Aware Multi-Agent Coordination Engine
    Uses Risk & Failure output BEFORE final decision authority.
    """

    # ---------------------------------------------------------
    # 1️⃣ Extract Core Signals
    # ---------------------------------------------------------

    anomaly_prob = detection["anomaly_probability"]
    uncertainty = detection["uncertainty_score"]
    context_risk = context["final_contextual_risk"]

    policy_score = policy.get("policy_risk_score", 0)
    impact_score = impact.get("impact_score", 0)
    privacy_score = privacy.get("privacy_risk_score", 0)

    ransomware_prob = threat.get("ransomware_probability", 0)
    exfiltration_prob = threat.get("exfiltration_probability", 0)

    threat_score = max(ransomware_prob, exfiltration_prob)

    # ---------------------------------------------------------
    # 2️⃣ Risk Agent Signals
    # ---------------------------------------------------------

    instability_score = risk["instability_score"]
    automation_safe = risk["automation_safe"]
    failure_mode = risk["failure_mode"]

    # ---------------------------------------------------------
    # 3️⃣ Normalize Raw Signals
    # ---------------------------------------------------------

    entropy_signal = min(raw["file_entropy_avg"] / 8.0, 1.0)
    outbound_signal = min(raw["outbound_traffic_mb"] / 1000.0, 1.0)
    privilege_signal = raw["privilege_escalation_flag"]
    criticality_signal = raw["criticality_level"] / 5.0

    escalation_factor = 0

    if entropy_signal > 0.7 and outbound_signal > 0.6:
        escalation_factor += 0.15

    if privilege_signal == 1 and anomaly_prob > 0.6:
        escalation_factor += 0.15

    if criticality_signal > 0.8:
        escalation_factor += 0.1

    # ---------------------------------------------------------
    # 4️⃣ Weighted Fusion
    # ---------------------------------------------------------

    fused_risk = (
        0.25 * threat_score +
        0.20 * impact_score +
        0.15 * privacy_score +
        0.15 * policy_score +
        0.15 * context_risk +
        0.10 * anomaly_prob
    )

    fused_risk += escalation_factor
    fused_risk = max(0, min(fused_risk, 1.0))

    # ---------------------------------------------------------
    # 5️⃣ Conflict Quantification
    # ---------------------------------------------------------

    scores = [policy_score, threat_score, impact_score, privacy_score]
    disagreement = max(scores) - min(scores)

    if disagreement > 0.5:
        conflict_level = "HIGH"
    elif disagreement > 0.25:
        conflict_level = "MODERATE"
    else:
        conflict_level = "LOW"

    # ---------------------------------------------------------
    # 6️⃣ Confidence Modeling (Risk-Aware)
    # ---------------------------------------------------------

    detection_confidence = 1 - uncertainty
    agreement_factor = 1 - disagreement

    base_confidence = (
        0.5 * detection_confidence +
        0.3 * agreement_factor +
        0.2 * (1 - escalation_factor)
    )

    # Risk penalty reduces confidence
    system_confidence = base_confidence * (1 - 0.5 * instability_score)
    system_confidence = max(0, min(system_confidence, 1.0))

    # ---------------------------------------------------------
    # 7️⃣ Threat Stage Classification
    # ---------------------------------------------------------

    if ransomware_prob > exfiltration_prob:
        dominant_threat = "RANSOMWARE"
    else:
        dominant_threat = "DATA_EXFILTRATION"

    if fused_risk >= 0.8:
        threat_stage = "CRITICAL COMPROMISE"
    elif fused_risk >= 0.6:
        threat_stage = "ACTIVE ATTACK"
    elif fused_risk >= 0.4:
        threat_stage = "SUSPICIOUS ACTIVITY"
    else:
        threat_stage = "LOW RISK"

    # ---------------------------------------------------------
    # 8️⃣ Risk-Aware Action Logic
    # ---------------------------------------------------------

    if not automation_safe:
        recommended_action = "FORCE_HUMAN_REVIEW"

    elif fused_risk >= 0.8 and system_confidence >= 0.6:
        recommended_action = "EXECUTE_AUTOMATED_CONTAINMENT"

    elif fused_risk >= 0.6:
        recommended_action = "ESCALATE_TO_HUMAN_ANALYST"

    elif fused_risk >= 0.4:
        recommended_action = "ENABLE_ADAPTIVE_MONITORING"

    else:
        recommended_action = "SAFE_PASS"

    # ---------------------------------------------------------
    # 9️⃣ Structured Output
    # ---------------------------------------------------------

    return {
        "fused_risk_score": round(fused_risk, 4),
        "system_confidence": round(system_confidence, 4),
        "conflict_level": conflict_level,
        "dominant_threat": dominant_threat,
        "threat_stage": threat_stage,
        "instability_score": round(instability_score, 4),
        "failure_mode": failure_mode,
        "escalation_factor": round(escalation_factor, 4),
        "recommended_action": recommended_action,
        "structured_profile": {
            "threat_score": round(threat_score, 4),
            "impact_score": round(impact_score, 4),
            "privacy_score": round(privacy_score, 4),
            "policy_score": round(policy_score, 4),
            "context_risk": round(context_risk, 4),
            "anomaly_probability": round(anomaly_prob, 4)
        }
    }