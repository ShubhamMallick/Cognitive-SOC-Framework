from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import json

# Import dashboard backend
from Dashboard.dashboard_backend import (
    dashboard_backend,
    get_dashboard_summary,
    process_event,
    get_agent_metrics,
    get_system_health,
    get_threat_intelligence,
    get_learning_status
)

router = APIRouter()

# =====================================================
# DASHBOARD DATA MODELS
# =====================================================

class EventData(BaseModel):
    """Model for incoming SOC events"""
    device_id: str
    department: str
    criticality_level: int
    file_entropy_avg: float
    outbound_traffic_mb: float
    unique_external_ips: int
    dns_request_count: int
    process_spawn_count: int
    failed_auth_attempts: int
    privilege_escalation_flag: int
    configuration_change_flag: int
    antivirus_alert_flag: int
    network_segment: str = "STANDARD"
    security_posture: str = "MEDIUM"

class DashboardResponse(BaseModel):
    """Model for dashboard API responses"""
    success: bool
    data: Dict[str, Any] = {}
    message: str = ""
    timestamp: str

# =====================================================
# DASHBOARD MAIN ENDPOINTS
# =====================================================

@router.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard():
    """
    Get complete dashboard data including all metrics, alerts, and trends
    """
    try:
        dashboard_data = await get_dashboard_summary()
        return {
            "success": True,
            "data": dashboard_data,
            "message": "Dashboard data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard error: {str(e)}")

@router.post("/dashboard/event", response_model=Dict[str, Any])
async def process_soc_event(event: EventData):
    """
    Process a new SOC event through the complete agent pipeline
    """
    try:
        # Convert Pydantic model to dict
        event_data = event.dict()
        
        # Process event through dashboard backend
        result = await process_event(event_data)
        
        return {
            "success": True,
            "data": result,
            "message": "Event processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event processing error: {str(e)}")

# =====================================================
# DASHBOARD METRICS ENDPOINTS
# =====================================================

@router.get("/dashboard/metrics", response_model=Dict[str, Any])
async def get_dashboard_metrics():
    """
    Get detailed agent performance metrics
    """
    try:
        metrics = await get_agent_metrics()
        return {
            "success": True,
            "data": metrics,
            "message": "Metrics retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics error: {str(e)}")

@router.get("/dashboard/health", response_model=Dict[str, Any])
async def get_dashboard_health():
    """
    Get system health status
    """
    try:
        health = await get_system_health()
        return {
            "success": True,
            "data": health,
            "message": "Health status retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check error: {str(e)}")

@router.get("/dashboard/threats", response_model=Dict[str, Any])
async def get_threat_data():
    """
    Get threat intelligence and trend data
    """
    try:
        threats = await get_threat_intelligence()
        return {
            "success": True,
            "data": threats,
            "message": "Threat intelligence retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Threat intelligence error: {str(e)}")

@router.get("/dashboard/learning", response_model=Dict[str, Any])
async def get_learning_data():
    """
    Get learning and adaptation status
    """
    try:
        learning = await get_learning_status()
        return {
            "success": True,
            "data": learning,
            "message": "Learning status retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning status error: {str(e)}")

# =====================================================
# DASHBOARD SUMMARY ENDPOINTS
# =====================================================

@router.get("/dashboard/summary", response_model=Dict[str, Any])
async def get_dashboard_summary_data():
    """
    Get dashboard summary statistics
    """
    try:
        dashboard_data = dashboard_backend.get_dashboard_data()
        summary = dashboard_data.get("summary", {})
        
        return {
            "success": True,
            "data": summary,
            "message": "Summary statistics retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary error: {str(e)}")

@router.get("/dashboard/alerts", response_model=Dict[str, Any])
async def get_recent_alerts():
    """
    Get recent security alerts
    """
    try:
        dashboard_data = dashboard_backend.get_dashboard_data()
        alerts = dashboard_data.get("recent_alerts", [])
        
        return {
            "success": True,
            "data": alerts,
            "message": "Recent alerts retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alerts error: {str(e)}")

@router.get("/dashboard/performance", response_model=Dict[str, Any])
async def get_performance_data():
    """
    Get system performance metrics
    """
    try:
        dashboard_data = dashboard_backend.get_dashboard_data()
        performance = dashboard_data.get("agent_performance", {})
        
        return {
            "success": True,
            "data": performance,
            "message": "Performance data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance error: {str(e)}")

# =====================================================
# DASHBOARD REAL-TIME ENDPOINTS
# =====================================================

@router.get("/dashboard/realtime", response_model=Dict[str, Any])
async def get_realtime_data():
    """
    Get real-time dashboard data for live updates
    """
    try:
        dashboard_data = dashboard_backend.get_dashboard_data()
        
        # Extract real-time relevant data
        realtime_data = {
            "current_alerts": dashboard_data.get("recent_alerts", [])[-5:],  # Last 5 alerts
            "system_health": dashboard_data.get("system_health", {}),
            "current_metrics": dashboard_data.get("summary", {}),
            "timestamp": dashboard_data.get("timestamp")
        }
        
        return {
            "success": True,
            "data": realtime_data,
            "message": "Real-time data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Real-time data error: {str(e)}")

# =====================================================
# DASHBOARD CHART DATA ENDPOINTS
# =====================================================

@router.get("/dashboard/charts/threat-trends", response_model=Dict[str, Any])
async def get_threat_trends_chart():
    """
    Get threat trends data for chart visualization
    """
    try:
        trends = await get_threat_intelligence()
        
        chart_data = {
            "labels": [f"{hour:02d}:00" for hour in range(24)],
            "datasets": [
                {
                    "label": "Threat Count",
                    "data": [trends.get(hour, {}).get("threat_count", 0) for hour in range(24)],
                    "backgroundColor": "rgba(231, 76, 60, 0.2)",
                    "borderColor": "rgba(231, 76, 60, 1)",
                    "borderWidth": 2
                },
                {
                    "label": "Average Risk",
                    "data": [trends.get(hour, {}).get("average_risk", 0) for hour in range(24)],
                    "backgroundColor": "rgba(241, 196, 15, 0.2)",
                    "borderColor": "rgba(241, 196, 15, 1)",
                    "borderWidth": 2
                }
            ]
        }
        
        return {
            "success": True,
            "data": chart_data,
            "message": "Threat trends chart data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart data error: {str(e)}")

@router.get("/dashboard/charts/decision-distribution", response_model=Dict[str, Any])
async def get_decision_distribution_chart():
    """
    Get decision distribution data for chart visualization
    """
    try:
        dashboard_data = dashboard_backend.get_dashboard_data()
        distribution = dashboard_data.get("decision_distribution", {})
        
        # Flatten distribution data
        all_decisions = set()
        for hour_data in distribution.values():
            all_decisions.update(hour_data.keys())
        
        chart_data = {
            "labels": list(all_decisions),
            "datasets": []
        }
        
        # Create dataset for each decision type
        for decision in all_decisions:
            data = []
            for hour in range(24):
                data.append(distribution.get(hour, {}).get(decision, 0))
            
            chart_data["datasets"].append({
                "label": decision,
                "data": data,
                "backgroundColor": f"rgba({hash(decision) % 255}, {hash(decision * 2) % 255}, {hash(decision * 3) % 255}, 0.8)",
                "borderWidth": 2
            })
        
        return {
            "success": True,
            "data": chart_data,
            "message": "Decision distribution chart data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chart data error: {str(e)}")

@router.get("/dashboard/charts/performance", response_model=Dict[str, Any])
async def get_performance_chart():
    """
    Get performance metrics data for chart visualization
    """
    try:
        performance = await get_agent_metrics()
        
        chart_data = {
            "labels": ["Processing Time", "Fused Risk", "System Confidence"],
            "datasets": [
                {
                    "label": "Current Values",
                    "data": [
                        performance.get("processing_time", {}).get("current", 0),
                        performance.get("fused_risk", {}).get("current", 0),
                        performance.get("system_confidence", {}).get("current", 0)
                    ],
                    "backgroundColor": [
                        "rgba(52, 152, 219, 0.8)",
                        "rgba(231, 76, 60, 0.8)",
                        "rgba(46, 204, 113, 0.8)"
                    ],
                    "borderWidth": 2
                },
                {
                    "label": "Average Values",
                    "data": [
                        performance.get("processing_time", {}).get("average", 0),
                        performance.get("fused_risk", {}).get("average", 0),
                        performance.get("system_confidence", {}).get("average", 0)
                    ],
                    "backgroundColor": [
                        "rgba(52, 152, 219, 0.4)",
                        "rgba(231, 76, 60, 0.4)",
                        "rgba(46, 204, 113, 0.4)"
                    ],
                    "borderWidth": 2
                }
            ]
        }
        
        return {
            "success": True,
            "data": chart_data,
            "message": "Performance chart data retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Performance chart error: {str(e)}")
