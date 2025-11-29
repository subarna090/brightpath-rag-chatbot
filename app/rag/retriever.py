"""Document retrieval from vector store"""
from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.storage.vectorstore import get_vectorstore
from app.config import settings
from app.utils.logger import logger
from typing import List, Optional

class DocumentRetriever:
    """Retrieves relevant documents from vector store"""
    
    def __init__(self):
        """Initialize retriever with vector store"""
        self.vectorstore = get_vectorstore()
    
    def get_relevant_documents(
        self, 
        query: str, 
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Retrieve top-k relevant documents for a query
        
        Args:
            query: Search query
            k: Number of documents to retrieve (defaults to settings.TOP_K)
            
        Returns:
            List of relevant documents
        """
        if k is None:
            k = settings.TOP_K
        
        if not self.vectorstore:
            logger.warning("⚠️  Vector store not available")
            return []
        
        try:
            logger.info(f"🔍 Retrieving {k} documents for query: {query[:50]}...")
            documents = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"✅ Retrieved {len(documents)} documents")
            return documents
            
        except Exception as e:
            logger.error(f"❌ Error retrieving documents: {str(e)}")
            return []
    
    def get_relevant_documents_with_scores(
        self, 
        query: str, 
        k: Optional[int] = None
    ) -> List[tuple]:
        """
        Retrieve documents with similarity scores
        
        Args:
            query: Search query
            k: Number of documents to retrieve
            
        Returns:
            List of (document, score) tuples
        """
        if k is None:
            k = settings.TOP_K
        
        if not self.vectorstore:
            return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
            
        except Exception as e:
            logger.error(f"❌ Error retrieving documents with scores: {str(e)}")
            return []
