"""init

Revision ID: 915c86385069
Revises: 
Create Date: 2022-08-08 21:00:52.302903

"""
from alembic import op
import sqlalchemy as sa

# alembic init alembic
# alembic revision -m "init"
# alembic upgrade head
# alembic downgrade -1


# revision identifiers, used by Alembic.
revision = '915c86385069'
down_revision = None
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