"""add foreign key to posts table

Revision ID: 8b897daf74d2
Revises: f2fb88666a0e
Create Date: 2025-02-02 13:02:20.973113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b897daf74d2'
down_revision: Union[str, None] = 'f2fb88666a0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_uuid', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', 
                          source_table='posts', 
                          referent_table='users', 
                          local_cols=['owner_uuid'], 
                          remote_cols=['uuid'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_uuid')
