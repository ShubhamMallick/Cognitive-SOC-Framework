def human_review_agent(raw, authority):
    """
    Escalation to human SOC analyst.
    """

    device_id = raw["device_id"]

    return {
        "escalation": True,
        "assigned_queue": "Tier-2 SOC Analyst",
        "ticket_priority": "HIGH",
        "device": device_id,
        "status": "AWAITING_REVIEW"
    }