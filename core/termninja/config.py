from . import cursor

#
#   clears screen and prompts the next question
#
GENERIC_QUIZ_INITIAL_QUESTION = f"""{cursor.CLEAR}

TOTAL SCORE:   {cursor.GREEN}{{total_score}}{cursor.RESET}
POINTS EARNED: {cursor.GREEN}{{earned}}{cursor.RESET}

{cursor.BLUE}{{prompt}}{cursor.RESET}
{{progress}}{cursor.RESET}

{cursor.YELLOW}# {cursor.RESET}"""


#
#   gets sent every second or so to countdown time remaining
#
GENERIC_QUIZ_PROGRESS_UPDATE = (
    f"{cursor.SAVE}{cursor.up(2)}{cursor.HOME}"
    f"{cursor.ERASE_TO_LINE_END}{{progress}} "
    f"{cursor.RESTORE}"
)


#
#   gets send on user input to clear said input from the terminal
#
GENERIC_QUIZ_CLEAR_ENTRY = (
    f"{cursor.ERASE_LINE}{cursor.up(1)}{cursor.ERASE_LINE}"
    f"{cursor.YELLOW}# {cursor.RESET}"
)

GENERIC_QUIZ_INTERMISSION_REPORT = (
    f"\n\nCorrect answer: {{correct_answer}}\n"
    f"Points earned:  {{earned_points}}\n\n"
    f"{cursor.blue('Press enter to continue...')}"
)
