import asyncio
from slugify import slugify
from . import cursor


class Manager:
    #
    # public api
    #
    game_class = None
    icon = None
    description = None
    player_count = 1

    def __init__(self):
        self.slug = slugify(self.get_name())

    def get_name(self):
        """
        The name of the Game
        """
        return getattr(self, 'name', self.__class__.__name__)

    def get_game_class(self):
        """
        A way to override the choice of game class
        """
        return self.game_class

    def get_game_kwargs(self):
        """
        Kwargs to pass to Game instance initialization
        """
        return {}

    async def initialize(self):
        """
        Called by server to set up async environment

        Producer:
            Server -> player_connected -> queue player

        Consumer:
            _start_game_task() -> retrieve from queue

        """
        self._player_queue = asyncio.Queue()
        asyncio.create_task(self._start_game_task())

    async def player_connected(self, player):
        """
        When server determines a player wants to play this game, this method
        is called. Responsible for  queuing the
        player.
        """
        await player.send(
            f"{cursor.PAGE_DOWN}"
            f"{cursor.down(50)}"
            f"{cursor.HOME}"
        )
        await self._player_queue.put(player)

    #
    # private api
    #
    async def _start_game_task(self):
        """
        Block until self.player_count players have connected, then call run.
        """
        while True:
            asyncio.create_task(self._launch_game(*[
                await self._player_queue.get()
                for _ in range(self.player_count)
            ]))

    async def _launch_game(self, *players):
        """
        create an instance of game_class and call it's run
        method
        """
        game_class = self.get_game_class()
        game = game_class(*players,
                          game_slug=self.slug,
                          **self.get_game_kwargs())
        asyncio.create_task(game.start())
