from server.commands.parsers.parser_base import CommandParserBase


class CommandParserSay(CommandParserBase):
    """
    Parses input for login command
    """
    INDEX_MESSAGE = 1

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.message = self.parse_message()

    def parse_message(self) -> str:
        return self.SEPARATOR.join(self.args)
