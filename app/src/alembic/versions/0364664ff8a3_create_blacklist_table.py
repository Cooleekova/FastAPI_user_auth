"""create blacklist table

Revision ID: 0364664ff8a3
Revises: 193876617957
Create Date: 2022-08-30 16:50:34.186521

"""
from enum import unique
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0364664ff8a3'
down_revision = '193876617957'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "blacklist",
        sa.Column("token", sa.String(250), unique=True),
        sa.Column("email", sa.String(50))
    )


def downgrade() -> None:
    op.drop_table('blacklist')
