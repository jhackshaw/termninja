from .server import BaseServer
from .mixins import (OptionalAuthenticationMixin,
                     SSLMixin,
                     RegisterGamesMixin,
                     ThrottleConnectionsMixin)


class Server(RegisterGamesMixin,
             SSLMixin,
             ThrottleConnectionsMixin,
             OptionalAuthenticationMixin,
             BaseServer):
    pass
