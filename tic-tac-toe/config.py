from termninja import cursor


TIE_VALUE = 15
WIN_VALUE = 70

X_MARKER = cursor.blue('X')
O_MARKER = cursor.yellow('O')

YOUR_TURN_MESSAGE = cursor.green(
    "It's your turn, choose a square\n# "
)

OTHER_PLAYER_TURN_MESSAGE = cursor.yellow(
    "Hold on, other player choosing...\n"
)

PLAYER_TIMED_OUT_MESSAGE = cursor.red(
    "\nPlayer took too long and lost their turn!!\n"
)

BOARD_FORMAT = cursor.CLEAR + """

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

WELCOME_MESSAGE = f"""{cursor.CLEAR}

{cursor.YELLOW}
  888   d8b        888                   888                    
  888   Y8P        888                   888                    
  888              888                   888                    
  888888888 .d8888b888888 8888b.  .d8888b888888 .d88b.  .d88b.  
  888   888d88P"   888       "88bd88P"   888   d88""88bd8P  Y8b 
  888   888888     888   .d888888888     888   888  88888888888 
  Y88b. 888Y88b.   Y88b. 888  888Y88b.   Y88b. Y88..88PY8b.     
  "Y888888 "Y8888P "Y888"Y888888 "Y8888P "Y888 "Y88P"  "Y8888{cursor.RESET}
                                      

    {cursor.blue("Searching for an opponent...")}

"""
