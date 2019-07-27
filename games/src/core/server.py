import termninja_db as db
import asyncio
import functools
import signal
import os
import uvloop
from .reloader import watchdog
from .player import Player
from .messages import TERMNINJA_PROMPT


uvloop.install()


class Server:
    def __init__(self):
        self.managers = []
        self._prompt = None

    def add_game_manager(self, manager_class):
        instance = manager_class(idx=len(self.managers)+1)
        self.managers.append(instance)

    def start(self, host="0.0.0.0", port=3000, debug=True):
        """
        Run dis
        """
        if (debug and
                os.environ.get('TERMNINJA_SERVER_RUNNING') != "true"):
            watchdog(2)
        else:
            asyncio.run(self._start_serving(host, port), debug=debug)

    def _make_game_prompt(self):
        game_choices = "\n".join([
            f"{idx+1}) {manager.get_name()}"
            for idx, manager in enumerate(self.managers)
        ])
        return TERMNINJA_PROMPT.format(game_choices)

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
        try:
            choice = int(raw_choice.strip())
            if 0 < choice <= len(self.managers):
                return choice - 1
            return None
        except ValueError:
            return None

    async def _start_serving(self, host, port):
        """
        connect to db
        """
        await self._initialize()
        server = await asyncio.start_server(
            self._on_connection,
            host=host,
            port=port,
            reuse_port=True
        )
        async with server:
            try:
                await server.serve_forever()
            except asyncio.CancelledError:
                await self._teardown()

    async def _initialize(self):
        self._prompt = self._make_game_prompt()
        self._register_signal_handlers()
        await db.conn.connect()
        await self._initialize_managers()

    async def _teardown(self):
        await db.conn.disconnect()

    async def _initialize_managers(self):
        await asyncio.gather(*[
            m._initialize() for m in self.managers
        ])

    async def _on_connection(self, reader, writer):
        """
        Queue a newly connected player after calling appropriate hooks.
        """
        player = Player(reader, writer)
        print('[+] connection: ', player.address)
        try:
            choice = await self._get_game_choice(player)
            await self.managers[choice]._player_connected(player)
        except ConnectionResetError:
            await player.close()

    async def _get_game_choice(self, player):
        while True:
            await player.send(self._prompt)
            raw_choice = await player.readline()
            choice = self._validate_choice(raw_choice)
            if choice is not None:
                return choice
