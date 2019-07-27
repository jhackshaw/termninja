from .manager import BaseManager
from .mixins import (OptionalAuthenticationMixin,
                     ConnectDatabaseMixin)


__all__ = ['BaseManager', 'Manager', 'OptionalAuthenticationMixin',
           'ConnectDatabaseMixin']


class Manager(ConnectDatabaseMixin,
              OptionalAuthenticationMixin,
              BaseManager):
    pass
