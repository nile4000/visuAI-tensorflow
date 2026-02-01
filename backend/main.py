from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import os
from dotenv import load_dotenv

from models.schemas import (
    DescribeRequest, DescribeResponse,
    AskRequest, AskResponse,
    HealthResponse
)
from services.omni_service import OmniService

# Load environment variables
load_dotenv()

# Global state
start_time = time.time()
omni_service: OmniService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global omni_service
    
    # Startup
    print("🚀 Starting OmniRL Backend Server...")
    use_mock = os.getenv("USE_MOCK_RESPONSES", "true").lower() == "true"
    omni_service = OmniService(use_mock=use_mock)
    
    if use_mock:
        print("⚠️  Running in MOCK mode - using template responses")
    else:
        print("✅ Model loaded successfully")
    
    yield
    
    # Shutdown
    print("👋 Shutting down OmniRL Backend Server...")


# Create FastAPI app
app = FastAPI(
    title="OmniRL Vision-Language API",
    description="Backend API for visuAI image understanding with OmniRL",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== ENDPOINTS ====================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "OmniRL Vision-Language API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    
    Returns service status and model information
    """
    global start_time, omni_service
    
    uptime = time.time() - start_time
    
    return HealthResponse(
        status="healthy",
        model_loaded=omni_service is not None and (omni_service.use_mock or omni_service.model_loaded),
        version="1.0.0",
        uptime=uptime
    )


@app.post("/api/describe", response_model=DescribeResponse, tags=["Description"])
async def describe_image(request: DescribeRequest):
    """
    Generate natural language description from image predictions
    
    Takes MobileNet predictions and generates a human-friendly description.
    
    Example:
    ```json
    {
        "predictions": [
            {"className": "laptop", "probability": 0.9},
            {"className": "desk", "probability": 0.3}
        ]
    }
    ```
    
    Returns:
    ```json
    {
        "text": "A laptop computer is visible on a desk.",
        "confidence": 0.85,
        "processing_time": 0.023,
        "used_predictions": ["laptop", "desk"]
    }
    ```
    """
    global omni_service
    
    if omni_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        description, confidence, used_predictions, processing_time = omni_service.generate_description(
            request.predictions
        )
        
        return DescribeResponse(
            text=description,
            confidence=confidence,
            processing_time=processing_time,
            used_predictions=used_predictions
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Description generation failed: {str(e)}")


@app.post("/api/ask", response_model=AskResponse, tags=["Q&A"])
async def ask_question(request: AskRequest):
    """
    Answer questions about the image based on predictions
    
    Takes MobileNet predictions and a user question, returns an answer.
    
    Example:
    ```json
    {
        "predictions": [
            {"className": "cat", "probability": 0.95},
            {"className": "furniture", "probability": 0.3}
        ],
        "question": "What animal is in the image?"
    }
    ```
    
    Returns:
    ```json
    {
        "text": "The animal appears to be a cat.",
        "confidence": 0.9,
        "processing_time": 0.045,
        "question": "What animal is in the image?"
    }
    ```
    """
    global omni_service
    
    if omni_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    
    try:
        answer, confidence, processing_time = omni_service.answer_question(
            request.predictions,
            request.question
        )
        
        return AskResponse(
            text=answer,
            confidence=confidence,
            processing_time=processing_time,
            question=request.question
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question answering failed: {str(e)}")


# ==================== DEVELOPMENT ====================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🌐 Starting server at http://{host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
