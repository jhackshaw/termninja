import termninja_db as db
import asyncio
from slugify import slugify


class ConnectDatabaseMixin:
    ping_database_interval = 2 * 60  # every 2 minutes

    def get_game_kwargs(self):
        return {
            'manager_slug': self.slug
        }

    async def on_manager_ready(self):
        self.slug = slugify(self.get_name())
        asyncio.create_task(self._update_database_task())
        return await super().on_manager_ready()

    async def _update_database_task(self):
        await db.games.create_or_update_game(self.slug, {
            'server_name': self.get_name(),
            'description': self.description,
            'idx': self.idx
        })
        while True:
            await self.ping_database()
            await asyncio.sleep(self.ping_database_interval)

    async def ping_database(self):
        await db.games.update_game(self.slug)
