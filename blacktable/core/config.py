"""
Core configuration for BlackTable
"""
import os
from typing import Optional


class AIConfig:
    """Configuration for AI services"""
    OPENAI_MODEL = "gpt-4o"
    ANTHROPIC_MODEL = "claude-3-sonnet"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    
    @classmethod
    def get_openai_api_key(cls) -> Optional[str]:
        """Get OpenAI API key from environment"""
        return os.getenv("OPENAI_API_KEY")
    
    @classmethod
    def get_anthropic_api_key(cls) -> Optional[str]:
        """Get Anthropic API key from environment"""
        return os.getenv("ANTHROPIC_API_KEY")
