import os
from app import app


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)
    app.run(host="0.0.0.0", port=3000, debug=debug)
