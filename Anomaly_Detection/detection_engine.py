import numpy as np
import pandas as pd


def run_detection(input_df, rf, iso):

    # Supervised probability
    prob = rf.predict_proba(input_df)[0][1]

    # Isolation Forest deviation
    deviation = -iso.decision_function(input_df)[0]
    deviation = deviation / (1 + deviation)

    # Uncertainty computation
    epsilon = 1e-9
    entropy_score = -(
        prob * np.log(prob + epsilon) +
        (1 - prob) * np.log(1 - prob + epsilon)
    )

    disagreement = abs(prob - deviation)
    uncertainty = (entropy_score + disagreement) / 2

    # SOC Decision Logic
    if prob > 0.9:
        decision = "AUTO-CONTAIN"
    elif prob > 0.75 and uncertainty < 0.4:
        decision = "AUTO-CONTAIN (High Confidence)"
    elif uncertainty > 0.45:
        decision = "ESCALATE TO HUMAN"
    else:
        decision = "MONITOR"

    # Feature Importance
    importances = pd.Series(
        rf.feature_importances_,
        index=input_df.columns
    ).sort_values(ascending=False).head(10)

    return {
        "anomaly_probability": float(prob),
        "deviation_score": float(deviation),
        "uncertainty_score": float(uncertainty),
        "decision": decision,
        "top_features": importances.to_dict()
    }