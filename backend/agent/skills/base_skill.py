"""
Base Skill class for the AI Task Agent System
Defines the interface for all agent skills
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime, timedelta


class BaseSkill(ABC):
    """
    Abstract base class for all agent skills
    """
    
    @abstractmethod
    def apply(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply the skill to the input text and update the data
        
        Args:
            text: Input text to process
            data: Current data dictionary to update
            
        Returns:
            Updated data dictionary
        """
        pass