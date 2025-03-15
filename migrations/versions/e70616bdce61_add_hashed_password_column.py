"""Add hashed_password column

Revision ID: e70616bdce61
Revises: 4280ee947220
Create Date: 2025-03-14 01:49:14.210047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e70616bdce61'
down_revision: Union[str, None] = '4280ee947220'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False, server_default='default_hashed_value'))
    op.execute("UPDATE users SET hashed_password = 'default_hashed_value'")  # Заміни на реальний хеш
    op.alter_column('users', 'hashed_password', server_default=None)  # Видаляємо дефолт після оновлення
    op.drop_column('users', 'password')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('password', sa.String(), nullable=False, server_default='default_password'))
    op.execute("UPDATE users SET password = 'default_password'")
    op.alter_column('users', 'password', server_default=None)
    op.drop_column('users', 'hashed_password')