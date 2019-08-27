import asyncio
import os
import random
import linecache
import inspect
from .. import cursor
from ..game import (StoreGamesWithResultMessageMixin,
                    StoreGamesWithSnapshotMixin,
                    Game)


class HangmanBoard:
    _guessed_label = f'{cursor.RESET}{cursor.RED}missed:{cursor.RESET}{cursor.BLUE}'  # noqa: E501
    board = (
        f"{cursor.BLUE}"
        f"     ______\n"
        f"    |      |\n"
        f"    |\n"
        f"    |            {_guessed_label}\n"
        f"    |\n"
        f"   _|_\n"
        f"  |   |____\n"
        f"  |        |\n"
        f"  |________|{cursor.RESET}\n\n"
    )

    board_fmt = (
        f"{cursor.blue('   ______')}\n"
        f"{cursor.blue('  |      |')}\n"
        f"{cursor.blue('  |      ')}{{0}}\n"
        f"{cursor.blue('  |     ')}{{2}}{{1}}{{3}}  {cursor.red('missed: ')}{{letters}}\n"   # noqa: E501
        f"{cursor.blue('  |     ')}{{4}} {{5}}\n"
        f"{cursor.blue(' _|_         ')}{{word}}\n"
        f"{cursor.blue('|   |____')}\n"
        f"{cursor.blue('|        |')}\n"
        f"{cursor.blue('|________|')}\n\n"
        f"{{description}}\n"
    )

    body_parts = {
        #  turn num: (x, y, symbol)
        1: (8, 12, '0'),
        2: (7, 12, '|'),
        3: (7, 11, '/'),
        4: (7, 13, '\\'),
        5: (6, 11, '/'),
        6: (6, 13, '\\')
    }

    @classmethod
    def draw_body_part(cls, part: int, color=cursor.yellow):
        x, y, char = cls.body_parts[part]
        return cursor.replace_relative(x, y, color(char))

    @classmethod
    def draw_word(cls, word: str):
        out = f'{cursor.ERASE_TO_LINE_END}{word}'
        return cursor.replace_relative(5, 18, out)

    @classmethod
    def draw_letters(cls, letters: str):
        out = f'{cursor.ERASE_TO_LINE_END}{letters}'
        return cursor.replace_relative(7, 26, out)

    @classmethod
    def draw_result(cls, result):
        return cursor.replace_relative(3, 26, result)


class Hangman(StoreGamesWithResultMessageMixin,
              StoreGamesWithSnapshotMixin,
              Game):
    description = (
        "Hangman where the words are the names of celebrities. "
        "It's up to you to hang or save them."
    )
    name = 'Celebrity Hangman'
    icon = "dizzy"
    center_snapshot = False
    bold_snapshot = False
    wordlist = f"{os.path.dirname(__file__)}/wordlist.txt"
    frame_delay = 0.3

    def __init__(self, *args):
        super().__init__(*args)
        self.guessed_letters = set()
        self.missed_letters = []
        self.word, self.description = self.get_random_word()
        self.guess_word = self.prepare_guess_word(self.word)

    def get_random_word(self):
        # should read this into memory
        idx = random.randint(0, 986)
        w, d = linecache.getline(self.wordlist, idx).split(' | ')
        return w, self.wrap_description(d)

    def wrap_description(self, description):
        ret = ''
        for i in range(0, len(description) // 60):
            ret += description[i*60: (i+1)*60] + '\n'
        return ret

    def prepare_guess_word(self, word):
        return [
            '_' if c.isalpha() else c for c in word
        ]

    @property
    def display_guess_word(self):
        return ' '.join(self.guess_word)

    @property
    def display_missed_letters(self):
        return ', '.join(self.missed_letters)

    @property
    def word_complete(self):
        return ''.join(self.guess_word) == self.word

    @property
    def misses(self):
        return len(self.missed_letters)

    def initial_frame(self):
        return (
            f'{HangmanBoard.board}'
            f'{HangmanBoard.draw_word(self.display_guess_word)}'
        )

    def update_guess_word(self, choice):
        for idx, c in enumerate(self.word):
            if c.lower() == choice.lower():
                self.guess_word[idx] = c

    def is_good_guess(self, choice):
        for c in self.word:
            if c.lower() == choice.lower():
                return True
        return False

    async def run(self):
        await self.player.send(self.initial_frame())
        await self.player.clear_input_buffer()
        async for frames in self.iter_frames():
            if inspect.isasyncgen(frames):
                async for frame in frames:
                    await self.player.send(frame)
            else:
                await self.player.send(frames)
        await self.player.send(self.description)

    async def iter_frames(self):
        while True:
            choice = await self.get_player_choice()

            # early out for double guessing
            if choice in self.guessed_letters:
                if choice in self.missed_letters:
                    yield self.on_already_missed(choice)
                else:
                    yield self.on_already_guessed(choice)
                continue

            self.guessed_letters.add(choice)

            if self.is_good_guess(choice):
                yield self.on_correct_guess(choice)
            else:
                yield self.on_incorrect_guess(choice)

            if self.misses == 6:
                yield self.on_loss()
                return
            elif self.word_complete:
                yield self.on_win()
                return

    async def get_player_choice(self):
        while True:
            choice = await self.player.read_raw(8)  # allows both -i and not -i
            if choice.endswith('\n'):
                await self.player.send(f'{cursor.up(1)}{cursor.ERASE_LINE}')
                choice = choice.strip()
            if choice.isalpha() and len(choice) == 1:
                return choice.lower()

    async def on_already_guessed(self, choice):
        tmp = [
            cursor.yellow(c) if c.lower() == choice else c
            for c in self.guess_word
        ]
        yield HangmanBoard.draw_word(' '.join(tmp))
        await asyncio.sleep(self.frame_delay)
        yield HangmanBoard.draw_word(self.display_guess_word)

    async def on_already_missed(self, choice):
        tmp = [
            cursor.yellow(c) if c == choice else c
            for c in self.missed_letters
        ]
        yield HangmanBoard.draw_letters(', '.join(tmp))
        await asyncio.sleep(self.frame_delay)
        yield HangmanBoard.draw_letters(self.display_missed_letters)

    async def on_correct_guess(self, choice):
        self.update_guess_word(choice)
        tmp = [
            cursor.green(c) if c.lower() == choice else c
            for c in self.guess_word
        ]
        yield HangmanBoard.draw_word(' '.join(tmp))
        await asyncio.sleep(self.frame_delay)
        yield HangmanBoard.draw_word(self.display_guess_word)

    async def on_incorrect_guess(self, choice):
        tmp = ', '.join([*self.missed_letters, cursor.red(choice)])
        self.missed_letters.append(choice)
        yield HangmanBoard.draw_letters(tmp) +\
            HangmanBoard.draw_body_part(self.misses, color=cursor.red)
        await asyncio.sleep(self.frame_delay)
        yield HangmanBoard.draw_letters(self.display_missed_letters) +\
            HangmanBoard.draw_body_part(self.misses)

    def on_loss(self):
        word = cursor.red(' '.join(list(self.word)))
        return (
            f"{HangmanBoard.draw_word(word)}"
            f"{HangmanBoard.draw_result(cursor.red('HANGED'))}"
        )

    def on_win(self):
        word = cursor.green(' '.join(list(self.word)))
        return (
            f"{HangmanBoard.draw_word(word)}"
            f"{HangmanBoard.draw_result(cursor.green('SPARED'))}"
        )

    def make_result_message_for(self, player):
        if self.misses < 6:
            return f"Spared {self.word}"
        return f"Hanged {self.word}"

    def make_final_snapshot(self):
        misses = self.misses
        parts = (
            cursor.yellow(values[2]) if misses >= part_num else ' '
            for part_num, values in HangmanBoard.body_parts.items()
        )
        word_color = cursor.green if self.word_complete else cursor.red
        return HangmanBoard.board_fmt.format(
            *parts,
            word=word_color(self.display_guess_word),
            letters=','.join(self.missed_letters),
            description=self.description
        )
