def classify_risk_band(risk_score):

    if risk_score >= 0.85:
        return "CRITICAL"
    elif risk_score >= 0.65:
        return "HIGH"
    elif risk_score >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"


def classify_confidence_band(uncertainty):

    if uncertainty < 0.3:
        return "HIGH"
    elif uncertainty < 0.6:
        return "MEDIUM"
    else:
        return "LOW"