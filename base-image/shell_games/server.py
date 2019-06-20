import asyncio
from .user import User


def single_player(handler):
    def wrapped(reader, writer):
        return handler(User(reader, writer))
    return wrapped

def add_to_queue_handler(queue):
    async def handler(reader, writer):
        await queue.put(User(reader, writer))
    return handler

async def start_server(queue, host, port):
    server = await asyncio.start_server(
        add_to_queue_handler(queue),
        host=host,
        port=port,
        reuse_port=True
    )
    async with server:
        await server.serve_forever()

async def start_games(queue, player_count, handler):
    while True:
        asyncio.create_task(handler(*[
            await queue.get() for _ in range(player_count)
        ]))

async def main(handler, host, port, player_count):
    queue = asyncio.Queue()
    server_task = asyncio.create_task(
        start_server(queue, host, port)
    )
    start_games_task = asyncio.create_task(
        start_games(queue, player_count, handler)
    )
    await asyncio.gather(
        server_task,
        start_games_task
    )

def start_game(handler, host, port, player_count=1):    
    try:
        asyncio.run(main(handler, host, port, player_count))
    except KeyboardInterrupt:
        print("user shutdown\n")