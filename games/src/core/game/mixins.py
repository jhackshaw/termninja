import termninja_db as db
import asyncio
from src.core import cursor


class StoreGamesMixin:
    async def teardown(self):
        await asyncio.gather(
            super().teardown(),
            self.store_round_played()
        )

    async def store_round_played(self):
        """
        For each player, record the fact that this player
        played this game in the db
        """
        await asyncio.gather(*[
            self.add_round_played(p)
            for p in self._players
        ])

    async def add_round_played(self, player, **kwargs):
        await db.rounds.add_round_played(
            self.manager_slug,
            player.identity['username'],  # this gives us None for anonymous
            player.earned,
            **kwargs
        )


class StoreGamesWithResultMessageMixin(StoreGamesMixin):
    async def add_round_played(self, player, **kwargs):
        return await super().add_round_played(
            player,
            result_message=self.make_result_message_for(player),
            **kwargs
        )

    def make_result_message_for(self, player):
        """
        Probably override this with something more discriptive,
        e.g. Lost to opponent
             Averaged X% in Y quiz
             etc
        """
        raise NotImplementedError


class StoreGamesWithSnapshotMixin(StoreGamesMixin):
    async def add_round_played(self, *args, **kwargs):
        return await super().add_round_played(
            *args,
            result_snapshot=self._get_snapshot(),
            **kwargs
        )

    def _get_snapshot(self):
        snapshot = self.make_final_snapshot()
        return cursor.ansi_to_html(snapshot)

    def make_final_snapshot(self):
        raise NotImplementedError
