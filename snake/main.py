import asyncio
import itertools
import random
from shell_games import Cursor, Controller, Server
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
        self.score = 0
        self.game_over = False
        self.direction = random.choice(
            list(self.DIRECTIONS.keys())
        )

    def init_board(self):
        header = f"\n\t\t\tSCORE: {Cursor.GREEN}{{score}}{Cursor.RESET}"
        top = " " * (self.PADDING+1) + \
              Cursor.blue("=" * self.WIDTH) + "\n"
        mid = " " * self.PADDING + \
              Cursor.blue("|") + \
              "{}" * self.WIDTH + \
              Cursor.blue("|\n") 
        self.board = header + "\n\n" + top + mid*self.HEIGHT + top

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
            self.update_snake(new_head)

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
        self.fills[self.snake[0][0]][self.snake[0][1]] = Cursor.yellow("#")
        self.fills[new_head[0]][new_head[1]] = Cursor.red("@")
        self.snake.insert(0, new_head)
        if self.eats_food(new_head):
            self.score += 1
            self.spawn_food()
        else:
            tail = self.snake.pop()
            self.fills[tail[0]][tail[1]] = " "
    
    @property
    def effective_height(self):
        return self.HEIGHT + 2

    def render(self):
        return self.board.format(*itertools.chain(*self.fills), score=self.score)


class SnakeController(Controller):
    DELAY = 0.14

    def setUp(self, user):
        self.board = SnakeBoard()
        self.user = user
        self.disconnected = False

    async def run(self):
        while not self.board.game_over:
            await self.handle_input()
            self.board.tick()
            await self.send_board()
            await asyncio.sleep(self.DELAY)
        await self.user.close()

    async def handle_input(self):
        try:
            data = await self.user.read(timeout=0.2)
            self.board.turn(data[-1])
        except asyncio.TimeoutError:
            pass
    
    async def send_board(self):
        await self.user.send(
            f"{Cursor.CLEAR_ALT}{self.board.render()}"
        )

    async def on_disconnect(self, err):
        print("disconnected")


class SnakeServer(Server):
    controller_class = SnakeController
    allow_reuse_address = True

    async def user_connected(self, user):
        await user.send(WELCOME_MESSAGE)
        await user.readline()


if __name__ == "__main__":
    server = SnakeServer()
    server.start()