"""add content column to posts table

Revision ID: 406b65a92b3c
Revises: 2b153dd80c22
Create Date: 2026-03-23 08:08:31.218185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '406b65a92b3c'
down_revision: Union[str, Sequence[str], None] = '2b153dd80c22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
