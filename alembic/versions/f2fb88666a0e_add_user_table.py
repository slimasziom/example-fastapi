"""add user table

Revision ID: f2fb88666a0e
Revises: 7d0dd2660cfe
Create Date: 2025-02-02 12:54:54.389998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2fb88666a0e'
down_revision: Union[str, None] = '7d0dd2660cfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('uuid', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('uuid'),
                    sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')
