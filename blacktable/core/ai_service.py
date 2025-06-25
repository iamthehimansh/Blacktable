"""
AI Service for structured data generation using Pydantic models
"""
import json
import os
from typing import Any, Type, TypeVar
from pydantic import BaseModel
import openai
from anthropic import Anthropic
from dotenv import load_dotenv

from .config import AIConfig

# Load environment variables
load_dotenv()

T = TypeVar('T', bound=BaseModel)


class AIService:
    """AI service for generating structured data using Pydantic models"""
    
    def __init__(self, provider: str = "openai"):
        """
        Initialize AI service with specified provider
        
        Args:
            provider: AI provider ("openai" or "anthropic")
        """
        self.provider = provider
        self.config = AIConfig()
        
        if provider == "openai":
            api_key = self.config.get_openai_api_key()
            if not api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            self.client = openai.OpenAI(api_key=api_key)
        elif provider == "anthropic":
            api_key = self.config.get_anthropic_api_key()
            if not api_key:
                raise ValueError("Anthropic API key not found in environment variables")
            self.client = Anthropic(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def generate_structured_response(
        self, 
        prompt: str, 
        response_model: Type[T],
        system_prompt: str = None
    ) -> T:
        """
        Generate structured response using Pydantic model
        
        Args:
            prompt: User prompt
            response_model: Pydantic model class for response structure
            system_prompt: Optional system prompt
            
        Returns:
            Instance of response_model with generated data
        """
        # Create schema prompt
        schema = response_model.model_json_schema()
        schema_prompt = f"""
You must respond with valid JSON that matches this exact schema:
{json.dumps(schema, indent=2)}

User request: {prompt}

Respond only with valid JSON, no other text or formatting.
"""
        
        if self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": schema_prompt})
            
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=messages,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
                response_format={"type": "json_object"}
            )
            
            result_text = response.choices[0].message.content
            # log all output to log.log
            # with open("log.log", "a") as log_file:
            #     log_file.write(f"Full Prompt: {schema_prompt}\n")
            #     log_file.write(f"AI Response: {result_text}\n")
            
        elif self.provider == "anthropic":
            full_prompt = f"{system_prompt}\n\n{schema_prompt}" if system_prompt else schema_prompt
            
            response = self.client.messages.create(
                model=self.config.ANTHROPIC_MODEL,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            result_text = response.content[0].text
        
        try:
            # Parse JSON and create Pydantic model instance
            result_data = json.loads(result_text)
            return response_model(**result_data)
        except (json.JSONDecodeError, Exception) as e:
            raise ValueError(f"Failed to parse AI response as valid JSON for {response_model.__name__}: {e}")
    
    def generate_text_response(self, prompt: str, system_prompt: str = None) -> str:
        """
        Generate simple text response
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        if self.provider == "openai":
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=messages,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE
            )
            
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            response = self.client.messages.create(
                model=self.config.ANTHROPIC_MODEL,
                max_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
                messages=[{"role": "user", "content": full_prompt}]
            )
            
            return response.content[0].text
