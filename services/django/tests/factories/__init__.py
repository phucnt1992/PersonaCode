import factory
from faker_music import MusicProvider

from .album_factory import AlbumFactory
from .artist_factory import ArtistFactory
from .genre_factory import GenreFactory
from .market_factory import MarketFactory
from .spotify_credential_factory import SpotifyCredentialFactory

factory.Faker.add_provider(MusicProvider)

__all__ = [
    "SpotifyCredentialFactory",
    "AlbumFactory",
    "ArtistFactory",
    "MarketFactory",
    "GenreFactory",
]
