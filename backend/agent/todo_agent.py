from dataclasses import dataclass
from typing import List
import re

@dataclass
class AgentTask:
    title: str
    priority: str
    tags: List[str]

def todo_agent(text: str) -> AgentTask:
    original_text = text
    text = text.lower().strip()

    # priority detection
    priority = "MEDIUM"  # Default to MEDIUM to match the existing API
    if "urgent" in text or "jaldi" in text or "asap" in text or "immediately" in text:
        priority = "HIGH"
    elif "low" in text or "later" in text:
        priority = "LOW"

    # tags detection
    tags = []
    if "work" in text or "office" in text or "job" in text:
        tags.append("work")
    if "personal" in text or "me" in text or "my" in text:
        tags.append("personal")
    if "shopping" in text or "buy" in text:
        tags.append("shopping")
    if "meeting" in text or "call" in text:
        tags.append("meeting")

    # title extraction - extract a meaningful title from the text
    # Remove priority-related words to get cleaner title
    clean_text = re.sub(r'\b(urgent|jaldi|asap|low|later|high|medium)\b', '', original_text, flags=re.IGNORECASE)
    # Remove tag-related words
    clean_text = re.sub(r'\b(work|personal|shopping|meeting|call|office|job|buy)\b', '', clean_text, flags=re.IGNORECASE)
    # Clean up extra spaces
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    # Use the first meaningful part as title (up to first punctuation or first 5 words)
    title_parts = clean_text.split()[:5]  # Take up to 5 words for title
    title = ' '.join(title_parts) if title_parts else "New Task"

    return AgentTask(
        title=title,
        priority=priority,
        tags=tags
    )