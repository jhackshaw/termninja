import asyncio
import random
from .. import cursor
from ..game import (Game,
                    StoreGamesWithSnapshotMixin,
                    StoreGamesWithResultMessageMixin)
from . import config


class Board:
    def __init__(self):
        self.tree = random.choice(config.TREES)

    @classmethod
    def replace_cell(cls, x, y, val):
        x_offset = x * 2 + config.PADDING + 3
        return (
            f'{cursor.HOME}{cursor.SAVE}'
            f'{cursor.up(config.HEIGHT + 1 - y)}'
            f'{cursor.move_to_column(x_offset)}'
            f'{val}{cursor.RESTORE}'
        )

    @classmethod
    def replace_score(cls, score):
        x = len(config.SCORE_MESSAGE)
        return cls.replace_cell(x, -3, score)

    def __str__(self):
        return config.EMPTY_BOARD.format(self.tree)

    def __repr__(self):
        return '<SnakeBoard>'

    def render_snapshot(self, snake, food=None):
        board = [
            [config.EMPTY_CELL for _ in range(config.WIDTH)]
            for _ in range(config.HEIGHT)
        ]
        head_x, head_y = snake[0]
        board[head_y][head_x] = config.HEAD
        for y, x in snake[1:]:
            board[x][y] = config.BODY
        if food is not None:
            y, x, s = food
            board[x][y] = s

        rows = [f"{self.tree}{''.join(r)}{self.tree}" for r in board]
        board_str = '\n'.join(rows)
        return (
            f"{self.tree * (config.WIDTH + 2)}\n"
            f"{board_str}\n"
            f"{self.tree * (config.WIDTH + 2)}\n"
        )


class Snake(StoreGamesWithSnapshotMixin,
            StoreGamesWithResultMessageMixin,
            Game):
    name = "Snake"
    player_count = 1
    icon = "dragon"
    description = config.DESCRIPTION

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

    def __init__(self, *players):
        super().__init__(*players)
        self.player = players[0]
        self.snake = [(10, 10)]
        self.direction = (1, 0)
        self.board = Board()
        self.food = None
        self.spawn_food()

    @classmethod
    async def on_player_connected(cls, player):
        """
        Let the player know the best way to play before
        queuing them for the game
        """
        await player.send(config.WELCOME_MESSAGE)
        await player.clear_input_buffer()
        await player.readline()
        await super().on_player_connected(player)

    async def run(self):
        await self.player.send(self.initial_frame())
        async for frame in self.iter_frames():
            await self.player.send(frame)
            waited = await self._input_opportunity()
            await asyncio.sleep(config.DELAY - waited)
        await self.player.send(config.GAME_OVER)

    async def _input_opportunity(self):
        try:
            start = self.time
            inp = await self.player.read(8, timeout=config.DELAY)
            self.change_direction(inp[0])
            return self.time - start
        except asyncio.TimeoutError:
            return config.DELAY

    async def iter_frames(self):
        while True:
            new_head = self.get_next_head()

            if self.check_game_over(new_head):
                return

            frame = (
                f'{self.board.replace_cell(*new_head, config.HEAD)}'
                f'{self.board.replace_cell(*self.snake[0], config.BODY)}'
            )

            self.snake.insert(0, new_head)
            eats_food = self.check_eats_food(new_head)

            if eats_food:
                self.spawn_food()
                await self.player.on_earned_points(1)
                frame += self.board.replace_cell(*self.food)
                frame += self.board.replace_score(self.player.earned)
            else:
                old_tail = self.snake.pop()
                frame += self.board.replace_cell(*old_tail,
                                                 config.EMPTY_CELL)
            yield frame

    def initial_frame(self):
        return (
            f'{str(self.board)}'
            f'{self.board.replace_cell(*self.food)}'
        )

    def get_next_head(self):
        return (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1]
        )

    def spawn_food(self):
        cell = random.choice(list(config.ALL_CELLS - set(self.snake)))
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
        return self.board.render_snapshot(self.snake, food=self.food)

    def make_result_message_for(self, player):
        return f'Consumed {player.earned} critters'
