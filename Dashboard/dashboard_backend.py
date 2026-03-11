"""
SOC Dashboard Backend Service
Aggregates and processes data from all SOC agents for dashboard visualization
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict, deque
import statistics
import numpy as np

# Import all SOC agents
from Agents.threat_agent import threat_agent
from Agents.risk_failure_agent import risk_failure_agent
from Agents.containment_agent import containment_agent
from Agents.outcome_feedback_agent import outcome_feedback_agent
from Agents.reinforcement_learning_agent import reinforcement_learning_agent, adaptive_policy, learning_memory
from Agents.audit_memory_agent import audit_memory_agent
from Agents.policy_agent import policy_agent
from Agents.impact_agent import impact_agent
from Agents.privacy_agent import privacy_agent
from Agents.human_review_agent import human_review_agent
from Agents.adaptive_monitoring_agent import adaptive_monitoring_agent
from Agents.safe_pass_agent import safe_pass_agent
from Agents.authority_agent import authority_agent

# Import anomaly detection
from Anomaly_Detection.detection_engine import run_detection

class DashboardBackend:
    """
    Central dashboard backend that aggregates data from all SOC agents
    and provides endpoints for dashboard visualization
    """
    
    def __init__(self):
        self.agent_results = deque(maxlen=1000)  # Store last 1000 agent results
        self.system_metrics = defaultdict(list)
        self.alert_history = deque(maxlen=500)
        self.performance_metrics = defaultdict(deque)
        self.learning_progress = deque(maxlen=200)
        
    async def process_soc_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a SOC event and update dashboard metrics"""
        try:
            timestamp = datetime.now()
            
            # Store the processed event data directly (no need to re-run pipeline)
            full_results = {
                "timestamp": timestamp.isoformat(),
                "raw": event_data.get("raw_data", {}),
                "detection": event_data.get("detection", {}),
                "context": event_data.get("context", {}),
                "policy": event_data.get("policy", {}),
                "threat": event_data.get("threat", {}),
                "impact": event_data.get("impact", {}),
                "privacy": event_data.get("privacy", {}),
                "risk": event_data.get("risk", {}),
                "coordination": event_data.get("coordination", {}),
                "authority": event_data.get("authority", {}),
                "execution": event_data.get("execution", {}),
                "audit": event_data.get("audit", {}),
                "outcome": event_data.get("outcome", {})
            }
            
            # Update system metrics
            await self._update_metrics(full_results)
            
            return {
                "success": True,
                "timestamp": timestamp.isoformat(),
                "event_id": f"event_{int(timestamp.timestamp())}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _run_anomaly_detection(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run anomaly detection pipeline"""
        try:
            # Extract features for anomaly detection
            features = [
                raw_data.get("file_entropy_avg", 0),
                raw_data.get("outbound_traffic_mb", 0),
                raw_data.get("unique_external_ips", 0),
                raw_data.get("dns_request_count", 0),
                raw_data.get("process_spawn_count", 0),
                raw_data.get("failed_auth_attempts", 0),
                raw_data.get("privilege_escalation_flag", 0),
                raw_data.get("configuration_change_flag", 0),
                raw_data.get("antivirus_alert_flag", 0)
            ]
            
            # Create DataFrame for detection
            import pandas as pd
            feature_df = pd.DataFrame([features])
            
            # Load models (simplified for dashboard)
            import joblib
            import os
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            try:
                rf = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "rf_anomaly_model.pkl"))
                iso = joblib.load(os.path.join(BASE_DIR, "Anomaly_Detection", "iso_anomaly_model.pkl"))
                
                # Run anomaly detection
                detection_results = run_detection(feature_df, rf, iso)
                
                return {
                    "anomaly_probability": float(detection_results.get("anomaly_probability", 0)),
                    "uncertainty_score": float(detection_results.get("uncertainty", 0.5)),
                    "feature_contributions": {},
                    "detection_confidence": 1 - float(detection_results.get("uncertainty", 0.5))
                }
            except Exception as model_error:
                # Fallback if models can't be loaded
                return {
                    "anomaly_probability": 0.3,
                    "uncertainty_score": 0.5,
                    "feature_contributions": {},
                    "error": f"Model loading error: {str(model_error)}"
                }
            
        except Exception as e:
            return {
                "anomaly_probability": 0.0,
                "uncertainty_score": 0.5,
                "feature_contributions": {},
                "error": str(e)
            }
    
    async def _analyze_context(self, raw_data: Dict[str, Any], detection: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze contextual risk factors"""
        try:
            # Department-based risk weighting
            department_risk = {
                "ICU": 0.9, "ER": 0.85, "Radiology": 0.8,
                "Cardiology": 0.75, "Surgery": 0.7, "Pharmacy": 0.6,
                "Administration": 0.4, "IT": 0.5
            }
            
            department = raw_data.get("department", "IT")
            dept_risk = department_risk.get(department, 0.5)
            
            # Criticality-based weighting
            criticality_risk = raw_data.get("criticality_level", 1) / 5.0
            
            # Time-based risk (business hours vs off-hours)
            current_hour = datetime.now().hour
            time_risk = 0.7 if 9 <= current_hour <= 17 else 0.9
            
            # Network context risk
            network_modifier = 1.0 if raw_data.get("network_segment") == "CRITICAL" else 0.8
            
            # Security posture
            security_modifier = 0.8 if raw_data.get("security_posture") == "HIGH" else 1.0
            
            # Final contextual risk
            final_contextual_risk = (
                0.4 * dept_risk +
                0.3 * criticality_risk +
                0.2 * time_risk +
                0.1 * network_modifier
            ) * security_modifier
            
            return {
                "department": department,
                "department_risk": dept_risk,
                "criticality_risk": criticality_risk,
                "time_risk": time_risk,
                "network_modifier": network_modifier,
                "security_modifier": security_modifier,
                "final_contextual_risk": round(final_contextual_risk, 4)
            }
            
        except Exception as e:
            return {
                "department": raw_data.get("department", "UNKNOWN"),
                "final_contextual_risk": 0.5,
                "error": str(e)
            }
    
    async def _run_agent_pipeline(self, raw_data: Dict[str, Any], 
                                 detection: Dict[str, Any], 
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Run all analysis agents"""
        try:
            # Run threat analysis
            threat_results = threat_agent(raw_data, detection, context)
            
            # Run policy analysis
            policy_results = policy_agent(raw_data, detection, context)
            
            # Run impact analysis
            impact_results = impact_agent(raw_data, detection, context)
            
            # Run privacy analysis
            privacy_results = privacy_agent(raw_data, detection, context)
            
            return {
                "threat": threat_results,
                "policy": policy_results,
                "impact": impact_results,
                "privacy": privacy_results
            }
            
        except Exception as e:
            return {
                "threat": {"error": str(e)},
                "policy": {"error": str(e)},
                "impact": {"error": str(e)},
                "privacy": {"error": str(e)}
            }
    
    async def _coordinate_agents(self, agents: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate between different agent outputs"""
        try:
            threat = agents.get("threat", {})
            policy = agents.get("policy", {})
            impact = agents.get("impact", {})
            privacy = agents.get("privacy", {})
            
            # Extract risk scores
            threat_score = max(threat.get("ransomware_probability", 0), 
                             threat.get("exfiltration_probability", 0))
            policy_score = policy.get("policy_risk_score", 0)
            impact_score = impact.get("impact_score", 0)
            privacy_score = privacy.get("privacy_risk_score", 0)
            
            # Calculate fused risk score
            fused_risk = (
                0.3 * threat_score +
                0.25 * policy_score +
                0.25 * impact_score +
                0.2 * privacy_score
            )
            
            # Calculate system confidence
            confidence_scores = [
                1 - 0.5,  # detection confidence (placeholder)
                1 - 0.5,  # policy confidence
                1 - 0.5,  # impact confidence
                1 - 0.5   # privacy confidence
            ]
            system_confidence = statistics.mean(confidence_scores)
            
            # Determine threat stage
            if fused_risk >= 0.8:
                threat_stage = "CRITICAL COMPROMISE"
            elif fused_risk >= 0.6:
                threat_stage = "ACTIVE THREAT"
            elif fused_risk >= 0.4:
                threat_stage = "SUSPICIOUS ACTIVITY"
            else:
                threat_stage = "MONITORING"
            
            # Recommended action
            if threat_stage == "CRITICAL COMPROMISE":
                recommended_action = "IMMEDIATE_CONTAINMENT"
            elif threat_stage == "ACTIVE THREAT":
                recommended_action = "ESCALATE_TO_HUMAN_ANALYST"
            elif threat_stage == "SUSPICIOUS ACTIVITY":
                recommended_action = "ADAPTIVE_MONITORING"
            else:
                recommended_action = "SAFE_PASS"
            
            return {
                "fused_risk_score": round(fused_risk, 4),
                "system_confidence": round(system_confidence, 4),
                "threat_stage": threat_stage,
                "recommended_action": recommended_action,
                "agent_scores": {
                    "threat": round(threat_score, 4),
                    "policy": round(policy_score, 4),
                    "impact": round(impact_score, 4),
                    "privacy": round(privacy_score, 4)
                }
            }
            
        except Exception as e:
            return {
                "fused_risk_score": 0.5,
                "system_confidence": 0.5,
                "threat_stage": "UNKNOWN",
                "recommended_action": "SAFE_PASS",
                "error": str(e)
            }
    
    async def _analyze_risk_failure(self, raw_data: Dict[str, Any],
                                  detection: Dict[str, Any],
                                  context: Dict[str, Any],
                                  agents: Dict[str, Any]) -> Dict[str, Any]:
        """Run risk and failure analysis"""
        try:
            return risk_failure_agent(
                raw_data, detection, context,
                agents.get("policy", {}),
                agents.get("threat", {}),
                agents.get("impact", {}),
                agents.get("privacy", {})
            )
        except Exception as e:
            return {
                "instability_score": 0.5,
                "automation_safe": True,
                "failure_mode": "STABLE",
                "error": str(e)
            }
    
    async def _make_authority_decision(self, raw_data: Dict[str, Any],
                                     detection: Dict[str, Any],
                                     context: Dict[str, Any],
                                     risk: Dict[str, Any],
                                     coordination: Dict[str, Any]) -> Dict[str, Any]:
        """Make final authority decision"""
        try:
            return authority_agent(raw_data, detection, context, risk, coordination)
        except Exception as e:
            return {
                "final_decision": "SAFE_PASS",
                "execution_mode": "AUTOMATED",
                "severity_level": "LOW",
                "error": str(e)
            }
    
    async def _execute_decision(self, raw_data: Dict[str, Any],
                              authority: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the authority decision"""
        try:
            decision = authority.get("final_decision", "SAFE_PASS")
            
            if decision == "EXECUTE_AUTOMATED_CONTAINMENT":
                return containment_agent(raw_data, authority)
            elif decision == "HUMAN_ANALYST_REVIEW":
                return human_review_agent(raw_data, authority)
            elif decision == "ADAPTIVE_MONITORING_MODE":
                return adaptive_monitoring_agent(raw_data, authority)
            else:
                return safe_pass_agent(raw_data, authority)
                
        except Exception as e:
            return {
                "status": "EXECUTION_ERROR",
                "error": str(e)
            }
    
    async def _audit_decision(self, raw_data: Dict[str, Any],
                            detection: Dict[str, Any],
                            context: Dict[str, Any],
                            risk: Dict[str, Any],
                            coordination: Dict[str, Any],
                            authority: Dict[str, Any],
                            execution: Dict[str, Any]) -> Dict[str, Any]:
        """Audit the decision process"""
        try:
            return audit_memory_agent(
                raw_data, detection, context, risk, coordination, authority, execution
            )
        except Exception as e:
            return {
                "final_decision": "SAFE_PASS",
                "execution_mode": "AUTOMATED",
                "severity_level": "LOW",
                "error": str(e)
            }
    
    async def _evaluate_outcome(self, raw_data: Dict[str, Any],
                              detection: Dict[str, Any],
                              coordination: Dict[str, Any],
                              authority: Dict[str, Any],
                              execution: Dict[str, Any],
                              audit: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate decision outcome"""
        try:
            return outcome_feedback_agent(
                raw_data, detection, coordination, authority, execution, audit
            )
        except Exception as e:
            return {
                "actual_threat_detected": False,
                "reward_signal": 0.0,
                "learning_memory_size": 0,
                "error": str(e)
            }
    
    async def _update_learning(self):
        """Update reinforcement learning"""
        try:
            reinforcement_learning_agent()
        except Exception as e:
            print(f"Learning update error: {e}")
    
    async def _update_metrics(self, results: Dict[str, Any]):
        """Update system metrics"""
        try:
            timestamp = results.get("timestamp")
            
            # Store full results
            self.agent_results.append(results)
            
            # Update alert history
            if results.get("authority", {}).get("severity_level") in ["CRITICAL", "HIGH"]:
                self.alert_history.append({
                    "timestamp": timestamp,
                    "severity": results["authority"]["severity_level"],
                    "decision": results["authority"]["final_decision"],
                    "device_id": results["raw"].get("device_id")
                })
            
            # Update performance metrics
            self.performance_metrics["processing_time"].append(
                datetime.now().timestamp() - datetime.fromisoformat(timestamp).timestamp()
            )
            self.performance_metrics["fused_risk"].append(
                results["coordination"]["fused_risk_score"]
            )
            self.performance_metrics["system_confidence"].append(
                results["coordination"]["system_confidence"]
            )
            
            # Update learning progress
            if "outcome" in results:
                self.learning_progress.append({
                    "timestamp": timestamp,
                    "reward_signal": results["outcome"]["reward_signal"],
                    "learning_memory_size": results["outcome"]["learning_memory_size"]
                })
            
        except Exception as e:
            print(f"Metrics update error: {e}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get aggregated dashboard data"""
        try:
            return {
                "summary": self._get_summary_metrics(),
                "recent_alerts": list(self.alert_history)[-10:],
                "agent_performance": self._get_agent_performance(),
                "learning_progress": list(self.learning_progress)[-20:],
                "system_health": self._get_system_health(),
                "threat_trends": self._get_threat_trends(),
                "decision_distribution": self._get_decision_distribution(),
                "adaptive_policies": adaptive_policy,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_summary_metrics(self) -> Dict[str, Any]:
        """Get summary metrics"""
        try:
            if not self.agent_results:
                return {
                    "total_events": 0,
                    "severity_distribution": {},
                    "decision_distribution": {},
                    "average_risk": 0.0,
                    "average_confidence": 0.0,
                    "critical_alerts": 0,
                    "high_alerts": 0
                }
            
            recent_results = list(self.agent_results)[-100:]  # Last 100 events
            
            # Count severity levels
            severity_counts = defaultdict(int)
            decision_counts = defaultdict(int)
            total_risk = 0
            total_confidence = 0
            
            for result in recent_results:
                authority = result.get("authority", {})
                coordination = result.get("coordination", {})
                
                severity_counts[authority.get("severity_level", "UNKNOWN")] += 1
                decision_counts[authority.get("final_decision", "UNKNOWN")] += 1
                total_risk += coordination.get("fused_risk_score", 0)
                total_confidence += coordination.get("system_confidence", 0)
            
            return {
                "total_events": len(recent_results),
                "severity_distribution": dict(severity_counts),
                "decision_distribution": dict(decision_counts),
                "average_risk": round(total_risk / len(recent_results), 4) if recent_results else 0,
                "average_confidence": round(total_confidence / len(recent_results), 4) if recent_results else 0,
                "critical_alerts": severity_counts.get("CRITICAL", 0),
                "high_alerts": severity_counts.get("HIGH", 0)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_agent_performance(self) -> Dict[str, Any]:
        """Get agent performance metrics"""
        try:
            performance = {}
            
            for metric_name, values in self.performance_metrics.items():
                if values:
                    values_list = list(values)
                    performance[metric_name] = {
                        "current": round(values_list[-1], 4),
                        "average": round(statistics.mean(values_list), 4),
                        "min": round(min(values_list), 4),
                        "max": round(max(values_list), 4),
                        "trend": "increasing" if len(values_list) > 1 and values_list[-1] > values_list[-2] else "decreasing"
                    }
                else:
                    performance[metric_name] = {
                        "current": 0, "average": 0, "min": 0, "max": 0, "trend": "stable"
                    }
            
            return performance
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        try:
            if not self.agent_results:
                return {
                    "status": "NO_DATA",
                    "health_score": 0.0,
                    "automation_safe_rate": 0.0,
                    "override_rate": 0.0,
                    "average_instability": 0.0,
                    "total_events": 0
                }
            
            recent_results = list(self.agent_results)[-50:]  # Last 50 events
            
            # Calculate health metrics
            automation_safe_count = sum(
                1 for result in recent_results
                if result.get("risk", {}).get("automation_safe", False)
            )
            
            override_triggered_count = sum(
                1 for result in recent_results
                if result.get("authority", {}).get("override_triggered", False)
            )
            
            avg_instability = statistics.mean([
                result.get("risk", {}).get("instability_score", 0.5)
                for result in recent_results
            ])
            
            # Determine health status
            health_score = (automation_safe_count / len(recent_results)) * 100
            if health_score >= 80:
                status = "HEALTHY"
            elif health_score >= 60:
                status = "WARNING"
            else:
                status = "CRITICAL"
            
            return {
                "status": status,
                "health_score": round(health_score, 2),
                "automation_safe_rate": round(automation_safe_count / len(recent_results), 4),
                "override_rate": round(override_triggered_count / len(recent_results), 4),
                "average_instability": round(avg_instability, 4),
                "total_events": len(recent_results)
            }
            
        except Exception as e:
            return {"error": str(e), "status": "ERROR"}
    
    def _get_threat_trends(self) -> Dict[str, Any]:
        """Get threat trend analysis"""
        try:
            if not self.agent_results:
                return {
                    "hourly_threats": {},
                    "hourly_risk": {},
                    "trend_data": []
                }
            
            recent_results = list(self.agent_results)[-100:]
            
            # Group by hour
            hourly_threats = defaultdict(list)
            hourly_risk = defaultdict(list)
            
            for result in recent_results:
                timestamp = result.get("timestamp")
                if timestamp:
                    hour = datetime.fromisoformat(timestamp).hour
                    threat = result.get("threat", {})
                    risk = result.get("coordination", {}).get("fused_risk_score", 0)
                    
                    hourly_threats[hour].append(threat.get("ransomware_probability", 0))
                    hourly_risk[hour].append(risk)
            
            # Calculate hourly averages
            hourly_avg_threats = {}
            hourly_avg_risk = {}
            
            for hour in range(24):
                if hour in hourly_threats:
                    hourly_avg_threats[hour] = statistics.mean(hourly_threats[hour])
                    hourly_avg_risk[hour] = statistics.mean(hourly_risk[hour])
                else:
                    hourly_avg_threats[hour] = 0
                    hourly_avg_risk[hour] = 0
            
            return {
                "hourly_threats": hourly_avg_threats,
                "hourly_risk": hourly_avg_risk,
                "trend_data": [
                    {"hour": h, "threat": hourly_avg_threats[h], "risk": hourly_avg_risk[h]}
                    for h in range(24)
                ]
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_decision_distribution(self) -> Dict[str, Any]:
        """Get decision distribution over time"""
        try:
            if not self.agent_results:
                return {
                    "decisions": {},
                    "execution_modes": {},
                    "severity_levels": {}
                }
            
            recent_results = list(self.agent_results)[-50:]
            
            # Count decisions
            decision_counts = defaultdict(int)
            execution_counts = defaultdict(int)
            severity_counts = defaultdict(int)
            
            for result in recent_results:
                authority = result.get("authority", {})
                execution = result.get("execution", {})
                
                decision_counts[authority.get("final_decision", "UNKNOWN")] += 1
                execution_counts[authority.get("execution_mode", "UNKNOWN")] += 1
                severity_counts[authority.get("severity_level", "UNKNOWN")] += 1
            
            return {
                "decisions": dict(decision_counts),
                "execution_modes": dict(execution_counts),
                "severity_levels": dict(severity_counts)
            }
            
        except Exception as e:
            return {"error": str(e)}

# Global dashboard instance
dashboard_backend = DashboardBackend()

# Dashboard API endpoints
async def get_dashboard_summary():
    """Get dashboard summary"""
    return dashboard_backend.get_dashboard_data()

async def process_event(event_data: Dict[str, Any]):
    """Process a SOC event"""
    return await dashboard_backend.process_soc_event(event_data)

async def get_agent_metrics():
    """Get detailed agent metrics"""
    return dashboard_backend._get_agent_performance()

async def get_system_health():
    """Get system health status"""
    return dashboard_backend._get_system_health()

async def get_threat_intelligence():
    """Get threat intelligence data"""
    return dashboard_backend._get_threat_trends()

async def get_learning_status():
    """Get learning and adaptation status"""
    return {
        "adaptive_policies": adaptive_policy,
        "learning_memory_size": len(learning_memory),
        "recent_learning": list(dashboard_backend.learning_progress)[-10:],
        "policy_contexts": list(adaptive_policy.keys())
    }
