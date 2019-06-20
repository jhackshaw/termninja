from common import Cursor, start_game
from config import (WELCOME,)



async def writer(r, w):
    w.send(WELCOME)
    await w.drain()
    await r.readline()

async def handle_round(r, w, score):
    await w.send(f"Current score: {score}")
    number = random.choice(1, 100)
    guess = None
    while guess != number:
        data = await r.readline()
        
        try:
            guess = int(data.strip())
        except ValueError:
            continue
        

def high_or_low(reader, writer):
    await welcome(reader, writer)
    while True:
        try:
            score += await handle_round(reader, writer, score)
        except ConnectionResetError:
            print("disconnected")


if __name__ == "__main__":
    start_game(high_or_low, "0.0.0.0", 3000)