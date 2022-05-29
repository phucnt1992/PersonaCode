import typing


class SpotifyCredential(typing.TypedDict):
    access_token: str
    token_type: str
    expires_in: int
