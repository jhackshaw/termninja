import asyncio
from termninja import db


class Controller:
    def __init__(self, *players):
        self._players = players
        self.setUp(*players)
    
    def setUp(self, *players):
        """
        Initialization for subclasses. don't override __init__()
        """
        pass
    
    @classmethod
    def get_friendly_name(cls):
        """
        The name that represents this game in the database
        """
        return getattr(cls, 'friendly_name', cls.__name__)

    async def start(self):
        """
        Call run and handle any errors. should not be overriden.
        """
        try:
            await self.run()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            await self.on_disconnect()
            await self.teardown()

    async def run(self):
        """
        Subclass's logic for the controller
        """
        raise NotImplementedError

    async def on_disconnect(self):
        """
        Hook for any diconnect actions
        players are closed immediately after this.
        """
        pass
    
    async def teardown(self):
        """
        Close all player streams
        """
        close_task = asyncio.gather(*[
            p.close() for p in self._players
        ])
        store_task = asyncio.gather(*[
            self.store_round_played(p) for p in self._players
        ])
        await asyncio.gather(
            close_task,
            store_task
        )
    
    async def send_to_players(self, msg):
        """
        Send message to all players in this controller
        """
        return await asyncio.gather(*[
            p.send(msg) for p in self._players
        ])

    async def store_round_played(self, player):
        """
        Record the fact that this player played this game in the db
        """
        await db.rounds.add_round_played(
            self.get_friendly_name(),
            player.identity['username'],
            player.earned
        )


class GenericQuizController(Controller):
    pass