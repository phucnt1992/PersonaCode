"""Get Markets from Spotify feature tests."""

from asyncio import AbstractEventLoop
from types import coroutine

from aioresponses import aioresponses
from music.services.spotify import AsyncSpotifyClient
from pytest_bdd import scenario, then, when

from .factories import MarketFactory


@scenario("getMarketsFromSpotify.feature", "Get the markets data")
def test_get_the_markets_data():
    """Get the markets data."""
    pass


@when("I request to get market data", target_fixture="request_result")
async def i_request_to_get_market_data(
    spotify_client: AsyncSpotifyClient, auth_aioresponse: aioresponses
):
    auth_aioresponse.get(
        "https://api.spotify.com/v1/markets",
        status=200,
        payload={
            "markets": list(
                map(
                    lambda x: x.country_code,
                    MarketFactory.create_batch(10),
                )
            )
        },
    )

    return await spotify_client.get_available_markets()


@then("the market data should be received")
def the_market_data_should_be_received(
    request_result: coroutine, event_loop: AbstractEventLoop
):
    result = event_loop.run_until_complete(request_result)
    assert len(result) == 10
