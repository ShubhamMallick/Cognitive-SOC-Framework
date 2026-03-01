import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

# ============================================
# LOAD MODELS
# ============================================

rf = joblib.load("rf_anomaly_model.pkl")
iso = joblib.load("iso_anomaly_model.pkl")

# Load dataset only for categorical encoder reference
df_ref = pd.read_csv("uncertainty_aware_soc_dataset_30000_noisy.csv")

# Create encoders again
from sklearn.preprocessing import LabelEncoder
from Anomaly_Detection import run_detection

categorical_cols = ["device_id", "device_type", "department", "firmware_version"]
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    le.fit(df_ref[col])
    encoders[col] = le

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(page_title="Uncertainty-Aware SOC", layout="wide")
st.title("🚨 Uncertainty-Aware SOC Decision Engine")

# ============================================
# INPUT FORM
# ============================================

st.sidebar.header("Device Context")

device_id = st.sidebar.selectbox("Device ID", df_ref["device_id"].unique())
device_type = st.sidebar.selectbox("Device Type", df_ref["device_type"].unique())
department = st.sidebar.selectbox("Department", df_ref["department"].unique())
criticality_level = st.sidebar.slider("Criticality Level", 1, 5, 3)
firmware_version = st.sidebar.selectbox("Firmware Version", df_ref["firmware_version"].unique())

st.sidebar.header("System Metrics")

cpu = st.sidebar.slider("CPU Usage %", 0, 100, 40)
memory = st.sidebar.slider("Memory Usage %", 0, 100, 50)
disk_write = st.sidebar.slider("Disk Write MB/min", 0, 1500, 50)
disk_read = st.sidebar.slider("Disk Read MB/min", 0, 300, 80)
process_spawn = st.sidebar.slider("Process Spawn Count", 0, 100, 10)

st.sidebar.header("File System Metrics")

rename = st.sidebar.slider("File Rename Count", 0, 2000, 5)
new_files = st.sidebar.slider("New File Creation Count", 0, 1000, 10)
entropy = st.sidebar.slider("File Entropy Avg", 0.0, 8.0, 5.5)
encrypted_ratio = st.sidebar.slider("Encrypted Extension Ratio", 0.0, 1.0, 0.0)

st.sidebar.header("Network Metrics")

outbound = st.sidebar.slider("Outbound Traffic MB", 0, 1000, 20)
inbound = st.sidebar.slider("Inbound Traffic MB", 0, 200, 40)
unique_ips = st.sidebar.slider("Unique External IPs", 0, 50, 1)
dns = st.sidebar.slider("DNS Request Count", 0, 200, 10)
unusual_port = st.sidebar.selectbox("Unusual Port Flag", [0, 1])

st.sidebar.header("Security Signals")

privilege = st.sidebar.selectbox("Privilege Escalation", [0, 1])
config_change = st.sidebar.selectbox("Configuration Change", [0, 1])
antivirus = st.sidebar.selectbox("Antivirus Alert", [0, 1])
failed_auth = st.sidebar.slider("Failed Auth Attempts", 0, 20, 0)

# ============================================
# PREDICTION
# ============================================

if st.button("Analyze Device"):

    input_data = pd.DataFrame([{
        "device_id": device_id,
        "device_type": device_type,
        "department": department,
        "criticality_level": criticality_level,
        "firmware_version": firmware_version,
        "cpu_usage_percent": cpu,
        "memory_usage_percent": memory,
        "disk_write_mb_per_min": disk_write,
        "disk_read_mb_per_min": disk_read,
        "process_spawn_count": process_spawn,
        "file_rename_count": rename,
        "new_file_creation_count": new_files,
        "file_entropy_avg": entropy,
        "encrypted_extension_ratio": encrypted_ratio,
        "outbound_traffic_mb": outbound,
        "inbound_traffic_mb": inbound,
        "unique_external_ips": unique_ips,
        "dns_request_count": dns,
        "unusual_port_flag": unusual_port,
        "privilege_escalation_flag": privilege,
        "configuration_change_flag": config_change,
        "antivirus_alert_flag": antivirus,
        "failed_auth_attempts": failed_auth
    }])

    # Encode categorical
    for col in categorical_cols:
        input_data[col] = encoders[col].transform(input_data[col])

    # Run Detection
    detection_result = run_detection(input_data, rf, iso)
    prob = detection_result["anomaly_probability"]
    deviation = detection_result["deviation_score"]
    uncertainty = detection_result["uncertainty_score"]
    decision = detection_result["decision"]

    # ============================================
    # DISPLAY RESULTS
    # ============================================

    col1, col2, col3 = st.columns(3)

    col1.metric("Anomaly Probability", f"{prob:.3f}")
    col2.metric("Deviation Score", f"{deviation:.3f}")
    col3.metric("Uncertainty Score", f"{uncertainty:.3f}")

    st.subheader("SOC Decision")
    st.write(decision)

    # ============================================
    # FEATURE IMPORTANCE VISUALIZATION
    # ============================================

    st.subheader("Top Feature Contributions")

    importances = detection_result["top_features"]

    fig, ax = plt.subplots()
    pd.Series(importances).plot(kind="bar", ax=ax)
    ax.set_title("Top 10 Important Features")
    st.pyplot(fig)