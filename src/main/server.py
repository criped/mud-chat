"""
A simple MUD server template for the k6 home challenge.
Requires the 'websockets' library from PyPi.
Start with
    server.py [--host <HOST>] [--port <PORT]
Defaults to localhost, port 9878.
This is currently a simple echo-server. Modify this file as much
as you want and don't be shy to throw away any code you don't want/like/need.
"""

import argparse
import asyncio
import json
import secrets
import signal
import websockets


URI_SCHEME = "ws"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 9878


class Session:
    """
    Class representing the connection.
    """
    def __init__(self, token, websocket):
        """
        Initialize the session.
        Args:
            token (str): Token/Session-id.
        """
        self.token = secrets.token_hex(32)
        self.websocket = websocket

    async def send(self, message):
        """
        Send message across the connection to the player.
        Args:
            message (str): The message to send.
        """
        data = {"text": message, "token": self.token}
        await self.websocket.send(json.dumps(data))


class MUDServer:

    def __init__(self):
        self.sessions = {}

    async def recv(self, websocket, path, session):
        """
        Waiting for commands from the player over the connection.
        """
        async for message in websocket:
            data = json.loads(message)

            if data['token'] != session.token:
                await session.send("Token mismatch! Disconnecting.")
                websocket.close()

            text = data['text']

            await session.send(f"[echo]: '{text}'")

        # when websocket closes, wipe the session too
        print(f"Disconnected session {session.token}")
        del self.sessions[session.token]

    async def handle_connection(self, websocket, path):
        """
        Handle the lifetime of a new websocket connection.
        """
        print("New connection established.")

        # create a new session
        token = secrets.token_hex(32)
        session = self.sessions[token] = Session(token, websocket)

        # make sure to close socket on Ctrl-C
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGTERM, loop.create_task, websocket.close())

        # first connection - sync token to client
        await session.send("")
        # start waiting for commands
        try:
            await self.recv(websocket, path, session)
        except websockets.exceptions.ConnectionClosed:
            print("A Connection closed.")


def server():
    """
    Start the server, accepting arguments from the command line.
    server.py [--host <HOST>] [--port <PORT>]
    """
    parser = argparse.ArgumentParser(description="Simple MUD client")
    parser.add_argument('--host', default=DEFAULT_HOST, type=str,
                        help="host to use")
    parser.add_argument('--port', '-p', default=DEFAULT_PORT, type=int,
                        help="port to use")

    args = parser.parse_args()

    server = MUDServer()

    start_server = websockets.serve(server.handle_connection, args.host, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)

    print(f"Server running on {URI_SCHEME}://{args.host}:{args.port}!")
    try:
        asyncio.get_event_loop().run_forever()
    except (RuntimeError, KeyboardInterrupt):
        print("Server stopped!")


if __name__ == "__main__":
    server()
