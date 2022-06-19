from django.db import models
from django.utils.translation import gettext_lazy as _
from ._base import BaseAuditModel


class Image(BaseAuditModel):
    class Meta:
        db_table = 'music"."images'
        managed = False

    id = models.BigAutoField(_("id"), primary_key=True)
    url = models.URLField(_("url"), max_length=2048, null=False, unique=True)
    height = models.IntegerField(_("height"), default=300, null=False)
    width = models.IntegerField(_("width"), default=300, null=False)

    source = models.ForeignKey(
        "Source",
        name="source",
        on_delete=models.CASCADE,
        null=False,
        related_name="images",
    )
