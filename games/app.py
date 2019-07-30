import os
from src.core import Server
from src.games import SnakeManager, SubnetRacerManager, TicTacToeManager


app = Server()

app.add_game_manager(SnakeManager)
app.add_game_manager(SubnetRacerManager)
app.add_game_manager(TicTacToeManager)


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)

    app.start(
        host="0.0.0.0",
        port=3000,
        debug=debug
    )
