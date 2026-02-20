from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime

# Request/Response Models for API

class StudentFeatures(BaseModel):
    """Student features for prediction"""
    gpa: float = Field(..., ge=0, le=4, description="Grade Point Average (0-4)")
    attendance: float = Field(..., ge=0, le=100, description="Attendance percentage (0-100)")
    assignments_submitted: float = Field(..., ge=0, le=100, description="Percentage of assignments submitted")
    extracurricular: int = Field(..., ge=0, le=1, description="Involved in extracurricular activities (0=No, 1=Yes)")
    age: int = Field(..., ge=16, le=50, description="Student age")
    
    @validator('attendance')
    def attendance_percentage(cls, v):
        if v > 100:
            raise ValueError('Attendance cannot exceed 100%')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "gpa": 3.2,
                "attendance": 85.5,
                "assignments_submitted": 90.0,
                "extracurricular": 1,
                "age": 20
            }
        }

class PredictionResponse(BaseModel):
    """Prediction result"""
    student_id: Optional[str] = None
    dropout_probability: float = Field(..., ge=0, le=1)
    risk_level: str  # "Low", "Medium", "High"
    shap_values: Dict[str, float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "S12345",
                "dropout_probability": 0.85,
                "risk_level": "High",
                "shap_values": {
                    "gpa": 0.32,
                    "attendance": 0.45,
                    "assignments_submitted": 0.12,
                    "extracurricular": -0.08,
                    "age": 0.03
                }
            }
        }

class StudentRecord(BaseModel):
    """Complete student record from database"""
    student_id: str
    features: StudentFeatures
    prediction: PredictionResponse
    actual_dropout: Optional[str] = None  # "Yes", "No", or null
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    model_loaded: bool
    database_connected: bool
    timestamp: datetime = Field(default_factory=datetime.now)

class StudentsListResponse(BaseModel):
    """List of students for dashboard"""
    total: int
    students: List[StudentRecord]
    risk_distribution: Dict[str, int]  # {"Low": 45, "Medium": 30, "High": 25}