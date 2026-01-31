from pydantic import BaseModel
from typing import Optional

class BaseResponse(BaseModel):
    """Base response model for all API responses"""
    success: bool
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    code: Optional[str] = None

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str