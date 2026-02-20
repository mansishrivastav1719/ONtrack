import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "dropout_prediction")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "students")
    
    # Model Configuration
    MODEL_PATH = os.getenv("MODEL_PATH", "../model/xgboost_model.pkl")
    
    # API Configuration
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    
    # Risk thresholds (probability)
    RISK_THRESHOLDS = {
        "low": 0.3,
        "medium": 0.7  # Above this is high risk
    }
    
    # Feature names (must match training data)
    FEATURE_NAMES = [
        "gpa",
        "attendance",
        "assignments_submitted",
        "extracurricular",
        "age"
    ]

# Create a global config object
config = Config()