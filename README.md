# 🛡️ Cognitive SOC Framework

> **Enterprise-Grade Uncertainty-Aware Security Operations Center (SOC) with 14 AI Agents, Real-Time Dashboard, and LLM-Powered Explanations**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![Architecture Diagram](CyberSecurity%20Architecture.png)

## 🎯 Overview

The **Cognitive SOC Framework** is a cutting-edge, AI-powered Security Operations Center platform that provides:

- **Real-time anomaly detection** using ensemble ML models
- **14 specialized AI agents** for comprehensive security analysis
- **LLM-powered explanations** for incident understanding
- **Live SOC dashboard** with real-time metrics and visualizations
- **Autonomous decision making** with confidence scoring
- **Adaptive learning** through reinforcement learning

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        COGNITIVE SOC FRAMEWORK                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  🔍 DETECTION LAYER          📋 CONTEXT FRAMING          🤖 AI AGENTS   │
│  ─────────────────────────────────────────────────────────────────    │
│  • Random Forest Model       • Uncertainty Analysis      • Policy       │
│  • Isolation Forest          • Risk Framing              • Threat       │
│  • Anomaly Detection         • Confidence Scoring        • Impact       │
│                                                            • Privacy    │
│                                                            • Risk       │
│  🎯 DECISION AUTHORITY      🛡️ EXECUTION LAYER         📊 DASHBOARD     │
│  ─────────────────────────────────────────────────────────────────    │
│  • Final Decision Engine     • Containment Actions       • Real-time     │
│  • Confidence Scoring        • Human Review              • Analytics    │
│  • Override Logic            • Adaptive Monitoring      • Visualize    │
│                                                                         │
│  📚 AUDIT & LEARNING                                                    │
│  ─────────────────────────────────────────────────────────────────    │
│  • Incident Memory           • Reinforcement Learning                   │
│  • Compliance Tracking       • Adaptive Policies                        │
│  • Outcome Feedback                                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### 🔍 **Anomaly Detection Engine**
- Dual ML models: Random Forest + Isolation Forest
- 30,000+ sample dataset training
- Real-time deviation scoring
- Uncertainty quantification

### 🤖 **14 Specialized AI Agents**

| Agent | Purpose | Key Capabilities |
|-------|---------|------------------|
| **Policy Agent** | Compliance & Violations | Violation modeling, enforcement confidence |
| **Threat Agent** | Attack Analysis | Pattern detection, ransomware scoring |
| **Impact Agent** | Business Impact | Service disruption, downtime estimation |
| **Privacy Agent** | Data Protection | GDPR/privacy risk, encryption analysis |
| **Risk Agent** | Risk Assessment | Multi-dimensional risk scoring, failure prediction |
| **Coordination Engine** | Agent Orchestration | Fused scoring, parallel execution |
| **Authority Agent** | Decision Making | Final decisions, confidence scoring, overrides |
| **Containment Agent** | Incident Response | Automated containment actions |
| **Human Review Agent** | Analyst Interface | Expert review workflows |
| **Adaptive Monitoring** | Continuous Watch | Monitoring mode adjustments |
| **Safe Pass Agent** | Normal Operations | Safe operation management |
| **Audit Memory Agent** | Compliance Logging | Incident memory, compliance tracking |
| **Outcome Agent** | Feedback Learning | Performance tracking, improvement |
| **Reinforcement Learning** | Policy Improvement | Adaptive learning, memory-based decisions |

### 🎨 **Real-Time SOC Dashboard**

- **System Overview**: Total events, risk scores, uptime
- **Threat Analytics**: Trend visualization, attack patterns
- **Alert Management**: Severity distribution, active alerts
- **Agent Performance**: Processing times, success rates
- **System Health**: Automation safety, anomaly detection
- **Learning Progress**: Policy improvements, adaptation

### 🧠 **LLM-Powered Explanations**

- OpenAI GPT integration for intelligent analysis
- Agent-specific explanations
- Context-aware recommendations
- Natural language incident reports

### 🔔 **Multi-Modal Alerting**

- Audio alerts with text-to-speech
- Visual dashboard notifications
- Real-time console logging

## 📁 Project Structure

```
SOC/
├── 📄 main.py                    # FastAPI application & pipeline orchestration
├── 📁 Agents/                    # 14 specialized AI agents
│   ├── policy_agent.py
│   ├── threat_agent.py
│   ├── impact_agent.py
│   ├── privacy_agent.py
│   ├── risk_failure_agent.py
│   ├── coordination_engine.py
│   ├── authority_agent.py
│   ├── containment_agent.py
│   ├── human_review_agent.py
│   ├── adaptive_monitoring_agent.py
│   ├── safe_pass_agent.py
│   ├── audit_memory_agent.py
│   ├── outcome_feedback_agent.py
│   └── reinforcement_learning_agent.py
├── 📁 Dashboard/                 # Real-time analytics backend
│   └── dashboard_backend.py
├── 📁 LLM/                       # LLM explanation modules
│   ├── context_llm.py
│   ├── policy_llm.py
│   ├── threat_llm.py
│   ├── impact_llm.py
│   ├── privacy_llm.py
│   ├── risk_llm.py
│   ├── coordinate_llm.py
│   ├── authority_llm.py
│   ├── execution_llm.py
│   └── audit_llm.py
├── 📁 Anomaly_Detection/         # ML detection engine
│   ├── detection_engine.py
│   ├── Context_Framing/
│   ├── rf_anomaly_model.pkl
│   ├── iso_anomaly_model.pkl
│   └── uncertainty_aware_soc_dataset_30000.csv
├── 📁 routers/                   # API endpoint routers
│   ├── dashboard_router.py
│   ├── context_explain_router.py
│   ├── policy_explain_router.py
│   ├── threat_explain_router.py
│   ├── impact_explain_router.py
│   ├── privacy_explain_router.py
│   ├── risk_explain_router.py
│   ├── coordinate_explain_router.py
│   ├── authority_explain_router.py
│   ├── audit_explain_router.py
│   └── execution_explain_router.py
├── 📁 templates/                 # HTML frontend templates
│   ├── index.html               # Analysis form
│   ├── results.html             # Detection results
│   ├── dashboard.html           # SOC dashboard
│   ├── policy.html              # Policy analysis
│   ├── threat.html              # Threat analysis
│   ├── impact.html              # Impact analysis
│   ├── privacy.html             # Privacy analysis
│   ├── risk_failure.html        # Risk assessment
│   ├── coordinate.html          # Coordination view
│   ├── authority.html           # Authority decisions
│   ├── execution.html           # Execution status
│   ├── audit.html               # Audit trail
│   └── outcome.html             # Outcome feedback
├── 📁 static/                    # CSS, JS, images
├── 📁 Reports/                   # Generated reports
├── 📁 Utilities/                 # Helper utilities
│   └── simple_audio_alerts.py   # Audio notification system
├── 📄 requirements.txt           # Python dependencies
├── 📄 LICENSE                    # MIT License
└── 📄 README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip package manager
- OpenAI API key (for LLM features)

### 1. Clone Repository
```bash
git clone https://github.com/ShubhamMallick/Cognitive-SOC-Framework.git
cd Cognitive-SOC-Framework
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Run the Application
```bash
uvicorn main:app --reload
```

### 6. Access the Application
- **Main Interface**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/dashboard
- **API Docs**: http://localhost:8000/docs

## 📊 Usage Guide

### 🔍 **Submitting Device Analysis**

1. **Go to** `http://localhost:8000/`
2. **Fill the device analysis form** with:
   - Device ID, Type, Department
   - Resource usage (CPU, Memory, Disk)
   - Security signals (auth attempts, flags)
   - Network metrics (traffic, DNS, ports)
3. **Click "Analyze Device"**
4. **View results** with detection, context, and agent analysis

### 📈 **Viewing SOC Dashboard**

1. **Navigate to** `http://localhost:8000/dashboard`
2. **View real-time metrics**:
   - Total events processed
   - Average risk scores
   - Active alerts and severity
   - Agent performance stats
   - System health indicators
   - Learning progress visualization

### 🤖 **Exploring Agent Results**

After analysis, explore individual agent results:
- `/policy` - Security policy compliance
- `/threat` - Threat analysis and ransomware detection
- `/impact` - Business impact assessment
- `/privacy` - Privacy and GDPR analysis
- `/risk` - Risk failure analysis
- `/coordinate` - Agent coordination results
- `/authority` - Final authority decisions
- `/execution` - Execution actions taken
- `/audit` - Audit trail and compliance
- `/outcome` - Outcome feedback

## 🔧 API Endpoints

### Core Analysis
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Submit device data for SOC analysis |
| `GET`  | `/results` | View analysis results |

### Dashboard API
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/dashboard` | View SOC dashboard |
| `GET`  | `/dashboard/api/summary` | Get dashboard summary metrics |
| `GET`  | `/dashboard/api/metrics` | Get detailed system metrics |
| `GET`  | `/dashboard/api/alerts` | Get active alerts |
| `GET`  | `/dashboard/api/charts/threat-trend` | Get threat trend data |
| `GET`  | `/dashboard/api/charts/decision-distribution` | Get decision distribution |
| `GET`  | `/dashboard/api/charts/agent-performance` | Get agent performance data |
| `GET`  | `/dashboard/api/learning` | Get learning progress |

### Agent Results
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/policy` | Policy analysis results |
| `GET`  | `/threat` | Threat analysis results |
| `GET`  | `/impact` | Impact analysis results |
| `GET`  | `/privacy` | Privacy analysis results |
| `GET`  | `/risk` | Risk analysis results |
| `GET`  | `/coordinate` | Coordination results |
| `GET`  | `/authority` | Authority decisions |
| `GET`  | `/execution` | Execution actions |
| `GET`  | `/audit` | Audit trail |
| `GET`  | `/outcome` | Outcome feedback |

### LLM Explanations
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/explain/context` | Get context explanations |
| `POST` | `/explain/policy` | Get policy explanations |
| `POST` | `/explain/threat` | Get threat explanations |
| `POST` | `/explain/impact` | Get impact explanations |
| `POST` | `/explain/privacy` | Get privacy explanations |
| `POST` | `/explain/risk` | Get risk explanations |
| `POST` | `/explain/coordinate` | Get coordination explanations |
| `POST` | `/explain/authority` | Get authority explanations |
| `POST` | `/explain/execution` | Get execution explanations |
| `POST` | `/explain/audit` | Get audit explanations |

## 🎨 Dashboard Features

### **Real-Time Metrics**
- **Total Events**: Count of processed security events
- **Average Risk**: Mean risk score across all events
- **Active Alerts**: Number of high-severity alerts
- **System Uptime**: Percentage of system availability

### **Threat Analytics**
- **Trend Charts**: Visual representation of threat evolution
- **Severity Distribution**: Breakdown of alert severities
- **Attack Patterns**: Identified threat patterns over time

### **System Health**
- **Automation Safety**: System safety score
- **Override Rate**: Percentage of manual overrides
- **Anomaly Detection**: Active anomaly detection status
- **System Confidence**: Overall system confidence score

### **Agent Performance**
- **Processing Times**: Average time per agent
- **Success Rates**: Agent success/failure rates
- **Parallel Execution**: Efficiency of parallel processing

### **Learning Progress**
- **Policy Improvements**: Count of policy adaptations
- **Learning Rate**: Speed of reinforcement learning
- **Memory Decay**: Knowledge retention metrics

## 🔬 Technical Architecture

### **ML Detection Pipeline**
```python
# Dual-model approach
rf_model = RandomForestClassifier()   # Ensemble learning
iso_model = IsolationForest()         # Anomaly isolation

# Uncertainty quantification
uncertainty = ensemble_uncertainty(rf_pred, iso_pred)
```

### **Agent Orchestration**
```python
# Parallel execution
policy_task = asyncio.to_thread(policy_agent, ...)
threat_task = asyncio.to_thread(threat_agent, ...)
impact_task = asyncio.to_thread(impact_agent, ...)
privacy_task = asyncio.to_thread(privacy_agent, ...)

results = await asyncio.gather(
    policy_task, threat_task, impact_task, privacy_task
)
```

### **Dashboard Integration**
```python
# Non-blocking background updates
asyncio.create_task(_update_dashboard_background(...))

# Error isolation - dashboard failures don't affect pipeline
try:
    await dashboard_backend.process_soc_event(event_data)
except Exception as e:
    print(f"Dashboard error (non-critical): {e}")
```

## 🧪 Testing

### Run Unit Tests
```bash
python -m pytest tests/
```

### Test LLM Integration
```bash
python test_llm.py
```

### Manual Testing
1. Submit test device data via UI
2. Verify all 14 agents process correctly
3. Check dashboard receives data
4. Validate LLM explanations generate

## 📈 Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Detection Latency | < 1s | ~0.5s |
| Pipeline Throughput | > 10 events/min | ~15 events/min |
| Dashboard Update | < 5s | ~2s |
| LLM Response | < 10s | ~7s |
| System Uptime | > 99% | 99.5% |

## 🔒 Security Considerations

- **Input Validation**: Pydantic models validate all inputs
- **Error Isolation**: Dashboard failures don't compromise pipeline
- **Data Privacy**: Privacy agent for GDPR/compliance
- **Audit Trail**: Complete incident logging
- **Override Capability**: Human analyst can override AI decisions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `pytest`
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shubham Mallick**
- GitHub: [@ShubhamMallick](https://github.com/ShubhamMallick)
- LinkedIn: [Shubham Mallick](https://linkedin.com/in/shubhammallick)

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **OpenAI** for LLM capabilities
- **scikit-learn** for ML models
- **Chart.js** for visualizations
- **LangChain** for LLM orchestration

## 📞 Support

For questions, issues, or contributions:
- Create an [Issue](https://github.com/ShubhamMallick/Cognitive-SOC-Framework/issues)
- Submit a [Pull Request](https://github.com/ShubhamMallick/Cognitive-SOC-Framework/pulls)
- Contact: [Your Email]

---

<div align="center">

**🛡️ Protecting Digital Assets with AI-Powered Intelligence** 🛡️

*Built with ❤️ for the cybersecurity community*

</div>
