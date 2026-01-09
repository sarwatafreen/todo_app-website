"""
Language Detection Skill for the AI Task Agent System
Detects language based on keywords in the text
"""
from typing import Dict, Any
from .base_skill import BaseSkill


class LanguageDetectionSkill(BaseSkill):
    """
    Skill to detect language based on keywords in the text
    """
    
    def apply(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply language detection to the input text and update the data
        
        Args:
            text: Input text to process
            data: Current data dictionary to update
            
        Returns:
            Updated data dictionary
        """
        if not isinstance(text, str):
            return data
        
        # Detect Urdu language keywords
        if "کام" in text or "یاد دہانی" in text:
            data["language"] = "urdu"
        
        # Add more language detection rules as needed
        # For example, detecting other languages based on keywords
        
        return data