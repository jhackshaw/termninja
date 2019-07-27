import random
import ipaddress
import itertools
from src.core.manager import BaseManager
from src.core.game import GenericQuizGame, GenericQuestion

# use np.random.choice(..., p=WEIGHTS) instead?
WEIGHTS = [0, 0, 0, 0, 1, 1, 1, 1,  # 1st octet
           4, 1, 1, 1, 1, 1, 1, 1,  # 2nd octet
           4, 1, 1, 1, 1, 2, 2, 2,  # 3rd octet
           6, 3, 3, 3, 3, 3, 1, 0]  # 4th octet
CIDRS = list(itertools.chain(*[
    [idx for _ in range(WEIGHTS[idx])]
    for idx in range(0, 32)
]))


def broadcast_question(host, cidr):
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    return (
        f"What is the broadcast address in the network {host}/{cidr}?",
        f"{network.broadcast_address}"
    )


def network_id_question(host, cidr):
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    return (
        f"What is the network address for the network {host}/{cidr}?",
        f"{network.network_address}"
    )


def subnet_mask_question(host, cidr):
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    return (
        f"what is the subnet mask for the cidr /{cidr}?",
        f"{network.netmask}"
    )


def first_host_question(host, cidr):
    if cidr > 30:
        cidr = 30
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    return (
        f"What is the first usable host in the network {host}/{cidr}?",
        f"{network.network_address + 1}"
    )


def last_host_question(host, cidr):
    if cidr > 30:
        cidr = 30
    network = ipaddress.IPv4Network(f"{host}/{cidr}", strict=False)
    return (
        f"What is the last usable host in the network {host}/{cidr}?",
        f"{network.broadcast_address - 1}"
    )


def num_usable_hosts_question(host, cidr):
    if cidr > 30:
        cidr = 30
    return (
        f"How many usable hosts are in the network {host}/{cidr}?",
        f"{2**(32-cidr) - 2}"
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
    octets = [str(random.randint(0, 255)) for _ in range(4)]
    host = ".".join(octets)
    cidr = random.choice(CIDRS)
    question_type = random.choice(QUESTION_TYPES)
    return question_type(host, cidr)


class SubnetRacer(GenericQuizGame):
    async def iter_questions(self):
        for _ in range(25):
            prompt, answer = get_question()
            yield GenericQuestion(prompt, answer)


class SubnetRacerManager(BaseManager):
    name = "Subnet Racer"
    game_class = SubnetRacer
    player_count = 1
    description = (
        "Race against the clock while you "
        "calculate subnets in your head"
    )
