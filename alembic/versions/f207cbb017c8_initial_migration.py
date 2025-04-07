"""Initial migration

Revision ID: f207cbb017c8
Revises: 
Create Date: 2025-04-06 20:01:20.642003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f207cbb017c8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ragdoc',
        sa.Column('doc_id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
        sa.Column('embeddings', sa.LargeBinary(), nullable=False),
    )

    op.create_table(
        'user',
        sa.Column('user_id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=False)

    op.create_table(
        'message',
        sa.Column('message_id', sa.Integer(), primary_key=True),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.user_id'), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('message')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('ragdoc')