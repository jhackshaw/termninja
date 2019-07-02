
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


WELCOME_MESSAGE = f"""{Cursor.CLEAR}

                        {Cursor.YELLOW}
                        888   d8b        888                   888                    
                        888   Y8P        888                   888                    
                        888              888                   888                    
                        888888888 .d8888b888888 8888b.  .d8888b888888 .d88b.  .d88b.  
                        888   888d88P"   888       "88bd88P"   888   d88""88bd8P  Y8b 
                        888   888888     888   .d888888888     888   888  88888888888 
                        Y88b. 888Y88b.   Y88b. 888  888Y88b.   Y88b. Y88..88PY8b.     
                        "Y888888 "Y8888P "Y888"Y888888 "Y8888P "Y888 "Y88P"  "Y8888{Cursor.RESET}
                                                            

                            {Cursor.BLUE}Searching for an opponent...{Cursor.RESET}








"""

print(art)
                                