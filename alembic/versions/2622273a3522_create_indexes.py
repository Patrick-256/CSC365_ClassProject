"""create indexes

Revision ID: 2622273a3522
Revises: df2c4c9d8b7a
Create Date: 2023-05-24 14:10:49.926222

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '2622273a3522'
down_revision = 'df2c4c9d8b7a'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_index('idx_fantasy_league_name', 'fantasy_leagues', [sa.text('fantasy_league_name text_pattern_ops')])
    op.create_index('idx_user_name', 'users', [sa.text('user_name text_pattern_ops')])


def downgrade() -> None:
    pass
