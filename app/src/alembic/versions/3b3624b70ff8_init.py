"""init

Revision ID: 3b3624b70ff8
Revises: 915c86385069
Create Date: 2022-08-09 23:15:09.021988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b3624b70ff8'
down_revision = '915c86385069'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(50)),
        sa.Column("password", sa.String(200)),
        sa.Column("fullname", sa.String(50)),
        sa.Column("created_on", sa.DateTime),
        sa.Column("status", sa.String(1)),
    )



def downgrade() -> None:
    op.drop_table('users')