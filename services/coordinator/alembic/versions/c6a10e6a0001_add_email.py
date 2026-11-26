from alembic import op
import sqlalchemy as sa


revision = "c6a10e6a0001"
down_revision = "b6289dc8b48c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "jobs",
        sa.Column(
            "email",
            sa.String(254),
            nullable=False,
            server_default="client@demo.ghostnet"
        )
    )


def downgrade():
    op.drop_column("jobs", "email")