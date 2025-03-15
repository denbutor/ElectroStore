"""Create users table

Revision ID: a213b289e573
Revises: cbc34e35fde1
Create Date: 2025-03-13 20:32:57.813391

"""
from typing import Sequence, Union
from sqlalchemy import Column, Integer, String, Enum
from alembic import op
import sqlalchemy as sa
from app.db.models.user import UserRole

# revision identifiers, used by Alembic.
revision: str = 'a213b289e573'
down_revision: Union[str, None] = 'cbc34e35fde1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('surname', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('nova_post_department', sa.String(), nullable=False),
        sa.Column('role', sa.Enum(UserRole), default=UserRole.client, nullable=False),

    )

def downgrade():
    """Downgrade schema."""
    op.drop_table('users')
