"""FastAPI application - Main entry point"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import sys

# Import models and config
from app.config import settings
from app.models import ChatRequest, ChatResponse, HealthResponse, Citation, Message
from app.rag.pipeline import RAGPipeline
from app.utils.logger import logger

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG-powered HR Policy Assistant for BrightPath Analytics"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG pipeline instance
rag_pipeline = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG pipeline on startup"""
    global rag_pipeline
    try:
        logger.info("🚀 Starting up BrightPath RAG Chatbot...")
        rag_pipeline = RAGPipeline()
        logger.info("✅ RAG Pipeline ready")
    except Exception as e:
        logger.error(f"❌ Failed to initialize RAG Pipeline: {str(e)}")
        rag_pipeline = None

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to BrightPath RAG Chatbot",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        rag_pipeline=rag_pipeline is not None,
        vector_store=rag_pipeline is not None and rag_pipeline.retriever.vectorstore is not None
    )

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint - Process user query and return RAG-based answer
    
    Args:
        request: ChatRequest with query and optional chat_history
        
    Returns:
        ChatResponse with answer, sources, and citations
    """
    # Validate input
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # Check if pipeline is ready
    if rag_pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="RAG Pipeline not initialized. Check your OpenAI API key."
        )
    
    try:
        logger.info(f"📨 Chat request: {request.query[:50]}...")
        
        # Convert chat history if provided
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
        
        # Execute RAG pipeline
        result = rag_pipeline.invoke(request.query, chat_history)
        
        # Parse citations
        citations = [
            Citation(
                content=c["content"],
                source=c["source"],
                chunk_id=c.get("chunk_id")
            )
            for c in result["citations"]
        ]
        
        response = ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            citations=citations
        )
        
        logger.info(f"✅ Chat response sent")
        return response
        
    except Exception as e:
        logger.error(f"❌ Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/api/info", tags=["Info"])
async def get_info():
    """Get application information"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "openai_model": settings.MODEL_CHAT,
        "embedding_model": settings.MODEL_EMBEDDING,
        "vector_store": settings.CHROMA_PATH,
        "top_k": settings.TOP_K
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
