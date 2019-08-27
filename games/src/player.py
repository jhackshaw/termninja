import asyncio
import datetime


anonymous_identity = {
    "username": None,
    "total_score": 0,
    "play_token_expires_at": None
}


def format_timedelta(delta):
    total_seconds = delta.total_seconds()
    hours = total_seconds // (60 * 60)
    total_seconds %= 60 * 60
    minutes = total_seconds // 60
    total_seconds %= 60
    return f"{hours:.0f}h {minutes:.0f}m {total_seconds:.0f}s"


class Player:
    """
    Wraps the standard StreamReader, StreamWriter for more
    concise api for these types of applications.
    """

    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        """
        Pass the reader, writer objects as created by something
        like asyncio.start_server()
        """
        self.reader = reader
        self.writer = writer
        self.identity = anonymous_identity
        self.total_score = 0
        self.earned = 0
        self.emoji_support = True
        self._play_token_expires_at = None

    @property
    def play_token_expires_at(self):
        if self.identity['play_token_expires_at'] is None:
            return 'never'
        now = datetime.datetime.now()
        delta = self.identity['play_token_expires_at'] - now
        return format_timedelta(delta)

    @property
    def username(self):
        name = self.identity['username']
        if name is None:
            return 'anonymous'
        return name

    @property
    def address(self):
        addr = self.writer.get_extra_info('peername')
        return addr[0]

    def assign_db_user(self, user):
        self.total_score = user['total_score']
        self.identity = user

    async def send(self, msg: str):
        """
        encode and send message and wait until
        appropriate to call send again

        Args:
            msg (str): non-encoded message to be sent
        """
        self.writer.write(msg.encode())
        await self.writer.drain()

    async def read_raw(self, size, timeout=None):
        data = await asyncio.wait_for(
            self.reader.read(size), timeout
        )
        if data == b'':
            raise ConnectionResetError
        return data.decode()

    async def read(self, size=8, timeout=None):
        """
        attempt to read size bytes in timeout time

        Args:
            timeout (float): raise TimeoutError if exceeded
            size (int): maximum number of bytes to read

        Returns:
            decoded input received

        Raises:
            TimoutError: if timeout exceed while reading
            ConnectionResetError: if EOF is received while reading
        """
        data = await self.read_raw(size, timeout)
        return data.strip()

    async def clear_input_buffer(self):
        """
        read anything sitting in reader and throw it away
        """
        try:
            await asyncio.wait_for(
                self.reader.read(1024), 0.1
            )
        except asyncio.TimeoutError:
            pass

    async def readline(self, timeout=None):
        """
        read a single line. throw ResetError if user disconnected

        Args:
            timeout (float): raise TimeoutError if exceeded

        Returns:
            decoded input with newline stripped off

        Raises:
            ConnectionResetError:
                if the user disconnected while attempting read
            TimeoutError:
                if timeout exceed while attempting read
        """
        data = await asyncio.wait_for(self.reader.readline(),
                                      timeout=timeout)
        if data == b'' or not data.endswith(b'\n'):
            raise ConnectionResetError()
        return data.strip().decode()

    async def read_until_valid(self,
                               validator,
                               coerce=str,
                               timeout=None,
                               prompt="\n# "):
        """
        recieve input 1 line at a time until it passes validation.

        Args:
            validator (func): validation function f(data) -> True or False
            coerce (func): attempt to cast input using this function
            timeout (float): raise TimeoutError if exceeded
            prompt (str): send this string after bad input

        Returns:
            Coerced and validated input

        Raises:
            asyncio.TimeoutError

        """
        return await asyncio.wait_for(
            self._readlines_until_validates(coerce, validator), timeout
        )

    async def on_earned_points(self, earned):
        """
        Whenever the player earns points, update the players total score
        and their earned points for this round
        """
        self.earned += earned
        self.total_score += earned

    async def _readlines_until_validates(self, coerce, validator):
        """
        Implementation of read_until_valid in a single
        coroutine that can be timed out by calling function
        """
        while True:
            try:
                data = await self.readline()
                data = coerce(data)
                if validator(data):
                    return data
            except ValueError:
                continue

    async def close(self):
        """
        Close the stream (send and EOF if possible).
        """
        try:
            self.writer.write_eof()
            await self.writer.drain()
        except (ConnectionResetError, BrokenPipeError, NotImplementedError):
            pass
        self.writer.close()
        await self.writer.wait_closed()
        print("[-] connection closed")
