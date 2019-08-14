import asyncio
import functools
import signal
import os
import termninja_db as db
from src.core.player import Player
from .reloader import watchdog
from .messages import TERMNINJA_PROMPT


class BaseServer:
    #
    # public api
    #
    def __init__(self):
        self.managers = []
        self._prompt = None

    def add_game_manager(self, manager_class):
        instance = manager_class()
        self.managers.append(instance)

    def start(self, debug=True, **kwargs):
        """
        Run dis
        """
        if (debug and
                os.environ.get('TERMNINJA_SERVER_RUNNING') != "true"):
            watchdog(2)
        else:
            asyncio.run(self._start_serving(**kwargs), debug=debug)

    async def on_player_connected(self, player):
        """
        First hook opportunity for a connection to the server
        """
        print(f'[+] connection from {player.address}')

    async def should_accept_player(self, player):
        """
        Hook to determine if this connection/player should be allowed to play
        """
        return True

    async def on_player_accepted(self, player):
        """
        Hook called when player is allowed to play
        """
        pass

    async def on_server_ready(self):
        """
        Called just before the server is ready to begin accepting connections
        """
        pass

    async def start_async_server(self, **kwargs):
        """
        Call to asyncio start_server can be overriden to
        customize parameters passed
        """
        return await asyncio.start_server(
            self._on_connection,
            reuse_port=True,
            **kwargs
        )

    async def get_game_choice(self, player):
        try:
            # for scripted environments to pipe from stdin
            # e.g. termninja client
            raw_choice = await player.readline(timeout=0.1)
            choice = self._validate_choice(raw_choice)
            if choice is not None:
                await player.clear_input_buffer()
                return choice
        except asyncio.TimeoutError:
            pass
        while True:
            await player.send(self._prompt)
            raw_choice = await player.readline()
            choice = self._validate_choice(raw_choice)
            if choice is not None:
                return choice

    def make_game_prompt(self):
        """
        E.g.
            1) Snake
            2) Subnet Racer
            ....
        """
        game_choices = "\n".join([
            f"{idx+1}) {manager.get_name()}"
            for idx, manager in enumerate(self.managers)
        ])
        return TERMNINJA_PROMPT.format(game_choices)

    #
    # private api
    #
    def _register_signal_handlers(self):
        """
        Register handlers in the event loop for stop signals
        """
        loop = asyncio.get_running_loop()
        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(self._handle_stop_signal)
            )

    def _handle_stop_signal(self):
        """
        Kill dis
        """
        for task in asyncio.Task.all_tasks():
            task.cancel()

    def _validate_choice(self, raw_choice):
        """
        It's an integer and there's a game at the index specified
        """
        try:
            choice = int(raw_choice.strip())
            if 0 < choice <= len(self.managers):
                return choice - 1
            return None
        except ValueError:
            return None

    async def _start_serving(self, **kwargs):
        """
        connect to db
        """
        await self._initialize()
        await self.on_server_ready()
        server = await self.start_async_server(**kwargs)
        async with server:
            try:
                await server.serve_forever()
            except asyncio.CancelledError:
                await self._teardown()

    async def _initialize(self):
        self._prompt = self.make_game_prompt()
        self._register_signal_handlers()
        await db.conn.connect()
        await self._initialize_managers()

    async def _teardown(self):
        await db.conn.disconnect()

    async def _initialize_managers(self):
        await asyncio.gather(*[
            m.initialize() for m in self.managers
        ])

    async def _on_connection(self, reader, writer):
        """
        Queue a newly connected player after calling appropriate hooks.
        """
        player = Player(reader, writer)
        try:
            await self._accept_player(player)
            choice = await self.get_game_choice(player)
            await self.managers[choice].player_connected(player)
        except (ConnectionResetError, ConnectionRefusedError):
            await player.close()

    async def _accept_player(self, player):
        """
        This is where available server hooks are called for mixins
        """
        await self.on_player_connected(player)
        if not await self.should_accept_player(player):
            raise ConnectionRefusedError
        await self.on_player_accepted(player)
