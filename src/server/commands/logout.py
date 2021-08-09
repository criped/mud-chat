from channels.auth import logout, get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from contrib.mud_auth.models import User
from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin
from world.models import Room


class CommandLogout(CommandAbstract):
    ALIASES = ('quit', 'exit', 'logout')
    HELP = _('logout - To leave the game. You can also user `exit` or `quit`.')
    MESSAGE_SUCCESS = _('Logged out successfully! ')
    MESSAGE_SUCCESS_BROADCAST = _('User {username} is offline now.')

    def __init__(self, connection, parser: CommandParserLogin, *args, **kwargs) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
        Logs connected user out.

        It removes the user from the game world. Besides, it notifies all the online users.
        """

        user = await get_user(self.connection.scope)
        await logout(self.connection.scope)

        current_room = await Room.get_room_by_id(user.location_id)
        await self.connection.channel_layer.group_discard(
            str(current_room.id),
            self.connection.channel_name
        )

        await self.send_chat_message(self.MESSAGE_SUCCESS)
        await self.send_broadcast_message(self.MESSAGE_SUCCESS_BROADCAST.format(username=user.username))
        await User.set_is_online(user, False)

    @staticmethod
    async def is_available(connection, *args, **kwargs) -> bool:
        user = await get_user(connection.scope)
        return type(user) != AnonymousUser
