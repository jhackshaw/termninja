from .server import BaseServer
from .mixins import (OptionalAuthenticationMixin,
                     SSLMixin,
                     RegisterGamesMixin)


class Server(RegisterGamesMixin,
             OptionalAuthenticationMixin,
             SSLMixin,
             BaseServer):
    pass
