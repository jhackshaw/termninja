import asyncio


class BaseManager:
    game_class = None
    player_count = 1

    def __init__(self, idx=None):
        self.idx = idx

    #
    # public api
    #
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

    async def on_manager_ready(self):
        """
        Hook called when the server is initialized
        """
        pass

    async def on_player_connected(self, player):
        """
        Hook called when a player first connects to this game
        """
        pass

    async def should_accept_player(self, player):
        """
        Hook called to determine if a player should be allowed to play
        """
        return True

    async def on_player_accepted(self, player):
        """
        Hook called after a player is determined to be allowed to play
        """
        pass

    async def on_player_rejected(self, player):
        """
        Hook called after a player is determined not allowed to play.
        """
        pass

    #
    # private api
    #
    async def _initialize(self):
        """
        Called by Server prior to accepting connections. Create a queue for
        players and start a task that launches games from that queue.

        Producer:
            Server -> _player_connected -> queue player

        Consumer:
            _start_game_task()

        """
        self._player_queue = asyncio.Queue()
        asyncio.create_task(self._start_game_task())
        await self.on_manager_ready()

    async def _player_connected(self, player):
        """
        When server determines a player wants to play this game, this method
        is called. Responsible for calling appropriate hooks and queuing the
        player.
        """
        try:
            await self.on_player_connected(player)
            if await self.should_accept_player(player):
                await self.on_player_accepted(player)
                await self._player_queue.put(player)
            else:
                await self.on_player_rejected(player)
                await player.close()
        except BrokenPipeError:
            await self.on_disconnect_before_queue(player)
            player.close()

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
        game = game_class(*players, **self.get_game_kwargs())
        asyncio.create_task(game.start())
