import asyncio


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