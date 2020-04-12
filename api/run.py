import os
import ssl
from app import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=os.environ.get("DEBUG", False))
