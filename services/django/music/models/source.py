from django.db import models

from ._base import BaseModel, include_schema


class Source(BaseModel):
    class Meta:
        db_table = 'music"."sources'
        managed = False

    markets = models.ManyToManyField(
        "Country",
        name="markets",
        db_table=include_schema("source_markets"),
        related_name="sources",
    )

    genres = models.ManyToManyField(
        "Genre",
        name="genres",
        db_table=include_schema("source_genres"),
        related_name="sources",
    )
