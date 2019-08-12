import datetime
import asyncio
import os
import ssl
import termninja_db as db
from src.core import cursor


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
        return True

    async def on_token_accepted(self, player, db_user):
        await player.send(self.token_accepted_message)
        player.assign_db_user(db_user)
        return True

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
            f"score:            {cursor.green(player.score)}\n"
            f"token expires in: {cursor.green(player.play_token_expires_at)}\n"
            f"\n{cursor.yellow('Press enter to continue...')}"
        )
        await player.readline()
        return await super().on_player_accepted(player)
