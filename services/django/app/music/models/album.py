from django.db import models
from django.contrib.postgres.fields import ArrayField

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


class Album(models.Model):
    class DatePrecision(models.TextChoices):
        YEAR = "Y", "year"
        MONTH = "M", "month"
        DATE = "D", "date"

    class Meta:
        managed = False

    album_id = models.BigAutoField(name="id")
    source_id = models.CharField(name="source_id", max_length=50, null=False)
    name = models.TextField(name="name", max_length=300, null=False)
    uri = models.CharField(name="uri", max_length=100, null=True)
    available_markets = ArrayField(
        models.CharField(max_length=100),
        name="available_markets",
        blank=False,
        null=True,
    )

    release_date = models.CharField(name="release_date", max_length=10, null=False)
    release_date_precision = models.CharField(
        name="release_date_precision",
        max_length=1,
        choices=DatePrecision.choices,
        default=DatePrecision.MONTH,
        null=False,
    )
    album_type = models.CharField(name="album_type", max_length=100, null=False)
    total_tracks = models.PositiveSmallIntegerField(name="total_tracks", null=False)
