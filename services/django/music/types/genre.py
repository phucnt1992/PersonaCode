from __future__ import annotations

from spotipy2 import types


class Genre(types.BaseType):
    def __init__(self, name: str, **kwargs):
        self.name = name

    @classmethod
    def from_dict(cls, name: str) -> Genre:
        return cls(name)
