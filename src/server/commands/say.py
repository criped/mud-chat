from channels.auth import logout, get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin


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
        location = "random_location"  # TODO: manage rooms

        await self.send_group_message(self.parser.message, location, user.username)

    @staticmethod
    async def is_available(connection, *args, **kwargs) -> bool:
        user = await get_user(connection.scope)
        return type(user) != AnonymousUser
