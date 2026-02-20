import joblib
import numpy as np
import shap
from config import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DropoutPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = config.FEATURE_NAMES
        self.shap_explainer = None
        self.load_model()
    
    def load_model(self):
        """Load the trained XGBoost model"""
        try:
            self.model = joblib.load(config.MODEL_PATH)
            logger.info(f"✅ Model loaded from {config.MODEL_PATH}")
            
            # Initialize SHAP explainer (using TreeExplainer for XGBoost)
            self.shap_explainer = shap.TreeExplainer(self.model)
            logger.info("✅ SHAP explainer initialized")
            
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            self.model = None
            self.shap_explainer = None
            return False
    
    def predict(self, features):
        """
        Predict dropout probability for a single student
        
        Args:
            features: Dict or array of feature values in correct order
        
        Returns:
            dict: Contains probability, risk_level, and shap_values
        """
        if self.model is None:
            logger.error("❌ Model not loaded")
            return None
        
        try:
            # Convert features to numpy array
            if isinstance(features, dict):
                # If features is a dict, extract values in correct order
                feature_array = np.array([features[name] for name in self.feature_names]).reshape(1, -1)
            else:
                # If already array-like, just reshape
                feature_array = np.array(features).reshape(1, -1)
            
            # Get probability prediction
            probability = self.model.predict_proba(feature_array)[0][1]  # Probability of dropout
            
            # Determine risk level
            risk_level = self._get_risk_level(probability)
            
            # Calculate SHAP values for this prediction
            shap_values = self._calculate_shap(feature_array)
            
            logger.info(f"✅ Prediction made: {probability:.2f} ({risk_level} risk)")
            
            return {
                "dropout_probability": float(probability),
                "risk_level": risk_level,
                "shap_values": shap_values
            }
            
        except Exception as e:
            logger.error(f"❌ Prediction failed: {e}")
            return None
    
    def predict_batch(self, features_list):
        """Predict for multiple students at once"""
        if self.model is None:
            logger.error("❌ Model not loaded")
            return None
        
        try:
            # Convert list of dicts to numpy array
            if isinstance(features_list[0], dict):
                feature_array = np.array([
                    [f[name] for name in self.feature_names] 
                    for f in features_list
                ])
            else:
                feature_array = np.array(features_list)
            
            # Get probabilities
            probabilities = self.model.predict_proba(feature_array)[:, 1]
            
            results = []
            for i, prob in enumerate(probabilities):
                results.append({
                    "dropout_probability": float(prob),
                    "risk_level": self._get_risk_level(prob)
                })
            
            logger.info(f"✅ Batch prediction for {len(results)} students")
            return results
            
        except Exception as e:
            logger.error(f"❌ Batch prediction failed: {e}")
            return None
    
    def _get_risk_level(self, probability):
        """Convert probability to risk category"""
        if probability < config.RISK_THRESHOLDS["low"]:
            return "Low"
        elif probability < config.RISK_THRESHOLDS["medium"]:
            return "Medium"
        else:
            return "High"
    
    def _calculate_shap(self, feature_array):
        """Calculate SHAP values for a single prediction"""
        if self.shap_explainer is None:
            # Return dummy values if SHAP not available
            return {name: 0.0 for name in self.feature_names}
        
        try:
            # Calculate SHAP values
            shap_values = self.shap_explainer.shap_values(feature_array)
            
            # Convert to dictionary with feature names
            shap_dict = {}
            for i, name in enumerate(self.feature_names):
                shap_dict[name] = float(shap_values[0][i])
            
            return shap_dict
            
        except Exception as e:
            logger.error(f"❌ SHAP calculation failed: {e}")
            return {name: 0.0 for name in self.feature_names}
    
    def get_feature_importance(self):
        """Get global feature importance from the model"""
        if self.model is None:
            return {name: 0.0 for name in self.feature_names}
        
        try:
            importance = self.model.feature_importances_
            return {
                name: float(importance[i]) 
                for i, name in enumerate(self.feature_names)
            }
        except Exception as e:
            logger.error(f"❌ Failed to get feature importance: {e}")
            return {name: 0.0 for name in self.feature_names}
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None

# Create a global predictor instance
predictor = DropoutPredictor()