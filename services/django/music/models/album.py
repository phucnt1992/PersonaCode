from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseAuditModel

# Create your models here.
"""
{
  "album_type": "compilation",
  "total_tracks": 9,
  "available_markets": [
    "CA",
    "BR",
    "IT"
  ],
  "external_urls": {
    "spotify": "string"
  },
  "href": "string",
  "id": "2up3OPMp9Tb4dAKM2erWXQ",
  "images": [
    {
      "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228\n",
      "height": 300,
      "width": 300
    }
  ],
  "name": "string",
  "release_date": "1981-12",
  "release_date_precision": "year",
  "restrictions": {
    "reason": "market"
  },
  "type": "album",
  "uri": "spotify:album:2up3OPMp9Tb4dAKM2erWXQ",
  "artists": [
    {
      "external_urls": {
        "spotify": "string"
      },
      "followers": {
        "href": "string",
        "total": 0
      },
      "genres": [
        "Prog rock",
        "Grunge"
      ],
      "href": "string",
      "id": "string",
      "images": [
        {
          "url": "https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228\n",
          "height": 300,
          "width": 300
        }
      ],
      "name": "string",
      "popularity": 0,
      "type": "artist",
      "uri": "string"
    }
  ],
  "tracks": {
    "href": "https://api.spotify.com/v1/me/shows?offset=0&limit=20\n",
    "items": [
      {}
    ],
    "limit": 20,
    "next": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
    "offset": 0,
    "previous": "https://api.spotify.com/v1/me/shows?offset=1&limit=1",
    "total": 4
  }
}
"""


class Album(BaseAuditModel):
    class DatePrecision(models.TextChoices):
        YEAR = "Y", _("year")
        MONTH = "M", _("month")
        DATE = "D", _("date")

    class Meta:
        db_table = "albums"
        managed = False

    id = models.BigAutoField(_("id"), primary_key=True)
    external_id = models.CharField(_("external_id"), max_length=36, null=False)
    name = models.CharField(_("name"), max_length=300, null=False)
    uri = models.CharField(_("uri"), max_length=300, null=True)
    release_date = models.CharField(_("release_date"), max_length=10, null=False)
    release_date_precision = models.CharField(
        _("release_date_precision"),
        max_length=1,
        choices=DatePrecision.choices,
        default=DatePrecision.MONTH,
        null=False,
    )
    total_tracks = models.PositiveSmallIntegerField(_("total_tracks"), null=False)
    href = models.CharField(_("href"), max_length=2048, null=False)

    type = models.ForeignKey(
        "AlbumType",
        name="album_type",
        related_name="albums",
        on_delete=models.CASCADE,
        null=False,
    )

    source = models.ForeignKey(
        "Source",
        name="source",
        related_name="albums",
        on_delete=models.CASCADE,
        null=False,
    )

    images = models.ManyToManyField(
        "Image",
        name="images",
        related_name="albums",
        db_table="album_images",
    )

    available_markets = models.ManyToManyField(
        "Country",
        name="available_markets",
        related_name="albums",
        db_table="album_markets",
    )
