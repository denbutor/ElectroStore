"""Create users table1

Revision ID: 4280ee947220
Revises: 0aca3387a932
Create Date: 2025-03-13 21:15:33.930821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4280ee947220'
down_revision: Union[str, None] = '0aca3387a932'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('surname', sa.String(100), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('city', sa.String(100), nullable=False),
        sa.Column('phone_number', sa.String(13), nullable=False),
        sa.Column('nova_post_department', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('client', 'admin', name='userrole'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
