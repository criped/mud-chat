from channels.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin
from world.models import Room


class CommandSay(CommandAbstract):
    ALIASES = ('say',)
    HELP = _('say <message> - To say something in your current room.')

    def __init__(self, connection, parser: CommandParserLogin, *args, **kwargs) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
            Sends message entered by the user to its current location
        """
        user = await get_user(self.connection.scope)
        current_room = await Room.get_room_by_id(user.location_id)
        await self.send_group_message(self.parser.message, str(current_room.id), user.username)

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        user = await get_user(connection.scope)
        return type(user) != AnonymousUser
