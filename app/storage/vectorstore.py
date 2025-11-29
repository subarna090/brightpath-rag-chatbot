"""Vector store management using Chroma"""
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings
from app.utils.logger import logger
from typing import Optional

_vectorstore_instance: Optional[Chroma] = None

def get_vectorstore() -> Optional[Chroma]:
    """Get or create vector store instance"""
    global _vectorstore_instance
    
    if _vectorstore_instance is not None:
        return _vectorstore_instance
    
    try:
        embeddings = OpenAIEmbeddings(
            model=settings.MODEL_EMBEDDING,
            api_key=settings.OPENAI_API_KEY
        )
        
        _vectorstore_instance = Chroma(
            persist_directory=settings.CHROMA_PATH,
            embedding_function=embeddings,
            collection_name="brightpath_hr_policies"
        )
        
        logger.info(f"✅ Vector store initialized at {settings.CHROMA_PATH}")
        return _vectorstore_instance
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize vector store: {str(e)}")
        return None

def init_empty_vectorstore() -> bool:
    """Initialize empty vector store if it doesn't exist"""
    try:
        embeddings = OpenAIEmbeddings(
            model=settings.MODEL_EMBEDDING,
            api_key=settings.OPENAI_API_KEY
        )
        
        Chroma(
            persist_directory=settings.CHROMA_PATH,
            embedding_function=embeddings,
            collection_name="brightpath_hr_policies"
        )
        
        logger.info("✅ Empty vector store created")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize empty vector store: {str(e)}")
        return False
