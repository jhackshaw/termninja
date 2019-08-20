import os
from src.server import Server
from src.snake import Snake
from src.subnet_racer import SubnetRacer

app = Server()

app.add_game(Snake)
app.add_game(SubnetRacer)


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)

    app.start(
        host="0.0.0.0",
        port=3000,
        debug=debug
    )
