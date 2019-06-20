import asyncio


class Cursor:
    ESCAPE = "\x1b["
    RESET = f"{ESCAPE}0m"
    CLEAR = f"{ESCAPE}1J"
    RED = f"{ESCAPE}1;31m"
    GREEN = f"{ESCAPE}1;32m"
    YELLOW = f"{ESCAPE}1;33m"
    BLUE = f"{ESCAPE}1;34m"
    SAVE = f"{ESCAPE}s"
    RESTORE = f"{ESCAPE}u"
    ERASE_LINE = f"{ESCAPE}2K"
    HOME = f"{ESCAPE}1G"

    @classmethod
    def blue(cls, msg):
        return f"{cls.BLUE}{ msg }{cls.RESET}"

    @classmethod
    def green(cls, msg):
        return f"{cls.GREEN}{ msg }{cls.RESET}"

    @classmethod
    def red(cls, msg):
        return f"{cls.RED}{ msg }{cls.RESET}"
    
    @classmethod
    def yellow(cls, msg):
        return f"{cls.YELLOW}{ msg }{cls.RESET}"

    @classmethod
    def move_to(cls, y, x):
        return f"{cls.ESCAPE}{y};{y}H"
    
    @classmethod
    def up(cls, n):
        return f"{cls.ESCAPE}{n}A"
    
    @classmethod
    def down(cls, n):
        return f"{cls.ESCAPE}{n}B"

    @classmethod
    def reset(cls, n):
        return f"{cls.CLEAR}{cls.move_to(0,0)}"

    @classmethod
    def resize(cls, h, w):
        return f"{cls.ESCAPE}8;{w};{h}t"

    @classmethod
    def get_color_for_percentage(cls, percent):
        if percent < 0.33:
            return cls.RED
        if percent < 0.66:
            return cls.YELLOW
        return cls.GREEN



async def main(handler, host, port):
    # ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # ssl_context.check_hostname = False
    # ssl_context.load_cert_chain('server.crt', 'server.key')
    server = await asyncio.start_server(
        handler,
        host=host,
        port=port,
        reuse_port=True
        # ssl=ssl_context
    )
    async with server:
        await server.serve_forever()



def start_game(handler, host, port):
    try:
        asyncio.run(main(handler, host, port))
    except KeyboardInterrupt:
        print("user shutdown\n")
