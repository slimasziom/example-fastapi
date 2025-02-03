"""add content to posts table

Revision ID: 7d0dd2660cfe
Revises: a80f11fae551
Create Date: 2025-02-02 12:47:46.793708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d0dd2660cfe'
down_revision: Union[str, None] = 'a80f11fae551'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
