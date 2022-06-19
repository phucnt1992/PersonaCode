from django.db import models
from django.utils.translation import gettext_lazy as _

from ._base import BaseDefinitionModel, include_schema


class Country(BaseDefinitionModel):
    class Meta:
        db_table = include_schema("countries")
        managed = False

    alpha_2 = models.CharField(_("alpha_2"), max_length=2, null=False)
    alpha_3 = models.CharField(_("alpha_3"), max_length=3, null=False)
    country_code = models.CharField(_("country_code"), max_length=3, null=False)
    iso_3166_2 = models.CharField(_("iso_3166_2"), max_length=13, null=False)
    region = models.CharField(_("region"), max_length=10, null=True)
    sub_region = models.CharField(_("sub_region"), max_length=100, null=True)
    intermediate_region = models.CharField(
        _("intermediate_region"), max_length=100, null=True
    )
    region_code = models.CharField(_("region_code"), max_length=3, null=True)
    sub_region_code = models.CharField(_("sub_region_code"), max_length=3, null=True)
    intermediate_region_code = models.CharField(
        _("intermediate_region_code"), max_length=3, null=True
    )
