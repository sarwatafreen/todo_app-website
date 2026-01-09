# Todo Full-Stack Web Application - Data Model

## Entity: Task

### Attributes
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null, Auto-generated | Unique identifier for the task |
| title | String (255) | Not Null | Title of the task |
| description | String (1000) | Nullable | Detailed description of the task |
| completed | Boolean | Not Null, Default: False | Completion status of the task |
| priority | String (enum) | Not Null, Default: "MEDIUM" | Priority level (LOW, MEDIUM, HIGH) |
| tags | JSON | Nullable | List of tags associated with the task |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when the task was created |
| updated_at | DateTime | Not Null, Auto-generated | Timestamp when the task was last updated |

### SQL Schema
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    priority VARCHAR(20) DEFAULT 'MEDIUM',
    tags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Entity Relationships
- The Task entity is standalone with no relationships to other entities in Phase II

## Indexes
- Primary Key index on `id`
- Index on `completed` field for efficient filtering
- Index on `priority` field for efficient filtering
- Index on `created_at` for sorting operations
- GIN index on `tags` for efficient tag-based queries

## SQLModel Definition
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List
import json

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str = "MEDIUM"  # Enum: LOW, MEDIUM, HIGH
    tags: Optional[List[str]] = None

class Task(TaskBase, table=True):
    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## API Data Transfer Objects (DTOs)

### TaskCreate
```python
class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    priority: str = "MEDIUM"  # Enum: LOW, MEDIUM, HIGH
    tags: Optional[List[str]] = None
```

### TaskRead
```python
class TaskRead(SQLModel):
    id: UUID
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    tags: Optional[List[str]]
    created_at: datetime
    updated_at: datetime
```

### TaskUpdate
```python
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None  # Enum: LOW, MEDIUM, HIGH
    tags: Optional[List[str]] = None
```

## Validation Rules
- Title is required and must be between 1-255 characters
- Description is optional and can be up to 1000 characters
- Priority is required and must be one of: "LOW", "MEDIUM", "HIGH"
- Tags is optional and must be a list of strings
- Completed defaults to False when creating a new task
- created_at and updated_at are automatically managed by the system