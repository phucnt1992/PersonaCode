import factory
from faker_music import MusicProvider

from .spotify_credential_factory import SpotifyCredentialFactory
from .album_factory import AlbumFactory
from .artist_factory import ArtistFactory
from .market_factory import MarketFactory


factory.Faker.add_provider(MusicProvider)

__all__ = ["SpotifyCredentialFactory", "AlbumFactory", "ArtistFactory", "MarketFactory"]
