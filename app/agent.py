"""
ContentAgent - Core LLM interaction module for e-commerce content generation.
"""

import os
import re
from typing import Dict, Any, Union
from openai import OpenAI

class ContentAgent:
    """
    Content generation agent that interacts with LLMs to create e-commerce content.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the ContentAgent with API configuration.
        
        Args:
            api_key: OpenAI API key. If None, will try to load from environment or config.py
        """
        if api_key is None:
            api_key = self._load_api_key()
        
        self.client = OpenAI(api_key=api_key)
        print("🔑 API key configured successfully")
    
    def _load_api_key(self) -> str:
        """
        Load API key using secure methods in order of preference:
        1. Environment variable OPENAI_API_KEY
        2. config.py file (fallback for development)
        """
        # Method 1: Environment variable (RECOMMENDED)
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print("🔒 Using API key from environment variable")
            return api_key
        
        # Method 2: config.py file (fallback)
        try:
            import config
            if not hasattr(config, 'OPENAI_API_KEY') or not config.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not found or empty in config.py")
            
            api_key = config.OPENAI_API_KEY
            if api_key == "YOUR_API_KEY_HERE":
                raise ValueError("Please update OPENAI_API_KEY in config.py with your actual API key")
            
            print("⚠️  Using API key from config.py (consider using environment variable for better security)")
            return api_key
            
        except ImportError:
            pass  # config.py doesn't exist, that's fine
        
        # No API key found
        print("❌ Error: No OpenAI API key found!")
        print("\n🔒 SECURE SETUP OPTIONS:")
        print("1. Environment Variable (RECOMMENDED):")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        print("   # Add to ~/.bashrc or ~/.zshrc for persistence")
        print("\n2. Docker Environment:")
        print("   docker-compose run -e OPENAI_API_KEY='your-key' content_agent ...")
        print("\n3. Config File (Development only):")
        print("   Create config.py with: OPENAI_API_KEY = 'your-api-key-here'")
        print("   ⚠️  WARNING: Never commit config.py with real API keys!")
        
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    
    def _get_nested_value(self, data: dict, key_path: str) -> Any:
        """
        Get nested dictionary value using dot notation.
        
        Args:
            data: The dictionary to search
            key_path: Dot-separated path like 'display.type' or simple key like 'name'
            
        Returns:
            The value at the specified path, or empty string if not found
        """
        if '.' not in key_path:
            return data.get(key_path, '')
        
        keys = key_path.split('.')
        current = data
        
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return ''
        
        return current
    
    def _format_list_value(self, value: Any) -> str:
        """
        Format list values for insertion into prompts.
        
        Args:
            value: The value to format
            
        Returns:
            Formatted string representation
        """
        if isinstance(value, list):
            if all(isinstance(item, (str, int, float)) for item in value):
                return ', '.join(str(item) for item in value)
            else:
                return str(value)
        return str(value)
    
    def _construct_prompt(self, product_data: Dict[str, Any], prompt_template: str) -> str:
        """
        Construct the final prompt by replacing placeholders with product data.
        
        Args:
            product_data: Dictionary containing product information
            prompt_template: Template string with placeholders like {name}, {display.type}
            
        Returns:
            Fully constructed prompt string
        """
        # Find all placeholders in the template
        placeholders = re.findall(r'\{([^}]+)\}', prompt_template)
        
        final_prompt = prompt_template
        
        for placeholder in placeholders:
            # Get the value for this placeholder
            value = self._get_nested_value(product_data, placeholder)
            
            # Format the value appropriately
            formatted_value = self._format_list_value(value)
            
            # Replace the placeholder
            final_prompt = final_prompt.replace(f'{{{placeholder}}}', str(formatted_value))
            
            # Log if placeholder wasn't found in product data
            if not value and value != 0:  # 0 is a valid value
                print(f"⚠️  Warning: Placeholder '{placeholder}' not found in product data")
        
        return final_prompt
    
    def generate_content(
        self, 
        product_data: Dict[str, Any], 
        prompt_template: str,
        llm_model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """
        Generate content using the LLM based on product data and prompt template.
        
        Args:
            product_data: Dictionary containing product information
            prompt_template: Template string with placeholders
            llm_model: LLM model to use (default: gpt-3.5-turbo)
            temperature: Creativity level (0.0-2.0, default: 0.7)
            max_tokens: Maximum tokens in response (default: 500)
            
        Returns:
            Generated content string
        """
        # Construct the final prompt
        final_prompt = self._construct_prompt(product_data, prompt_template)
        
        print(f"🔧 Using model: {llm_model}")
        print(f"🌡️  Temperature: {temperature}")
        print(f"📏 Max tokens: {max_tokens}")
        
        try:
            # Make the API call
            response = self.client.chat.completions.create(
                model=llm_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful e-commerce content generation assistant specialized in creating engaging product descriptions and marketing content."
                    },
                    {
                        "role": "user", 
                        "content": final_prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Extract and return the generated content
            generated_content = response.choices[0].message.content.strip()
            return generated_content
            
        except Exception as e:
            print(f"❌ LLM API Error: {e}")
            if "rate limit" in str(e).lower():
                print("💡 Tip: You may have hit the API rate limit. Please wait a moment and try again.")
            elif "authentication" in str(e).lower():
                print("💡 Tip: Please check your API key configuration")
            raise 