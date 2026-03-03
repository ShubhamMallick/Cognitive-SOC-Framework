from Agents.reinforcement_learning_agent import learning_memory


def outcome_feedback_agent(raw, detection, coordination, authority, execution, audit):
    """
    Evaluates decision quality and generates reinforcement reward.
    """

    decision = authority["final_decision"]
    fused_risk = coordination["fused_risk_score"]

    # ---------------------------------------------------------
    # Determine if actual threat likely existed
    # (Simulated ground truth logic)
    # ---------------------------------------------------------

    actual_threat_detected = fused_risk >= 0.6

    # ---------------------------------------------------------
    # Reward Logic
    # ---------------------------------------------------------

    if decision == "EXECUTE_AUTOMATED_CONTAINMENT":
        reward = 1.0 if actual_threat_detected else -0.5

    elif decision == "HUMAN_ANALYST_REVIEW":
        reward = 0.6 if actual_threat_detected else 0.3

    elif decision == "ADAPTIVE_MONITORING_MODE":
        reward = 0.5 if actual_threat_detected else 0.2

    elif decision == "SAFE_PASS":
        reward = -0.7 if actual_threat_detected else 0.8

    else:
        reward = 0.0

    # Store reward for reinforcement
    learning_memory.append(reward)

    return {
        "actual_threat_detected": actual_threat_detected,
        "reward_signal": round(reward, 3),
        "learning_memory_size": len(learning_memory)
    }