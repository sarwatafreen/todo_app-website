"""Initial tables for users and tasks

Revision ID: 001
Revises:
Create Date: 2026-01-27 19:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('email', sa.VARCHAR(length=255), nullable=False),
        sa.Column('role', sa.VARCHAR(length=50), nullable=False, default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, default=0),
        sa.Column('last_failed_login', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('account_locked_until', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('hashed_password', sa.VARCHAR(length=255), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create tasks table
    op.create_table('task',
        sa.Column('id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('owner_id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('due_date', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_user_email', 'users', ['email'])
    op.create_index('ix_user_role', 'users', ['role'])
    op.create_index('ix_task_owner_id', 'task', ['owner_id'])
    op.create_index('ix_task_is_completed', 'task', ['is_completed'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_task_is_completed', table_name='task')
    op.drop_index('ix_task_owner_id', table_name='task')
    op.drop_index('ix_user_role', table_name='users')
    op.drop_index('ix_user_email', table_name='users')

    # Drop tables
    op.drop_table('task')
    op.drop_table('users')