from fastapi import APIRouter, HTTPException, status
from models.schemas import StudentFeatures, PredictionResponse
from models.predictor import predictor
from database import db
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/predict", tags=["predictions"])

@router.post("/", response_model=PredictionResponse)
async def predict_dropout(student: StudentFeatures):
    """
    Predict dropout risk for a single student
    
    - **gpa**: Grade Point Average (0-4)
    - **attendance**: Attendance percentage (0-100)
    - **assignments_submitted**: Percentage of assignments submitted (0-100)
    - **extracurricular**: Involved in activities (0=No, 1=Yes)
    - **age**: Student age
    """
    logger.info(f"Received prediction request: {student}")
    
    # Check if model is loaded
    if not predictor.is_loaded():
        logger.error("Model not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Prediction model not available"
        )
    
    try:
        # Convert Pydantic model to dict
        features_dict = student.dict()
        
        # Make prediction
        prediction_result = predictor.predict(features_dict)
        
        if prediction_result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Prediction failed"
            )
        
        logger.info(f"Prediction successful: {prediction_result}")
        
        # Return prediction response
        return PredictionResponse(
            dropout_probability=prediction_result["dropout_probability"],
            risk_level=prediction_result["risk_level"],
            shap_values=prediction_result["shap_values"]
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.post("/with-storage/", response_model=PredictionResponse)
async def predict_and_store(student: StudentFeatures, student_id: str):
    """
    Predict dropout risk and store result in database
    
    - **student_id**: Unique identifier for the student
    - Plus all student features
    """
    logger.info(f"Received prediction with storage request for student {student_id}")
    
    # First get prediction
    prediction_response = await predict_dropout(student)
    
    try:
        # Prepare data for storage
        student_record = {
            "student_id": student_id,
            "features": student.dict(),
            "prediction": {
                "probability": prediction_response.dropout_probability,
                "risk_level": prediction_response.risk_level,
                "shap_values": prediction_response.shap_values,
                "timestamp": datetime.now()
            },
            "actual_dropout": None,  # Will be updated later if known
            "timestamp": datetime.now()
        }
        
        # Store in database
        db.insert_student(student_record)
        logger.info(f"Stored prediction for student {student_id}")
        
    except Exception as e:
        logger.error(f"Storage failed but prediction succeeded: {e}")
        # Don't fail the request if storage fails - just log it
    
    return prediction_response

@router.get("/feature-importance/")
async def get_feature_importance():
    """
    Get global feature importance from the model
    Used for the Feature Insights page
    """
    if not predictor.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not available"
        )
    
    importance = predictor.get_feature_importance()
    return {
        "feature_importance": importance,
        "feature_names": list(importance.keys()),
        "importance_values": list(importance.values())
    }

@router.post("/batch/")
async def predict_batch(students: list[StudentFeatures]):
    """
    Predict for multiple students at once
    """
    if not predictor.is_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not available"
        )
    
    # Convert list of Pydantic models to list of dicts
    features_list = [s.dict() for s in students]
    
    # Get batch predictions
    results = predictor.predict_batch(features_list)
    
    if results is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Batch prediction failed"
        )
    
    return {
        "total": len(results),
        "predictions": results
    }