"""Add content column to Post table

Revision ID: 3897b452ab27
Revises: d8f7f72bf4b5
Create Date: 2023-11-19 11:24:25.138698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3897b452ab27'
down_revision: Union[str, None] = 'd8f7f72bf4b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))  
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
