from ._base import BaseAuditModel


class AlbumType(BaseAuditModel):
    class Meta:
        db_table = "album_types"
        managed = False
