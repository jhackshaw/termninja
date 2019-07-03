import asyncio
from .user import User
from .cursor import Cursor
from .controller import Controller
from .db import db


class Server:
    HOST = "0.0.0.0"
    PORT = 3000
    controller_class = Controller
    player_count = 1
    
    def start(self):
        """
        Start listening for connections and starting games.
        Should not be overridden
        """
        try:
            asyncio.run(self._start_serving(), debug=True)
        except KeyboardInterrupt:
            print("[!] user shutdown")
    
    def get_controller_class(self):
        return self.controller_class

    async def user_connected(self, user):
        """
        First read/write opportunity for a connected user. Good
        place to send initial welcome messages, etc.
        """
        pass

    async def should_accept_user(self, user):
        """ Any logic to determine if the user is allowed to play
        """
        return True
    
    async def on_user_accepted(self, user):
        """
        First read/write opportunity after a user is accepted
        """
        pass      

    async def _start_serving(self):
        """
        1. connect to the database
        2. start _self._server_task()
            producer of users
        3. start _self.start_game_task()
            consumer of users to start controller to handle connected users 
        4. run until complete/cancelled
        5. disconnect from the database
        """
        await self._initialize()
        try:
            server_task = asyncio.create_task(
                self._server_task()
            )
            start_games_task = asyncio.create_task(
                self._start_game_task()
            )
            await asyncio.gather(
                server_task,
                start_games_task
            )
        except asyncio.CancelledError:
            pass
        finally:
            await self._teardown()
    
    async def _initialize(self):
        """
        initialize environment for the server
        """
        await db.connect()
        print("[+] db connected")
        self._player_queue = asyncio.Queue()

    async def _teardown(self):
        """
        teardown any resources, etc.
        """
        await db.disconnect()
        print("[-] db disconnected")

    async def _server_task(self):
        """
        Start the async server.
        """
        server = await asyncio.start_server(
            self._on_connection,
            host=self.HOST,
            port=self.PORT,
            reuse_port=True
        )
        async with server:
            await server.serve_forever()

    async def _on_connection(self, reader, writer):
        """
        Queue a newly connected user after calling appropriate hooks.
        """
        addr = writer.get_extra_info('peername')
        print(f"[+] connection {addr[0]}")
        user = User(reader, writer)
        try:
            await self.user_connected(user)
            await self._accept_user(user)
        except ConnectionResetError:
            print("connection closed before player queued")
            await user.close()

    async def _accept_user(self, user):
        """
        Determine if a user should be accepted, call appropriate hooks,
        add user to the _player_queue
        """
        if await self.should_accept_user(user):
            await self.on_user_accepted(user)
            await self._player_queue.put(user)
        else:
            await user.close() 

    async def _start_game_task(self):
        """
        Block until self.player_count users have connected, then call run.
        """
        while True:
            asyncio.create_task(self._launch_game(*[
                await self._player_queue.get() for _ in range(self.player_count)
            ]))

    async def _launch_game(self, *users):
        """
        create an instance of game_controller and call it's run
        method
        """
        controller_class = self.get_controller_class()
        controller = controller_class(*users)
        asyncio.create_task(controller.start()) 


class RequireTokenServer(Server):
    """ 
    Only accept user's if they provide a valid, signed JWT
    """
    enter_token_prompt = "Enter your token: "

    async def should_accept_user(self, user):
        await user.send(self.enter_token_prompt)
        token = await user.readline()
        return self.verify_token(token)
    
    async def on_user_accepted(self, user):
        await user.send(
            f"{Cursor.up(1)}"
            f"{Cursor.move_to_column(len(self.enter_token_prompt))}"
            f"{Cursor.ERASE_TO_LINE_END}"
            f"{Cursor.green(' accepted')}\n"
        )
        return await super().on_user_accepted(user)

    def verify_token(self, token):
        return token == "shellgames" # will verify jwt, this for now

