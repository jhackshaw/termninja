from termninja.cursor import Cursor


# constants
ROUND_LENGTH = 60

#
#   sent once on first connection
#
WELCOME_MESSAGE = f"""{Cursor.CLEAR}
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


"""

#
#   ask the user to press enter before starting
#
PRESS_ENTER_MESSAGE = f"""
{Cursor.BLUE}Press enter to continue...{Cursor.RESET}
"""


#
#   clears screen and prompts the next question
#
INITIAL_QUESTION = f"""{Cursor.CLEAR}

POINTS EARNED: {Cursor.GREEN}{{score}}{Cursor.RESET}

{Cursor.BLUE}{{prompt}}{Cursor.RESET}
{{progress}} {Cursor.GREEN}{{time}}{Cursor.RESET}

{Cursor.YELLOW}# {Cursor.RESET}"""


#
#       gets sent every second or so to countdown time remaining
#
PROGRESS_UPDATE = f"{Cursor.SAVE}{Cursor.up(2)}{Cursor.HOME}" + \
                  f"{Cursor.ERASE_TO_LINE_END}{{progress}} " + \
                  f"{Cursor.GREEN}{{time}}{Cursor.RESET}{Cursor.RESTORE}"


#
#       gets send on user input to clear said input from the terminal
#
CLEAR_ENTRY = f"{Cursor.ERASE_LINE}{Cursor.up(1)}{Cursor.ERASE_LINE}{Cursor.GREEN}# {Cursor.RESET}"
