from channels.auth import logout, get_user
from django.utils.translation import ugettext_lazy as _

from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin


class CommandLogout(CommandAbstract):
    ALIASES = ('quit', 'exit', 'logout')
    MESSAGE_SUCCESS = _('Logged out successfully! ')
    MESSAGE_SUCCESS_BROADCAST = _('User {username} is offline now.')

    def __init__(self, connection, parser: CommandParserLogin) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
        Logs connected user out.

        It removes the user from the game world. Besides, it notifies all the online users.
        """

        user = await get_user(self.connection.scope)
        await logout(self.connection.scope)

        await self.connection.channel_layer.group_discard(
            "random_location",  # TODO: manage rooms
            self.connection.channel_name
        )

        await self.send_chat_message(self.MESSAGE_SUCCESS)
        await self.send_broadcast_message(self.MESSAGE_SUCCESS_BROADCAST.format(username=user.username))
