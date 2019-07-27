import argparse
from src.core import Server
from src.games import SnakeManager, SubnetRacerManager, TicTacToeManager


app = Server()

app.add_game_manager(SnakeManager)
app.add_game_manager(SubnetRacerManager)
app.add_game_manager(TicTacToeManager)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', action='store',
                        type=int, dest='port', default=3000)
    parser.add_argument('--host', action='store',
                        type=str, dest='host', default='0.0.0.0')
    parser.add_argument('--debug', action='store_true',
                        dest='debug')

    args = parser.parse_args()

    app.start(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
