from channels.auth import login
from django.utils.translation import ugettext_lazy as _

from contrib.mud_auth.models import User
from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin
from server.commands.parsers.parser_register import CommandParserRegister


class CommandRegister(CommandAbstract):
    ALIASES = ('register', 'r')
    MESSAGE_ERROR_USER_ALREADY_EXISTING = _('User {username} already existing')
    MESSAGE_SUCCESS = _('User {username} registered successfully! Please, log in to start.')

    def __init__(self, connection, parser: CommandParserRegister) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
        Logs in an user by username and password.

        It checks that the user exists and that the given password is correct, sending a text to the user
        for each specific case.
        """
        username = self.parser.username
        user_exists = await User.check_exists(username)
        if not user_exists:
            user = await User.register_user(username, self.parser.password)
            await login(self.connection.scope, user)
            await self.send_chat_message(
                self.MESSAGE_SUCCESS.format(username=username)
            )
        else:
            await self.send_chat_message(
                self.MESSAGE_ERROR_USER_ALREADY_EXISTING.format(username=username)
            )