import asyncio
import itertools
import random
from termninja import cursor
from termninja.server import TermninjaServer
from termninja.controller import (TermninjaController,
                                  StoreGamesWithSnapshotMixin)
from config import WELCOME_MESSAGE


class SnakeBoard:
    WIDTH = 45
    HEIGHT = 15
    PADDING = 10
    DIRECTIONS = {
        "w": (-1, 0),
        "a": (0, -1),
        "s": (1, 0),
        "d": (0, 1)
    }
    INVALID_TURNS = {
        "a": "d",
        "d": "a",
        "w": "s",
        "s": "w"
    }

    def __init__(self):
        self.init_board()
        self.init_fills()
        self.init_snake()
        self.init_food()
        self.game_over = False
        self.direction = random.choice(
            list(self.DIRECTIONS.keys())
        )

    def init_board(self):
        """
        self.board is a format string with WIDTH*HEIGHT number
        of arguments expected
        """
        top = " " * (self.PADDING+1) + \
              cursor.blue("=" * self.WIDTH) + "\n"
        mid = " " * self.PADDING + \
              cursor.blue("|") + \
              "{}" * self.WIDTH + \
              cursor.blue("|\n") 
        self.board = top + mid*self.HEIGHT + top

    def init_fills(self):
        """
        Fills contains the string representation of each cell
        on the board to be used in the self.board format string
        """
        self.fills = [
            [" " for _ in range(self.WIDTH)]
            for _ in range(self.HEIGHT)
        ]
    
    def init_snake(self):
        """
        In the beginning, there was a snake with only a head
        """
        head = (self.HEIGHT // 2, self.WIDTH // 2)
        self.snake = [head,]
        self.fills[head[0]][head[1]] = cursor.red("@")
    
    def init_food(self):
        """
        Food options are the set of all cells in the board
        """
        self.food_options = set(
            (r, c)
            for r in range(self.HEIGHT)
            for c in range(self.WIDTH)
        )
        self.spawn_food()

    def spawn_food(self):
        """
        Pick a random spot for the next snake food. Options
        are the set of all unoccupied cells.
        """
        choices = self.food_options - set(self.snake)
        self.food = random.choice(list(choices))
        self.fills[self.food[0]][self.food[1]] = cursor.green("*")

    def turn(self, turn):
        if self.is_valid_turn(turn):
            self.direction = turn
    
    def is_valid_turn(self, turn):
        """
        Turning the exact oposite direction is not allowed. Eg.
        if you're going to the right you can't start going left
        """
        invalid = self.INVALID_TURNS.get(self.direction)
        return turn in self.INVALID_TURNS and turn != invalid

    def tick(self):
        """
        Each tick updates the board by one. Basically move the
        snake one cell and check for collisions with the wall
        or some food
        """
        delta_y, delta_x = self.DIRECTIONS[self.direction]
        new_head = (self.snake[0][0] + delta_y, self.snake[0][1] + delta_x)
        if self.check_game_over(new_head):
            self.game_over = True
        else:
            return self.update_snake(new_head)

    def check_game_over(self, new_head):
        """
        Game is over if they've run into a wall or themself
        """
        new_y, new_x = new_head
        if new_x >= self.WIDTH or new_x < 0:
            # hit side will
            return True
        if new_y >= self.HEIGHT or new_y < 0:
            # hit top or bot wall
            return True
        for y, x in self.snake:
            # hit themself
            if new_y == y and new_x == x:
                return True

    def eats_food(self, new_head):
        return self.food[0] == new_head[0] and self.food[1] == new_head[1]

    def update_snake(self, new_head):
        """
        Move the head in the current direction and remove
        the last cell from the tail unless food was eaten.
        Return whether or not food was eaten.
        """
        self.fills[self.snake[0][0]][self.snake[0][1]] = cursor.yellow("#")
        self.fills[new_head[0]][new_head[1]] = cursor.red("@")
        self.snake.insert(0, new_head)
        if self.eats_food(new_head):
            self.spawn_food()
            return True
        else:
            tail = self.snake.pop()
            self.fills[tail[0]][tail[1]] = " "
            return False
    
    def render(self):
        """
        Fill self.board in with the contents of self.fills
        """
        return self.board.format(*itertools.chain(*self.fills))


class SnakeController(StoreGamesWithSnapshotMixin,
                      TermninjaController):
    DELAY = 0.17 # this seems to be the sweet spot

    def setUp(self, player):
        self.board = SnakeBoard()
        self.player = player
        self.disconnected = False

    def make_header(self):
        return (
            f"\tTOTAL SCORE: {cursor.green(self.player.score)}\n"
            f"\tEARNED: {cursor.green(self.player.earned)}\n\n"
        )

    async def run(self):
        """
        Loop through:
            - attempt to get input
            - tick() the board to update
            - send a frame
            - sleep
        """
        while not self.board.game_over:
            time_spent = await self.handle_input()
            got_food = self.board.tick()
            if got_food:
                asyncio.create_task(self.earned_point())
            await self.send_board()
            await asyncio.sleep(self.DELAY - time_spent)

    async def handle_input(self):
        """
        Read input if it's there and send to the board
        The return is the amount of time that we waited
        for input
        """
        try:
            start = self.get_time()
            data = await self.player.read(timeout=self.DELAY)
            self.board.turn(data[-1])
            return self.get_time() - start
        except asyncio.TimeoutError:
            return self.DELAY
    
    async def send_board(self):
        """
        Send one frame
        """
        await self.player.send(
            f"{cursor.CLEAR}"
            f"{self.make_header()}"
            f"{self.board.render()}"
        )
    
    async def earned_point(self):
        """
        Create the task but don't block while waiting for it
        Allows player.on_earned_points to do some work
        """
        asyncio.create_task(self.player.on_earned_points(1))

    def make_result_message_for(self, player):
        return f'Ate {player.earned} pieces of snake food'

    def make_final_snapshot(self):
        return self.board.render()


class SnakeServer(TermninjaServer):
    friendly_name = "Snake"
    controller_class = SnakeController
    player_count = 1

    async def on_player_connected(self, player):
        """
        Let the player know the best way to play before
        queuing them for the game
        """
        await player.send(WELCOME_MESSAGE)
        await player.clear_input_buffer()
        await player.readline()
        await super().on_player_connected(player)


if __name__ == "__main__":
    server = SnakeServer()
    server.start()