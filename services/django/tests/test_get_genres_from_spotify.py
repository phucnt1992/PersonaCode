"""Get genres from Spotify feature tests."""

from asyncio import AbstractEventLoop
from types import coroutine

from aioresponses import aioresponses
from music.services.spotify import AsyncSpotifyClient
from pytest_bdd import scenario, then, when

from .factories import GenreFactory


@scenario("getGenresFromSpotify.feature", "Get the genres data")
def test_get_the_genres_data():
    """Get the genres data."""
    pass


@when("I request to get genre data", target_fixture="request_result")
async def i_request_to_get_genre_data(
    spotify_client: AsyncSpotifyClient, auth_aioresponse: aioresponses
):
    auth_aioresponse.get(
        "https://api.spotify.com/v1/recommendations/available-genre-seeds",
        status=200,
        payload={
            "genres": list(
                map(
                    lambda x: x.name,
                    GenreFactory.create_batch(10),
                )
            )
        },
    )

    return await spotify_client.get_genres()


@then("the genre data should be received")
def the_genre_data_should_be_received(
    request_result: coroutine, event_loop: AbstractEventLoop
):
    result = event_loop.run_until_complete(request_result)
    assert len(result) == 10
