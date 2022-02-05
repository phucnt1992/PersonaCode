"""initialize db

Revision ID: 41422609940f
Revises:
Create Date: 2022-01-28 16:35:09.748085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41422609940f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "albums",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("source_id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("uri", sa.String(length=300), nullable=True),
        sa.Column("release_date", sa.String(length=10), nullable=False),
        sa.Column("release_date_precision", sa.String(length=1), nullable=False),
        sa.Column("album_type", sa.String(length=100), nullable=False),
        sa.Column("total_tracks", sa.SmallInteger(), nullable=False),
        sa.Column("available_markets", sa.ARRAY(sa.String), nullable=True),
    )


def downgrade():
    op.drop_table("albums")
