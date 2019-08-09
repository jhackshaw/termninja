import datetime
import termninja_db as db
from src.core import cursor


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
        if not token:
            await player.clear_input_buffer()
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
