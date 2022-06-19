from ._base import BaseAuditModel, include_schema


class AlbumType(BaseAuditModel):
    class Meta:
        db_table = include_schema("album_types")
        managed = False
