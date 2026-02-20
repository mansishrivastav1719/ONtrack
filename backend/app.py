from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

# Import routes
from routes import predict, students
from database import db
from models.predictor import predictor
from models.schemas import HealthResponse
from config import config

import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle startup and shutdown events
    """
    # Startup
    logger.info("🚀 Starting up Dropout Prediction API...")
    
    # Check database connection
    if db.check_connection():
        logger.info("✅ Database connected")
    else:
        logger.warning("⚠️ Database connection failed - will retry on requests")
    
    # Check model loading
    if predictor.is_loaded():
        logger.info("✅ Model loaded successfully")
        # Log feature importance for debugging
        importance = predictor.get_feature_importance()
        logger.info(f"📊 Feature importance: {importance}")
    else:
        logger.warning("⚠️ Model failed to load - predictions will not work")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Dropout Prediction API...")

# Create FastAPI app
app = FastAPI(
    title="Student Dropout Prediction API",
    description="ML-powered API to predict students at risk of dropping out",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc documentation
)

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predict.router)
app.include_router(students.router)

@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "🎓 Student Dropout Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "predict": "/predict/",
            "students": "/students/",
            "feature_importance": "/predict/feature-importance/"
        }
    }

@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring
    Returns status of API, database, and model
    """
    logger.debug("Health check requested")
    
    return HealthResponse(
        status="healthy",
        model_loaded=predictor.is_loaded(),
        database_connected=db.check_connection(),
        timestamp=datetime.now()
    )

@app.get("/debug/routes", tags=["debug"])
async def list_routes():
    """
    Debug endpoint to list all available routes
    """
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods) if hasattr(route, "methods") else None
        })
    return {"routes": routes}

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    """
    Global exception handler
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "An internal server error occurred",
            "detail": str(exc),
            "path": request.url.path
        }
    )

# Run with: uvicorn app:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True  # Auto-reload on code changes
    )