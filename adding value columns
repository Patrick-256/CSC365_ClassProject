"""adding value columns

Revision ID: df2c4c9d8b7a
Revises: 9c4bb46735e3
Create Date: 2023-05-22 17:04:44.447927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df2c4c9d8b7a'
down_revision = '9c4bb46735e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('players', sa.Column('player_value', sa.Integer))
    op.add_column('fantasy_teams', sa.Column('fantasy_team_balance', sa.Integer))
    op.add_column('fantasy_leagues', sa.Column('fantasy_league_budget', sa.Integer))


def downgrade() -> None:
    pass
