import os
import ssl
from app import app


if __name__ == "__main__":
    debug = os.environ.get('DEBUG', False)
    ssl = os.environ.get('TERMNINJA_API_SSL', None)
    cert_path = os.environ.get('TERMNINJA_CERT_PATH', '/certs')

    if ssl and os.path.exists(cert_path):
        ssl = {
            'cert': f'{cert_path}/fullchain.pem',
            'key': f'{cert_path}/privkey.pem'
        }

    app.run(host="0.0.0.0",
            port=3000,
            debug=debug,
            ssl=ssl)
