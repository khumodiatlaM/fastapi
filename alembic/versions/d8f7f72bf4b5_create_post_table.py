"""Create post table

Revision ID: d8f7f72bf4b5
Revises: 
Create Date: 2023-11-19 11:13:41.344178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8f7f72bf4b5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(length=255), nullable=False),
                    )
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
