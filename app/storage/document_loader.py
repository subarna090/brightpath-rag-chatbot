"""Document loading and chunking for HR policies"""
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.config import settings
from app.utils.logger import logger
from typing import List

def load_hr_documents(docs_path: str = "./docs") -> List[Document]:
    """Load all HR markdown documents from docs folder"""
    try:
        if not os.path.exists(docs_path):
            logger.warning(f"⚠️  Docs path does not exist: {docs_path}")
            return []
        
        # Load all BrightPath_* files (with or without .md extension)
        loader = DirectoryLoader(
            docs_path,
            glob="BrightPath_*",
            loader_cls=TextLoader,
            show_progress=True,
            loader_kwargs={"encoding": "utf-8"}
        )
        
        logger.info(f"🔄 Loading documents from {docs_path}...")
        documents = loader.load()
        logger.info(f"📄 Loaded {len(documents)} documents")
        
        if not documents:
            logger.warning("⚠️  No documents found!")
            return []
        
        return documents
        
    except Exception as e:
        logger.error(f"❌ Error loading documents: {str(e)}")
        return []

def chunk_documents(documents: List[Document]) -> List[Document]:
    """Split documents into chunks for embedding"""
    try:
        if not documents:
            logger.warning("⚠️  No documents to chunk")
            return []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        logger.info(f"🔄 Chunking documents (size={settings.CHUNK_SIZE}, overlap={settings.CHUNK_OVERLAP})...")
        chunks = text_splitter.split_documents(documents)
        logger.info(f"✂️  Created {len(chunks)} chunks")
        
        # Add metadata to chunks
        for i, chunk in enumerate(chunks):
            chunk.metadata.update({
                "chunk_id": i,
                "doc_type": "hr_policy",
                "company": "BrightPath Analytics"
            })
        
        return chunks
        
    except Exception as e:
        logger.error(f"❌ Error chunking documents: {str(e)}")
        return []

def load_and_chunk_documents(docs_path: str = "./docs") -> List[Document]:
    """Load and chunk documents in one step"""
    documents = load_hr_documents(docs_path)
    chunks = chunk_documents(documents)
    return chunks
