import asyncio
import os
import random
import ipaddress
import itertools
from shell_games import Cursor, RequireTokenServer, Controller
from config import (WELCOME_MESSAGE,
                    PRESS_ENTER_MESSAGE,
                    PROGRESS_UPDATE,
                    INITIAL_QUESTION,
                    CLEAR_ENTRY,
                    ROUND_LENGTH,
                    SCREEN_WIDTH)

# use np.random.choice(..., p=WEIGHTS) instead?
WEIGHTS = [0, 0, 0, 0, 1, 1, 1, 1, # 1st octet
           4, 1, 1, 1, 1, 1, 1, 1, # 2nd octet
           4, 1, 1, 1, 1, 1, 1, 1, # 3rd octet
           6, 3, 3, 3, 3, 3, 3, 2] # 4th octet
CIDRS = list(itertools.chain(*[
    [idx for _ in range(WEIGHTS[idx])]
    for idx in range(0, 32)
]))

def broadcast_question(host, cidr, network):
    return (
        f"What is the broadcast address in the network {host}/{cidr}?",
        f"{network.broadcast_address}"
    )

def network_id_question(host, cidr, network):
    return (
        f"What is the network address for the network {host}/{cidr}?",
        f"{network.network_address}"
    )

def subnet_mask_question(host, cidr, network):
    return (
        f"what is the subnet mask for the cidr /{cidr}?",
        f"{network.netmask}"
    )

def first_host_question(host, cidr, network):
    if cidr > 30:
        cidr = 30
    return (
        f"What is the first usable host in the network {host}/{cidr}?",
        f"{network.network_address + 1}"
    )

def last_host_question(host, cidr, network):
    if cidr > 30:
        cidr = 30
    return (
        f"What is the last usable host in the network {host}/{cidr}?",
        f"{network.broadcast_address - 1}"
    )

def num_usable_hosts_question(host, cidr, network):
    return (
        f"How many usable hosts are in the network {host}/{cidr}?",
        f"{network.num_addresses - 2}"
    )

QUESTION_TYPES = [
    broadcast_question,
    network_id_question,
    subnet_mask_question,
    first_host_question,
    last_host_question,
    num_usable_hosts_question
]

def get_question():
    octets = [str(random.randint(0,255)) for _ in range(4)]
    host = ".".join(octets)
    cidr = random.choice(CIDRS)
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    question_type = random.choice(QUESTION_TYPES)
    return question_type(host, cidr, network)


class SubnetRacerController(Controller):
    def setUp(self, user):
        self.user = user
        self.score = 0
        self.loop = asyncio.get_event_loop()

    async def run(self):
        try:
            while True:
                self.on_earned_points(await self.round())
        except ConnectionResetError:
            print("user disconnected", flush=True)
    
    async def round(self):
        start = self.get_time()
        question, answer = get_question()
        await self.prompt(question)

        while True:
            cur_time = self.get_time()
            remiaining_time = int(ROUND_LENGTH - (cur_time - start))
            await self.update_progress(remiaining_time)
            guess = await self.get_answer()

            if guess is not None:
                # clear the input line in the terminal 
                # if something was actually entered
                await self.clear_user_entry()
            if self.check_answer(guess, answer):
                # you earned however much time was remiaining points
                return remiaining_time
            if cur_time - start > ROUND_LENGTH:
                # ran out of time, 0 points
                return 0
    
    async def prompt(self, question):
        msg = INITIAL_QUESTION.format(
            prompt=question,
            progress="#" * ROUND_LENGTH,
            time="60",
            score=self.score
        )
        await self.user.send(msg)

    async def update_progress(self, time_remaining):
        percent_remaining = time_remaining / ROUND_LENGTH
        count = int(percent_remaining * ROUND_LENGTH)
        progress = Cursor.color_by_percentage(percent_remaining, '#' * count)
        msg = PROGRESS_UPDATE.format(
            progress=progress,
            time=time_remaining,
            value=ROUND_LENGTH - time_remaining
        )
        await self.user.send(msg)

    async def get_answer(self):
        try:
            return await self.user.readline(timeout=0.5)
        except asyncio.TimeoutError:
            return None

    async def clear_user_entry(self):
        await self.user.send(CLEAR_ENTRY)
    
    def check_answer(self, guess, expected):
        return guess == expected

    def get_time(self):
        return self.loop.time()
    
    def on_earned_points(self, earned):
        self.score += earned
        

class SubnetRacerServer(RequireTokenServer):
    controller_class = SubnetRacerController
    player_count = 1

    async def user_connected(self, user):
        await user.send(WELCOME_MESSAGE)
    
    async def on_user_accepted(self, user):
        await super().on_user_accepted(user)
        await user.send(PRESS_ENTER_MESSAGE)
        await user.readline()


if __name__ == "__main__":
    server = SubnetRacerServer()
    server.start()