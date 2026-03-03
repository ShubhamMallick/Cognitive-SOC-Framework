# =========================================================
# Reinforcement Learning Agent (Adaptive Policy Engine)
# =========================================================

# Global adaptive decision thresholds
adaptive_policy = {
    "containment_threshold": 0.75,
    "monitoring_threshold": 0.45
}

# Memory buffer storing outcome rewards
learning_memory = []


def reinforcement_learning_agent():
    """
    Updates adaptive decision thresholds
    based on accumulated outcome rewards.
    """

    global adaptive_policy
    global learning_memory

    if not learning_memory:
        return

    avg_reward = sum(learning_memory) / len(learning_memory)

    # If decisions were good → slightly lower containment threshold
    if avg_reward > 0.7:
        adaptive_policy["containment_threshold"] = max(
            0.6,
            adaptive_policy["containment_threshold"] - 0.02
        )
    else:
        adaptive_policy["containment_threshold"] = min(
            0.9,
            adaptive_policy["containment_threshold"] + 0.02
        )

    # Monitoring threshold stays below containment
    adaptive_policy["monitoring_threshold"] = max(
        0.3,
        adaptive_policy["containment_threshold"] - 0.25
    )

    # Clear memory after update
    learning_memory.clear()