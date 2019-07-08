import asyncio
import itertools
import random
from termninja.server import TermninjaServer
from termninja.controller import Controller
from termninja.cursor import Cursor
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
        top = " " * (self.PADDING+1) + \
              Cursor.blue("=" * self.WIDTH) + "\n"
        mid = " " * self.PADDING + \
              Cursor.blue("|") + \
              "{}" * self.WIDTH + \
              Cursor.blue("|\n") 
        self.board = top + mid*self.HEIGHT + top

    def init_fills(self):
        self.fills = [
            [" " for _ in range(self.WIDTH)]
            for _ in range(self.HEIGHT)
        ]
    
    def init_snake(self):
        head = (self.HEIGHT // 2, self.WIDTH // 2)
        self.snake = [head,]
        self.fills[head[0]][head[1]] = Cursor.red("@")
    
    def init_food(self):
        self.food_options = set(
            (r, c)
            for r in range(self.HEIGHT)
            for c in range(self.WIDTH)
        )
        self.spawn_food()

    def spawn_food(self):
        choices = self.food_options - set(self.snake)
        self.food = random.choice(list(choices))
        self.fills[self.food[0]][self.food[1]] = Cursor.green("*")

    def turn(self, turn):
        if self.is_valid_turn(turn):
            self.direction = turn
    
    def is_valid_turn(self, turn):
        invalid = self.INVALID_TURNS.get(self.direction)
        return turn in self.INVALID_TURNS and turn != invalid

    def tick(self):
        delta_y, delta_x = self.DIRECTIONS[self.direction]
        new_head = (self.snake[0][0] + delta_y, self.snake[0][1] + delta_x)
        if self.check_game_over(new_head):
            self.game_over = True
        else:
            return self.update_snake(new_head)

    def check_game_over(self, new_head):
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
        self.fills[self.snake[0][0]][self.snake[0][1]] = Cursor.yellow("#")
        self.fills[new_head[0]][new_head[1]] = Cursor.red("@")
        self.snake.insert(0, new_head)
        if self.eats_food(new_head):
            self.spawn_food()
            return True
        else:
            tail = self.snake.pop()
            self.fills[tail[0]][tail[1]] = " "
            return False
    
    @property
    def effective_height(self):
        return self.HEIGHT + 2

    def render(self):
        return self.board.format(*itertools.chain(*self.fills))


class SnakeController(Controller):
    friendly_name = "Snake"
    DELAY = 0.17 # this seems to be the sweet spot

    def setUp(self, player):
        self.board = SnakeBoard()
        self.player = player
        self.disconnected = False

    def make_header(self):
        return (
            f"\tTOTAL SCORE: {Cursor.green(self.player.score)}\n"
            f"\tEARNED: {Cursor.green(self.player.earned)}\n\n"
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
            return 0
    
    async def send_board(self):
        await self.player.send(
            f"{Cursor.CLEAR}"
            f"{self.make_header()}"
            f"{self.board.render()}"
        )
    
    async def earned_point(self):
        await self.player.on_earned_points(1)


class SnakeServer(TermninjaServer):
    controller_class = SnakeController

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