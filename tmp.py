
class Cursor:
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

art = f"""{Cursor.CLEAR}{Cursor.GREEN}

                _____                   _   _ _       _       
                |_   _|                 | \ | (_)     (_)      
                | | ___ _ __ _ __ ___ |  \| |_ _ __  _  __ _ 
                | |/ _ \ '__| '_ ` _ \| . ` | | '_ \| |/ _` |
                | |  __/ |  | | | | | | |\  | | | | | | (_| |
                \_/\___|_|  |_| |_| |_\_| \_/_|_| |_| |\__,_|
                                                    _/ |      
                                                    |__/

{Cursor.RESET}
"""

print(art)
                                