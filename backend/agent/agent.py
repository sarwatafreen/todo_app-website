"""
Agent class for the AI Task Agent System
Manages and executes a collection of skills
"""
from typing import List, Dict, Any
from .skills.base_skill import BaseSkill


class Agent:
    """
    Agent that manages and executes a collection of skills
    """
    
    def __init__(self, skills: List[BaseSkill] = None):
        """
        Initialize the agent with a list of skills
        
        Args:
            skills: List of skills to use (optional)
        """
        self.skills = skills or []
    
    def add_skill(self, skill: BaseSkill):
        """
        Add a skill to the agent
        
        Args:
            skill: Skill to add
        """
        self.skills.append(skill)
    
    def process(self, text: str) -> Dict[str, Any]:
        """
        Process text through all skills and return the result

        Args:
            text: Input text to process

        Returns:
            Processed data dictionary
        """
        data = {"title": text}

        for skill in self.skills:
            data = skill.apply(text, data)

        return data

    def run(self, text: str) -> Dict[str, Any]:
        """
        Process text through all skills and return the result (alias for process)

        Args:
            text: Input text to process

        Returns:
            Processed data dictionary
        """
        return self.process(text)