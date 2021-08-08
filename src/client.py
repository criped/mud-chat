"""
A simple MUD client for the k6 home assignment.
Requires the 'websockets' library from PyPi.
Usage:
    client.py [-s <server>] [-p <port>]
Default is connecting to localhost, port 9878.
Modify this file if you want, but the focus of this assignment
is on the server side.
"""

import argparse
import asyncio
import json
import signal

import websockets

URI_SCHEME = "ws"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9878
PATH = 'mud'
PROMPT = ">"


class MUDClient:
    """
    A simple MUD client for sending JSON data to a server.
    Data format (JSON):
        {
            "text": <str>,
            "token": <str>
        }
    """

    def __init__(self, server: str, port: int):
        """
        Starts the client.
        Args:
            server: The server address/host to connect to.
            port: The server port to connect to.
        """

        self.server = server
        self.port = port
        self.websocket = None
        self.tasks = []
        self.token: str = None

    async def handle_user_input(self):
        """
        Catch user entering something on the command line and send it to the connected server.
        """
        loop = asyncio.get_event_loop()

        while True:
            text = await loop.run_in_executor(None, input, f"{PROMPT}\n")

            data = {
                "text": text,
                "token": self.token
            }
            if self.websocket:
                await self.websocket.send(json.dumps(data))
            else:
                print("No connection to server.")

    async def handle_server_recv(self):
        """
        Connect to server and handle all data coming from it.
        Args:
            data: The incoming (JSON) data from the server.
        """
        async for data in self.websocket:

            data = json.loads(data)
            token = data.get("token")

            if self.token is None:
                self.token = token
            elif self.token != token:
                print("[client] Invalid token received from server! Aborting.")
                await self.websocket.close()

            text = data.get("text")
            if text:
                print(f"{text}\n{PROMPT}")

        # make sure that closing the websocket kills all coroutines
        asyncio.get_event_loop().stop()

    async def run(self):
        """
        Connect to server and set up handlers for sending/receiving data.
        """
        uri = f"{URI_SCHEME}://{self.server}:{self.port}/{PATH}/"
        self.websocket = await websockets.connect(uri)

        # make sure to close socket on Ctrl-C
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, loop.create_task, self.websocket.close())

        # run coroutines
        self.tasks = [
            self.handle_server_recv(),
            self.handle_user_input()
        ]
        await asyncio.gather(*self.tasks)


def client():
    """
    Start the client, accepting arguments from the command line.
    """
    parser = argparse.ArgumentParser(description="Simple MUD client")
    parser.add_argument('--host', default=DEFAULT_HOST, type=str,
                        help="server host to connect to")
    parser.add_argument('--port', '-p', default=DEFAULT_PORT, type=int,
                        help="server port to connect to")

    args = parser.parse_args()

    print(f"Connecting to {URI_SCHEME}://{args.host}:{args.port} ...")

    client = MUDClient(args.host, args.port)

    try:
        asyncio.get_event_loop().run_until_complete(client.run())
    except (RuntimeError, KeyboardInterrupt):
        print("Client stopped.")
    except Exception as err:
        print(f"Connection error: {err}")


if __name__ == "__main__":
    client()
