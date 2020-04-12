import asyncio
import random
from .. import cursor
from ..game import (
    Game,
    PromptForEmojiSupportMixin,
    StoreGamesWithSnapshotMixin,
    StoreGamesWithResultMessageMixin,
)


class BoardMeta(type):
    def __new__(cls, name, bases, dct):
        board = super().__new__(cls, name, bases, dct)
        board.PAD = " " * board.PADDING
        board.ALL_CELLS = board.make_all_cells()
        board.EMPTY_BOARD_FORMAT = cls.make_empty_board_format(board)
        return board

    @classmethod
    def make_empty_board_format(cls, board_cls):
        top_line = f"{board_cls.PAD}{'{0}' * (board_cls.WIDTH + 2)}\n"
        middle_line = (
            f"{board_cls.PAD}{'{0}'}"
            f"{board_cls.WIDTH * board_cls.EMPTY_CELL}{'{0}'}\n"
        )
        return (
            f"{board_cls.PAD}{board_cls.SCORE_MESSAGE}   \n"
            f"{top_line}"
            f"{middle_line * board_cls.HEIGHT}"
            f"{top_line}"
        )


class AsciiBoard(metaclass=BoardMeta):
    HEIGHT = 15
    WIDTH = 28
    PADDING = 6
    EMPTY_CELL = " "
    HEAD = cursor.red("@")
    BODY = cursor.yellow("#")
    FOODS = [cursor.red("*"), cursor.green("%"), cursor.magenta("&")]
    TREES = [cursor.blue("+")]
    SCORE_MESSAGE = "Score: "
    X_MOD = 1

    @classmethod
    def make_all_cells(cls):
        return set([(x, y) for x in range(0, cls.WIDTH) for y in range(0, cls.HEIGHT)])

    @classmethod
    def make_empty_board(cls):
        # pylint: disable=no-member
        return cls.EMPTY_BOARD_FORMAT.format(random.choice(cls.TREES))

    @classmethod
    def save_cursor_state(cls, message):
        return f"{cursor.HOME}{cursor.SAVE}" f"{message}" f"{cursor.RESTORE}"

    @classmethod
    def replace_cell(cls, x, y, val):
        cell_size = len(cls.EMPTY_CELL)
        x_offset = x * cell_size + cls.PADDING + cls.X_MOD
        return cls.save_cursor_state(
            f"{cursor.up(cls.HEIGHT + 1 - y)}"
            f"{cursor.move_to_column(x_offset)}"
            f"{val}"
        )

    @classmethod
    def replace_score(cls, score):
        x = len(cls.SCORE_MESSAGE)
        return cls.replace_cell(x, -2, score)

    @classmethod
    def make_snapshot_from_state(cls, snake, food=None):
        wall = random.choice(AsciiBoard.TREES)
        board = [
            [AsciiBoard.EMPTY_CELL for _ in range(cls.WIDTH)] for _ in range(cls.HEIGHT)
        ]
        head_x, head_y = snake[0]
        board[head_y][head_x] = AsciiBoard.HEAD
        for x, y in snake[1:]:
            board[y][x] = AsciiBoard.BODY

        x, y, _ = food
        board[y][x] = random.choice(AsciiBoard.FOODS)

        board_body = "\n".join([f'{wall}{"".join(row)}{wall}' for row in board])

        return (
            f"{wall * (cls.WIDTH + 2)}\n" f"{board_body}\n" f"{wall * (cls.WIDTH + 2)}"
        )


class EmojiBoard(AsciiBoard):
    HEAD = "\U0001F534"  # red circle
    BODY = "\U0001F535"  # blue circle
    FOODS = [
        "\U0001F401",  # mouse
        "\U0001F414",  # chicken
        "\U0001F400",  # rat
        "\U0001F41B",  # bug
        "\U0001F41D",  # honeybee
    ]
    TREES = [
        "\U0001F332",  # evergreen
        "\U0001F333",  # deciduous
        "\U0001F334",  # palm
        "\U0001F335",  # cactus
    ]
    SCORE_MESSAGE = "\U0001F480"  # skull
    EMPTY_CELL = "  "
    X_MOD = 3


class Snake(
    StoreGamesWithSnapshotMixin,
    StoreGamesWithResultMessageMixin,
    PromptForEmojiSupportMixin,
    Game,
):
    name = "Snake"
    player_count = 1
    icon = "dragon"

    delay = 0.17
    welcome_message = (
        f"{cursor.CLEAR}"
        f"{cursor.YELLOW}Make sure to run this game 'real-time' (-i)\n"
        f"See website for details{cursor.RESET}"
    )
    description = "An all ascii take on the classic game of snake."
    game_over = cursor.red("\n\nGAME OVER\n\n")

    directions = {"a": (-1, 0), "s": (0, 1), "d": (1, 0), "w": (0, -1)}
    valid_directions = {(-1, 0): "ws", (0, -1): "ad", (1, 0): "ws", (0, 1): "ad"}

    def __init__(self, *args):
        super().__init__(*args)
        self.board = EmojiBoard if self.player.emoji_support else AsciiBoard
        self.snake = [(self.board.WIDTH // 2, self.board.HEIGHT // 10)]
        self.direction = (1, 0)
        self.food = None
        self.spawn_food()

    @classmethod
    async def on_player_connected(cls, player):
        """
        Let the player know the best way to play before
        queuing them for the game
        """
        await player.send(cls.welcome_message)
        await super().on_player_connected(player)

    async def run(self):
        await self.player.send(self.initial_frame())
        async for frame in self.iter_frames():
            await self.player.send(frame)
            waited = await self._input_opportunity()
            await asyncio.sleep(self.delay - waited)
        await self.player.send(self.game_over)

    async def _input_opportunity(self):
        try:
            start = self.time
            inp = await self.player.read(8, timeout=self.delay)
            self.change_direction(inp[0])
            return self.time - start
        except asyncio.TimeoutError:
            return self.delay

    async def iter_frames(self):
        while True:
            new_head = self.get_next_head()

            if self.check_game_over(new_head):
                return

            frame = (
                f"{self.board.replace_cell(*new_head, self.board.HEAD)}"
                f"{self.board.replace_cell(*self.snake[0], self.board.BODY)}"
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
                frame += self.board.replace_cell(*old_tail, self.board.EMPTY_CELL)
            yield frame

    def initial_frame(self):
        return (
            f"{self.board.make_empty_board()}" f"{self.board.replace_cell(*self.food)}"
        )

    def get_next_head(self):
        return (
            self.snake[0][0] + self.direction[0],
            self.snake[0][1] + self.direction[1],
        )

    def spawn_food(self):
        # pylint: disable=no-member
        cell = random.choice(list(self.board.ALL_CELLS - set(self.snake)))
        self.food = (*cell, random.choice(self.board.FOODS))

    def check_eats_food(self, new_head):
        return new_head == self.food[:2]

    def check_game_over(self, new_head):
        x, y = new_head
        if not 0 <= x <= self.board.WIDTH - 1:
            return True
        if not 0 <= y <= self.board.HEIGHT - 1:
            return True
        for cell in self.snake:
            if cell == new_head:
                return True
        return False

    def change_direction(self, inp):
        if inp in self.valid_directions[self.direction]:
            self.direction = self.directions[inp]

    def make_final_snapshot(self):
        return self.board.make_snapshot_from_state(self.snake, self.food)

    def make_result_message_for(self, player):
        return f"Consumed {player.earned} critters"

