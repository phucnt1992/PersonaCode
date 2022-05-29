from aioresponses import aioresponses
import pytest
import pytest_asyncio

from music.services.spotify import AsyncSpotifyClient

from .factories.spotify_credential_factory import SpotifyCredentialFactory


@pytest.fixture(name="auth_aioresponse")
def auth_aioresponse():
    with aioresponses() as m:
        m.post(
            "https://accounts.spotify.com/api/token",
            status=200,
            payload=dict(SpotifyCredentialFactory.create()),
        )
        yield m


@pytest_asyncio.fixture(name="spotify_client")
async def create_spotify_client():
    async with AsyncSpotifyClient("test_client_id", "test_client_secret") as s:
        yield s
