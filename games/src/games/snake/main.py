import asyncio
import random
from src.core import cursor, Manager
from src.core.game import Game, StoreGamesWithSnapshotMixin
from . import config


class Snake(StoreGamesWithSnapshotMixin, Game):
    directions = {
        'a': (-1, 0),
        's': (0, 1),
        'd': (1, 0),
        'w': (0, -1)
    }
    valid_directions = {
        (-1, 0): 'ws',
        (0, -1): 'ad',
        (1, 0): 'ws',
        (0, 1): 'ad'
    }
    all_cells = set([
        (x, y)
        for x in range(0, config.WIDTH)
        for y in range(0, config.HEIGHT)
    ])

    def setUp(self, player):
        self.player = player
        self.board = self.make_board()
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        self.food = None
        self.loop = asyncio.get_running_loop()
        self.spawn_food()

    async def run(self):
        await self.player.send(self.initial_frame())
        async for frame in self.iter_frames():
            await self.player.send(frame)
            waited = await self._input_opportunity()
            await asyncio.sleep(config.DELAY - waited)
        await self.player.send(config.GAME_OVER)

    async def _input_opportunity(self):
        try:
            start = self.loop.time()
            inp = await self.player.read(8, timeout=config.DELAY)
            self.change_direction(inp[0])
            return self.loop.time() - start
        except asyncio.TimeoutError:
            return config.DELAY

    async def iter_frames(self):
        while True:
            new_head = self.get_next_head()

            if self.check_game_over(new_head):
                return

            frame = (
                f'{self.term_replace_cell(*new_head, config.SNAKE_HEAD)}'
                f'{self.term_replace_cell(*self.snake[0], config.SNAKE_BODY)}'
            )

            self.snake.insert(0, new_head)
            eats_food = self.check_eats_food(new_head)

            if eats_food:
                self.spawn_food()
                await self.player.on_earned_points(1)
                frame += self.term_replace_cell(*self.food)
                frame += self.term_replace_score(self.player.earned)
            else:
                old_tail = self.snake.pop()
                frame += self.term_replace_cell(*old_tail, "  ")
            yield frame

    @staticmethod
    def term_replace_cell(x, y, val):
        return (
            f'{cursor.HOME}{cursor.SAVE}'
            f'{cursor.up(config.HEIGHT + 1 - y)}'
            f'{cursor.move_to_column(x * 2 + config.PADDING + 3)}'
            f'{val}{cursor.RESTORE}'
        )

    def term_replace_score(self, score):
        x = len(config.SCORE_MESSAGE)
        y = -3
        return self.term_replace_cell(x, y, score)

    @staticmethod
    def make_board():
        return config.EMPTY_BOARD.format(random.choice(config.TREES))

    def initial_frame(self):
        return (
            f'{cursor.CLEAR}{cursor.PAGE_DOWN}{cursor.HOME}'
            f'{config.PADDING * " "}{config.SCORE_MESSAGE}  0\n\n'
            f'{self.board}'
            f'{self.term_replace_cell(*self.snake[0], config.SNAKE_HEAD)}'
            f'{self.term_replace_cell(*self.food)}'
        )

    def get_next_head(self):
        return (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )

    def spawn_food(self):
        cell = random.choice(list(self.all_cells - set(self.snake)))
        self.food = (*cell, random.choice(config.FOODS))

    def check_eats_food(self, new_head):
        return new_head == self.food[:2]

    def check_game_over(self, new_head):
        x, y = new_head
        if not 0 <= x <= config.WIDTH - 1:
            return True
        if not 0 <= y <= config.HEIGHT - 1:
            return True
        for cell in self.snake:
            if cell == new_head:
                return True
        return False

    def change_direction(self, inp):
        if inp in self.valid_directions[self.direction]:
            self.direction = self.directions[inp]

    def make_final_snapshot(self):
        board = [list(line.strip()) for line in self.board.split('\n') if line]
        head_x, head_y = self.snake[0]
        board[head_y + 1][head_x*2 + 1] = config.SNAKE_HEAD
        board[head_y + 1][head_x*2 + 2] = ''
        for x, y in self.snake[1:]:
            board[y + 1][x*2 + 1] = config.SNAKE_BODY
            board[y + 1][x*2 + 2] = ''
        food_x, food_y, food = self.food
        board[food_y + 1][food_x*2 + 1] = food
        board[food_y + 1][food_x*2 + 2] = ''
        board[0].pop()
        board[-1].pop()
        board_str = "\n".join([''.join(row) for row in board])
        return (
            f'{" " * config.PADDING}{config.SCORE_MESSAGE}  '
            f'{self.player.earned}\n\n'
            f'{board_str}'
        )

    def make_result_message_for(self, player):
        return f'Consumed {player.earned} critters'


class SnakeManager(Manager):
    name = "Snake"
    game_class = Snake
    player_count = 1
    icon = "dragon"
    description = config.DESCRIPTION

    async def on_player_connected(self, player):
        """
        Let the player know the best way to play before
        queuing them for the game
        """
        await player.send(config.WELCOME_MESSAGE)
        await player.clear_input_buffer()
        await player.readline()
        await super().on_player_connected(player)
