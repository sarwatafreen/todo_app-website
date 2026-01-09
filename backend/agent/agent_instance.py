"""
Agent instance for the AI Task Agent System
"""
from backend.agent.agent import Agent
from backend.agent.skills.due_date import DueDateSkill
from backend.agent.skills.language_detection import LanguageDetectionSkill


# Create the main agent instance with all skills
agent = Agent()
agent.add_skill(DueDateSkill())
agent.add_skill(LanguageDetectionSkill())