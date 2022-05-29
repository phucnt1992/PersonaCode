from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class BaseAuditModel(models.Model):
    class Meta:
        abstract = True

    created_at = CreationDateTimeField(_("created_at"))
    updated_at = ModificationDateTimeField(_("updated_at"))


class BaseDefinitionModel(BaseAuditModel):
    class Meta:
        abstract = True

    id = models.SmallAutoField(_("id"), primary_key=True)
    name = models.CharField(_("name"), max_length=100, null=False, unique=True)
