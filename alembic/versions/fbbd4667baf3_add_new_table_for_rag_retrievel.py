"""add new table for rag retrievel

Revision ID: fbbd4667baf3
Revises: cd43f0088635
Create Date: 2025-04-04 11:08:58.957745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbbd4667baf3'
down_revision: Union[str, None] = 'cd43f0088635'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
