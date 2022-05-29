from datetime import datetime, timedelta

import factory
import factory.fuzzy
from music.types import SpotifyCredential


class SpotifyCredentialFactory(factory.Factory):
    token_type = "bearer"
    access_token = factory.Faker("lexify", text="????????????????????????????????")
    expires_in = factory.LazyAttribute(
        lambda o: int(datetime.timestamp(datetime.utcnow() + timedelta(days=1)))
    )

    class Meta:
        model = SpotifyCredential
