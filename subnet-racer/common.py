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
    def color_by_percentage(cls, percent, msg):
        if percent < 0.33:
            return cls.red(msg)
        if percent < 0.66:
            return cls.yellow(msg)
        return cls.green(msg)


class User:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send(self, msg):
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def readline(self, timeout=None):
        try:
            data = await asyncio.wait_for(self.reader.readline(), 
                                          timeout=timeout)
            return data.strip().decode()
        except asyncio.TimeoutError:
            return None

    async def close(self):
        if self.writer.can_write_eof():
            self.writer.write_eof()
        await self.writer.drain()
        self.writer.close()
        await self.writer.wait_closed()
    

async def main(handler, host, port, two_player=False):
    server = await asyncio.start_server(
        handler,
        host=host,
        port=port,
        reuse_port=True
    )
    async with server:
        await server.serve_forever()

def start_game(handler, host, port):
    try:
        asyncio.run(main(handler, host, port))
    except KeyboardInterrupt:
        print("user shutdown\n")
