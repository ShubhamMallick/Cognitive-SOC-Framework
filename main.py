from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Import detection + context modules
from Anomaly_Detection import run_detection
from Anomaly_Detection.Context_Framing import ContextFramingEngine


# =====================================================
# FASTAPI INITIALIZATION
# =====================================================

app = FastAPI(title="Uncertainty-Aware SOC Framework")

context_engine = ContextFramingEngine()


# =====================================================
# LOAD MODELS
# =====================================================

rf = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "rf_anomaly_model.pkl"))
iso = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "iso_anomaly_model.pkl"))

df_ref = pd.read_csv(
    os.path.join(BASE_DIR, "Anomaly_Detection", "uncertainty_aware_soc_dataset_30000_noisy.csv")
)

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


# =====================================================
# PYDANTIC INPUT MODEL
# =====================================================

class DeviceData(BaseModel):
    device_id: str
    device_type: str
    department: str
    criticality_level: int
    firmware_version: str

    cpu_usage_percent: float
    memory_usage_percent: float
    disk_write_mb_per_min: float
    disk_read_mb_per_min: float
    process_spawn_count: int

    file_rename_count: int
    new_file_creation_count: int
    file_entropy_avg: float
    encrypted_extension_ratio: float

    outbound_traffic_mb: float
    inbound_traffic_mb: float
    unique_external_ips: int
    dns_request_count: int
    unusual_port_flag: int

    privilege_escalation_flag: int
    configuration_change_flag: int
    antivirus_alert_flag: int
    failed_auth_attempts: int


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# =====================================================
# RESULTS ROUTE
# =====================================================

@app.get("/results")
async def show_results(request: Request, data: str):
    result = json.loads(data)
    return templates.TemplateResponse("results.html", {"request": request, "result": result})


# =====================================================
# ANALYZE ROUTE
# =====================================================

@app.post("/analyze")
def analyze_device(data: DeviceData):

    try:
        # Convert input to dictionary
        input_dict = data.dict()

        # Convert to DataFrame
        input_df = pd.DataFrame([input_dict])

        # Encode categorical columns
        for col in categorical_cols:
            input_df[col] = encoders[col].transform(input_df[col])

        # ==============================
        # Run Anomaly Detection
        # ==============================

        detection_result = run_detection(input_df, rf, iso)

        # ==============================
        # Run Context Framing
        # ==============================

        context_result = context_engine.frame_context(
            anomaly_prob=detection_result["anomaly_probability"],
            deviation_score=detection_result["deviation_score"],
            uncertainty=detection_result["uncertainty_score"],
            features=input_dict
        )

        # ==============================
        # Combine Results
        # ==============================

        return JSONResponse({
            "detection": detection_result,
            "context": context_result
        })

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )