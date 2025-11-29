"""LLM (Large Language Model) integration with OpenAI"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings
from app.utils.logger import logger
from app.utils.prompts import RAG_SYSTEM_PROMPT
from typing import Optional

class OpenAILLM:
    """OpenAI Language Model wrapper"""
    
    def __init__(self):
        """Initialize OpenAI chat model"""
        try:
            self.llm = ChatOpenAI(
                model=settings.MODEL_CHAT,
                temperature=0.1,
                api_key=settings.OPENAI_API_KEY,
                max_tokens=1500
            )
            logger.info(f"✅ LLM initialized: {settings.MODEL_CHAT}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize LLM: {str(e)}")
            self.llm = None
    
    def generate(self, prompt: str) -> str:
        """
        Generate response using OpenAI
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated response text
        """
        if not self.llm:
            return "❌ LLM not available. Please check your OpenAI API key."
        
        try:
            messages = [
                SystemMessage(content=RAG_SYSTEM_PROMPT),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {str(e)}")
            return f"I encountered an error: {str(e)}"
    
    def generate_with_system(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate response with custom system prompt
        
        Args:
            system_prompt: System message
            user_prompt: User message
            
        Returns:
            Generated response text
        """
        if not self.llm:
            return "❌ LLM not available"
        
        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"❌ Error generating response: {str(e)}")
            return f"Error: {str(e)}"
