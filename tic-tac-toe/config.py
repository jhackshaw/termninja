from shell_games import Cursor


YOUR_TURN_MESSAGE = Cursor.green(
    "It's your turn, choose a square\n# "
)

OTHER_PLAYER_TURN_MESSAGE = Cursor.yellow(
    "Hold on, other player choosing...\n"
)

PLAYER_TIMED_OUT_MESSAGE = Cursor.red(
    "\nPlayer took too long and lost their turn!!\n"
)

BOARD_FORMAT = Cursor.CLEAR + """

       Tic-Tac-Toe
  
       1|    2|    3
     {}  |  {}  |  {}
   _____|_____|_____
       4|    5|    6
     {}  |  {}  |  {}   
   _____|_____|_____
       7|    8|    9
     {}  |  {}  |  {}     
        |     |

"""

WELCOME_MESSAGE = f"""{Cursor.CLEAR}

    {BOARD_FORMAT.format(*" "*9)}


    {Cursor.blue("Searching for an opponent...")}

"""
