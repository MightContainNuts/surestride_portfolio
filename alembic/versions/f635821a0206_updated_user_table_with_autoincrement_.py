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
    pass

def downgrade() -> None:
    """Downgrade schema."""
    # Reverse the changes by creating the original schema again
    pass

