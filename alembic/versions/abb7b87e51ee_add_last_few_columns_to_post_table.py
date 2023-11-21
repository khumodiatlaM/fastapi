"""Add last few columns to post table

Revision ID: abb7b87e51ee
Revises: 0aa92b294fea
Create Date: 2023-11-21 20:12:02.779523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abb7b87e51ee'
down_revision: Union[str, None] = '0aa92b294fea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.String(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
