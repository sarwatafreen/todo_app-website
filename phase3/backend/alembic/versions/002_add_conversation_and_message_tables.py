"""Add conversation and message tables

Revision ID: 002
Revises: 001
Create Date: 2026-01-30 13:30:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql
from sqlalchemy import Enum as SQLEnum
import uuid
from enum import Enum

# revision identifiers
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversation table
    op.create_table('conversation',
        sa.Column('id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('title', sa.VARCHAR(length=255), nullable=True),
        sa.Column('user_id', sa.VARCHAR(length=255), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create message table
    op.create_table('message',
        sa.Column('id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('conversation_id', sa.VARCHAR(length=36), nullable=False),
        sa.Column('user_id', sa.VARCHAR(length=255), nullable=False),
        sa.Column('role', SQLEnum('user', 'assistant', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('order_index', sa.Integer(), nullable=False, default=0),
        sa.Column('timestamp', postgresql.TIMESTAMP(timezone=True),
                 server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_timestamp', 'message', ['timestamp'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_message_timestamp', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')
    op.drop_index('ix_conversation_user_id', table_name='conversation')

    # Drop tables
    op.drop_table('message')
    op.drop_table('conversation')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS messagerole_enum;")