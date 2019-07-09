from termninja import cursor

# constants
ROUND_LENGTH = 60

#
#   sent once on first connection
#
WELCOME_MESSAGE = fr"""{cursor.CLEAR}
{cursor.YELLOW}
               __---------__
             / _-----------_ \
            / /             \ \
            | |             | |
            |_|_____________|_|
         /-\|                 |/-\
        | _ |\       0       /| _ |
        |(_)| \      !      / |(_)|
        |___|__\_____!_____/__|___|
        [_____{cursor.RESET}{cursor.BLUE}|SUBNET RACER|{cursor.RESET}{cursor.YELLOW}______] 
         ||||    ~~~~~~~~     ||||
         `--'                 `--'

        Welcome to Subnet Racer!!!!{cursor.RESET}


"""

#
#   ask the user to press enter before starting
#
PRESS_ENTER_MESSAGE = f"""
{cursor.BLUE}Press enter to continue...{cursor.RESET}
"""


#
#   clears screen and prompts the next question
#
INITIAL_QUESTION = f"""{cursor.CLEAR}

POINTS EARNED: {cursor.GREEN}{{score}}{cursor.RESET}

{cursor.BLUE}{{prompt}}{cursor.RESET}
{{progress}} {cursor.GREEN}{{time}}{cursor.RESET}

{cursor.YELLOW}# {cursor.RESET}"""


#
#       gets sent every second or so to countdown time remaining
#
PROGRESS_UPDATE = f"{cursor.SAVE}{cursor.up(2)}{cursor.HOME}" + \
                  f"{cursor.ERASE_TO_LINE_END}{{progress}} " + \
                  f"{cursor.GREEN}{{time}}{cursor.RESET}{cursor.RESTORE}"


#
#       gets send on user input to clear said input from the terminal
#
CLEAR_ENTRY = f"{cursor.ERASE_LINE}{cursor.up(1)}{cursor.ERASE_LINE}{cursor.GREEN}# {cursor.RESET}"
