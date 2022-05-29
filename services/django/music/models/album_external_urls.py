from django.db import models
from django.utils.translation import gettext_lazy as _


class AlbumExternalUrl(models.Model):
    class Meta:
        db_table = "album_external_urls"
        managed = False

    id = models.BigAutoField(_("id"), primary_key=True)
    url = models.URLField(_("url"), max_length=2048, null=False)

    album = models.ForeignKey(
        "Album",
        name="album",
        related_name="album",
        on_delete=models.CASCADE,
        null=False,
    )
    source = models.ForeignKey(
        "Source",
        name="source",
        related_name="source",
        on_delete=models.CASCADE,
        null=False,
    )
