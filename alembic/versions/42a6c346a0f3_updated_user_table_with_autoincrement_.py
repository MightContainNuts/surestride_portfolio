"""Updated user table with autoincrement for id

Revision ID: 42a6c346a0f3
Revises: 215dc21a8163
Create Date: 2025-04-02 15:59:41.911101

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42a6c346a0f3'
down_revision: Union[str, None] = '215dc21a8163'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass