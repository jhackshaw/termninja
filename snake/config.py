from shell_games import Cursor

WELCOME_MESSAGE = f"""{Cursor.CLEAR}
{Cursor.GREEN}
                /^\/^\\
              _|__|  O|
      \/     /~     \_/ \\
      \____|__________/  \\
              \_______      \\
                      `\     \                 \\
                        |     |                  \\
                      /      /                    \\
                      /     /                       \\\\
                    /      /                         \ \\
                  /     /                            \  \\
                /     /             _----_            \   \\
                /     /           _-~      ~-_         |   |
              (      (        _-~    _--_    ~-_     _/   |
                \      ~-____-~    _-~    ~-_    ~-_-~    /
                  ~-_           _-~          ~-_       _-~
                    ~--______-~                ~-___-~
{Cursor.RESET}

  - Use the following command for the best experience:
  {Cursor.YELLOW}stty -icanon && nc <host> <port>{Cursor.RESET}


  {Cursor.BLUE}Press enter when ready....{Cursor.RESET}"""
