import asyncio
from .. import cursor
from .messages import (GENERIC_QUIZ_INITIAL_QUESTION,
                       GENERIC_QUIZ_PROGRESS_UPDATE,
                       GENERIC_QUIZ_CLEAR_ENTRY,
                       GENERIC_QUIZ_INTERMISSION_REPORT)


class BaseGame:
    def __init__(self, *players, **kwargs):
        self._players = players
        self._loop = asyncio.get_running_loop()
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.setUp(*players)

    def setUp(self, *players):
        """
        Initialization for subclasses. don't override __init__()
        """
        pass

    def get_time(self):
        return self._loop.time()

    async def start(self):
        """
        Call run and handle any errors. should not be overriden.
        """
        try:
            await self.run()
        except (BrokenPipeError, ConnectionResetError):
            await self.on_disconnect()
        finally:
            await self.teardown()

    async def run(self):
        """
        Subclass's logic for the controller
        """
        raise NotImplementedError

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


class GenericQuizGameBase(BaseGame):
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
        start = self.get_time()
        await self.prompt(question)
        while True:
            # calculate time remaining and update progress bar
            cur_time = self.get_time()
            remiaining_time = int(round_length - (cur_time - start))
            await self.update_progress(round_length, remiaining_time)

            guess = await self.get_answer()
            if guess is not None:
                # clear the input line in the terminal
                # if something was actually entered
                await self.clear_player_entry()
            if question.check_answer(guess):
                # you earned however much time was remiaining points
                return remiaining_time
            if cur_time - start > round_length:
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
            total_score=self.player.score
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
