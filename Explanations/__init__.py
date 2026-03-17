"""
Explanations Package Initialization
Provides SHAP and LIME model explainability for SOC Framework
"""

from .shap_lime_backend import SHAPLIMEExplainer, initialize_explainer, explain_anomaly, get_explainer_info

__all__ = [
    'SHAPLIMEExplainer',
    'initialize_explainer', 
    'explain_anomaly',
    'get_explainer_info'
]

__version__ = "1.0.0"
__description__ = "SHAP and LIME explanations for SOC anomaly detection"
