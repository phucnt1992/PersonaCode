from ._base import BaseAuditModel, include_schema


class Genre(BaseAuditModel):
    class Meta:
        db_table = include_schema("genres")
        managed = False
