"""Configuration settings for the application"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings from environment variables"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "sk-placeholder-key")
    MODEL_CHAT: str = os.getenv("MODEL_CHAT", "gpt-4o-mini")
    MODEL_EMBEDDING: str = os.getenv("MODEL_EMBEDDING", "text-embedding-3-small")
    
    # Chroma Vector Store Configuration
    CHROMA_PATH: str = os.getenv("CHROMA_PATH", "./chroma_db")
    
    # RAG Configuration
    TOP_K: int = int(os.getenv("TOP_K", "5"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # Application Configuration
    APP_NAME: str = "BrightPath RAG Chatbot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()