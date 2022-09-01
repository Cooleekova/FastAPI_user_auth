"""create OTPS tables

Revision ID: c3e2124165a0
Revises: 0364664ff8a3
Create Date: 2022-09-01 16:45:48.911625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3e2124165a0'
down_revision = '0364664ff8a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "otps",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("recipient_id", sa.String(100)),
        sa.Column("session_id", sa.String(100)),
        sa.Column("otp_code", sa.String(6)),
        sa.Column("status", sa.String(1)),
        sa.Column("created_on", sa.DateTime),
        sa.Column("updated_on", sa.DateTime),
        sa.Column("otp_failed_count", sa.Integer, default=0)
        
    )
    op.create_table(
        "otp_blocks",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("recipient_id", sa.String(100)),
        sa.Column("created_on", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table('otps')
    op.drop_table('otp_blocks')




