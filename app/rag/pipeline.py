"""RAG Pipeline - Retrieval + Generation"""
from langchain_core.prompts import PromptTemplate
from app.rag.llm import OpenAILLM
from app.rag.retriever import DocumentRetriever
from app.utils.prompts import RAG_PROMPT_TEMPLATE
from app.utils.logger import logger
from typing import Dict, Any, List

class RAGPipeline:
    """Complete RAG pipeline: retrieve documents + generate answer"""
    
    def __init__(self):
        """Initialize RAG pipeline components"""
        self.retriever = DocumentRetriever()
        self.llm = OpenAILLM()
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template=RAG_PROMPT_TEMPLATE
        )
        logger.info("✅ RAG Pipeline initialized")
    
    def invoke(
        self, 
        query: str, 
        chat_history: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Execute RAG pipeline: retrieve + generate
        
        Args:
            query: User question
            chat_history: Previous messages (for context, not used in current version)
            
        Returns:
            Dict with answer, sources, and citations
        """
        try:
            logger.info(f"🚀 RAG Pipeline processing: {query[:50]}...")
            
            # Step 1: Retrieve relevant documents
            docs = self.retriever.get_relevant_documents(query)
            
            if not docs:
                logger.warning("⚠️  No documents retrieved")
                return {
                    "answer": "I don't have information about that topic in my knowledge base.",
                    "sources": [],
                    "citations": []
                }
            
            # Step 2: Build context from retrieved documents
            context = "\n\n".join([
                f"Document: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
                for doc in docs
            ])
            
            logger.info(f"📚 Retrieved {len(docs)} documents, total context: {len(context)} chars")
            
            # Step 3: Create prompt with context and question
            prompt_text = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Step 4: Generate answer using LLM
            logger.info("🤖 Generating answer with LLM...")
            answer = self.llm.generate(prompt_text)
            
            # Step 5: Extract sources and citations
            sources = list(set([
                doc.metadata.get("source", "Unknown")
                for doc in docs
            ]))
            
            citations = [
                {
                    "content": doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_id": doc.metadata.get("chunk_id", 0)
                }
                for doc in docs[:3]  # Top 3 citations
            ]
            
            result = {
                "answer": answer,
                "sources": sources,
                "citations": citations
            }
            
            logger.info(f"✅ Pipeline completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ RAG Pipeline error: {str(e)}")
            return {
                "answer": f"Sorry, I encountered an error processing your question: {str(e)}",
                "sources": [],
                "citations": []
            }
