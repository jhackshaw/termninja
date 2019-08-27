import re
import bleach


color_codes_to_style = {
    '31': 'red',
    '32': 'lime',
    '33': 'yellow',
    '36': 'cyan',
    '35': 'magenta'
}
OPEN_SEQUENCE_RE = re.compile(
    r'\x1b\[(?P<sequence>.*?)(?P<terminator>[msuJKHABG]{1})'
)

ESCAPE = "\x1b["
RESET = f"{ESCAPE}0m"
CLEAR = f"{ESCAPE}2J"
CLEAR_TO_END = f"{ESCAPE}0J"
CLEAR_ALT = f"{ESCAPE}1J{ESCAPE}0;0H"

PAGE_DOWN = f"{ESCAPE}60T"

SAVE = f"{ESCAPE}s"
RESTORE = f"{ESCAPE}u"
ERASE_LINE = f"{ESCAPE}2K"
ERASE_TO_LINE_END = f"{ESCAPE}0K"
HOME = f"{ESCAPE}1G"

RED = f"{ESCAPE}31;1m"
GREEN = f"{ESCAPE}32;1m"
YELLOW = f"{ESCAPE}33;1m"
BLUE = f"{ESCAPE}36;1m"
MAGENTA = f"{ESCAPE}35;1m"


def red(msg):
    return f"{RED}{ msg }{RESET}"


def green(msg):
    return f"{GREEN}{ msg }{RESET}"


def yellow(msg):
    return f"{YELLOW}{ msg }{RESET}"


def blue(msg):
    return f"{BLUE}{ msg }{RESET}"


def magenta(msg):
    return f"{MAGENTA}{ msg }{RESET}"


def move_to(y, x):
    return f"{ESCAPE}{y};{y}H"


def up(n):
    return f"{ESCAPE}{n}A"


def down(n):
    return f"{ESCAPE}{n}B"


def move_to_column(col):
    return f"{ESCAPE}{col}G"


def replace_relative(x, y, val):
    return (
        f'{HOME}{SAVE}'
        f'{up(x)}{move_to_column(y)}'
        f'{val}'
        f'{RESTORE}'
    )


def resize(h, w):
    return f"{ESCAPE}8;{w};{h}t"


def color_by_percentage(percent, msg):
    if percent < 0.33:
        return red(msg)
    if percent < 0.66:
        return yellow(msg)
    return green(msg)


def get_color_for(color_code):
    return color_codes_to_style.get(color_code, '')


def make_span(match):
    if not match.group('terminator') == 'm':
        # it's something other than a color
        return ""

    # it's a color, make a span
    color = match.group('sequence').split(';')[0]
    return f'<span style="color: {get_color_for(color)}">'


def ansi_to_html(ansi, centered=True, bold=True):
    # make newlines into <br/> tags
    ret = ansi.replace('\n', '<br/>')

    # make RESET into </span>
    ret = ret.replace('\x1b[0m', '</span>')

    # replace the rest of the sequences according to
    # make_span
    html = re.sub(OPEN_SEQUENCE_RE, make_span, ret)

    classes = 'text-center' if centered else ''
    classes += ' font-weight-bold' if bold else ''

    # clean the resulting html just to be sure, there
    # is bound to be user input in the original ansi
    # depending on how it's being used. Probably still
    # not necessary because we are explicitly definining
    # the tags that are allowed, but still, better safe.
    return bleach.clean(
        f'<pre class="{classes}">{html}</pre>',
        tags=['span', 'br', 'pre'],
        attributes=['style', 'class'],
        styles=['color', 'background-color', 'padding', 'width']
    )
