from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ..models.user import User

class TodoService:
    def __init__(self, session: Session):
        self.session = session

    def create_todo(self, todo_create: TodoCreate, user_id: UUID) -> TodoRead:
        """Create a new todo for a user."""
        # Verify the user exists
        user = self.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        # Create the todo
        db_todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            is_completed=todo_create.is_completed,
            user_id=user_id,
            due_date=todo_create.due_date
        )

        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)

        # Convert to TodoRead model manually
        return TodoRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            is_completed=db_todo.is_completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            due_date=db_todo.due_date
        )

    def get_todos_by_user(self, user_id: UUID) -> List[TodoRead]:
        """Get all todos for a specific user."""
        todos = self.session.exec(
            select(Todo).where(Todo.user_id == user_id)
        ).all()

        # Convert to TodoRead models manually
        return [
            TodoRead(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                is_completed=todo.is_completed,
                user_id=todo.user_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
                due_date=todo.due_date
            )
            for todo in todos
        ]

    def get_todo_by_id(self, todo_id: UUID, user_id: UUID) -> Optional[TodoRead]:
        """Get a specific todo by ID for a user."""
        todo = self.session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).first()

        if not todo:
            return None

        # Convert to TodoRead model manually
        return TodoRead(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            is_completed=todo.is_completed,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            due_date=todo.due_date
        )

    def update_todo(self, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[TodoRead]:
        """Update a specific todo for a user."""
        db_todo = self.session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).first()

        if not db_todo:
            return None

        # Update fields that are provided
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)

        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)

        # Convert to TodoRead model manually
        return TodoRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            is_completed=db_todo.is_completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            due_date=db_todo.due_date
        )

    def delete_todo(self, todo_id: UUID, user_id: UUID) -> bool:
        """Delete a specific todo for a user."""
        db_todo = self.session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).first()

        if not db_todo:
            return False

        self.session.delete(db_todo)
        self.session.commit()
        return True

    def toggle_todo_completion(self, todo_id: UUID, user_id: UUID, is_completed: bool) -> Optional[TodoRead]:
        """Toggle the completion status of a specific todo for a user."""
        db_todo = self.session.exec(
            select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        ).first()

        if not db_todo:
            return None

        db_todo.is_completed = is_completed
        self.session.add(db_todo)
        self.session.commit()
        self.session.refresh(db_todo)

        # Convert to TodoRead model manually
        return TodoRead(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            is_completed=db_todo.is_completed,
            user_id=db_todo.user_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at,
            due_date=db_todo.due_date
        )