import asyncio
from termninja.server import TermninjaServer
from termninja.controller import TermninjaController
from config import (YOUR_TURN_MESSAGE,
                    OTHER_PLAYER_TURN_MESSAGE,
                    PLAYER_TIMED_OUT_MESSAGE,
                    BOARD_FORMAT,
                    WELCOME_MESSAGE,
                    TIE_VALUE,
                    WIN_VALUE,
                    X_MARKER,
                    O_MARKER)


class TicTacToeBoard:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.fills = [" " for _ in range(9)]
    
    def get_val(self, board_index):
        return self.board[board_index-1]
    
    def set_val(self, board_index, player_id):
        self.board[board_index-1] = player_id
        self.fills[board_index-1] = self.get_player_marker(player_id)

    def valid_move(self, mv):
        """
        Only currently empty cells are valid moves
        """
        return 0 < mv < 10 and self.get_val(mv) == " "

    def get_player_marker(self, player):
        if player == 0:
            return X_MARKER
        return O_MARKER
      
    @staticmethod
    def part_is_winner(part):
        """
        Checks if a list of 3 characters is a tic-tac-toe winner
        """
        # if a list is a winning combo
        st = part[0]
        return st != " " and all([p == st for p in part])

    def check_over(self):
        # check horizontal wins: [1,2,3] [4,5,6] [7,8,9]
        for i in range(0, 7, 3):
            if self.part_is_winner(self.board[i:i+3]):
                return True
        
        # check vertical wins: [1,4,7] [2,5,8] [3,6,9]
        for i in range(0, 3):
            if self.part_is_winner(self.board[i:i+7:3]):
                return True
        
        # check diagonal wins: [1,5,9] [3,5,7]
        if self.part_is_winner(self.board[2:7:2]):
            return True
        if self.part_is_winner(self.board[0:9:4]):
            return True

    def render(self):
        return BOARD_FORMAT.format(*self.fills)


class TicTacToeController(TermninjaController):
    def setUp(self, player1, player2):
        self.players = [player1, player2]
        self.board = TicTacToeBoard()
        self.current_turn = 0
    
    def next_turn(self):
        """
        1, 0, 1, 0, 1 ....
        """
        self.current_turn ^= 1
    
    async def run(self):
        """
        Do at most 9 rounds before it's a tie
        """
        await self.send_board()
        for i in range(9):
            await self.do_round(i)
            if self.board.check_over():
                return await self.handle_winner(i)
        await self.handle_tie()

    async def do_round(self, round_number):
        """
        No matter what a player needs to make a valid choice and
        then the board gets updated.
        """
        choice = await self.get_player_choice()
        self.board.set_val(choice, self.current_turn)
        await self.send_board()
        self.next_turn()
    
    async def get_player_choice(self):
        """
        Each player gets 8 seconds to make a valid choice before
        they lose their turn to the other player
        """
        while True:
            try:
                await self.prompt_players(self.current_turn)
                await self.players[self.current_turn].clear_input_buffer()
                return await self.players[self.current_turn].read_until_valid(
                    self.board.valid_move, coerce=int, timeout=8.0
                )
            except asyncio.TimeoutError:
                await self.send_to_players(PLAYER_TIMED_OUT_MESSAGE)
                self.next_turn()

    async def send_board(self):
        await self.send_to_players(
            self.board.render()
        )
    
    async def prompt_players(self, turn):
        await asyncio.gather(
            self.players[turn].send(YOUR_TURN_MESSAGE),
            self.players[turn-1].send(OTHER_PLAYER_TURN_MESSAGE)
        )

    async def handle_tie(self):
        await asyncio.gather(*[
            p.on_earned_points(TIE_VALUE) for p in self.players
        ])

    async def handle_winner(self, winner):
        self.players[winner].on_earned_points(WIN_VALUE)

    def make_result_message_for(self, player, other_player):
        if player.earned == TIE_VALUE:
            return f'Tied against {other_player.username}'
        elif player.earned == WIN_VALUE:
            return f'Won against {other_player.username}'
        else:
            return f'Lost against {other_player.username}'


class TicTacToeServer(TermninjaServer):
    friendly_name = "Tic-Tac-Toe"
    controller_class = TicTacToeController
    player_count = 2


if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
