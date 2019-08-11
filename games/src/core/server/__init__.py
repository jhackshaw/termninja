from .server import BaseServer
from .mixins import (OptionalAuthenticationMixin,
                     SSLMixin)


class Server(OptionalAuthenticationMixin,
             SSLMixin,
             BaseServer):
    pass
