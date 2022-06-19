import asyncio
from typing import List, Union

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.query import QuerySet
from music.models import Country, Source
from music.services import AsyncSpotifyClient
from music.types import Market


class Command(BaseCommand):
    help = "Fetch available markets from spotify"

    def handle(self, *args, **options):
        new_market_count = asyncio.run(
            self.__fetch_markets(
                settings.SPOTIFY_CLIENT_ID, settings.SPOTIFY_CLIENT_SECRET
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully fetching new {new_market_count} market(s)."
            )
        )

    async def __fetch_markets(self, client_id: str, client_secret: str) -> int:
        async with AsyncSpotifyClient(
            client_id=client_id, client_secret=client_secret
        ) as s:
            markets = await s.get_available_markets()

        spotify = await self.__get_or_create_spotify()
        existed_markets = await self.__get_existed_markets(spotify)
        new_markets = await self.__filter_new_markets(markets, existed_markets)
        await self.__save_new_markets(spotify, new_markets)

        return len(new_markets)

    def __get_country_code(self, value: Union[Country, Market]) -> List[str]:
        return value.country_code

    @sync_to_async
    def __get_or_create_spotify(self) -> Source:
        obj, created = Source.objects.get_or_create(id=1, name="spotify")
        if created:
            obj.save()

        return obj

    @sync_to_async
    def __get_existed_markets(self, source: Source) -> QuerySet[Country]:
        return source.markets.all()

    @sync_to_async
    def __filter_new_markets(
        self, spotify_markets: List[Market], existed_markets: QuerySet[Country]
    ) -> QuerySet[Country]:
        return Country.objects.filter(
            alpha_2__in=list(map(self.__get_country_code, spotify_markets))
        ).exclude(alpha_2__in=list(map(self.__get_country_code, existed_markets)))

    @sync_to_async
    def __save_new_markets(self, source: Source, markets: List[Market]) -> None:
        source.markets.add(*markets)
        source.save()
