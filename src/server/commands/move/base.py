from channels.auth import get_user
from channels.db import database_sync_to_async

from contrib.mud_auth.models import User
from server.commands.base import CommandAbstract
from server.commands.parsers.parser_login import CommandParserLogin
from world.models import RoomExit


class CommandBaseMove(CommandAbstract):
    DIRECTION: str = ''

    def __init__(self, connection, parser: CommandParserLogin, *args, **kwargs) -> None:
        super().__init__(connection, parser)

    async def run(self) -> None:
        """
            Moves user to an adjacent room
        """
        current_location = self.connection.scope['session']['current_location_id']

        await self.connection.channel_layer.group_discard(
            str(current_location),
            self.connection.channel_name
        )

        destination = await RoomExit.get_exit_destination(current_location, self.DIRECTION)
        await self.connection.channel_layer.group_add(
            str(destination.id),
            self.connection.channel_name
        )
        user = await get_user(self.connection.scope)
        await User.update_location(user, destination.id)

        self.connection.scope['session']['current_location_id'] = destination.id
        await database_sync_to_async(self.connection.scope['session'].save)()

    @classmethod
    async def is_available(cls, connection, *args, **kwargs) -> bool:
        try:
            location_id = connection.scope['session']['current_location_id'],
        except KeyError:
            return False
        else:
            return await RoomExit.check_exit(
                location_id,
                cls.DIRECTION
            )
