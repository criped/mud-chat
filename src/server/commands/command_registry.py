from typing import Tuple

from django.utils.translation import ugettext_lazy as _

from server.commands.login import CommandLogin
from server.commands.logout import CommandLogout
from server.commands.parsers.parser_base import CommandParserBase
from server.commands.parsers.parser_login import CommandParserLogin
from server.commands.parsers.parser_logout import CommandParserLogout
from server.commands.parsers.parser_register import CommandParserRegister
from server.commands.register import CommandRegister


class CommandNotFoundException(Exception):
    msg = _('Command not found. Make sure the command is in the command registry.')

    def __str__(self):
        return str(self.msg)


class CommandRegistry:
    COMMAND_REGISTRY = {
        CommandLogin: CommandParserLogin,
        CommandRegister: CommandParserRegister,
        CommandLogout: CommandParserLogout
    }

    @classmethod
    def get_command_from_message(cls, input_message: str) -> Tuple:
        """
        Utility to get the command configuration given an input text.
        The command is searched over all Command's aliases.
        :param input_message: text entered by user
        :return: tuple containing command class and parser class
        """
        parser = CommandParserBase(input_message)

        command_config = None
        for command_class in cls.COMMAND_REGISTRY.keys():
            if parser.command_name in command_class.ALIASES:
                command_config = command_class, cls.COMMAND_REGISTRY[command_class]

        if not command_config:
            raise CommandNotFoundException(parser.command_name)

        return command_config
