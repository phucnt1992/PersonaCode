from django.db import models

from ._base import BaseAuditModel


class Source(BaseAuditModel):
    class Meta:
        db_table = "sources"
        managed = False

    markets = models.ManyToManyField(
        "Country",
        name="markets",
        db_table="source_markets",
        related_name="sources",
    )

    genres = models.ManyToManyField(
        "Genre",
        name="genres",
        db_table="source_genres",
        related_name="sources",
    )
