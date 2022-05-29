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


def upgrade():
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
    )

    op.create_table(
        "genres",
        *master_columns,
        sa.UniqueConstraint("name", name="genres_name_key"),
    )

    op.create_table(
        "source_genres",
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "sources.id",
                name="source_genres_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "genre_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "genres.id",
                name="source_genres_genre_id_fkey",
                eondelete="CASCADE",
            ),
            nullable=False,
        ),
    )
    op.create_index(
        "source_genres_source_id_genre_id_idx",
        "source_genres",
        ["source_id", "genre_id"],
    )

    op.create_table(
        "source_markets",
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "sources.id",
                name="source_markets_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "country_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "countries.id",
                name="source_markets_country_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )

    op.create_table(
        "images",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("url", sa.String(length=2048), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False, default=300),
        sa.Column("width", sa.Integer(), nullable=False, default=300),
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "sources.id",
                name="source_images_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        *audit_columns,
        sa.UniqueConstraint("url", name="images_url_key"),
    )

    # Album Tables
    op.create_table(
        "album_types",
        *master_columns,
        sa.UniqueConstraint("name", name="album_types_name_key"),
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
                "album_types.id",
                name="albums_album_type_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "sources.id",
                name="albums_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        *audit_columns,
    )
    op.create_index("albums_external_id_idx", "albums", ["external_id"])

    op.create_table(
        "album_external_urls",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "album_id",
            sa.BigInteger(),
            sa.ForeignKey(
                "albums.id",
                name="album_external_urls_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "sources.id",
                name="album_external_urls_source_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("url", sa.String(length=2048), nullable=False),
    )
    op.create_index(
        "albums_external_url_idx",
        "album_external_urls",
        ["album_external_urls_album_id_fkey", "album_external_urls_source_id_fkey"],
    )

    op.create_table(
        "album_genres",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "album_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "albums.id",
                name="album_genres_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "genre_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "generes.id",
                name="source_genres_genre_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )
    op.create_index(
        "album_genres_idx",
        "album_genres",
        ["album_genres_album_id_fkey", "source_genres_genre_id_fkey"],
    )

    op.create_table(
        "album_images",
        sa.Column(
            "album_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "albums.id",
                name="album_images_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "image_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "images.id",
                name="source_images_image_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )
    op.create_index(
        "album_images_idx",
        "album_images",
        ["album_images_album_id_fkey", "source_images_image_id_fkey"],
    )

    op.create_table(
        "album_markets",
        sa.Column(
            "album_id",
            sa.BigInteger(),
            sa.ForeignKey(
                "albums.id",
                name="album_markets_album_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "country_id",
            sa.SmallInteger(),
            sa.ForeignKey(
                "countries.id",
                name="album_markets_country_id_fkey",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
    )

    # SEEDING DATA
    with open(os.path.join(FIXTURES_DIR, "countries.csv")) as countries_csv_file:
        csv_reader = csv.DictReader(countries_csv_file)
        countries_data = []
        for row in csv_reader:
            countries_data.append(
                {
                    "name": row[0],
                    "alpha_2": row[1],
                    "alpha_3": row[2],
                    "country_code": row[3],
                    "iso_3166_2": row[4],
                    "region": row[5],
                    "sub_region": row[6],
                    "intermediate_region": row[7],
                    "region_code": row[8],
                    "sub_region_code": row[9],
                    "intermediate_region_code": row[10],
                }
            )
        op.bulk_insert(table=countries_table, rows=countries_data)


def downgrade():
    op.drop_table("album_markets")
    op.drop_table("album_types")
    op.drop_table("album_external_urls")
    op.drop_table("album_genres")
    op.drop_table("album_images")
    op.drop_table("albums")

    op.drop_table("source_markets")
    op.drop_table("countries")

    op.drop_table("source_genres")
    op.drop_table("genres")

    op.drop_table("source_images")
    op.drop_table("images")

    op.drop_table("sources")
