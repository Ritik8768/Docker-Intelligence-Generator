"""
Model Interface Module
Abstract interface for LLM model calls.
"""

from abc import ABC, abstractmethod
from typing import Dict


class ModelInterface(ABC):
    """Abstract interface for model interactions."""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate output from prompt.
        
        Args:
            prompt: Input prompt string
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if model is available and responding.
        
        Returns:
            True if model is healthy
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        """
        Get model information.
        
        Returns:
            Dictionary with model details
        """
        pass
