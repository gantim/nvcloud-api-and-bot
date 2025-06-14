"""Create tg user. upd

Revision ID: dd21611b4855
Revises: 60386b763c55
Create Date: 2025-05-19 20:32:41.030893

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dd21611b4855'
down_revision: Union[str, None] = '60386b763c55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tgusers', 'user_id',
               existing_type=sa.BIGINT(),
               type_=sa.UUID(),
               nullable=True)
    #op.create_unique_constraint(None, 'tgusers', ['user_id'])
    #op.create_foreign_key(None, 'tgusers', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    #op.drop_constraint(None, 'tgusers', type_='foreignkey')
    #op.drop_constraint(None, 'tgusers', type_='unique')
    op.alter_column('tgusers', 'user_id',
               existing_type=sa.UUID(),
               type_=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
