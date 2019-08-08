import os
import ssl
from src.core import Server
from src.games import SnakeManager, SubnetRacerManager, TicTacToeManager


app = Server()

app.add_game_manager(SnakeManager)
app.add_game_manager(SubnetRacerManager)
app.add_game_manager(TicTacToeManager)


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)
    use_ssl = os.environ.get('TERMNINJA_API_SSL', None)
    cert_path = os.environ.get('TERMNINJA_CERT_PATH', '/etc/letsencrypt')

    ssl_ctx = None
    if use_ssl and os.path.exists(cert_path):
        ssl_ctx = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH
        )
        ssl_ctx.load_cert_chain(
            f'{cert_path}/live/play.term.ninja/fullchain.pem',
            f'{cert_path}/live/play.term.ninja/privkey.pem'
        )
    app.start(
        host="0.0.0.0",
        port=3000,
        debug=debug,
        ssl_ctx=ssl_ctx
    )
