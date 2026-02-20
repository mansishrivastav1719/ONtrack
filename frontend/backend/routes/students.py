from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional, List
from database import db
from models.schemas import StudentRecord, StudentsListResponse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/students", tags=["students"])

@router.get("/", response_model=StudentsListResponse)
async def get_all_students(
    limit: int = Query(100, ge=1, le=1000, description="Number of students to return"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level (Low/Medium/High)")
):
    """
    Get all students with optional filtering
    
    - **limit**: Maximum number of students to return
    - **risk_level**: Filter by risk level
    """
    logger.info(f"Fetching students with limit={limit}, risk_level={risk_level}")
    
    # Check database connection
    if not db.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    try:
        # Get all students
        students = db.get_all_students(limit=limit)
        
        # Filter by risk level if specified
        if risk_level:
            students = [
                s for s in students 
                if s.get("prediction", {}).get("risk_level") == risk_level
            ]
        
        # Get risk distribution for dashboard
        risk_distribution = db.get_risk_distribution()
        
        # Convert MongoDB documents to StudentRecord format
        # Note: You'll need to add proper ObjectId handling
        formatted_students = []
        for s in students:
            # Convert ObjectId to string for JSON serialization
            s["_id"] = str(s["_id"])
            formatted_students.append(s)
        
        logger.info(f"Returning {len(formatted_students)} students")
        
        return StudentsListResponse(
            total=len(formatted_students),
            students=formatted_students,
            risk_distribution=risk_distribution
        )
        
    except Exception as e:
        logger.error(f"Error fetching students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch students: {str(e)}"
        )

@router.get("/{student_id}", response_model=StudentRecord)
async def get_student_by_id(student_id: str):
    """
    Get a specific student by ID
    """
    logger.info(f"Fetching student: {student_id}")
    
    if not db.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    try:
        student = db.get_student_by_id(student_id)
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student {student_id} not found"
            )
        
        # Convert ObjectId to string
        student["_id"] = str(student["_id"])
        
        logger.info(f"Found student: {student_id}")
        return student
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch student: {str(e)}"
        )

@router.get("/stats/risk-distribution/")
async def get_risk_distribution():
    """
    Get distribution of students by risk level
    Used for the pie/bar chart on dashboard
    """
    logger.info("Fetching risk distribution")
    
    if not db.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    try:
        distribution = db.get_risk_distribution()
        
        # Ensure all risk levels are present
        for level in ["Low", "Medium", "High"]:
            if level not in distribution:
                distribution[level] = 0
        
        return {
            "distribution": distribution,
            "labels": list(distribution.keys()),
            "values": list(distribution.values()),
            "total": sum(distribution.values())
        }
        
    except Exception as e:
        logger.error(f"Error fetching risk distribution: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch distribution: {str(e)}"
        )

@router.get("/stats/kpi/")
async def get_kpi_summary():
    """
    Get KPI summary for dashboard:
    - Total students
    - Percentage high risk
    - Average GPA
    - Average attendance
    """
    logger.info("Fetching KPI summary")
    
    if not db.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    try:
        students = db.get_all_students(limit=1000)
        
        if not students:
            return {
                "total_students": 0,
                "high_risk_percentage": 0,
                "avg_gpa": 0,
                "avg_attendance": 0
            }
        
        # Calculate KPIs
        total = len(students)
        
        # Count high risk students
        high_risk_count = sum(
            1 for s in students 
            if s.get("prediction", {}).get("risk_level") == "High"
        )
        high_risk_percentage = (high_risk_count / total) * 100 if total > 0 else 0
        
        # Calculate average GPA and attendance
        gpa_sum = sum(s.get("features", {}).get("gpa", 0) for s in students)
        attendance_sum = sum(s.get("features", {}).get("attendance", 0) for s in students)
        
        avg_gpa = gpa_sum / total if total > 0 else 0
        avg_attendance = attendance_sum / total if total > 0 else 0
        
        return {
            "total_students": total,
            "high_risk_percentage": round(high_risk_percentage, 1),
            "avg_gpa": round(avg_gpa, 2),
            "avg_attendance": round(avg_attendance, 1),
            "high_risk_count": high_risk_count,
            "low_risk_count": total - high_risk_count  # Simplified, you might want medium risk too
        }
        
    except Exception as e:
        logger.error(f"Error fetching KPI summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch KPI summary: {str(e)}"
        )

@router.delete("/{student_id}")
async def delete_student(student_id: str):
    """
    Delete a student record (use carefully!)
    """
    logger.warning(f"Delete request for student: {student_id}")
    
    if not db.check_connection():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not connected"
        )
    
    try:
        # Note: You'll need to add a delete method to database.py
        # For now, return not implemented
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Delete functionality not implemented yet"
        )
        
    except Exception as e:
        logger.error(f"Error deleting student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete student: {str(e)}"
        )