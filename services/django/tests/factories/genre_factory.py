import factory
from music.types import Genre


class GenreFactory(factory.Factory):
    name = factory.Faker("music_genre")

    class Meta:
        model = Genre
