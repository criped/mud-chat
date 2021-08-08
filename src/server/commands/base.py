from abc import abstractmethod, ABC
from typing import Tuple

from server.messages.base import Message


class CommandAbstract(ABC):
    ALIASES: Tuple = tuple()
    HELP: str = ''

    @abstractmethod
    def __init__(self, connection, parser, *args, **kwargs) -> None:
        self.connection = connection
        self.parser = parser

    @abstractmethod
    async def run(self) -> None:
        ...

    @staticmethod
    @abstractmethod
    async def is_available(connection, *args, **kwargs) -> bool:
        """
        Determines if the command is available for the user at that moment and location.
        :param connection: websocket connection
        :param args: additional context in positinonal arguments
        :param kwargs: additional context in positinonal arguments
        :return: True if available, False if not.
        """
        ...

    async def send_chat_message(self, text):
        await self.connection.chat_message(
            Message(text).payload
        )

    async def send_broadcast_message(self, text):
        for group in self.connection.channel_layer.groups.keys():
            print(f"sending to group {group}")
            await self.connection.channel_layer.group_send(
                group,
                Message(text).payload
            )
