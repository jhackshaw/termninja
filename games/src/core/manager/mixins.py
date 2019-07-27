import termninja_db as db
import asyncio
import datetime
from slugify import slugify
from .. import cursor


class OptionalAuthenticationMixin:
    """
    Allow a player to authenticate if they want to update score,
    otherwise play anonymously
    """
    enter_token_prompt = (
        "Enter a play token or press enter "
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
        await player.send(self.enter_token_prompt)
        token = await player.readline()
        if token == "":
            # play anonymously
            return True
        user = await db.users.select_by_play_token(token)
        if user is None:
            # invalid token
            await player.send(self.token_rejected_message)
            return False
        if self.token_is_expired(user['play_token_expires_at']):
            # expired token
            await player.send(self.token_expired_message)
            return False
        # accepted token
        await player.send(self.token_accepted_message)
        player.assign_db_user(user)
        return True

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
