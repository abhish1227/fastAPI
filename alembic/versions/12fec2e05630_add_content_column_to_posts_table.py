"""add Content Column to posts table

Revision ID: 12fec2e05630
Revises: cec3e1c6875e
Create Date: 2025-08-02 16:51:36.496770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12fec2e05630'
down_revision: Union[str, Sequence[str], None] = 'cec3e1c6875e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
