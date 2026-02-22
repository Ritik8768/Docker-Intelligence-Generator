"""
Ollama Client Module
Concrete implementation of ModelInterface for Ollama.
"""

import os
import requests
import time
from typing import Dict
from src.model_interface import ModelInterface


class OllamaClient(ModelInterface):
    """Ollama implementation of ModelInterface."""
    
    def __init__(
        self,
        base_url: str = None,
        model: str = "llama3.2:3b",
        timeout: int = 60,
        max_retries: int = 3
    ):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
        """
        if base_url is None:
            base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
    
    def generate(self, prompt: str) -> str:
        """
        Generate output from prompt using Ollama.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated Dockerfile content
            
        Raises:
            ConnectionError: If cannot connect to Ollama
            TimeoutError: If request times out
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1  # Low temperature for consistent output
            }
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    timeout=self.timeout
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get('response', '').strip()
                
            except requests.exceptions.Timeout:
                if attempt == self.max_retries - 1:
                    raise TimeoutError(f"Request timed out after {self.max_retries} attempts")
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except requests.exceptions.ConnectionError:
                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Cannot connect to Ollama at {self.base_url}")
                time.sleep(2 ** attempt)
                
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"Request failed: {str(e)}")
                time.sleep(2 ** attempt)
        
        raise RuntimeError("Failed to generate after all retries")
    
    def health_check(self) -> bool:
        """
        Check if Ollama is running and model is available.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            models = data.get('models', [])
            
            # Check if our model is available
            model_names = [m.get('name', '') for m in models]
            return any(self.model in name for name in model_names)
            
        except Exception:
            return False
    
    def get_model_info(self) -> Dict[str, str]:
        """
        Get information about the model.
        
        Returns:
            Dictionary with model information
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            models = data.get('models', [])
            
            for model in models:
                if self.model in model.get('name', ''):
                    return {
                        'name': model.get('name', 'unknown'),
                        'size': str(model.get('size', 0)),
                        'modified': model.get('modified_at', 'unknown')
                    }
            
            return {
                'name': self.model,
                'size': 'unknown',
                'modified': 'unknown'
            }
            
        except Exception as e:
            return {
                'name': self.model,
                'error': str(e)
            }
