from typing import Tuple, List, Dict

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from pycodestyle import lru_cache

from server.commands.parsers.parser_base import CommandParserBase
from server.utils import import_class


class CommandNotFoundException(Exception):
    msg = _(
        'Command not found or not available. '
        'Make sure the command is in the command registry and use help for more info about available commands. '
    )

    def __str__(self):
        return str(self.msg)


class CommandRegistry:
    @classmethod
    @lru_cache(None)
    def registered_commands(cls) -> Dict:
        """
        Imports base commands and the ones registered for extension
        :return: dictionary containing command class and command parsers
        """
        commands_config = settings.MUD_COMMANDS_BASE
        if hasattr(settings, 'MUD_COMMANDS'):
            commands_config.update(settings.MUD_COMMANDS)
        return {
            import_class(command_class): import_class(command_parser)
            for command_class, command_parser in commands_config.items()
        }

    @classmethod
    def get_command_from_message(cls, input_message: str, available_command_classes: List) -> Tuple:
        """
        Utility to get the command configuration given an input text.
        The command is searched over all Command's aliases.
        :param input_message: text entered by user
        :param available_command_classes: commands available
        :return: tuple containing command class and parser class
        """
        parser = CommandParserBase(input_message)

        command_config = None
        for command_class in available_command_classes:
            if parser.command_name in command_class.ALIASES:
                command_config = command_class, cls.registered_commands()[command_class]

        if not command_config:
            raise CommandNotFoundException(parser.command_name)

        return command_config

    @classmethod
    async def get_available_commands(cls, connection) -> List:
        """
        Discover available commands available for the given connection.
        Each command must implement its `is_available()` method.
        :param connection: websocket connection to the end user
        """
        return [
            command_class for command_class in cls.registered_commands() if await command_class.is_available(connection)
        ]
