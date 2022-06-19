import logging
import os
import warnings

import alembic
import pytest
import pytest_asyncio
from aioresponses import aioresponses
from alembic.config import Config
from music.services import AsyncSpotifyClient
from pytest_bdd import given

from .factories.spotify_credential_factory import SpotifyCredentialFactory

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def django_db_setup():
    """Avoid creating/setting up the test database"""
    pass


@pytest.fixture
def db_access_without_rollback_and_truncate(
    request, django_db_setup, django_db_blocker
):
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ.setdefault("TESTING", "1")

    config = Config(os.path.join(BASE_DIR, "alembic.ini"))
    config.set_main_option("script_location", os.path.join(BASE_DIR, "alembic"))

    try:
        LOGGER.info("Try upgrading database...")
        alembic.command.upgrade(config, "head")
        LOGGER.info("Upgrading database is completed.")
        yield
    finally:
        LOGGER.info("Downgrading database")
        alembic.command.downgrade(config, "base")
        LOGGER.info("Downgrading database is completed.")


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


@given("system has client credentials")
def system_has_client_credentials():
    """system has client credentials."""
    pass
