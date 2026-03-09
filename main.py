from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import os
import json
import asyncio

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# =====================================================
# IMPORT DETECTION + CONTEXT MODULES
# =====================================================

from Anomaly_Detection import run_detection
from Anomaly_Detection.Context_Framing import ContextFramingEngine

# =====================================================
# IMPORT CONTEXT EXPLANATION ROUTER
# =====================================================

from routers.context_explain_router import router as context_router

# =====================================================
# IMPORT POLICY EXPLANATION ROUTER
# =====================================================

from routers.policy_explain_router import router as policy_router
from routers.threat_explain_router import router as threat_router
from routers.impact_explain_router import router as impact_router
from routers.privacy_explain_router import router as privacy_router
from routers.risk_explain_router import router as risk_router
from routers.coordinate_explain_router import router as coordinate_router
from routers.authority_explain_router import router as authority_router
from routers.audit_explain_router import router as audit_router
from routers.execution_explain_router import router as execution_router

# =====================================================
# IMPORT AGENTS
# =====================================================

from Agents.policy_agent import policy_agent
from Agents.threat_agent import threat_agent
from Agents.impact_agent import impact_agent
from Agents.privacy_agent import privacy_agent
from Agents.risk_failure_agent import risk_failure_agent
from Agents.coordination_engine import coordination_engine
from Agents.authority_agent import authority_agent

# Execution Agents
from Agents.containment_agent import containment_agent
from Agents.safe_pass_agent import safe_pass_agent
from Agents.human_review_agent import human_review_agent
from Agents.adaptive_monitoring_agent import adaptive_monitoring_agent
from Agents.audit_memory_agent import audit_memory_agent
from Agents.outcome_feedback_agent import outcome_feedback_agent

from Agents.reinforcement_learning_agent import adaptive_policy

# =====================================================
# IMPORT SIMPLE AUDIO ALERTS
# =====================================================

from Utilities.simple_audio_alerts import audio_alerts

# =====================================================
# FASTAPI INITIALIZATION
# =====================================================

app = FastAPI(title="Uncertainty-Aware SOC Framework")

# Register router for LLM explanations
app.include_router(context_router)
app.include_router(policy_router)
app.include_router(threat_router)
app.include_router(impact_router)
app.include_router(privacy_router)
app.include_router(risk_router)
app.include_router(coordinate_router)
app.include_router(authority_router)
app.include_router(audit_router)
app.include_router(execution_router)

context_engine = ContextFramingEngine()
agent_results = {}

# =====================================================
# LOAD MODELS
# =====================================================

rf = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "rf_anomaly_model.pkl"))
iso = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "iso_anomaly_model.pkl"))

df_ref = pd.read_csv(
    os.path.join(BASE_DIR, "Anomaly_Detection", "uncertainty_aware_soc_dataset_30000_noisy.csv")
)

categorical_cols = ["device_id", "device_type", "department", "firmware_version"]
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
# HOME ROUTE
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
# CORE PIPELINE
# =====================================================

async def run_agents_parallel(raw_features, detection_result, context_result):

    # -------------------------------------------------
    # 1️⃣ Parallel Agents
    # -------------------------------------------------

    policy_task = asyncio.to_thread(policy_agent, raw_features, detection_result, context_result)
    threat_task = asyncio.to_thread(threat_agent, raw_features, detection_result, context_result)
    impact_task = asyncio.to_thread(impact_agent, raw_features, detection_result, context_result)
    privacy_task = asyncio.to_thread(privacy_agent, raw_features, detection_result, context_result)

    policy_result, threat_result, impact_result, privacy_result = await asyncio.gather(
        policy_task, threat_task, impact_task, privacy_task
    )

    agent_results["policy"] = policy_result
    agent_results["threat"] = threat_result
    agent_results["impact"] = impact_result
    agent_results["privacy"] = privacy_result

    # -------------------------------------------------
    # 2️⃣ Risk & Failure
    # -------------------------------------------------

    risk_result = risk_failure_agent(
        raw=raw_features,
        detection=detection_result,
        context=context_result,
        policy=policy_result,
        threat=threat_result,
        impact=impact_result,
        privacy=privacy_result
    )

    agent_results["risk"] = risk_result

    # -------------------------------------------------
    # 3️⃣ Coordination
    # -------------------------------------------------

    coordination_result = coordination_engine(
        raw=raw_features,
        detection=detection_result,
        context=context_result,
        policy=policy_result,
        threat=threat_result,
        impact=impact_result,
        privacy=privacy_result,
        risk=risk_result
    )

    agent_results["coordination"] = coordination_result

    # -------------------------------------------------
    # 4️⃣ Authority
    # -------------------------------------------------

    authority_result = authority_agent(
        raw=raw_features,
        detection=detection_result,
        context=context_result,
        risk=risk_result,
        coordination=coordination_result
    )

    agent_results["authority"] = authority_result

    # -------------------------------------------------
    # 5️⃣ Execution Layer
    # -------------------------------------------------

    decision = authority_result["final_decision"]

    if decision == "EXECUTE_AUTOMATED_CONTAINMENT":
        execution_result = containment_agent(raw_features, authority_result)

    elif decision == "HUMAN_ANALYST_REVIEW":
        execution_result = human_review_agent(raw_features, authority_result)

    elif decision == "ADAPTIVE_MONITORING_MODE":
        execution_result = adaptive_monitoring_agent(raw_features, authority_result)

    else:
        execution_result = safe_pass_agent(raw_features, authority_result)

    agent_results["execution"] = execution_result

    # -------------------------------------------------
    # 6️⃣ Audit & Incident Memory
    # -------------------------------------------------

    audit_result = audit_memory_agent(
        raw=raw_features,
        detection=detection_result,
        context=context_result,
        risk=risk_result,
        coordination=coordination_result,
        authority=authority_result,
        execution=execution_result
    )

    agent_results["audit"] = audit_result

    # -------------------------------------------------
    # 7️⃣ Outcome & Feedback Agent
    # -------------------------------------------------

    outcome_result = outcome_feedback_agent(
        raw=raw_features,
        detection=detection_result,
        coordination=coordination_result,
        authority=authority_result,
        execution=execution_result,
        audit=audit_result
    )

    agent_results["outcome"] = outcome_result

    # -------------------------------------------------
    # 🎵 AUDIO ALERT: Pipeline Complete
    # -------------------------------------------------

    final_decision = authority_result["final_decision"]
    confidence = authority_result.get("decision_confidence")

    # Speak normal sentence about final result
    audio_alerts.alert_pipeline_complete(final_decision, confidence)


# =====================================================
# ANALYZE ROUTE
# =====================================================

@app.post("/analyze")
async def analyze_device(data: DeviceData):

    try:
        input_dict = data.dict()
        input_df = pd.DataFrame([input_dict])

        for col in categorical_cols:
            input_df[col] = encoders[col].transform(input_df[col])

        detection_result = run_detection(input_df, rf, iso)

        context_result = context_engine.frame_context(
            anomaly_prob=detection_result["anomaly_probability"],
            deviation_score=detection_result["deviation_score"],
            uncertainty=detection_result["uncertainty_score"],
            features=input_dict
        )

        await run_agents_parallel(input_dict, detection_result, context_result)

        # Store detection and context results for template access
        agent_results["detection"] = detection_result
        agent_results["context"] = context_result
        agent_results["raw"] = input_dict

        return JSONResponse({
            "detection": detection_result,
            "context": context_result
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


# =====================================================
# HTML ENDPOINTS
# =====================================================

@app.get("/policy")
async def show_policy(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "policy": agent_results.get("policy", {})
    }
    return templates.TemplateResponse("policy.html", {"request": request, "result": complete_result})

@app.get("/threat")
async def show_threat(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "threat": agent_results.get("threat", {})
    }
    return templates.TemplateResponse("threat.html", {"request": request, "result": complete_result})

@app.get("/impact")
async def show_impact(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "impact": agent_results.get("impact", {})
    }
    return templates.TemplateResponse("impact.html", {"request": request, "result": complete_result})

@app.get("/privacy")
async def show_privacy(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "privacy": agent_results.get("privacy", {})
    }
    return templates.TemplateResponse("privacy.html", {"request": request, "result": complete_result})

@app.get("/risk")
async def show_risk(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "policy": agent_results.get("policy", {}),
        "threat": agent_results.get("threat", {}),
        "impact": agent_results.get("impact", {}),
        "privacy": agent_results.get("privacy", {}),
        "risk": agent_results.get("risk", {})
    }
    return templates.TemplateResponse("risk_failure.html", {"request": request, "result": complete_result})

@app.get("/coordinate")
async def show_coordination(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "policy": agent_results.get("policy", {}),
        "threat": agent_results.get("threat", {}),
        "impact": agent_results.get("impact", {}),
        "privacy": agent_results.get("privacy", {}),
        "risk": agent_results.get("risk", {}),
        "coordinate": agent_results.get("coordination", {})
    }
    return templates.TemplateResponse("coordinate.html", {"request": request, "result": complete_result})

@app.get("/authority")
async def show_authority(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "risk": agent_results.get("risk", {}),
        "coordinate": agent_results.get("coordination", {}),
        "authority": agent_results.get("authority", {})
    }
    return templates.TemplateResponse("authority.html", {"request": request, "result": complete_result})

@app.get("/execution")
async def show_execution(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "authority": agent_results.get("authority", {}),
        "execution": agent_results.get("execution", {})
    }
    return templates.TemplateResponse("execution.html", {"request": request, "result": complete_result})

@app.get("/audit")
async def show_audit(request: Request):
    # Construct complete data structure for LLM explanations
    complete_result = {
        "raw": agent_results.get("raw", {}),
        "detection": agent_results.get("detection", {}),
        "context": agent_results.get("context", {}),
        "risk": agent_results.get("risk", {}),
        "coordinate": agent_results.get("coordination", {}),
        "authority": agent_results.get("authority", {}),
        "execution": agent_results.get("execution", {}),
        "audit": agent_results.get("audit", {})
    }
    return templates.TemplateResponse(
        "audit.html",
        {"request": request, "result": complete_result}
    )

@app.get("/outcome")
async def show_outcome(request: Request):
    return templates.TemplateResponse(
        "outcome.html",
        {"request": request, "result": agent_results.get("outcome")}
    )