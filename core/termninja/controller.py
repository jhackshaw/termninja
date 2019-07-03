import asyncio


class Controller:
    def __init__(self, *users):
        self._users = users
        self.setUp(*users)
    
    def setUp(self, *users):
        """
        initialization for subclasses. don't override __init__()
        """
        pass

    async def start(self):
        """
        call run and handle any errors. should not be overriden.
        """
        try:
            await self.run()
        except (BrokenPipeError, ConnectionResetError) as e:
            pass
        finally:
            print("caught disconnect in controller base...")
            await self.on_disconnect()
            await self.teardown()

    async def run(self):
        """
        Subclass's logic for the controller
        """
        raise NotImplementedError

    async def on_disconnect(self):
        """
        Any subclass action on disconnect.
        users are closed immediately after this.
        """
        pass
    
    async def teardown(self):
        """
        close all user streams
        """
        await asyncio.gather(*[
            u.close() for u in self._users
        ])
    
    async def send_to_users(self, msg):
        """
        send message to all users in this controller
        """
        return await asyncio.gather(*[
            u.send(msg) for u in self._users
        ])