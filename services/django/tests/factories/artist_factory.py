import factory
import factory.fuzzy
from spotipy2.types import Artist


class ArtistFactory(factory.Factory):
    external_urls = factory.Dict({"spotify": factory.Faker("uuid4")})
    followers = factory.Dict(
        {"href": factory.Faker("uri"), "total": factory.Faker("random_int")}
    )
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
    name = factory.Faker("name")
    popularity = factory.Faker("random_int")
    type = "artist"
    uri = factory.Faker("uri")

    class Meta:
        model = Artist
