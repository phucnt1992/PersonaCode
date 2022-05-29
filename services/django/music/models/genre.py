from ._base import BaseAuditModel


class Genre(BaseAuditModel):
    class Meta:
        db_table = "genres"
        managed = False
