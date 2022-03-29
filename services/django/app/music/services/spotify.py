fyrom contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Optional, Type

import httpx


class AsyncSpotifyClient(AbstractAsyncContextManager):


    _client: httpx.AsyncClient

    def __init__(self) -> None:
        self._client = httpx.AsyncClient(base_url='https://api.spotify.com/v1/')

    async def __aenter__(self) -> httpx.AsyncClient:
        return self._client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if not self._client.is_closed:
            await self._client.aclose()

    async def get_albums(self):
        resp = await self._client.get('/albums')
        resp.json
