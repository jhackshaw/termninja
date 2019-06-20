import asyncio
import os
import random
import ipaddress
import itertools
from shell_games import Cursor, start_game
from config import (WELCOME_MESSAGE,
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

def check_answer(ans, answer):
    return ans == answer

async def welcome(user):
    await user.send(WELCOME_MESSAGE)
    await user.readline()

async def get_answer(user):
    return await user.readline(timeout=0.5)

async def clear_user_entry(user):
    await user.send(CLEAR_ENTRY)

async def prompt(user, question, score):
    msg = INITIAL_QUESTION.format(
        prompt=question,
        progress="#" * ROUND_LENGTH,
        time="60",
        score=score
    )
    await user.send(msg)

async def update_progress(user, time_remaining):
    percent_remaining = time_remaining / ROUND_LENGTH
    count = int(percent_remaining * ROUND_LENGTH)
    progress = Cursor.color_by_percentage(percent_remaining, '#' * count)

    msg = PROGRESS_UPDATE.format(
        progress=progress,
        time=time_remaining,
        value=ROUND_LENGTH - time_remaining
    )
    await user.send(msg)

async def round(user, score):
    loop = asyncio.get_event_loop()
    question, answer = get_question()
    round_start = loop.time()

    await prompt(user, question, score)
    while True:
        time_remaining = int(60 - (loop.time() - round_start))
        await update_progress(user, time_remaining)
        ans = await get_answer(user)

        if ans is not None:
            await clear_user_entry(user)
            if check_answer(ans, answer):
                return time_remaining

        if loop.time() - round_start > ROUND_LENGTH:
            return 0

async def subnet_racer(user):
    try:
        await welcome(user)
        score = 0
        while True:
            score += await round(user, score)

    except ConnectionResetError:
        print("user disconnected", flush=True)


if __name__ == "__main__":
    start_game(subnet_racer, "0.0.0.0", 3000)