"""Updated user table with autoincrement for id and message

Revision ID: f635821a0206
Revises: 42a6c346a0f3
Create Date: 2025-04-02 16:02:12.459966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f635821a0206'
down_revision: Union[str, None] = '42a6c346a0f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create a new table with the correct column type
    op.create_table(
        'user_new',
        sa.Column('user_id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
    )

    # Copy data from the old table
    op.execute('INSERT INTO user_new (user_id, username, email, hashed_password, created_on) SELECT user_id, username, email, hashed_password, created_on FROM user')

    # Drop the old table
    op.drop_table('user')

    # Rename the new table
    op.rename_table('user_new', 'user')


def downgrade() -> None:
    """Downgrade schema."""
    # Reverse the changes by creating the original schema again
    op.create_table(
        'user_old',
        sa.Column('user_id', sa.String(32), primary_key=True),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_on', sa.DateTime(), nullable=False),
    )

    op.execute('INSERT INTO user_old (user_id, username, email, hashed_password, created_on) SELECT user_id, username, email, hashed_password, created_on FROM user')

    op.drop_table('user')

    op.rename_table('user_old', 'user')
