import factory
from music.types import Market


class MarketFactory(factory.Factory):
    country_code = factory.Faker("country_code")

    class Meta:
        model = Market
