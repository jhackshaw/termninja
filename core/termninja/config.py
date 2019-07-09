from .cursor import Cursor


#
#   clears screen and prompts the next question
#
GENERIC_QUIZ_INITIAL_QUESTION = f"""{Cursor.CLEAR}

TOTAL SCORE:   {Cursor.GREEN}{{total_score}}{Cursor.RESET}
POINTS EARNED: {Cursor.GREEN}{{earned}}{Cursor.RESET}

{Cursor.BLUE}{{prompt}}{Cursor.RESET}
{{progress}}{Cursor.RESET}

{Cursor.YELLOW}# {Cursor.RESET}"""


#
#   gets sent every second or so to countdown time remaining
#
GENERIC_QUIZ_PROGRESS_UPDATE = (
    f"{Cursor.SAVE}{Cursor.up(2)}{Cursor.HOME}"
    f"{Cursor.ERASE_TO_LINE_END}{{progress}} "
    f"{Cursor.RESTORE}"
)


#
#   gets send on user input to clear said input from the terminal
#
GENERIC_QUIZ_CLEAR_ENTRY = (
    f"{Cursor.ERASE_LINE}{Cursor.up(1)}{Cursor.ERASE_LINE}"
    f"{Cursor.YELLOW}# {Cursor.RESET}"
)

GENERIC_QUIZ_INTERMISSION_REPORT = (
    f"\n\nCorrect answer: {{correct_answer}}\n"
    f"Points earned:  {{earned_points}}\n\n"
    f"{Cursor.blue('Press enter to continue...')}"
)
