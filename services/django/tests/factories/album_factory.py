import factory
import factory.fuzzy
from spotipy2.types import Album

from .artist_factory import ArtistFactory


class AlbumFactory(factory.Factory):
    album_type = factory.Faker("sentence")
    available_markets = factory.Faker("country_code")
    artists = factory.List([factory.SubFactory(ArtistFactory) for _ in range(3)])
    copyrights = factory.Faker("sentence")
    external_ids = factory.Dict({"spotify": factory.Faker("uuid4")})
    external_urls = factory.Dict({"spotify": factory.Faker("uri")})
    genres = factory.Faker("music_subgenre")
    href = factory.Faker("uri")
    id = factory.Faker("lexify", text="??????????????????????")
    images = factory.List(
        [
            factory.Dict(
                {
                    "href": factory.Faker("uri"),
                    "height": factory.Faker("random_int"),
                    "width": factory.Faker("random_int"),
                }
            )
        ]
    )
    label = factory.Faker("random_number")
    name = factory.Faker("name")
    popularity = factory.Faker("random_number")
    release_date = factory.Faker("date")
    release_date_precision = factory.fuzzy.FuzzyChoice(("year", "month", "date"))
    restrictions = factory.Dict(
        {"reason": factory.fuzzy.FuzzyChoice(("market", "product", "explicit"))}
    )
    tracks = []
    type = "album"
    uri = factory.Sequence(lambda n: f"spotify:album:{n}")

    class Meta:
        model = Album
        inline_args = (
            "album_type",
            "artists",
            "available_markets",
            "copyrights",
            "external_ids",
            "external_urls",
            "genres",
            "href",
            "id",
            "images",
            "label",
            "name",
            "popularity",
            "release_date",
            "release_date_precision",
            "restrictions",
            "tracks",
            "type",
            "uri",
        )
