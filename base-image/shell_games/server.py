import asyncio
from .user import User


def greet_and_queue_handler(queue, greeting):
    async def handler(reader, writer):
        if greeting:
            writer.write(greeting.encode())
            await writer.drain()
        await queue.put(User(reader, writer))
    return handler

async def start_server(queue, host, port, greeting):
    server = await asyncio.start_server(
        greet_and_queue_handler(queue, greeting),
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

async def main(handler, host, port, player_count, greeting):
    queue = asyncio.Queue()
    server_task = asyncio.create_task(
        start_server(queue, host, port, greeting)
    )
    start_games_task = asyncio.create_task(
        start_games(queue, player_count, handler)
    )
    await asyncio.gather(
        server_task,
        start_games_task
    )

def start_game(handler, host, port, player_count=1, greeting=None):    
    try:
        asyncio.run(main(handler, host, port, player_count, greeting))
    except KeyboardInterrupt:
        print("user shutdown\n")