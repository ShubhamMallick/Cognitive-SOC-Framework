from .modifiers import (
    asset_modifier,
    network_modifier,
    security_modifier
)

from .risk_utils import (
    classify_risk_band,
    classify_confidence_band
)


class ContextFramingEngine:

    def frame_context(self,
                      anomaly_prob,
                      deviation_score,
                      uncertainty,
                      features):

        # Base anomaly fusion
        base_risk = (anomaly_prob + deviation_score) / 2

        # Context modifiers
        asset_mod = asset_modifier(features["criticality_level"])
        network_mod = network_modifier(
            features["outbound_traffic_mb"],
            features["unique_external_ips"],
            features["unusual_port_flag"]
        )
        security_mod = security_modifier(
            features["privilege_escalation_flag"],
            features["configuration_change_flag"],
            features["antivirus_alert_flag"],
            features["failed_auth_attempts"]
        )

        contextual_risk = base_risk * asset_mod * network_mod * security_mod
        contextual_risk = min(contextual_risk, 1.0)

        return {
            "base_risk": float(base_risk),
            "asset_modifier": float(asset_mod),
            "network_modifier": float(network_mod),
            "security_modifier": float(security_mod),
            "final_contextual_risk": float(contextual_risk),
            "risk_band": classify_risk_band(contextual_risk),
            "confidence_band": classify_confidence_band(uncertainty)
        }