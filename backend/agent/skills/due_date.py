"""
Due Date Skill for the AI Task Agent System
Extracts due dates from text based on keywords
"""
from datetime import datetime, timedelta
from typing import Dict, Any
from .base_skill import BaseSkill


class DueDateSkill(BaseSkill):
    """
    Skill to extract due dates from text based on keywords
    """

    def apply(self, text: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply due date extraction to the input text and update the data

        Args:
            text: Input text to process
            data: Current data dictionary to update

        Returns:
            Updated data dictionary
        """
        if not isinstance(text, str):
            return data

        text_lower = text.lower()

        if "kal" in text_lower:
            data["due_date"] = (datetime.now() + timedelta(days=1)).date().isoformat()

        if "aaj" in text_lower:
            data["due_date"] = datetime.now().date().isoformat()

        if "urgent" in text_lower:
            data["priority"] = "high"

        # Detect Urdu language keywords
        if "کام" in text or "یاد دہانی" in text:
            data["language"] = "urdu"

        return data