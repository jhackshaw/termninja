import asyncio
from typing import Callable


class User:
    """ Wraps the standard StreamReader, StreamWriter for more
    concise api for these types of applications.
    """

    def __init__(self,
                 reader: asyncio.StreamReader,
                 writer: asyncio.StreamWriter):
        """ Pass the reader, writer objects as created by something
        like asyncio.start_server()
        """
        self.reader = reader
        self.writer = writer

    async def send(self, msg: str):
        """ encode and send message and wait until 
        appropriate to call send again

        Args:
            msg (str): non-encoded message to be sent
        
        """

        self.writer.write(msg.encode())
        await self.writer.drain()

    async def read(self, size=8, timeout=None):
        """ attempt to read size bytes in timeout time

        Args:
            timeout (float): raise TimeoutError if exceeded
            size (int): maximum number of bytes to read
        
        Returns:
            decoded input received

        Raises:
            TimoutError: if timeout exceed while reading
            ConnectionResetError: if EOF is received while reading
        """
        data = await asyncio.wait_for(
            self.reader.read(size), timeout
        )
        if data == b'':
            raise ConnectionResetError
        return data.strip().decode()

    async def clear_input_buffer(self):
        """ read anything sitting in reader and throw it away
        """
        try:
            await asyncio.wait_for(
                self.reader.read(1024), 0.1
            )
        except asyncio.TimeoutError:
            pass

    async def readline(self, timeout: float=None):
        """ read a single line. throw ResetError if user disconnected

        Args:
            timeout (float): raise TimeoutError if exceeded
        
        Returns:
            decoded input with newline stripped off
        
        Raises:
            ConnectionResetError: if the user disconnected while attempting read
            TimeoutError: if timeout exceed while attempting read
        """
        data = await asyncio.wait_for(self.reader.readline(), 
                                      timeout=timeout)
        if data == b'' or not data.endswith(b'\n'):
            raise ConnectionResetError()
        return data.strip().decode()  

    async def read_until_valid(self,
                               validator: Callable,
                               coerce: Callable=str,
                               timeout: Callable=None,
                               prompt: str="\n# "):
        """ recieve input 1 line at a time until it passes validation.

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

    async def _readlines_until_validates(self,
                                         coerce: Callable,
                                         validator: Callable):
        """ Implementation of read_until_valid in a single
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
        """ Write EOF if applicable and close the stream
        """
        self.writer.close()
        await self.writer.wait_closed()
