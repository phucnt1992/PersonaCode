"""initialize db

Revision ID: 41422609940f
Revises:
Create Date: 2022-01-28 16:35:09.748085

"""
import csv
import os

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "41422609940f"
down_revision = None
branch_labels = None
depends_on = None

FIXTURES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures"
)

DEFAULT_SCHEMA = "music"


def upgrade():
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {DEFAULT_SCHEMA};")

    audit_columns = [
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
    ]

    master_columns = [
        sa.Column("id", sa.SmallInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        *audit_columns,
    ]

    # Definition Tables
    op.create_table(
        "sources",
        *master_columns,
        sa.UniqueConstraint("name", name="source_name_key"),
        schema=DEFAULT_SCHEMA,
    )

    countries_table = op.create_table(
        "countries",
        *master_columns,
        sa.Column("alpha_2", sa.String(length=2), nullable=False),
        sa.Column("alpha_3", sa.String(length=3), nullable=False),
        sa.Column("country_code", sa.String(length=3), nullable=False),
        sa.Column("iso_3166_2", sa.String(length=13), nullable=False),
        sa.Column("region", sa.String(length=10), nullable=True),
        sa.Column("sub_region", sa.String(length=100), nullable=True),
        sa.Column("intermediate_region", sa.String(length=100), nullable=True),
        sa.Column("region_code", sa.String(length=3), nullable=True),
        sa.Column("sub_region_code", sa.String(length=3), nullable=True),
        sa.Column("intermediate_region_code", sa.String(length=3), nullable=True),
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "genres",
        *master_columns,
        sa.UniqueConstraint("name", name="genres_name_key"),
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "source_genres",
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.sources.id",
                name="source_genres_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "genre_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.genres.id",
                name="source_genres_genre_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        schema=DEFAULT_SCHEMA,
    )
    op.create_index(
        "source_genres_source_id_genre_id_idx",
        "source_genres",
        ["source_id", "genre_id"],
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "source_markets",
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.sources.id",
                name="source_markets_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "country_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.countries.id",
                name="source_markets_country_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "images",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False, default=300),
        sa.Column("width", sa.Integer(), nullable=False, default=300),
        sa.Column(
            f"{DEFAULT_SCHEMA}.ource_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.sources.id",
                name="source_images_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        *audit_columns,
        sa.UniqueConstraint("url", name="images_url_key"),
        schema=DEFAULT_SCHEMA,
    )

    # Album Tables
    op.create_table(
        "album_types",
        *master_columns,
        sa.UniqueConstraint("name", name="album_types_name_key"),
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "albums",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("external_id", sa.String(36), nullable=False),
        sa.Column("name", sa.String(length=300), nullable=False),
        sa.Column("uri", sa.String(length=300), nullable=True),
        sa.Column("release_date", sa.String(length=10), nullable=False),
        sa.Column("release_date_precision", sa.String(length=1), nullable=False),
        sa.Column("total_tracks", sa.SmallInteger(), nullable=False),
        sa.Column("href", sa.String(length=2048), nullable=False),
        sa.Column(
            "album_type_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.album_types.id",
                name="albums_album_type_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.sources.id",
                name="albums_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        *audit_columns,
        schema=DEFAULT_SCHEMA,
    )
    op.create_index(
        "albums_external_id_idx",
        "albums",
        ["external_id"],
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "album_external_urls",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "album_id",
            sa.BigInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.albums.id",
                name="album_external_urls_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.sources.id",
                name="album_external_urls_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("url", sa.String(length=2048), nullable=False),
        schema=DEFAULT_SCHEMA,
    )
    op.create_index(
        "albums_external_url_idx",
        "album_external_urls",
        ["album_id", "source_id"],
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "album_genres",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "album_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.albums.id",
                name="album_genres_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "genre_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.genres.id",
                name="source_genres_genre_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        schema=DEFAULT_SCHEMA,
    )
    op.create_index(
        "album_genres_idx",
        "album_genres",
        ["album_id", "genre_id"],
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "album_images",
        sa.Column(
            "album_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.albums.id",
                name="album_images_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "image_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.images.id",
                name="source_images_image_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        schema=DEFAULT_SCHEMA,
    )
    op.create_index(
        "album_images_idx",
        "album_images",
        ["album_id", "image_id"],
        schema=DEFAULT_SCHEMA,
    )

    op.create_table(
        "album_markets",
        sa.Column(
            "album_id",
            sa.BigInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.albums.id",
                name="album_markets_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "country_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                f"{DEFAULT_SCHEMA}.countries.id",
                name="album_markets_country_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        schema=DEFAULT_SCHEMA,
    )

    # SEEDING DATA
    with open(os.path.join(FIXTURES_DIR, "countries.csv")) as countries_csv_file:
        csv_reader = csv.DictReader(countries_csv_file)
        countries_data = []
        for row in csv_reader:
            countries_data.append(
                {
                    "name": row["name"],
                    "alpha_2": row["alpha-2"],
                    "alpha_3": row["alpha-3"],
                    "country_code": row["country-code"],
                    "iso_3166_2": row["iso_3166-2"],
                    "region": row["region"],
                    "sub_region": row["sub-region"],
                    "intermediate_region": row["intermediate-region"],
                    "region_code": row["region-code"],
                    "sub_region_code": row["sub-region-code"],
                    "intermediate_region_code": row["intermediate-region-code"],
                }
            )
        op.bulk_insert(table=countries_table, rows=countries_data)


def downgrade():
    op.execute(f"DROP SCHEMA IF EXISTS {DEFAULT_SCHEMA} CASCADE")
