"""adding columns

Revision ID: cdae2eab0465
Revises: 1aa57769aa3d
Create Date: 2023-05-22 18:05:18.236747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdae2eab0465'
down_revision = '1aa57769aa3d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('players', sa.Column('player_value', sa.Integer))
    op.add_column('fantasy_teams', sa.Column('fantasy_team_balance', sa.Integer))
    op.add_column('fantasy_leagues', sa.Column('fantasy_league_budget', sa.Integer))


def downgrade() -> None:
    pass
