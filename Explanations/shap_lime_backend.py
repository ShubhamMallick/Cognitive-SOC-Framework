"""
SOC Framework SHAP & LIME Explanation Backend
Integrates model explainability with anomaly detection and context framing
"""

import shap
import lime
import lime.lime_tabular
import numpy as np
import pandas as pd
import joblib
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Import SOC detection and context modules
from Anomaly_Detection.detection_engine import run_detection
from Anomaly_Detection.Context_Framing.context_engine import ContextFramingEngine


class SHAPLIMEExplainer:
    """
    Unified SHAP and LIME explanation system for SOC anomaly detection
    Integrates with existing detection and context framing pipeline
    """
    
    def __init__(self, rf_model_path: str, iso_model_path: str, training_data_path: str):
        """
        Initialize SHAP and LIME explainers for anomaly detection models

        Args:
            rf_model_path: Path to Random Forest model
            iso_model_path: Path to Isolation Forest model  
            training_data_path: Path to training dataset
        """
        # Load models
        self.rf_model = joblib.load(rf_model_path)
        self.iso_model = joblib.load(iso_model_path)
        
        # Load training data for explainers
        self.training_data = pd.read_csv(training_data_path)
        
        # Define categorical columns (same as main.py)
        self.categorical_cols = ["device_id", "device_type", "department", "firmware_version"]
        
        # Create encoders for categorical data (same as main.py)
        self.encoders = {}
        from sklearn.preprocessing import LabelEncoder
        for col in self.categorical_cols:
            le = LabelEncoder()
            le.fit(self.training_data[col])
            self.encoders[col] = le
        
        # Preprocess training data for explainers
        self.training_features = self.training_data.copy()
        for col in self.categorical_cols:
            self.training_features[col] = self.encoders[col].transform(self.training_features[col])
        
        # Get feature columns (exclude target and label columns)
        exclude_cols = ['target', 'is_anomaly', 'stage_label']  # Exclude target and label columns
        self.feature_cols = [col for col in self.training_features.columns 
                            if col not in exclude_cols]
        self.training_features = self.training_features[self.feature_cols]
        
        print(f"📊 Total columns in dataset: {len(self.training_data.columns)}")
        print(f"📊 Feature columns for explanations: {len(self.feature_cols)}")
        print(f"📊 Excluded columns: {exclude_cols}")
        print(f"📊 Feature names: {self.feature_cols}")
        
        # Initialize SHAP explainer for Random Forest
        self.shap_explainer = shap.TreeExplainer(self.rf_model)
        
        # Initialize LIME explainer
        self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
            training_data=self.training_features.values,
            feature_names=self.feature_cols,
            class_names=['Normal', 'Anomaly'],
            mode='classification',
            discretize_continuous=False
        )
        
        # Initialize context engine
        self.context_engine = ContextFramingEngine()
        
        print(f"✅ SHAP/LIME Explainer initialized with {len(self.feature_cols)} features")
    
    def explain_anomaly_detection(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete anomaly detection with SHAP/LIME explanations
        
        Args:
            input_data: Dictionary of device features
            
        Returns:
            Complete analysis with detection, context, and explanations
        """
        # Convert to DataFrame for processing
        input_df = pd.DataFrame([input_data])
        
        # Preprocess categorical data (same as main.py)
        for col in self.categorical_cols:
            if col in input_df.columns:
                input_df[col] = self.encoders[col].transform(input_df[col])
        
        # Run standard anomaly detection
        detection_result = run_detection(input_df, self.rf_model, self.iso_model)
        
        # Run context framing
        context_result = self.context_engine.frame_context(
            anomaly_prob=detection_result["anomaly_probability"],
            deviation_score=detection_result["deviation_score"],
            uncertainty=detection_result["uncertainty_score"],
            features=input_data
        )
        
        # Generate SHAP explanation for Random Forest
        shap_explanation = self._generate_shap_explanation(input_df)
        
        # Generate LIME explanation for Isolation Forest
        lime_explanation = self._generate_lime_explanation(input_df)
        
        # Generate combined insights
        combined_insights = self._generate_combined_insights(
            detection_result, context_result, shap_explanation, lime_explanation
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "input_features": input_data,
            "detection": detection_result,
            "context": context_result,
            "explanations": {
                "shap": shap_explanation,
                "lime": lime_explanation,
                "combined": combined_insights
            }
        }
    
    def _generate_shap_explanation(self, input_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate SHAP explanation for Random Forest prediction
        
        Args:
            input_df: Input features as DataFrame
            
        Returns:
            SHAP explanation dictionary
        """
        try:
            # Get SHAP values
            shap_values = self.shap_explainer.shap_values(input_df)
            
            # Handle binary classification (list of arrays)
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Take positive class (anomaly)
            
            # Get prediction probabilities
            rf_proba = self.rf_model.predict_proba(input_df)[0]
            
            # Handle expected_value (could be array or scalar)
            expected_value = self.shap_explainer.expected_value
            if hasattr(expected_value, '__len__') and len(expected_value) > 1:
                expected_value = expected_value[1]  # Take positive class
            expected_value = float(expected_value)
            
            # Create explanation
            explanation = {
                "model_type": "Random Forest",
                "prediction_probability": float(rf_proba[1]),  # Anomaly probability
                "expected_value": expected_value,
                "feature_importance": {},
                "top_features": [],
                "summary": ""
            }
            
            # Map feature importance
            for i, feature in enumerate(self.feature_cols):
                explanation["feature_importance"][feature] = float(shap_values[0][i])
            
            # Get top contributing features
            top_features = sorted(explanation["feature_importance"].items(),
                               key=lambda x: abs(x[1]), reverse=True)[:10]
            explanation["top_features"] = top_features
            
            # Generate summary
            positive_features = [(f, v) for f, v in top_features if v > 0][:3]
            negative_features = [(f, v) for f, v in top_features if v < 0][:3]
            
            explanation["summary"] = self._create_shap_summary(positive_features, negative_features)
            
            return explanation
            
        except Exception as e:
            return {
                "model_type": "Random Forest",
                "error": str(e),
                "feature_importance": {},
                "top_features": [],
                "summary": "SHAP explanation generation failed"
            }
    
    def _generate_lime_explanation(self, input_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate LIME-style explanation for Random Forest prediction
        
        Args:
            input_df: Input features as DataFrame
            
        Returns:
            LIME explanation dictionary
        """
        try:
            print(f"🔍 LIME: Starting explanation for input shape: {input_df.shape}")
            
            # Get prediction probabilities from Random Forest
            rf_proba = self.rf_model.predict_proba(input_df)[0]
            prediction_class = self.rf_model.predict(input_df)[0]  # 0 for normal, 1 for anomaly
            
            print(f"🔍 LIME: RF prediction_proba: {rf_proba}")
            print(f"🔍 LIME: RF prediction: {prediction_class}")
            
            # Try real LIME first
            try:
                # Create a simpler predict function that returns probabilities
                def predict_proba_fn(x):
                    try:
                        # Convert to DataFrame if needed
                        if not isinstance(x, pd.DataFrame):
                            x = pd.DataFrame(x, columns=self.feature_cols)
                        return self.rf_model.predict_proba(x)
                    except Exception as e:
                        print(f"❌ LIME predict function error: {e}")
                        # Return default probabilities
                        return np.array([[0.5, 0.5]] * len(x))
                
                # Generate LIME explanation with smaller sample size for testing
                print("🔍 LIME: Generating real LIME explanation...")
                exp = self.lime_explainer.explain_instance(
                    data_row=input_df.iloc[0].values,
                    predict_fn=predict_proba_fn,
                    num_features=5,  # Reduced for testing
                    num_samples=1000  # Reduced for testing
                )
                
                print(f"🔍 LIME: Real LIME explanation generated successfully")
                
                # Create explanation
                explanation = {
                    "model_type": "Random Forest (LIME)",
                    "prediction_probability": float(rf_proba[1]),  # Anomaly probability
                    "prediction": "Anomaly" if prediction_class == 1 else "Normal",
                    "feature_contributions": {},
                    "top_features": [],
                    "summary": ""
                }
                
                # Map feature contributions
                feature_list = exp.as_list()
                print(f"🔍 LIME: Feature list length: {len(feature_list)}")
                
                for feature, weight in feature_list:
                    explanation["feature_contributions"][feature] = float(weight)
                
                # Get top contributing features
                top_features = sorted(explanation["feature_contributions"].items(),
                                   key=lambda x: abs(x[1]), reverse=True)[:5]
                explanation["top_features"] = top_features
                
                # Generate summary
                explanation["summary"] = self._create_lime_summary(top_features, explanation["prediction"])
                
                print(f"✅ LIME: Real LIME explanation completed successfully")
                return explanation
                
            except Exception as lime_error:
                print(f"⚠️ LIME: Real LIME failed, using fallback - {lime_error}")
                
                # Fallback: Use Random Forest feature importance as pseudo-LIME explanation
                feature_importance = self.rf_model.feature_importances_
                feature_names = self.feature_cols
                
                # Create feature importance mapping
                importance_map = {}
                for i, feature in enumerate(feature_names):
                    importance_map[feature] = float(feature_importance[i])
                
                # Get top features
                top_features = sorted(importance_map.items(), 
                                   key=lambda x: x[1], reverse=True)[:5]
                
                # Create fallback explanation
                explanation = {
                    "model_type": "Random Forest (Feature Importance)",
                    "prediction_probability": float(rf_proba[1]),  # Anomaly probability
                    "prediction": "Anomaly" if prediction_class == 1 else "Normal",
                    "feature_contributions": importance_map,
                    "top_features": top_features,
                    "summary": f"Based on Random Forest feature importance. Top contributors: {', '.join([f for f, _ in top_features[:3]])}"
                }
                
                print(f"✅ LIME: Fallback explanation completed successfully")
                return explanation
            
        except Exception as e:
            print(f"❌ LIME: Complete failure - {type(e).__name__}: {e}")
            import traceback
            print(f"❌ LIME: Traceback: {traceback.format_exc()}")
            
            return {
                "model_type": "Random Forest (LIME)",
                "error": f"{type(e).__name__}: {str(e)}",
                "feature_contributions": {},
                "top_features": [],
                "summary": "LIME explanation generation failed"
            }
    
    def _generate_combined_insights(self, detection: Dict, context: Dict, 
                                 shap: Dict, lime: Dict) -> Dict[str, Any]:
        """
        Generate combined insights from all explanations
        
        Args:
            detection: Detection results
            context: Context framing results
            shap: SHAP explanation
            lime: LIME explanation
            
        Returns:
            Combined insights dictionary
        """
        try:
            print("🔍 Combined: Starting insights generation")
            
            # Get top features from both models (handle different data types)
            shap_top = shap.get("top_features", [])
            lime_top = lime.get("top_features", [])
            
            # Ensure they are lists, not sets
            if isinstance(shap_top, set):
                shap_top = list(shap_top)
            if isinstance(lime_top, set):
                lime_top = list(lime_top)
            
            # Take only first 5 features
            shap_top = shap_top[:5]
            lime_top = lime_top[:5]
            
            print(f"🔍 Combined: SHAP top features: {len(shap_top)}")
            print(f"🔍 Combined: LIME top features: {len(lime_top)}")
            
            # Find common influential features
            shap_features = {f for f, v in shap_top} if isinstance(shap_top, list) else set()
            lime_features = {f for f, v in lime_top} if isinstance(lime_top, list) else set()
            common_features = shap_features.intersection(lime_features)
            
            # Risk assessment based on explanations
            explanation_risk = self._assess_explanation_risk(shap, lime)
            
            # Generate actionable insights
            actionable_insights = self._generate_actionable_insights(
                detection, context, shap_top, lime_top, common_features
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(detection, context, shap, lime)
            
            # Assess confidence
            confidence_assessment = self._assess_confidence(detection, context, shap, lime)
            
            result = {
                "model_agreement": self._check_model_agreement(shap, lime),
                "common_influential_features": list(common_features),
                "explanation_risk_level": explanation_risk,
                "actionable_insights": actionable_insights,
                "confidence_assessment": confidence_assessment,
                "recommendations": recommendations
            }
            
            print("✅ Combined: Insights generation completed successfully")
            return result
            
        except Exception as e:
            print(f"❌ Combined: Error generating insights - {type(e).__name__}: {e}")
            import traceback
            print(f"❌ Combined: Traceback: {traceback.format_exc()}")
            
            # Return safe fallback
            return {
                "model_agreement": "Unable to assess model agreement due to errors",
                "common_influential_features": [],
                "explanation_risk_level": "Medium",
                "actionable_insights": ["Explanation generation had errors, proceed with caution"],
                "confidence_assessment": "Low confidence due to explanation errors",
                "recommendations": ["Review system logs for explanation errors"]
            }
    
    def _create_shap_summary(self, positive_features: List, negative_features: List) -> str:
        """Create human-readable SHAP summary"""
        summary_parts = []
        
        if positive_features:
            pos_str = ", ".join([f"{f} (+{v:.3f})" for f, v in positive_features])
            summary_parts.append(f"Key anomaly indicators: {pos_str}")
        
        if negative_features:
            neg_str = ", ".join([f"{f} ({v:.3f})" for f, v in negative_features])
            summary_parts.append(f"Normalizing factors: {neg_str}")
        
        return " | ".join(summary_parts) if summary_parts else "No significant feature contributions detected"
    
    def _create_lime_summary(self, top_features: List, prediction: str) -> str:
        """Create human-readable LIME summary"""
        if not top_features:
            return "No significant local patterns detected"
        
        feature_str = ", ".join([f"{f} ({v:.3f})" for f, v in top_features[:3]])
        return f"Local analysis ({prediction}): {feature_str}"
    
    def _check_model_agreement(self, shap: Dict, lime: Dict) -> str:
        """Check if SHAP and LIME explanations agree"""
        shap_prob = shap.get("prediction_probability", 0.5)
        lime_pred = lime.get("prediction", "Normal")
        
        if shap_prob > 0.7 and lime_pred == "Anomaly":
            return "High agreement - both models indicate anomaly"
        elif shap_prob < 0.3 and lime_pred == "Normal":
            return "High agreement - both models indicate normal"
        else:
            return "Model disagreement - further investigation needed"
    
    def _assess_explanation_risk(self, shap: Dict, lime: Dict) -> str:
        """Assess risk level based on explanations"""
        shap_prob = shap.get("prediction_probability", 0.5)
        lime_prob = lime.get("prediction_probability", 0.5)
        
        combined_risk = (shap_prob + lime_prob) / 2
        
        if combined_risk > 0.8:
            return "Critical"
        elif combined_risk > 0.6:
            return "High"
        elif combined_risk > 0.4:
            return "Medium"
        else:
            return "Low"
    
    def _generate_actionable_insights(self, detection: Dict, context: Dict,
                                    shap_top: List, lime_top: List, 
                                    common_features: List) -> List[str]:
        """Generate actionable insights from explanations"""
        insights = []
        
        # Anomaly probability insights
        prob = detection.get("anomaly_probability", 0)
        if prob > 0.8:
            insights.append("High anomaly probability detected - immediate investigation recommended")
        
        # Common influential features
        if common_features:
            insights.append(f"Key risk factors: {', '.join(common_features[:3])}")
        
        # Contextual risk insights
        context_risk = context.get("final_contextual_risk", 0)
        if context_risk > 0.7:
            insights.append("High contextual risk - consider asset criticality and security factors")
        
        return insights
    
    def _assess_confidence(self, detection: Dict, context: Dict, 
                         shap: Dict, lime: Dict) -> str:
        """Assess overall confidence in predictions"""
        uncertainty = detection.get("uncertainty_score", 0.5)
        agreement = self._check_model_agreement(shap, lime)
        
        if uncertainty < 0.3 and "High agreement" in agreement:
            return "High confidence"
        elif uncertainty < 0.5:
            return "Medium confidence"
        else:
            return "Low confidence - human review recommended"
    
    def _generate_recommendations(self, detection: Dict, context: Dict,
                                shap: Dict, lime: Dict) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        # Based on detection decision
        decision = detection.get("decision", "MONITOR")
        if "AUTO-CONTAIN" in decision:
            recommendations.append("Execute automated containment procedures")
        elif "ESCALATE" in decision:
            recommendations.append("Escalate to human security analyst")
        else:
            recommendations.append("Continue monitoring with enhanced logging")
        
        # Based on explanations
        shap_prob = shap.get("prediction_probability", 0)
        if shap_prob > 0.9:
            recommendations.append("Isolate affected device immediately")
        
        return recommendations


# Global explainer instance
_explainer_instance = None


def initialize_explainer(rf_model_path: str, iso_model_path: str, training_data_path: str) -> SHAPLIMEExplainer:
    """
    Initialize global explainer instance
    
    Args:
        rf_model_path: Path to Random Forest model
        iso_model_path: Path to Isolation Forest model
        training_data_path: Path to training dataset
        
    Returns:
        Initialized SHAPLIMEExplainer instance
    """
    global _explainer_instance
    _explainer_instance = SHAPLIMEExplainer(rf_model_path, iso_model_path, training_data_path)
    return _explainer_instance


def explain_anomaly(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Explain anomaly detection for input data
    
    Args:
        input_data: Dictionary of device features
        
    Returns:
        Complete explanation results
    """
    if _explainer_instance is None:
        raise RuntimeError("Explainer not initialized. Call initialize_explainer() first.")
    
    return _explainer_instance.explain_anomaly_detection(input_data)


def get_explainer_info() -> Dict[str, Any]:
    """
    Get information about the initialized explainer
    
    Returns:
        Explainer configuration and status
    """
    if _explainer_instance is None:
        return {"status": "not_initialized"}
    
    return {
        "status": "initialized",
        "feature_count": len(_explainer_instance.feature_cols),
        "feature_names": _explainer_instance.feature_cols,
        "training_data_shape": _explainer_instance.training_features.shape,
        "models": {
            "random_forest": type(_explainer_instance.rf_model).__name__,
            "isolation_forest": type(_explainer_instance.iso_model).__name__
        }
    }
