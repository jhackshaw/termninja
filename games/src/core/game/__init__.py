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
    def make_result_message_for(self, player):
        return (
            f'Answered {(self.correct_count / self.question_count)*100:.2f}% '
            f'({self.correct_count}/{self.question_count}) '
            f'correctly'
        )
