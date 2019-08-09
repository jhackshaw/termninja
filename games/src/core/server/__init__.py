from .server import BaseServer
from .mixins import OptionalAuthenticationMixin


class Server(OptionalAuthenticationMixin,
             BaseServer):
    pass
