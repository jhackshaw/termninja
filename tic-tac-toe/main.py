import asyncio
from shell_games import Cursor, start_game
from config import (YOUR_TURN_MESSAGE,
                    OTHER_PLAYER_TURN_MESSAGE,
                    PLAYER_TIMED_OUT_MESSAGE,
                    BOARD_FORMAT,
                    WELCOME_MESSAGE)




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
        return 0 < mv < 10 and self.get_val(mv) == " "

    def get_player_marker(self, player):
        if player == 0:
            return Cursor.blue("X")
        return Cursor.yellow("O")
      
    @staticmethod
    def part_is_winner(part):
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


class TicTacToeController:
    def __init__(self, user1, user2):
        self.users = [user1, user2]
        self.board = TicTacToeBoard()
        self.current_turn = 0
    
    async def run(self):
        await self.send_board()
        for i in range(9):
            await self.do_round(i)
            if self.board.check_over():
                return await self.handle_winner(i)
        await self.handle_tie()

    async def do_round(self, round_number):
        choice = await self.get_player_choice()
        self.board.set_val(choice, self.current_turn)
        await self.send_board()
        self.next_turn()
    
    def next_turn(self):
        self.current_turn ^= 1 
    
    async def get_player_choice(self):
        while True:
            try:
                await self.prompt_players(self.current_turn)
                await self.users[self.current_turn].clear_input_buffer()
                return await self.users[self.current_turn].read_until_valid(
                    self.board.valid_move, coerce=int, timeout=8.0
                )
            except asyncio.TimeoutError:
                await asyncio.gather(*[
                    u.send(PLAYER_TIMED_OUT_MESSAGE) for u in self.users
                ])
                self.next_turn()

    async def send_board(self):
        msg = self.board.render()
        await asyncio.gather(*[
            u.send(msg) for u in self.users
        ])
    
    async def prompt_players(self, turn):
        await asyncio.gather(
            self.users[turn].send(YOUR_TURN_MESSAGE),
            self.users[turn-1].send(OTHER_PLAYER_TURN_MESSAGE)
        )

    async def handle_tie(self):
        print("tie game")    

    async def handle_winner(self, winner):
        print(f"{winner} wins", flush=True)


async def get_default_winner(user1, user2):
    try:
        await user1.send("other user disconnected, you win (by default)")
        return 0
    except BrokenPipeError:
        try:
            await user2.send("other user disconnected, you win (by default)")
            return 1
        except BrokenPipeError:
            return None

async def tic_tac_toe(user1, user2):
    try:
        controller = TicTacToeController(user1, user2)
        winner = await controller.run()
    except ConnectionResetError:
        print("reset")
        winner = await get_default_winner(user1, user2)
    print(f"winner is {winner}")


if __name__ == "__main__":
    start_game(tic_tac_toe, 
               "0.0.0.0",
               3000,
               player_count=2,
               greeting=WELCOME_MESSAGE)
