"""Pydantic models for request/response schemas"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Message(BaseModel):
    """Single message in conversation"""
    role: str  # "user" or "assistant"
    content: str

class Citation(BaseModel):
    """Citation reference to source document"""
    content: str
    source: str
    chunk_id: Optional[int] = None

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    query: str
    chat_history: Optional[List[Message]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How many annual leave days do I get?",
                "chat_history": [
                    {"role": "user", "content": "What is the leave policy?"},
                    {"role": "assistant", "content": "The leave policy includes..."}
                ]
            }
        }

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str
    sources: List[str]
    citations: List[Citation]
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "You are entitled to 18 days of annual leave...",
                "sources": ["BrightPath_Employee_Handbook.md"],
                "citations": [
                    {
                        "content": "Annual Leave: 18 days per calendar year...",
                        "source": "Leave Policy",
                        "chunk_id": 0
                    }
                ]
            }
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    rag_pipeline: bool
    vector_store: bool