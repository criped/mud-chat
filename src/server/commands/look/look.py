from django.utils.translation import ugettext_lazy as _

from server.commands.base import CommandAbstract
from server.commands.look.look_elements.room import LookElementRoom
from server.commands.look.look_elements.room_exits import LookElementRoomExits
from server.commands.look.look_elements.room_users import LookElementUsers
from server.commands.parsers.parser_login import CommandParserLogin


class CommandLook(CommandAbstract):
    ALIASES = ('look', 'l')
    HELP = _(
        'look - Get info about the game and current context such as current room name and description, '
        'as well as online players in the room.  Use `l` for shortcut'
    )

    # Elements must be laid out in the exact order they are meant to be shown
    ELEMENT_CLASSES = (LookElementRoom, LookElementUsers, LookElementRoomExits)

    def __init__(self, connection, parser: CommandParserLogin, *args, **kwargs) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
            Gets info about the game and current context such as current room name and description,
            as well as online players in the room
        """
        look_info = ''
        for element_class in self.ELEMENT_CLASSES:
            look_info += await element_class(self.connection).get_element_str()

        await self.send_chat_message(look_info)

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        return 'current_location_id' in connection.scope['session']
