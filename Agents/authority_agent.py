def authority_agent(raw, detection, context, risk, coordination):
    """
    Autonomous SOC Decision Authority
    Final execution layer after coordination.
    Converts recommendation into enforceable SOC action.
    """

    fused_risk = coordination["fused_risk_score"]
    system_confidence = coordination["system_confidence"]
    threat_stage = coordination["threat_stage"]
    recommended_action = coordination["recommended_action"]

    instability_score = risk["instability_score"]
    automation_safe = risk["automation_safe"]
    failure_mode = risk["failure_mode"]

    final_decision = None
    execution_mode = None
    override_triggered = False

    # ---------------------------------------------------------
    # 1️⃣ Hard Safety Overrides
    # ---------------------------------------------------------

    if not automation_safe:
        final_decision = "HUMAN_ANALYST_REVIEW"
        execution_mode = "MANUAL"
        override_triggered = True

    elif failure_mode in ["SYSTEM_UNSTABLE", "MODEL_UNCERTAIN"]:
        final_decision = "HUMAN_ANALYST_REVIEW"
        execution_mode = "MANUAL"
        override_triggered = True

    # ---------------------------------------------------------
    # 2️⃣ Critical Compromise Immediate Containment
    # ---------------------------------------------------------

    elif threat_stage == "CRITICAL COMPROMISE" and system_confidence >= 0.6:
        final_decision = "EXECUTE_AUTOMATED_CONTAINMENT"
        execution_mode = "AUTOMATED"

    # ---------------------------------------------------------
    # 3️⃣ Coordination Recommendation Handling
    # ---------------------------------------------------------

    else:

        if recommended_action == "EXECUTE_AUTOMATED_CONTAINMENT":
            if system_confidence >= 0.6 and instability_score < 0.5:
                final_decision = "EXECUTE_AUTOMATED_CONTAINMENT"
                execution_mode = "AUTOMATED"
            else:
                final_decision = "HUMAN_ANALYST_REVIEW"
                execution_mode = "MANUAL"
                override_triggered = True

        elif recommended_action == "ESCALATE_TO_HUMAN_ANALYST":
            final_decision = "HUMAN_ANALYST_REVIEW"
            execution_mode = "MANUAL"

        elif recommended_action == "ENABLE_ADAPTIVE_MONITORING":
            final_decision = "ADAPTIVE_MONITORING_MODE"
            execution_mode = "SEMI_AUTOMATED"

        else:
            final_decision = "SAFE_PASS"
            execution_mode = "AUTOMATED"

    # ---------------------------------------------------------
    # 4️⃣ Decision Severity Classification
    # ---------------------------------------------------------

    if final_decision == "EXECUTE_AUTOMATED_CONTAINMENT":
        severity = "CRITICAL"

    elif final_decision == "HUMAN_ANALYST_REVIEW":
        severity = "HIGH"

    elif final_decision == "ADAPTIVE_MONITORING_MODE":
        severity = "MEDIUM"

    else:
        severity = "LOW"

    # ---------------------------------------------------------
    # 5️⃣ Final Authority Output
    # ---------------------------------------------------------

    return {
        "final_decision": final_decision,
        "execution_mode": execution_mode,
        "severity_level": severity,
        "override_triggered": override_triggered,
        "decision_confidence": round(system_confidence, 4),
        "instability_score": round(instability_score, 4)
    }