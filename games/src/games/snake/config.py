from src.core import cursor

WELCOME_MESSAGE = fr"""{cursor.CLEAR}
{cursor.GREEN}
                /^\/^ \
              _|__|  O| \
      \/     /~     \_/  \
      \____|__________/   \
              \_______      \
                      `\     \                  \
                        |     |                   \
                      /      /                     \
                      /     /                       \ \
                    /      /                         \  \
                  /     /                            \   \
                /     /             _----_            \   \
                /     /           _-~      ~-_         |   |
              (      (        _-~    _--_    ~-_     _/   |
                \      ~-____-~    _-~    ~-_    ~-_-~    /
                  ~-_           _-~          ~-_       _-~
                    ~--______-~                ~-___-~
{cursor.RESET}

  - Use the following command for the best experience:
  {cursor.YELLOW}stty -icanon && nc <host> <port>{cursor.RESET}


  {cursor.BLUE}Press enter when ready....{cursor.RESET}

"""

DESCRIPTION = "An all ascii take on the classic game of snake."
