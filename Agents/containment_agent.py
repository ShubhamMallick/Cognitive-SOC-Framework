def containment_agent(raw, authority):
    """
    Simulated Automated Containment Logic.
    """

    device_id = raw["device_id"]

    containment_actions = [
        f"Isolate device {device_id} from network",
        "Revoke privileged sessions",
        "Block outbound traffic",
        "Trigger forensic snapshot"
    ]

    return {
        "containment_triggered": True,
        "actions_executed": containment_actions,
        "status": "DEVICE_ISOLATED"
    }