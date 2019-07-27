from .game import BaseGame, GenericQuizGameBase, GenericQuestion
from .mixins import (StoreGamesMixin,
                     StoreGamesWithResultMessageMixin,
                     StoreGamesWithSnapshotMixin)


__all__ = ['BaseGame', 'StoreGamesMixin', 'StoreGamesWithResultMessageMixin',
           'StoreGamesWithSnapshotMixin', 'Game', 'GenericQuizGameBase',
           'GenericQuestion', 'GenericQuizGame']


class Game(StoreGamesWithResultMessageMixin,
           BaseGame):
    pass


class GenericQuizGame(StoreGamesWithResultMessageMixin,
                      GenericQuizGameBase):
    pass
