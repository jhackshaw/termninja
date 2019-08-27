import os
from src.server import Server
from src.games.snake import Snake
from src.games.subnet_racer import SubnetRacer
from src.games.hangman import Hangman

app = Server()

app.add_game(Snake)
app.add_game(SubnetRacer)
app.add_game(Hangman)


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)

    app.start(
        host="0.0.0.0",
        port=3000,
        debug=debug
    )
