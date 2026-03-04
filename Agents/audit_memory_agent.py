from Agents.reinforcement_learning_agent import adaptive_policy


def audit_memory_agent(raw, detection, context, risk, coordination, authority, execution):
    """
    Autonomous SOC Decision Authority
    Final enforceable decision layer.

    Integrates:
    - Risk & Failure constraints
    - Coordination intelligence
    - Reinforcement-adaptive thresholds
    """

    # ---------------------------------------------------------
    # Extract Inputs
    # ---------------------------------------------------------

    fused_risk = coordination["fused_risk_score"]
    system_confidence = coordination["system_confidence"]
    threat_stage = coordination["threat_stage"]
    recommended_action = coordination["recommended_action"]

    instability_score = risk["instability_score"]
    automation_safe = risk["automation_safe"]
    failure_mode = risk["failure_mode"]

    # ---------------------------------------------------------
    # Reinforcement-Adaptive Thresholds (Context-Aware)
    # ---------------------------------------------------------

    # Context-specific policy selection
    context_key = f"{raw['department']}_{raw['criticality_level']}"

    policy = adaptive_policy.get(context_key, adaptive_policy["default"])

    containment_threshold = policy["containment_threshold"]
    monitoring_threshold = policy["monitoring_threshold"]

    final_decision = None
    execution_mode = None
    override_triggered = False

    # =========================================================
    # 1️⃣ HARD SAFETY OVERRIDES (NON-NEGOTIABLE)
    # =========================================================

    if not automation_safe:
        final_decision = "HUMAN_ANALYST_REVIEW"
        execution_mode = "MANUAL"
        override_triggered = True

    elif failure_mode in ["SYSTEM_UNSTABLE", "MODEL_UNCERTAIN"]:
        final_decision = "HUMAN_ANALYST_REVIEW"
        execution_mode = "MANUAL"
        override_triggered = True

    # =========================================================
    # 2️⃣ CRITICAL COMPROMISE IMMEDIATE CONTAINMENT
    # =========================================================

    elif threat_stage == "CRITICAL COMPROMISE" and system_confidence >= 0.6:
        final_decision = "EXECUTE_AUTOMATED_CONTAINMENT"
        execution_mode = "AUTOMATED"

    # =========================================================
    # 3️⃣ ADAPTIVE RISK-BASED DECISION (RL-Driven)
    # =========================================================

    elif fused_risk >= containment_threshold:
        if system_confidence >= 0.6 and instability_score < 0.5:
            final_decision = "EXECUTE_AUTOMATED_CONTAINMENT"
            execution_mode = "AUTOMATED"
        else:
            final_decision = "HUMAN_ANALYST_REVIEW"
            execution_mode = "MANUAL"
            override_triggered = True

    elif fused_risk >= monitoring_threshold:
        final_decision = "ADAPTIVE_MONITORING_MODE"
        execution_mode = "SEMI_AUTOMATED"

    # =========================================================
    # 4️⃣ COORDINATION FALLBACK LOGIC
    # =========================================================

    else:
        if recommended_action == "ESCALATE_TO_HUMAN_ANALYST":
            final_decision = "HUMAN_ANALYST_REVIEW"
            execution_mode = "MANUAL"

        else:
            final_decision = "SAFE_PASS"
            execution_mode = "AUTOMATED"

    # =========================================================
    # 5️⃣ SEVERITY CLASSIFICATION
    # =========================================================

    if final_decision == "EXECUTE_AUTOMATED_CONTAINMENT":
        severity = "CRITICAL"

    elif final_decision == "HUMAN_ANALYST_REVIEW":
        severity = "HIGH"

    elif final_decision == "ADAPTIVE_MONITORING_MODE":
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # =========================================================
    # 6️⃣ FINAL OUTPUT
    # =========================================================

    return {
        "final_decision": final_decision,
        "execution_mode": execution_mode,
        "severity_level": severity,
        "override_triggered": override_triggered,
        "decision_confidence": round(system_confidence, 4),
        "instability_score": round(instability_score, 4),
        "adaptive_containment_threshold": round(containment_threshold, 4),
        "adaptive_monitoring_threshold": round(monitoring_threshold, 4)
    }