"""create posts table

Revision ID: a80f11fae551
Revises: 
Create Date: 2025-02-02 12:38:13.894404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a80f11fae551'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'posts', 
        sa.Column('uuid', sa.Integer, nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
        )


def downgrade() -> None:
    op.drop_table('posts')
