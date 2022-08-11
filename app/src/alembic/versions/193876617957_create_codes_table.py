"""create codes table

Revision ID: 193876617957
Revises: 915c86385069
Create Date: 2022-08-11 15:59:05.963883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '193876617957'
down_revision = '915c86385069'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "codes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(50)),
        sa.Column("reset_code", sa.String(100)),
        sa.Column("status", sa.String(1)),
        sa.Column("expired_in", sa.DateTime),
       
    )


def downgrade() -> None:
    op.drop_table('codes')
