"""Fetch Markets Command feature tests."""

from io import StringIO

import pytest
from aioresponses import aioresponses
from django.core.management import call_command
from pytest_bdd import parsers, scenario, then, when

from .factories import MarketFactory


@pytest.mark.django_db
@scenario("fetchMarketsCommand.feature", "Fetch markets command should be success")
def test_fetch_markets_command(apply_migrations):
    """Fetch markets command should be success."""
    pass


@when(
    parsers.parse('the user calls "{command_name}" command'),
    target_fixture="command_result",
)
def the_user_call_a_command(
    auth_aioresponse: aioresponses,
    command_name: str,
) -> str:
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
    out = StringIO()
    call_command(command_name, stdout=out)
    return out.getvalue()


@then("the output should return successful message")
def the_output_should_return_successful_message(command_result: str):
    assert "Successfully fetching new 10 market(s)." in command_result


@then("the new markets should be stored in db")
def the_new_markets_should_be_stored_in_db():
    # import here to avoid circular import at module import time
    from music.models.source import Source

    assert Source.objects.get(pk=1).markets.count() == 10
