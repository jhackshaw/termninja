from .manager import BaseManager
from .mixins import ConnectDatabaseMixin


__all__ = ['BaseManager', 'Manager', 'ConnectDatabaseMixin']


class Manager(ConnectDatabaseMixin,
              BaseManager):
    pass
