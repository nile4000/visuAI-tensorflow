from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class Prediction(BaseModel):
    """Single prediction from MobileNet classification"""
    className: str = Field(..., description="Class name from MobileNet")
    probability: float = Field(..., ge=0.0, le=1.0, description="Confidence score")

    @field_validator('className')
    @classmethod
    def validate_class_name(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError("className cannot be empty")
        return v.strip()


class DescribeRequest(BaseModel):
    """Request for generating image description"""
    predictions: List[Prediction] = Field(..., min_length=1, max_length=10)
    
    @field_validator('predictions')
    @classmethod
    def validate_predictions(cls, v: List[Prediction]) -> List[Prediction]:
        if not v:
            raise ValueError("At least one prediction is required")
        # Sort by probability descending
        return sorted(v, key=lambda x: x.probability, reverse=True)


class AskRequest(BaseModel):
    """Request for answering questions about image"""
    predictions: List[Prediction] = Field(..., min_length=1, max_length=10)
    question: str = Field(..., min_length=3, max_length=500)
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError("Question must be at least 3 characters")
        return v.strip()


class ResponseBase(BaseModel):
    """Base response model"""
    text: str = Field(..., description="Generated text response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)


class DescribeResponse(ResponseBase):
    """Response for image description"""
    used_predictions: List[str] = Field(..., description="Predictions used in description")


class AskResponse(ResponseBase):
    """Response for question answering"""
    question: str = Field(..., description="Original question")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(default="1.0.0", description="API version")
    uptime: float = Field(..., description="Uptime in seconds")
