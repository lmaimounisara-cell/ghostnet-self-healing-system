"""add job status

Revision ID: b6289dc8b48c
Revises: 1a519c30837c
"""

from alembic import op
import sqlalchemy as sa

revision = "b6289dc8b48c"
down_revision = "1a519c30837c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "jobs",
        sa.Column(
            "status",
            sa.String(),
            server_default="pending",
            nullable=False
        )
    )


def downgrade():
    op.drop_column("jobs", "status")