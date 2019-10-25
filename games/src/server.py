import asyncio
import aioredis
import datetime
import functools
import signal
import os
import ssl
import termninja_db as db
from . import cursor
from .player import Player
from .reloader import watchdog
from .messages import TERMNINJA_PROMPT


class RegisterGamesMixin:
    """
    When the server starts update the available games in the database
    """
    ping_database_interval = 2 * 60  # every 2 minutes

    async def on_server_ready(self):
        all_games = {
            g.slug: {
                'name': g.name,
                'description': g.description,
                'icon': getattr(g, 'icon', None),
                'idx': idx+1
            }
            for idx, g in enumerate(self.games)
        }
        await db.games.register_games(all_games)
        return await super().on_server_ready()


class ThrottleConnectionsMixin:
    """
    Throttle connections to a set number per minute using
    redis.
    """
    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
    THROTTLED_MESSAGE = cursor.red('\n\n\t\tTHROTTLED\n\n')
    MAX_CONNECTIONS_PER_MINUTE = int(os.environ.get(
        'MAX_CONNECTIONS_PER_MINUTE', 5
    ))

    async def initialize(self):
        self.redis = await aioredis.create_redis_pool(
            f'redis://{self.REDIS_HOST}',
            maxsize=2
        )
        return await super().initialize()

    def make_key_for(self, player):
        now = datetime.datetime.now()
        return f'{player.address}:{now.minute}'

    async def should_accept_player(self, player):
        key = self.make_key_for(player)
        res = await self.redis.get(key)
        if res and int(res) > self.MAX_CONNECTIONS_PER_MINUTE:
            await player.send(self.THROTTLED_MESSAGE)
            return False
        trans = self.redis.multi_exec()
        trans.incr(key)
        trans.expire(key, 60)
        await trans.execute()
        return await super().should_accept_player(player)

    async def teardown(self):
        self.redis.close()
        await self.redis.wait_closed()


class SSLMixin:
    """
    Tell asyncio to wrap the server in ssl when specified  in
    environment variables
    """
    async def start_async_server(self, **kwargs):
        use_ssl = os.environ.get('TERMNINJA_API_SSL', None)
        cert_path = os.environ.get('TERMNINJA_CERT_PATH', '/etc/letsencrypt')

        ssl_ctx = None
        if use_ssl and os.path.exists(cert_path):
            ssl_ctx = self.make_ssl_context(cert_path)

        return await super().start_async_server(
            ssl=ssl_ctx,
            ssl_handshake_timeout=10 if use_ssl else None,
            **kwargs
        )

    def make_ssl_context(self, cert_path):
        ssl_ctx = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH
        )
        ssl_ctx.load_cert_chain(
            f'{cert_path}/live/play.term.ninja/fullchain.pem',
            f'{cert_path}/live/play.term.ninja/privkey.pem'
        )
        return ssl_ctx


class OptionalAuthenticationMixin:
    """
    Allow a player to authenticate if they want to update score,
    otherwise play anonymously
    """
    enter_token_prompt = (
        f"Enter a play token or press enter "
        "to play anonymously: "
    )
    erase_input = (
        f"{cursor.up(1)}"
        f"{cursor.move_to_column(len(enter_token_prompt))}"
        f"{cursor.ERASE_TO_LINE_END}"
    )
    token_accepted_message = f"{erase_input}{cursor.green(' accepted')}\n"
    token_rejected_message = f"{erase_input}{cursor.red(' rejected')}\n"
    token_expired_message = f"{erase_input}{cursor.red(' token expired')}\n"

    @staticmethod
    def token_is_expired(expiration_datetime):
        return expiration_datetime < datetime.datetime.now()

    async def should_accept_player(self, player):
        try:
            # this allows the token to be piped to stdin on ncat call
            # e.g. with termninja client script -t
            token = await player.readline(timeout=0.1)
            await player.send(f'{self.enter_token_prompt}\n')
        except asyncio.TimeoutError:
            # user must enter the token interactively
            await player.send(self.enter_token_prompt)
            token = await player.readline()

        # play anonymously
        if token == "":
            return await self.on_token_anonymous(player)

        db_user = await db.users.select_by_play_token(token)

        # token rejected
        if db_user is None:
            return await self.on_token_rejected(player)

        # token expired
        if self.token_is_expired(db_user['play_token_expires_at']):
            return await self.on_token_expired(player)

        # token accepted
        return await self.on_token_accepted(player, db_user)

    async def on_token_anonymous(self, player):
        return await super().should_accept_player(player)

    async def on_token_accepted(self, player, db_user):
        await player.send(self.token_accepted_message)
        player.assign_db_user(db_user)
        return await super().should_accept_player(player)

    async def on_token_rejected(self, player):
        await player.send(self.token_rejected_message)
        return False

    async def on_token_expired(self, player):
        await player.send(self.token_expired_message)
        return False

    async def on_player_accepted(self, player):
        await player.send(
            f"\n"
            f"username:         {cursor.green(player.username)}\n"
            f"score:            {cursor.green(player.total_score)}\n"
            f"token expires in: {cursor.green(player.play_token_expires_at)}\n"
            f"\n{cursor.yellow('Press enter to continue...')}"
        )
        await player.readline()
        return await super().on_player_accepted(player)


class BaseServer:
    def __init__(self):
        self.games = []
        self._prompt = None

    def add_game(self, game_class):
        self.games.append(game_class)

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
            f"{idx+1}) {game.name}"
            for idx, game in enumerate(self.games)
        ])
        return TERMNINJA_PROMPT.format(game_choices)

    async def initialize(self):
        self._register_signal_handlers()
        self._prompt = self.make_game_prompt()
        await db.conn.connect()

    async def teardown(self):
        await db.conn.disconnect()

    #
    # internal stuff
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
            if 0 < choice <= len(self.games):
                return choice - 1
            return None
        except ValueError:
            return None

    async def _start_serving(self, **kwargs):
        """
        connect to db
        """
        await self.initialize()
        await self.on_server_ready()
        server = await self.start_async_server(**kwargs)
        async with server:
            try:
                await server.serve_forever()
            except asyncio.CancelledError:
                await self.teardown()

    async def _on_connection(self, reader, writer):
        """
        Figure out what game they want to play and send them to the
        appropriate manager for that game
        """
        player = Player(reader, writer)
        try:
            await self._accept_player(player)
            choice = await self.get_game_choice(player)
            await self.games[choice].player_connected(player)
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


class Server(RegisterGamesMixin,
             ThrottleConnectionsMixin,
             OptionalAuthenticationMixin,
             SSLMixin,
             BaseServer):
    pass
