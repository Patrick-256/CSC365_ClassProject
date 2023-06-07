"""create indexes

Revision ID: ce130d679e24
Revises: cdae2eab0465
Create Date: 2023-05-24 14:48:33.321656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce130d679e24'
down_revision = 'cdae2eab0465'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index('idx_fantasy_league_name', 'fantasy_leagues',[sa.text('fantasy_league_name text_pattern_ops')])
    op.create_index('idx_user_name', 'users', [sa.text('user_name text_pattern_ops')])


def downgrade() -> None:
    pass
