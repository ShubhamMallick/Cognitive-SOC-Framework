# =========================================================
# Reinforcement Learning Agent (Adaptive Policy Engine)
# =========================================================

# Global adaptive decision thresholds per context
adaptive_policy = {
    "default": {
        "containment_threshold": 0.75,
        "monitoring_threshold": 0.45
    }
}

# Memory buffer storing outcome rewards with context
learning_memory = []


def reinforcement_learning_agent():
    """
    Updates adaptive decision thresholds
    based on accumulated outcome rewards per context.
    """

    global adaptive_policy
    global learning_memory

    if not learning_memory:
        return

    # Group rewards by context
    context_rewards = {}
    for reward, context in learning_memory:
        if context not in context_rewards:
            context_rewards[context] = []
        context_rewards[context].append(reward)

    # Update policy per context
    for context, rewards in context_rewards.items():
        avg_reward = sum(rewards) / len(rewards)

        # Initialize if not present
        if context not in adaptive_policy:
            adaptive_policy[context] = adaptive_policy["default"].copy()

        # Adjust containment threshold
        if avg_reward > 0.7:
            adaptive_policy[context]["containment_threshold"] = max(
                0.6,
                adaptive_policy[context]["containment_threshold"] - 0.02
            )
        else:
            adaptive_policy[context]["containment_threshold"] = min(
                0.9,
                adaptive_policy[context]["containment_threshold"] + 0.02
            )

        # Monitoring threshold stays below containment
        adaptive_policy[context]["monitoring_threshold"] = max(
            0.3,
            adaptive_policy[context]["containment_threshold"] - 0.25
        )

    # Clear memory after update
    learning_memory.clear()