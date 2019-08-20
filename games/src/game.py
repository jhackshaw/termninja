import asyncio
import termninja_db as db
from slugify import slugify
from abc import ABCMeta, abstractmethod
from . import cursor
from .messages import (GENERIC_QUIZ_INITIAL_QUESTION,
                       GENERIC_QUIZ_PROGRESS_UPDATE,
                       GENERIC_QUIZ_CLEAR_ENTRY,
                       GENERIC_QUIZ_INTERMISSION_REPORT)


class StoreGamesMixin:
    async def teardown(self):
        await asyncio.gather(
            super().teardown(),
            self.store_round_played()
        )

    async def store_round_played(self):
        """
        For each player, record the fact that this player
        played this game in the db
        """
        await asyncio.gather(*[
            self.add_round_played(p)
            for p in self._players
        ])

    async def add_round_played(self, player, **kwargs):
        await db.rounds.add_round_played(
            self.slug,
            player.identity['username'],  # this gives us None for anonymous
            player.earned,
            **kwargs
        )


class StoreGamesWithResultMessageMixin(StoreGamesMixin):
    async def add_round_played(self, player, **kwargs):
        return await super().add_round_played(
            player,
            message=self.make_result_message_for(player),
            **kwargs
        )

    def make_result_message_for(self, player):
        """
        Probably override this with something more discriptive,
        e.g. Lost to opponent
             Averaged X% in Y quiz
             etc
        """
        raise NotImplementedError


class StoreGamesWithSnapshotMixin(StoreGamesMixin):
    async def add_round_played(self, *args, **kwargs):
        return await super().add_round_played(
            *args,
            snapshot=self._get_snapshot(),
            **kwargs
        )

    def _get_snapshot(self):
        snapshot = self.make_final_snapshot()
        return cursor.ansi_to_html(snapshot)

    def make_final_snapshot(self):
        raise NotImplementedError


class SlugDescriptor:
    def __get__(self, instance, owner):
        if self._name not in owner.__dict__:
            setattr(owner, self._name, slugify(owner.name))
        return owner.__dict__[self._name]

    def __set_name__(self, owner, name):
        self._name = f'_{name}'


class Game(metaclass=ABCMeta):
    player_count = 1
    name = None
    slug = SlugDescriptor()

    def __init__(self, *players):
        self._players = players

    @property
    def time(self):
        return self.__loop.time()

    @classmethod
    async def player_connected(cls, player):
        if not hasattr(cls, '__queue'):
            await cls._initialize()
        await cls.on_player_connected(player)
        await cls.__queue.put(player)

    @classmethod
    async def on_player_connected(cls, player):
        await player.send(
            f'{cursor.CLEAR}'
            f'{cursor.PAGE_DOWN}'
            f'{cursor.down(50)}'
        )

    @classmethod
    async def _initialize(cls):
        cls.__loop = asyncio.get_running_loop()
        cls.__queue = asyncio.Queue()
        asyncio.create_task(cls._launcher())

    @classmethod
    async def _launcher(cls):
        while True:
            players = [
                await cls.__queue.get()
                for _ in range(cls.player_count)
            ]
            instance = cls(*players)
            asyncio.create_task(instance._start())

    async def _start(self):
        """
        Call run and handle any errors. should not be overriden.
        """
        try:
            await self.run()
        except (BrokenPipeError, ConnectionResetError):
            await self.on_disconnect()
        finally:
            await self.teardown()

    @abstractmethod
    async def run(self):
        """
        Subclass's logic for the controller
        """
        pass

    async def on_disconnect(self):
        """
        Hook for any diconnect actions. Players are
        closed immediately after this.
        """
        pass

    async def teardown(self):
        """
        Close all player streams
        """
        await asyncio.gather(*[
            p.close() for p in self._players
        ])

    async def send_to_players(self, msg):
        """
        Send message to all players in this controller
        """
        return await asyncio.gather(*[
            p.send(msg) for p in self._players
        ])


class GenericQuestion:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer

    def check_answer(self, answer):
        return self.answer == answer

    def get_value(self, remaining_time):
        return remaining_time

    def get_duration(self):
        return 60

    def get_display_answer(self):
        return self.answer


class GenericQuizGame(Game):
    INITIAL_QUESTION = GENERIC_QUIZ_INITIAL_QUESTION
    PROGRESS_UPDATE = GENERIC_QUIZ_PROGRESS_UPDATE
    CLEAR_ENTRY = GENERIC_QUIZ_CLEAR_ENTRY
    INTERMISSION_REPORT = GENERIC_QUIZ_INTERMISSION_REPORT

    def setUp(self, player):
        self.player = player
        self.correct_count = 0   # number of questions with > 0 points earned
        self.question_count = 1  # total number of questions played

    async def iter_questions(self):
        """
        This should be an async generator yielding some type
        of GenericQuestion
        """
        raise NotImplementedError

    async def run(self):
        """
        Do a round for every question keeping track of the score
        """
        async for question in self.iter_questions():
            earned = await self.round(question)
            self.question_count += 1
            if earned:
                self.correct_count += 1
            await self.player.on_earned_points(earned)
            await self.intermission(question, earned)

    async def round(self, question):
        """
        Allow guesses until the answer is correct or time runs out
        """
        round_length = question.get_duration()
        start = self.time
        await self.prompt(question)
        while True:
            # calculate time remaining and update progress bar
            remiaining_time = int(round_length - (self.time - start))
            await self.update_progress(round_length, remiaining_time)

            guess = await self.get_answer()
            if guess is not None:
                # clear the input line in the terminal
                # if something was actually entered
                await self.clear_player_entry()
            if question.check_answer(guess):
                # you earned however much time was remiaining points
                return remiaining_time
            if self.time - start > round_length:
                # ran out of time, 0 points
                return 0

    async def prompt(self, question):
        """
        Send the initial question
        """
        duration = question.get_duration()
        progress = self.get_progress_line(duration, duration)  # full time
        msg = self.INITIAL_QUESTION.format(
            prompt=question.prompt,
            progress=progress,
            earned=self.player.earned,
            total_score=self.player.total_score
        )
        await self.player.send(msg)

    def get_progress_line(self, round_length, time_remaining):
        """
        Color the line with the progress bar
        """
        percent_remaining = time_remaining / round_length
        count = int(percent_remaining * round_length)
        progress = f"{'#' * count} {time_remaining}"
        return cursor.color_by_percentage(percent_remaining, progress)

    async def update_progress(self, round_length, time_remaining):
        """
        Update the progress bar
        """
        progress = self.get_progress_line(round_length, time_remaining)
        msg = self.PROGRESS_UPDATE.format(
            progress=progress
        )
        await self.player.send(msg)

    async def get_answer(self):
        """
        Attempt to read an answer, if none submitted, return None
        """
        try:
            return await self.player.readline(timeout=0.5)
        except asyncio.TimeoutError:
            return None

    async def clear_player_entry(self):
        """
        Clear the user's input when they submitted something
        """
        await self.player.send(self.CLEAR_ENTRY)

    async def intermission(self, question, earned):
        """
        Send the user the results of that question and pause
        """
        color = cursor.red
        if earned > 0:
            color = cursor.green
        await self.player.send(GENERIC_QUIZ_INTERMISSION_REPORT.format(
            correct_answer=color(question.get_display_answer()),
            earned_points=color(earned)
        ))
        await self.player.readline()
