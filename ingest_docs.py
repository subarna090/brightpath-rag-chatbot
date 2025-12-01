#!/usr/bin/env python3
"""
Document ingestion script - Load HR documents into vector store
Run this AFTER adding HR docs to ./docs/ folder
"""
import os
import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import settings
from app.storage.document_loader import load_and_chunk_documents
from app.utils.logger import logger

def ingest_documents():
    """Load and ingest HR documents into Chroma vector store"""
    try:
        logger.info("=" * 60)
        logger.info("🚀 BrightPath RAG - Document Ingestion Started")
        logger.info("=" * 60)
        
        # Step 1: Check if docs folder exists
        docs_path = "./docs"
        if not os.path.exists(docs_path):
            os.makedirs(docs_path)
            logger.warning(f"⚠️  Created {docs_path} folder - please add BrightPath_*.md files")
            return
        
        # Step 2: Load and chunk documents
        chunks = load_and_chunk_documents(docs_path)
        
        if not chunks:
            logger.error("❌ No documents found! Add BrightPath_*.md files to ./docs/")
            return
        
        # Step 3: Create embeddings
        logger.info("🔄 Creating OpenAI embeddings...")
        embeddings = OpenAIEmbeddings(
            model=settings.MODEL_EMBEDDING,
            api_key=settings.OPENAI_API_KEY
        )
        
        # Step 4: Ingest into Chroma
        logger.info(f"💾 Ingesting {len(chunks)} chunks into Chroma...")
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=settings.CHROMA_PATH,
            collection_name="brightpath_hr_policies"
        )
        # Chroma persists automatically, no need to call persist()
        
        # Step 5: Verify ingestion
        logger.info("✅ Document ingestion completed successfully!")
        logger.info(f"📊 Stats:")
        logger.info(f"   - Total chunks: {len(chunks)}")
        logger.info(f"   - Vector store path: {settings.CHROMA_PATH}")
        logger.info(f"   - Embedding model: {settings.MODEL_EMBEDDING}")
        logger.info("=" * 60)
        logger.info("🎉 Ready to start chatbot! Run: docker compose up --build")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    ingest_documents()
