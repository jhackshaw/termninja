from . import cursor


TERMNINJA_PROMPT = fr"""
{cursor.CLEAR}{cursor.GREEN}
          _____                   _   _ _       _
         |_   _|                 | \ | (_)     (_)
           | | ___ _ __ _ __ ___ |  \| |_ _ __  _  __ _
           | |/ _ \ '__| '_ ` _ \| . ` | | '_ \| |/ _` |
           | |  __/ |  | | | | | | |\  | | | | | | (_| |
           \_/\___|_|  |_| |_| |_\_| \_/_|_| |_| |\__,_|
                                               / |
                                              |__/
{cursor.RESET}

{{}}

{cursor.yellow('Choose a game...')}
# """
