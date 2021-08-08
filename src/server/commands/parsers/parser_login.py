from server.commands.parsers.parser_base import CommandParserBase


class CommandParserLogin(CommandParserBase):
    """
    Parses input for login command
    """
    INDEX_USERNAME = 1
    INDEX_PASSWORD = 2

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.username = self.parse_username()
        self.password = self.parse_password()

    def parse_username(self) -> str:
        return self.parse_positional_argument(self.INDEX_USERNAME)

    def parse_password(self) -> str:
        return self.parse_positional_argument(self.INDEX_PASSWORD)
