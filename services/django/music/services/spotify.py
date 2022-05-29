from __future__ import annotations

from types import TracebackType
from typing import List, Optional, Type

from music.types import Market, Genre
from spotipy2 import Spotify
from spotipy2.auth import ClientCredentialsFlow


class AsyncSpotifyClient:
    _client: Spotify

    def __init__(self, client_id: str, client_secret: str) -> None:
        self._client = Spotify(
            ClientCredentialsFlow(client_id=client_id, client_secret=client_secret)
        )

    async def __aenter__(self) -> AsyncSpotifyClient:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._client:
            await self._client.__aexit__(exc_type, exc_value, traceback)

    async def get_albums(self):
        async with self._client as s:
            albums = await s.get_albums()
            return albums

    async def get_available_markets(self) -> List[Market]:
        async with self._client as s:
            markets = await s._get("markets")
            return [Market.from_dict(m) for m in markets["markets"]]

    async def get_genres(self) -> List[Genre]:
        async with self._client as s:
            genres = await s._get("recommendations/available-genre-seeds")
            return [Genre.from_dict(g) for g in genres["genres"]]
