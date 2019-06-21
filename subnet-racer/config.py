from shell_games import Cursor


# constants
ROUND_LENGTH = 60
SCREEN_WIDTH = 80


#
#   sent once on first connection
#
WELCOME_MESSAGE = f"""{Cursor.CLEAR}{Cursor.resize(SCREEN_WIDTH,30)}
{Cursor.YELLOW}
        __-------__
      / _---------_ \\
     / /           \ \\
     | |           | |
     |_|___________|_|
 /-\|                 |/-\\
| _ |\       0       /| _ |
|(_)| \      !      / |(_)|
|___|__\_____!_____/__|___|
[_____{Cursor.RESET}{Cursor.BLUE}|SUBNET RACER|{Cursor.RESET}{Cursor.YELLOW}______] 
 ||||    ~~~~~~~~     ||||
 `--'                 `--'

Welcome to Subnet Racer!!!!{Cursor.RESET}

{Cursor.GREEN}Press enter to continue...{Cursor.RESET}

"""



#
#   clears screen and prompts the next question
#
INITIAL_QUESTION = f"""{Cursor.CLEAR}

POINTS EARNED: {Cursor.GREEN}{{score}}{Cursor.RESET}


{Cursor.YELLOW}{{prompt}}{Cursor.RESET}
{{progress}} {Cursor.GREEN}{{time}}{Cursor.RESET}

{Cursor.YELLOW}# {Cursor.RESET}"""


#
#       gets sent every second or so to countdown time remaining
#
PROGRESS_UPDATE = f"{Cursor.SAVE}{Cursor.up(2)}{Cursor.HOME}" + \
                  f"{Cursor.ERASE_LINE}{{progress}} " + \
                  f"{Cursor.GREEN}{{time}}{Cursor.RESET}{Cursor.RESTORE}"


#
#       gets send on user input to clear said input from the terminal
#
CLEAR_ENTRY = f"{Cursor.ERASE_LINE}{Cursor.up(1)}{Cursor.ERASE_LINE}{Cursor.GREEN}# {Cursor.RESET}"
