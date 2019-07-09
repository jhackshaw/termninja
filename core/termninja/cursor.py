import re


ESCAPE = "\x1b["
RESET = f"{ESCAPE}0m"
CLEAR = f"{ESCAPE}2J"
CLEAR_ALT = f"{ESCAPE}1J{ESCAPE}0;0H"
SAVE = f"{ESCAPE}s"
RESTORE = f"{ESCAPE}u"
ERASE_LINE = f"{ESCAPE}2K"
ERASE_TO_LINE_END = f"{ESCAPE}0K"
HOME = f"{ESCAPE}1G"

RED = f"{ESCAPE}31;1m"
GREEN = f"{ESCAPE}32;1m"
YELLOW = f"{ESCAPE}33;1m"
BLUE = f"{ESCAPE}36;1m"


def blue(msg):
    return f"{BLUE}{ msg }{RESET}"

def green(msg):
    return f"{GREEN}{ msg }{RESET}"

def red(msg):
    return f"{RED}{ msg }{RESET}"

def yellow(msg):
    return f"{YELLOW}{ msg }{RESET}"

def move_to(y, x):
    return f"{ESCAPE}{y};{y}H"

def up(n):
    return f"{ESCAPE}{n}A"

def down(n):
    return f"{ESCAPE}{n}B"

def move_to_column(col):
    return f"{ESCAPE}{col}G"

def resize(h, w):
    return f"{ESCAPE}8;{w};{h}t"

def color_by_percentage(percent, msg):
    if percent < 0.33:
        return red(msg)
    if percent < 0.66:
        return yellow(msg)
    return green(msg)

def ansi_to_html(ansi):
    pass
