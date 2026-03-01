from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from Anomaly_Detection import run_detection
from Context_Framing import ContextFramingEngine

# ============================================
# INITIALIZE APP
# ============================================

app = Flask(__name__)

# ============================================
# LOAD MODELS
# ============================================

rf = joblib.load("rf_anomaly_model.pkl")
iso = joblib.load("iso_anomaly_model.pkl")

# ============================================
# LOAD DATASET FOR ENCODERS
# ============================================

df_ref = pd.read_csv("uncertainty_aware_soc_dataset_30000_noisy.csv")

categorical_cols = [
    "device_id",
    "device_type",
    "department",
    "firmware_version"
]

encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    le.fit(df_ref[col])
    encoders[col] = le


# ============================================
# HEALTH CHECK ROUTE
# ============================================

@app.route("/")
def home():
    return jsonify({"message": "Uncertainty-Aware SOC Backend Running"})


# ============================================
# MAIN ANALYSIS ROUTE
# ============================================

@app.route("/analyze", methods=["POST"])
def analyze_device():

    try:
        data = request.json

        input_data = pd.DataFrame([data])

        # Encode categorical features
        for col in categorical_cols:
            input_data[col] = encoders[col].transform(input_data[col])

        # Run Detection
        detection_result = run_detection(input_data, rf, iso)
        prob = detection_result["anomaly_probability"]
        deviation = detection_result["deviation_score"]
        uncertainty = detection_result["uncertainty_score"]

        # ============================================
        # Context Framing
        # ============================================

        features = input_data.iloc[0].to_dict()
        context_engine = ContextFramingEngine()
        context_result = context_engine.frame_context(prob, deviation, uncertainty, features)

        detection_result.update(context_result)

        return jsonify(detection_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    app.run(debug=True)