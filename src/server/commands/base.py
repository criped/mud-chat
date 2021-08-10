from abc import abstractmethod, ABC
from typing import Tuple

from server.messages.base import Message
from server.messages.group import GroupMessage


class CommandAbstract(ABC):
    """
    Abstract class that must be implemented by any Command. Commands are a key piece in this MUD game as they allow
    users to perform actions.

    You can implement your own command by following these steps
    1. Make sure you have installed this app into your django apps.
    2. Create your own command, inheriting from `src.server.commands.base.CommandBase`. You will have to implement
    all the abstract methods like the constructor, `run()` and `is_available()`.
    The last one is relevant so that the `help` command can show info about it.
    3. Create your command parser, inheriting from `src.server.commands.parsers.base.CommandParserBase`. Your previously
    created command class will receive it in order to manage the input arguments.
    4. Register it on your django settings file by extending the `COMMAND_CONFIG` dict. For example:
    ```
        # your settings.py
        MUD_COMMANDS = {
            'path.to.your.commands.module.CommandClass': ''path.to.your.command.parsers.module.CommandParserClass'
        }
    ```
    """
    ALIASES: Tuple = tuple()
    HELP: str = ''

    @abstractmethod
    def __init__(self, connection, parser, *args, **kwargs) -> None:
        self.connection = connection
        self.parser = parser

    @abstractmethod
    async def run(self) -> None:
        """
        Implements the actions to perfomed when the command is run
        """
        ...

    @classmethod
    @abstractmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        """
        Determines if the command is available for the user at that moment and location.
        :param connection: websocket connection
        :param args: additional context in positinonal arguments
        :param kwargs: additional context in positinonal arguments
        :return: True if available, False if not.
        """
        ...

    async def send_chat_message(self, text: str):
        await self.connection.chat_message(
            Message(text).payload
        )

    async def send_broadcast_message(self, text: str):
        for group in self.connection.channel_layer.groups.keys():
            await self.connection.channel_layer.group_send(
                group,
                Message(text).payload
            )

    async def send_group_message(self, text: str, group_name: str, username: str):
        await self.connection.channel_layer.group_send(
            group_name,
            GroupMessage(text, username, group_name, read_mode=False).payload
        )
