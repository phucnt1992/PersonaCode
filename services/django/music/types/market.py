from __future__ import annotations

from spotipy2 import types


class Market(types.BaseType):
    def __init__(self, country_code: str, **kwargs):
        self.country_code = country_code

    @classmethod
    def from_dict(cls, country_code: str) -> Market:
        return cls(country_code)
