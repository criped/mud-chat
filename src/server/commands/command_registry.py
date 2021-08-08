from typing import Tuple, List

from django.utils.translation import ugettext_lazy as _

from server.commands.help import CommandHelp
from server.commands.login import CommandLogin
from server.commands.logout import CommandLogout
from server.commands.parsers.parser_base import CommandParserBase
from server.commands.parsers.parser_help import CommandParserHelp
from server.commands.parsers.parser_login import CommandParserLogin
from server.commands.parsers.parser_logout import CommandParserLogout
from server.commands.parsers.parser_register import CommandParserRegister
from server.commands.register import CommandRegister


class CommandNotFoundException(Exception):
    msg = _(
        'Command not found or not available. '
        'Make sure the command is in the command registry and use help for more info about available commands. '
    )

    def __str__(self):
        return str(self.msg)


class CommandRegistry:
    COMMAND_REGISTRY = {
        CommandLogin: CommandParserLogin,
        CommandRegister: CommandParserRegister,
        CommandLogout: CommandParserLogout,
        CommandHelp: CommandParserHelp,
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
                command_config = command_class, cls.COMMAND_REGISTRY[command_class]

        if not command_config:
            raise CommandNotFoundException(parser.command_name)

        return command_config

    @classmethod
    async def get_available_commands(cls, connection) -> List:
        return [command_class for command_class in cls.COMMAND_REGISTRY if await command_class.is_available(connection)]
