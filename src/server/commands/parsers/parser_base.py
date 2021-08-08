from typing import List

from django.utils.translation import ugettext_lazy as _


class CommandParsingException(Exception):
    msg = _('Error. Arguments are not well formed.')

    def __str__(self):
        return str(self.msg)


class CommandParserBase:
    """
    Base class of command parsers.

    Children of this class should extend it with methods for each specific argument
    """

    SEPARATOR = ' '

    def __init__(self, text: str) -> None:
        self.text_splitted = text.split(self.SEPARATOR)
        self.command_name = self._parse_command_name()
        self.args = self._parse_arguments()

    def _parse_command_name(self) -> str:
        """
            :return: the command name
        """
        return self.text_splitted[0]

    def _parse_arguments(self) -> List[str]:
        """
        :return: command arguments
        """
        return self.text_splitted[1:] if len(self.text_splitted) > 1 else []

    def parse_positional_argument(self, pos_index):
        try:
            return self.text_splitted[pos_index]
        except IndexError:
            raise CommandParsingException()
